"""Read public GitHub sources and report new or changed observations."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]


def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def api(endpoint):
    result = subprocess.run(
        ["gh", "api", "--method", "GET", endpoint],
        capture_output=True, text=True, timeout=45, check=True,
    )
    return json.loads(result.stdout)


def collect(source, fetch=api):
    kind = source["kind"]
    if kind == "repo":
        repo = source["repo"]
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
            raise ValueError("Invalid repository name")
        commit = fetch(f"repos/{repo}/commits?per_page=1")[0]
        row = {
            "key": repo, "title": commit["commit"]["message"].splitlines()[0],
            "url": commit["html_url"], "revision": commit["sha"],
            "updated_at": commit["commit"]["committer"]["date"],
        }
        return [row], []
    if kind not in ("issues", "repositories"):
        raise ValueError(f"Unknown source kind: {kind}")
    query = urlencode({"q": source["query"], "sort": "updated", "order": "desc", "per_page": 100})
    data = fetch(f"search/{kind}?{query}")
    rows = []
    for item in data["items"]:
        row = {
            "key": item["html_url"], "url": item["html_url"],
            "title": item.get("title", item.get("full_name")),
            "updated_at": item["updated_at"],
        }
        if kind == "issues":
            row.update(state=item["state"], type="pr" if "pull_request" in item else "issue")
        else:
            row.update(description=item.get("description"), pushed_at=item["pushed_at"])
        rows.append(row)
    warnings = []
    if data.get("incomplete_results"):
        warnings.append("GitHub marked this search incomplete; retry or narrow the query.")
    if data["total_count"] > len(rows):
        warnings.append(f"Showing {len(rows)} of {data['total_count']} matches; narrow the query for full coverage.")
    return rows, warnings


def run(sources, state, fetch=api):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    report = {"checked_at": now, "changes": [], "sources": [], "errors": []}
    seen = state.setdefault("seen", {})
    ids = [s["id"] for s in sources]
    if len(ids) != len(set(ids)):
        raise ValueError("Source IDs must be unique")
    for source in sources:
        source_id = source["id"]
        try:
            rows, warnings = collect(source, fetch)
            # Changing a query starts a fresh baseline instead of reusing unrelated results.
            scope = hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()
            previous = seen.setdefault(scope, {})
            for row in rows:
                old = previous.get(row["key"])
                if old != row:
                    change = {"source": source_id, "status": "changed" if old else "first_seen", **row}
                    if old and source["kind"] == "repo":
                        change["compare_url"] = f"https://github.com/{source['repo']}/compare/{old['revision']}...{row['revision']}"
                    report["changes"].append(change)
                previous[row["key"]] = row
            report["sources"].append({"id": source_id, "observed": len(rows), "warnings": warnings})
            state.setdefault("last_success", {})[source_id] = now
        except (subprocess.SubprocessError, OSError, ValueError, KeyError, IndexError, TypeError) as error:
            # A failed source retains its last successful snapshot.
            if isinstance(error, subprocess.CalledProcessError):
                message = "GitHub request failed. Check authentication, repository access, and rate limits."
            else:
                message = str(error)
            report["errors"].append({"source": source_id, "error": message})
    return report


def escape(text):
    return re.sub(r"([\\`*_{}\[\]<>()#!|])", r"\\\1", " ".join(str(text).split()))


def markdown(report):
    lines = [f"# Source check · {report['checked_at']}", "",
             f"{len(report['changes'])} new or changed observations. {len(report['errors'])} failed sources.", "",
             "First seen means new to this job, not newly published. Search matches need review.", ""]
    for change in report["changes"][:20]:
        # GitHub returns the URLs; escaping prevents titles from injecting Markdown.
        lines.append(f"- {escape(change['source'])} / {change['status']}: [{escape(change['title'])}]({change['url']})")
        if "compare_url" in change:
            lines.append(f"  [Compare commits]({change['compare_url']})")
    if len(report["changes"]) > 20:
        lines.append(f"\nShowing 20 of {len(report['changes'])} changes. The JSON report contains all observations.")
    for source in report["sources"]:
        for warning in source["warnings"]:
            lines.append(f"- Coverage: {escape(source['id'])}. {escape(warning)}")
    for error in report["errors"]:
        lines.append(f"- Failed: {escape(error['source'])}. {escape(error['error'])}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("watch", "hunt"))
    parser.add_argument("--config", type=Path, default=ROOT / "watchlist.json")
    parser.add_argument("--state-dir", type=Path, default=ROOT / ".state")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "runs")
    args = parser.parse_args()
    state_path = args.state_dir / f"{args.mode}.json"
    state = read_json(state_path, {})
    report = run(read_json(args.config)[args.mode], state)
    # Write the report before advancing the saved state.
    write_json(args.output_dir / f"{args.mode}.json", report)
    (args.output_dir / f"{args.mode}.md").write_text(markdown(report))
    write_json(state_path, state)
    print(f"{len(report['changes'])} changes; {len(report['errors'])} failed sources. See {args.output_dir / (args.mode + '.md')}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())

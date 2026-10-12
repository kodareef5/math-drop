"""Check the published study against its original archive and classification."""

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "imports/2026-10-11-study"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check():
    manifest = json.loads((STUDY / "MANIFEST.json").read_text())
    archive = ROOT / "imports" / manifest["archive_name"]
    assert digest(archive.read_bytes()) == manifest["archive_sha256"], "Archive changed"
    entries = {row["path"]: row for row in manifest["files"]}
    assert len(entries) == len(manifest["files"]), "Duplicate manifest paths"
    prefix = "math-drop-study/"
    extracted = 0
    with zipfile.ZipFile(archive) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        assert len(names) == len(entries) == 551
        assert set(names) == {prefix + name for name in entries}
        for name, entry in entries.items():
            data = z.read(prefix + name)
            assert len(data) == entry["bytes"] and digest(data) == entry["sha256"], name
            if not name.endswith(".pyc"):
                assert (STUDY / name).read_bytes() == data, f"Extracted file changed: {name}"
                extracted += 1
    for path in STUDY.rglob("*.json"):
        json.loads(path.read_text())
    families = json.loads((STUDY / "catalogue.json").read_text())
    triage = json.loads((STUDY / "triage_all.json").read_text())
    family_ids = {int(row["num"]) for row in families}
    assert len(families) == len(family_ids) == len(triage) == 372
    assert {int(row["num"]) for row in triage} == family_ids, "Classification coverage differs"
    assert sum(len(row["manuscripts"]) for row in families) == 719
    opportunities = [row for path in (STUDY / "deep").glob("*.json")
                     if path.name != "lean_confidence.json"
                     for row in json.loads(path.read_text())]
    assert len(opportunities) == len({row["id"] for row in opportunities}) == 133
    print(f"551 archived files; {extracted} matching extracted files; 372 classified families; 719 manuscripts; 133 opportunities.")


if __name__ == "__main__":
    check()

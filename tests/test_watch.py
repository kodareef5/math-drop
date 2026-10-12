import unittest
from copy import deepcopy

from tools.watch import collect, markdown, run


class WatchTests(unittest.TestCase):
    source = {"id": "math", "kind": "repo", "repo": "example/math"}

    @staticmethod
    def commit(sha="a"):
        return [{"sha": sha, "html_url": f"https://github.com/example/math/commit/{sha}",
                 "commit": {"message": "A result\nDetails", "committer": {"date": "2026-10-12T00:00:00Z"}}}]

    def test_baseline_repeat_and_change(self):
        state = {}
        first = run([self.source], state, lambda _: self.commit())
        self.assertEqual(first["changes"][0]["status"], "first_seen")
        self.assertEqual(run([self.source], state, lambda _: self.commit())["changes"], [])
        changed = run([self.source], state, lambda _: self.commit("b"))
        self.assertTrue(changed["changes"][0]["compare_url"].endswith("/compare/a...b"))

    def test_failure_keeps_snapshot_and_success_timestamp(self):
        state = {}
        run([self.source], state, lambda _: self.commit())
        previous = deepcopy(state)
        def fail(_):
            raise OSError("offline")
        report = run([self.source], state, fail)
        self.assertEqual(state, previous)
        self.assertEqual(report["changes"], [])
        self.assertEqual(len(report["errors"]), 1)

    def test_failed_source_does_not_hide_other_sources(self):
        broken = {"id": "broken", "kind": "repo", "repo": "example/broken"}
        def fetch(url):
            return [] if "broken" in url else self.commit()
        report = run([broken, self.source], {}, fetch)
        self.assertEqual(len(report["changes"]), 1)
        self.assertEqual(len(report["errors"]), 1)

    def test_incomplete_and_capped_search_are_visible(self):
        source = {"id": "search", "kind": "issues", "query": "repo:example/math"}
        rows, warnings = collect(source, lambda _: {"items": [], "incomplete_results": True, "total_count": 101})
        self.assertEqual(rows, [])
        self.assertEqual(len(warnings), 2)

    def test_query_changes_reset_baseline(self):
        source = {"id": "search", "kind": "issues", "query": "old"}
        data = {"total_count": 1, "items": [{"html_url": "https://github.com/e/r/issues/1", "title": "result", "updated_at": "2026-10-12", "state": "open"}]}
        state = {}
        run([source], state, lambda _: data)
        source["query"] = "new"
        self.assertEqual(run([source], state, lambda _: data)["changes"][0]["status"], "first_seen")

    def test_remote_title_cannot_inject_markdown(self):
        report = run([self.source], {}, lambda _: self.commit())
        report["changes"][0]["title"] = "[fake](https://evil) <script>\n# heading"
        rendered = markdown(report)
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("\n# heading", rendered)
        self.assertNotIn("[fake](https://evil)", rendered)


if __name__ == "__main__":
    unittest.main()

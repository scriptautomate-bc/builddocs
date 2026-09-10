#!/usr/bin/env python3
"""Single source of truth for builddocs' supported doc targets.

Reads docs_targets.json and derives everything the workflow, the sitemap
index, and robots.txt need, so a release/branch only has to be edited in
one place.
"""
import json
import re
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "docs_targets.json"

MAJOR_SORT_RE = re.compile(r"\d+")


def load_targets():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    targets = config["targets"]
    for target in targets:
        if not target.get("release_version") and not target.get("doc_branch"):
            sys.exit(
                f"ERROR: target {target.get('major')!r} in {CONFIG_PATH} "
                "must set release_version or doc_branch"
            )
    return targets


def is_master(target):
    return not target["major"].isdigit()


def major_sort_key(target):
    match = MAJOR_SORT_RE.search(target["major"])
    return int(match.group()) if match else -1


def latest_major_target(targets):
    release_targets = [t for t in targets if not is_master(t)]
    if not release_targets:
        sys.exit(f"ERROR: no non-master targets found in {CONFIG_PATH}")
    return max(release_targets, key=major_sort_key)


def website_point_release(target):
    return (
        target.get("website_point_release")
        or target.get("release_version")
        or target["doc_branch"]
    )


def pdf_doc_branch(target):
    if target.get("doc_branch"):
        return target["doc_branch"]
    return f"v{target['release_version']}"


def to_matrix_entry(target):
    return {
        "major": target["major"],
        "website_release": target["major"],
        "website_point_release": website_point_release(target),
        "release_version": target.get("release_version"),
        "html_doc_branch": target.get("doc_branch"),
        "pdf_doc_branch": pdf_doc_branch(target),
    }


def cmd_matrix(targets):
    print(json.dumps([to_matrix_entry(t) for t in targets], separators=(",", ":")))


def cmd_latest_major(targets):
    print(latest_major_target(targets)["major"])


def cmd_robots_disallow(targets):
    latest_major = latest_major_target(targets)["major"]
    for target in targets:
        if is_master(target) or target["major"] == latest_major:
            print(target["major"])


def cmd_sitemap_majors(targets):
    latest_major = latest_major_target(targets)["major"]
    for target in targets:
        if target["major"] != latest_major:
            print(target["major"])


COMMANDS = {
    "matrix": cmd_matrix,
    "latest-major": cmd_latest_major,
    "robots-disallow": cmd_robots_disallow,
    "sitemap-majors": cmd_sitemap_majors,
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        print(f"usage: {sys.argv[0]} <{'|'.join(COMMANDS)}>", file=sys.stderr)
        return 1

    targets = load_targets()
    COMMANDS[sys.argv[1]](targets)
    return 0


if __name__ == "__main__":
    sys.exit(main())

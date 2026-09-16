#!/usr/bin/env python3
"""Build a self-contained offline workflow viewer from a research bundle."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_workflow import validate_bundle


def _json_for_script(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Directory containing the workflow bundle")
    parser.add_argument("--output", type=Path, help="Output HTML path; defaults to <bundle>/index.html")
    parser.add_argument("--template", type=Path, help="Optional custom viewer template")
    args = parser.parse_args()

    bundle = args.bundle.resolve()
    errors, warnings, _ = validate_bundle(bundle)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print("Viewer was not built because bundle validation failed.")
        return 1

    script_dir = Path(__file__).resolve().parent
    template = args.template or script_dir.parent / "assets" / "viewer-template" / "index.html"
    output = (args.output or bundle / "index.html").resolve()

    html = template.read_text(encoding="utf-8")
    replacements = {
        "__WORKFLOW_DATA__": json.loads((bundle / "workflow.json").read_text(encoding="utf-8")),
        "__SOURCES_DATA__": json.loads((bundle / "sources.json").read_text(encoding="utf-8")),
        "__ANNOTATIONS_DATA__": json.loads((bundle / "annotations.json").read_text(encoding="utf-8")),
        "__SEARCH_DATA__": json.loads((bundle / "search-log.json").read_text(encoding="utf-8")),
    }
    for token, value in replacements.items():
        if token not in html:
            print(f"ERROR: template is missing token {token}")
            return 1
        html = html.replace(token, _json_for_script(value), 1)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Built viewer: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

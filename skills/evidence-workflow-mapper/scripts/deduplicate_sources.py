#!/usr/bin/env python3
"""Report probable duplicate papers and patent-family records without modifying sources."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).casefold()
    return re.sub(r"[^a-z0-9]+", "", value)


def duplicate_key(source: dict[str, Any]) -> tuple[str, str] | None:
    identifiers = source.get("identifiers") or {}
    doi = normalize_text(str(identifiers.get("doi", "")))
    if doi:
        return "doi", doi
    if source.get("type") == "patent":
        family = normalize_text(str(source.get("family_id", "")))
        if family:
            return "patent-family", family
        publication = normalize_text(str(source.get("publication_number", "")))
        if publication:
            return "publication-number", publication
    title = normalize_text(str(source.get("title", "")))
    year = str(source.get("year", ""))
    if title:
        return "title-year", f"{title}:{year}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path, help="Path to sources.json")
    parser.add_argument("--output", type=Path, help="Optional duplicate report JSON path")
    args = parser.parse_args()

    data = json.loads(args.sources.read_text(encoding="utf-8"))
    groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for source in data.get("sources", []):
        key = duplicate_key(source)
        if key:
            groups[key].append(source.get("id", "<missing-id>"))

    duplicates = [
        {"match_type": key[0], "match_value": key[1], "source_ids": ids}
        for key, ids in sorted(groups.items())
        if len(ids) > 1
    ]
    report = {"schema_version": "1.0", "duplicate_groups": duplicates}
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote duplicate report: {args.output}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

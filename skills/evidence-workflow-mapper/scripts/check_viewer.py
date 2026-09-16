#!/usr/bin/env python3
"""Check a generated viewer for unresolved tokens and JavaScript syntax errors."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_MARKERS = (
    "Evidence Workflow Notebook",
    "workflowData",
    "renderNotebookPage",
    "renderPaperShelf",
    "export-notebook",
    "import-research",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Generated index.html")
    args = parser.parse_args()

    html = args.html.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in REQUIRED_MARKERS:
        if marker not in html:
            errors.append(f"missing required marker: {marker}")
    unresolved = sorted(set(re.findall(r"__[A-Z][A-Z0-9_]+__", html)))
    if unresolved:
        errors.append(f"unresolved template tokens: {', '.join(unresolved)}")

    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.IGNORECASE | re.DOTALL)
    if not scripts:
        errors.append("no inline JavaScript block found")

    node = shutil.which("node")
    if scripts and node:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
            handle.write("\n".join(scripts))
            temp_path = Path(handle.name)
        try:
            result = subprocess.run([node, "--check", str(temp_path)], capture_output=True, text=True, encoding="utf-8")
            if result.returncode:
                errors.append(f"JavaScript syntax check failed:\n{result.stderr.strip()}")
        finally:
            temp_path.unlink(missing_ok=True)
    elif scripts:
        print("WARNING: Node.js is unavailable; JavaScript syntax check was skipped.")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("Viewer integrity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

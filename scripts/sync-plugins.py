#!/usr/bin/env python3
"""Mirror skills/<name> into every plugins/<plugin>/skills/<name> that already lists it.

skills/ is the single source of truth (skills.sh and other agents read it).
plugins/ holds generated copies the Claude plugin marketplace needs.

Usage: python scripts/sync-plugins.py [--check]
"""
import filecmp
import shutil
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
check = "--check" in sys.argv


def differs(a: Path, b: Path) -> bool:
    if not b.exists():
        return True
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files:
        return True
    return any(differs(a / d, b / d) for d in cmp.common_dirs)


drift = []
for target in sorted(root.glob("plugins/*/skills/*")):
    source = root / "skills" / target.name
    if not source.is_dir():
        sys.exit(f"missing source: {source}")
    if differs(source, target):
        drift.append(target)
        if not check:
            shutil.rmtree(target)
            shutil.copytree(source, target)

for t in drift:
    print(("drift: " if check else "synced: ") + str(t.relative_to(root)))
sys.exit(1 if check and drift else 0)

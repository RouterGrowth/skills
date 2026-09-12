#!/usr/bin/env python3
"""Validate every skill in skills/: strict-YAML frontmatter, name matching the
folder, a real description, no em dashes, no key material. Run in CI and
before opening a PR: python3 scripts/check_skills.py"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
    slug = path.parent.name
    text = path.read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"{slug}: missing frontmatter block"); continue
    try:
        fm = yaml.safe_load(text[4:].split("\n---\n", 1)[0]) or {}
    except yaml.YAMLError as e:
        errors.append(f"{slug}: frontmatter is not strict YAML ({str(e).splitlines()[0]}); write description as a block scalar (>-)"); continue
    if fm.get("name") != slug:
        errors.append(f"{slug}: frontmatter name {fm.get('name')!r} must equal the folder name")
    desc = str(fm.get("description") or "")
    if len(desc) < 80:
        errors.append(f"{slug}: description is too short to trigger reliably ({len(desc)} chars)")
    if "\u2014" in text:
        errors.append(f"{slug}: em dash found; use a colon, a comma or two sentences")
    if re.search(r"rg_(live|test)_[A-Za-z0-9]{8,}|sk_(live|test)_[A-Za-z0-9]{8,}", text):
        errors.append(f"{slug}: looks like key material")
    if len(text.splitlines()) > 400:
        errors.append(f"{slug}: over 400 lines; move reference material to reference.md")

for e in errors:
    print("FAIL", e)
if errors:
    sys.exit(1)
print(f"ok: {len(list((ROOT / 'skills').glob('*/SKILL.md')))} skills pass")

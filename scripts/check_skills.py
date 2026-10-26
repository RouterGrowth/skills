#!/usr/bin/env python3
"""Validate every skill in skills/: strict-YAML frontmatter that claude.ai accepts on upload (only name, description,
license, compatibility, metadata, allowed-tools), a name that matches the folder and Anthropic's naming rules, a
description that triggers (80 to 1,024 characters), a version in metadata, at least three evals, no em dashes, no key
material, under 500 lines. Also checks that every harness manifest carries the same version and that no SKILL-like
file sits outside skills/ (installers would list it). Run in CI and before opening a PR:
python3 scripts/check_skills.py"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
errors: list[str] = []

skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
for path in skills:
    slug = path.parent.name
    text = path.read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"{slug}: missing frontmatter block"); continue
    try:
        fm = yaml.safe_load(text[4:].split("\n---\n", 1)[0]) or {}
    except yaml.YAMLError as e:
        errors.append(f"{slug}: frontmatter is not strict YAML ({str(e).splitlines()[0]}); write description as a block scalar (>-)"); continue
    extra = set(fm) - ALLOWED
    if extra:
        errors.append(f"{slug}: frontmatter keys {sorted(extra)} are refused by claude.ai uploads; put them under metadata")
    if fm.get("name") != slug:
        errors.append(f"{slug}: frontmatter name {fm.get('name')!r} must equal the folder name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) or len(slug) > 64 or "claude" in slug or "anthropic" in slug:
        errors.append(f"{slug}: name must be lowercase letters, digits and hyphens, at most 64 characters, without reserved words")
    desc = str(fm.get("description") or "")
    if len(desc) < 80:
        errors.append(f"{slug}: description is too short to trigger reliably ({len(desc)} chars)")
    if len(desc) > 1024:
        errors.append(f"{slug}: description is over 1,024 characters ({len(desc)})")
    if "<" in desc or ">" in desc:
        errors.append(f"{slug}: no angle brackets in the description")
    if not str((fm.get("metadata") or {}).get("version") or ""):
        errors.append(f"{slug}: metadata.version is missing")
    if "—" in text:
        errors.append(f"{slug}: em dash found; use a colon, a comma or two sentences")
    if re.search(r"rg_(live|test)_[A-Za-z0-9]{8,}|sk_(live|test)_[A-Za-z0-9]{8,}", text):
        errors.append(f"{slug}: looks like key material")
    if len(text.splitlines()) > 500:
        errors.append(f"{slug}: over 500 lines; move reference material to references/")
    ev = path.parent / "evals" / "evals.json"
    try:
        data = json.loads(ev.read_text())
        cases = data.get("evals", [])
        if data.get("skill_name") != slug or len(cases) < 3:
            errors.append(f"{slug}: evals/evals.json needs skill_name {slug!r} and at least three evals")
        if not any(c.get("should_trigger") is False for c in cases):
            errors.append(f"{slug}: add at least one near-miss eval with should_trigger false")
    except FileNotFoundError:
        errors.append(f"{slug}: evals/evals.json is missing")
    except json.JSONDecodeError as e:
        errors.append(f"{slug}: evals/evals.json is not valid JSON ({e})")

# installers scan the whole tree for SKILL.md or skill-shaped frontmatter
for stray in ROOT.rglob("*.md"):
    if "skills" in stray.relative_to(ROOT).parts[:1] or ".git" in stray.parts:
        continue
    head = stray.read_text(errors="ignore")[:200]
    if stray.name == "SKILL.md" or re.match(r"---\s*\n(#.*\n)*name:\s", head):
        errors.append(f"{stray.relative_to(ROOT)}: skill-shaped file outside skills/; installers will list it")

versions = {}
for manifest in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json", "gemini-extension.json"]:
    f = ROOT / manifest
    if f.exists():
        versions[manifest] = json.loads(f.read_text()).get("version")
if len(set(versions.values())) > 1:
    errors.append(f"manifest versions disagree: {versions}")

for e in errors:
    print("FAIL", e)
if errors:
    sys.exit(1)
print(f"ok: {len(skills)} skills pass, manifests at {next(iter(versions.values()), '?')}")

#!/usr/bin/env python3
"""Build one ZIP per skill for claude.ai (Settings > Capabilities > Skills > Upload) and for anyone who copies a skill
by hand: dist/<skill>.zip holds the skill folder (SKILL.md, evals, references) at its root, plus the LICENSE.
The release workflow attaches them to the GitHub release. Run: python3 scripts/package_skills.py [--output dist]"""

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=str(ROOT / "dist"))
    out = Path(ap.parse_args().output)
    out.mkdir(parents=True, exist_ok=True)
    for skill in sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md")):
        target = out / f"{skill.name}.zip"
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(skill.rglob("*")):
                if f.is_file() and not f.name.startswith("."):
                    z.write(f, Path(skill.name) / f.relative_to(skill))
            z.write(ROOT / "LICENSE", Path(skill.name) / "LICENSE")
        print(target.relative_to(ROOT) if target.is_relative_to(ROOT) else target)


if __name__ == "__main__":
    main()

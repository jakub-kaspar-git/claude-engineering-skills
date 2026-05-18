"""
Validační skript pro skills/ adresář.

Ověřuje:
1. Každý skill adresář obsahuje SKILL.md
2. SKILL.md má YAML frontmatter s povinnými poli (name, description, category)
3. SKILL.md obsahuje povinné sekce (Overview/Purpose)
4. Python soubory (.py) jsou syntakticky validní
"""

import os
import sys
import ast
import re

SKILLS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills")

REQUIRED_FRONTMATTER = {"name", "description", "category"}

# Adresáře, které jsou rodiče sub-skillů (ne listové skilly)
PARENT_DIRS = {"pump-design"}

errors = []
warnings = []
stats = {"skills": 0, "skill_md": 0, "py_files": 0, "py_valid": 0}


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    fields = {}
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key = line.split(":")[0].strip()
            fields[key] = True
    return fields


def validate_skill_dir(path, rel_path):
    """Validate a single skill directory."""
    skill_md = os.path.join(path, "SKILL.md")

    if not os.path.isfile(skill_md):
        errors.append(f"MISSING SKILL.md: {rel_path}/")
        return

    stats["skill_md"] += 1
    stats["skills"] += 1

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # Check frontmatter
    fm = extract_frontmatter(content)
    if fm is None:
        errors.append(f"NO FRONTMATTER: {rel_path}/SKILL.md")
    else:
        missing = REQUIRED_FRONTMATTER - set(fm.keys())
        if missing:
            errors.append(f"MISSING FIELDS in {rel_path}/SKILL.md: {', '.join(sorted(missing))}")

    # Check for Overview or Purpose section
    if "## Overview" not in content and "## Purpose" not in content:
        warnings.append(f"NO OVERVIEW SECTION: {rel_path}/SKILL.md")

    # Validate .py files
    for fname in os.listdir(path):
        if fname.endswith(".py"):
            py_path = os.path.join(path, fname)
            stats["py_files"] += 1
            try:
                with open(py_path, "r", encoding="utf-8") as f:
                    ast.parse(f.read())
                stats["py_valid"] += 1
            except SyntaxError as e:
                errors.append(f"SYNTAX ERROR: {rel_path}/{fname} line {e.lineno}: {e.msg}")


def walk_skills(base_dir):
    """Walk skills directory and validate each skill."""
    for category in sorted(os.listdir(base_dir)):
        cat_path = os.path.join(base_dir, category)
        if not os.path.isdir(cat_path):
            continue

        for skill in sorted(os.listdir(cat_path)):
            skill_path = os.path.join(cat_path, skill)
            if not os.path.isdir(skill_path):
                continue

            rel = f"{category}/{skill}"

            if skill in PARENT_DIRS:
                # Validate parent SKILL.md
                validate_skill_dir(skill_path, rel)
                # Validate sub-skills
                for sub in sorted(os.listdir(skill_path)):
                    sub_path = os.path.join(skill_path, sub)
                    if os.path.isdir(sub_path):
                        validate_skill_dir(sub_path, f"{rel}/{sub}")
            else:
                validate_skill_dir(skill_path, rel)


def main():
    print(f"Validating skills in: {SKILLS_DIR}\n")

    if not os.path.isdir(SKILLS_DIR):
        print(f"ERROR: {SKILLS_DIR} does not exist")
        sys.exit(1)

    walk_skills(SKILLS_DIR)

    # Report
    print(f"Skills found:    {stats['skills']}")
    print(f"SKILL.md files:  {stats['skill_md']}")
    print(f"Python files:    {stats['py_files']} ({stats['py_valid']} valid)")
    print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  WARN: {w}")
        print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  FAIL: {e}")
        print()
        print("VALIDATION FAILED")
        sys.exit(1)
    else:
        print("VALIDATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()

"""
Testy konfigurace .claude/settings.json a připravenosti repozitáře
pro batch zpracování státnicových otázek.

Spuštění: python test_settings.py
"""
import json
import os
import sys
import importlib

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, ".claude", "settings.json")

passed = 0
failed = 0
warnings = 0


def test(name, condition, msg_fail="", warn_only=False):
    global passed, failed, warnings
    if condition:
        print(f"  PASS  {name}")
        passed += 1
    elif warn_only:
        print(f"  WARN  {name} — {msg_fail}")
        warnings += 1
    else:
        print(f"  FAIL  {name} — {msg_fail}")
        failed += 1


# ═══════════════════════════════════════════════════════════════════
# 1. Settings file existence and JSON validity
# ═══════════════════════════════════════════════════════════════════
print("\n=== 1. Settings file structure ===")

test("settings.json exists",
     os.path.isfile(SETTINGS_PATH),
     f"Missing {SETTINGS_PATH}")

settings = None
if os.path.isfile(SETTINGS_PATH):
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            settings = json.load(f)
        test("settings.json is valid JSON", True)
    except json.JSONDecodeError as e:
        test("settings.json is valid JSON", False, str(e))

if settings is None:
    print("\nCannot continue — settings.json missing or invalid.")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════
# 2. Permission structure
# ═══════════════════════════════════════════════════════════════════
print("\n=== 2. Permission structure ===")

test("Has 'permissions' key",
     "permissions" in settings,
     "Top-level 'permissions' key missing")

perms = settings.get("permissions", {})

test("Has 'allow' list",
     isinstance(perms.get("allow"), list),
     "'allow' must be a list")

test("Has 'deny' list",
     isinstance(perms.get("deny"), list),
     "'deny' must be a list")

allow = perms.get("allow", [])
deny = perms.get("deny", [])

# ═══════════════════════════════════════════════════════════════════
# 3. Required ALLOW rules for batch question processing
# ═══════════════════════════════════════════════════════════════════
print("\n=== 3. Required ALLOW rules ===")

required_allows = {
    "Read": "Čtení SKILL.md a questions.txt",
    "Edit": "Editace Python souborů",
    "Glob": "Hledání souborů v skills/",
    "Grep": "Prohledávání obsahu skillů",
}

for rule, reason in required_allows.items():
    test(f"Allow: {rule} ({reason})",
         rule in allow,
         f"Missing '{rule}' in allow list")

# Pattern-based allows
pattern_allows = {
    "Write(output/**)": "Zápis .docx a .png do output/",
    "Write(*.py)": "Vytváření Python generátorů",
    "Bash(python *)": "Spouštění Python skriptů",
    "Bash(pip install *)": "Instalace závislostí",
}

for rule, reason in pattern_allows.items():
    found = any(rule in a for a in allow)
    test(f"Allow: {rule} ({reason})",
         found,
         f"Missing pattern '{rule}' in allow list")

# ═══════════════════════════════════════════════════════════════════
# 4. Required DENY rules for safety
# ═══════════════════════════════════════════════════════════════════
print("\n=== 4. Required DENY rules (safety) ===")

required_denies = {
    "Bash(rm -rf *)": "Ochrana před smazáním souborů",
    "Bash(rm -r *)": "Ochrana před rekurzivním mazáním",
    "Bash(git push *)": "Ochrana před push do remote",
    "Bash(git reset --hard*)": "Ochrana před ztrátou změn",
    "Bash(git checkout -- *)": "Ochrana před zahozením změn",
    "Bash(git clean *)": "Ochrana před smazáním untracked souborů",
    "Bash(curl *)": "Blokování síťových příkazů",
    "Bash(cd ..*)": "Blokování úniku z repo (cd ..)",
    "Bash(Invoke-*)": "Blokování PowerShell cmdlets",
}

for rule, reason in required_denies.items():
    found = any(rule in d for d in deny)
    test(f"Deny: {rule} ({reason})",
         found,
         f"Missing '{rule}' in deny list")

# ═══════════════════════════════════════════════════════════════════
# 5. Conflict check — no rule in both allow AND deny
# ═══════════════════════════════════════════════════════════════════
print("\n=== 5. Conflict check ===")

conflicts = set(allow) & set(deny)
test("No rules in both allow and deny",
     len(conflicts) == 0,
     f"Conflicting rules: {conflicts}")

# ═══════════════════════════════════════════════════════════════════
# 6. Security gaps — commands that SHOULD be denied but aren't
# ═══════════════════════════════════════════════════════════════════
print("\n=== 6. Security gap analysis ===")

# Check dangerous commands that are NOT explicitly allowed but also NOT denied
dangerous_patterns = [
    ("Bash(rm *)", "rm bez -rf je stále nebezpečný"),
    ("Bash(rmdir *)", "mazání adresářů"),
    ("Bash(mv /*)", "přesun systémových souborů"),
    ("Bash(chmod *)", "změna oprávnění"),
    ("Bash(net *)", "síťové příkazy Windows"),
    ("Bash(reg *)", "úprava Windows registry"),
]

for pattern, reason in dangerous_patterns:
    in_allow = any(pattern in a for a in allow)
    in_deny = any(pattern in d for d in deny)
    # It's OK if it's not in either — Claude will prompt the user
    # It's bad if it's in allow
    test(f"Not allowed: {pattern} ({reason})",
         not in_allow,
         f"'{pattern}' is in allow list — dangerous!",
         warn_only=not in_allow and not in_deny)

# ═══════════════════════════════════════════════════════════════════
# 7. Escape vectors — can Claude navigate outside repo?
# ═══════════════════════════════════════════════════════════════════
print("\n=== 7. Escape vector analysis ===")

escape_patterns = [
    "Bash(cd /*)",
    "Bash(cd C:*)",
    "Bash(cd ..*)",
]

for pattern in escape_patterns:
    found = any(pattern in d for d in deny)
    test(f"Deny: {pattern}",
         found,
         f"Missing — Claude could navigate outside repo")

# Check Write is NOT broadly allowed (only specific paths)
write_rules = [a for a in allow if a.startswith("Write")]
broad_write = any(a == "Write" for a in allow)
test("Write is not broadly allowed (only specific paths)",
     not broad_write,
     "Bare 'Write' allows writing ANYWHERE — restrict to paths",
     warn_only=False)

# ═══════════════════════════════════════════════════════════════════
# 8. Directory structure readiness
# ═══════════════════════════════════════════════════════════════════
print("\n=== 8. Directory structure ===")

required_dirs = [
    ("output", "Výstupní .docx soubory"),
    ("output/img", "Generované obrázky (matplotlib)"),
    ("output/pdf", "Exportované PDF"),
    ("questions", "Python generátory otázek"),
    ("skills", "Skill knihovna"),
]

for dirname, reason in required_dirs:
    path = os.path.join(BASE_DIR, dirname)
    test(f"Directory exists: {dirname}/ ({reason})",
         os.path.isdir(path),
         f"Missing directory: {path}")

# ═══════════════════════════════════════════════════════════════════
# 9. Required files
# ═══════════════════════════════════════════════════════════════════
print("\n=== 9. Required files ===")

required_files = [
    ("CLAUDE.md", "Projektové instrukce"),
    ("questions.txt", "Seznam státnicových otázek"),
    ("generate_question.py", "Vzorový generátor"),
    ("docx_engine.py", "DOCX engine s OMML"),
]

for filename, reason in required_files.items() if isinstance(required_files, dict) else required_files:
    path = os.path.join(BASE_DIR, filename)
    test(f"File exists: {filename} ({reason})",
         os.path.isfile(path),
         f"Missing: {path}")

# ═══════════════════════════════════════════════════════════════════
# 10. Python dependencies
# ═══════════════════════════════════════════════════════════════════
print("\n=== 10. Python dependencies ===")

critical_deps = [
    ("docx", "python-docx — generování .docx"),
    ("lxml", "lxml — XML/OMML zpracování"),
    ("latex2mathml", "latex2mathml — LaTeX→MathML"),
    ("numpy", "numpy — numerické výpočty"),
    ("matplotlib", "matplotlib — vizualizace"),
]

optional_deps = [
    ("comtypes", "comtypes — PDF export přes Word COM"),
    ("scipy", "scipy — optimalizace"),
    ("sympy", "sympy — symbolické výpočty"),
    ("pint", "pint — jednotky"),
    ("fluids", "fluids — inženýrská data"),
    ("CoolProp", "CoolProp — vlastnosti tekutin"),
]

for module, reason in critical_deps:
    try:
        importlib.import_module(module)
        test(f"Dependency (critical): {reason}", True)
    except ImportError:
        test(f"Dependency (critical): {reason}", False,
             f"pip install {module}")

for module, reason in optional_deps:
    try:
        importlib.import_module(module)
        test(f"Dependency (optional): {reason}", True)
    except ImportError:
        test(f"Dependency (optional): {reason}", False,
             f"pip install {module}", warn_only=True)

# ═══════════════════════════════════════════════════════════════════
# 11. OMML/XSL transform availability (Word equations)
# ═══════════════════════════════════════════════════════════════════
print("\n=== 11. OMML transform (Word equations) ===")

xsl_candidates = [
    os.path.expandvars(r"%ProgramFiles%\Microsoft Office\root\Office16\MML2OMML.XSL"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft Office\root\Office16\MML2OMML.XSL"),
    os.path.expandvars(r"%ProgramFiles%\Microsoft Office\Office16\MML2OMML.XSL"),
]

xsl_found = any(os.path.isfile(p) for p in xsl_candidates)
test("MML2OMML.XSL found (Word equation support)",
     xsl_found,
     "Microsoft Office not installed or XSL not found — equations won't render as OMML",
     warn_only=True)

# ═══════════════════════════════════════════════════════════════════
# 12. questions.txt validation
# ═══════════════════════════════════════════════════════════════════
print("\n=== 12. questions.txt validation ===")

questions_path = os.path.join(BASE_DIR, "questions.txt")
if os.path.isfile(questions_path):
    with open(questions_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    question_lines = [l.strip() for l in lines
                      if l.strip() and not l.strip().startswith("##")]
    test(f"questions.txt has questions ({len(question_lines)} found)",
         len(question_lines) > 0,
         "No questions found")

    numbered = [l for l in question_lines if l[0].isdigit() and ". " in l]
    test(f"Questions are numbered ({len(numbered)} numbered)",
         len(numbered) == len(question_lines),
         f"{len(question_lines) - len(numbered)} unnumbered lines")

    # Check for duplicate numbers
    numbers = []
    for l in numbered:
        num = l.split(".")[0].strip()
        if num.isdigit():
            numbers.append(int(num))
    duplicates = [n for n in numbers if numbers.count(n) > 1]
    test("No duplicate question numbers",
         len(set(duplicates)) == 0,
         f"Duplicate numbers: {set(duplicates)}")

    # Check sequential
    if numbers:
        expected = list(range(1, max(numbers) + 1))
        missing = set(expected) - set(numbers)
        test("Question numbers are sequential (1..N)",
             len(missing) == 0,
             f"Missing numbers: {sorted(missing)}")

# ═══════════════════════════════════════════════════════════════════
# 13. Dangerous mode compatibility check
# ═══════════════════════════════════════════════════════════════════
print("\n=== 13. --dangerously-skip-permissions compatibility ===")

test("Settings work WITHOUT dangerous mode (recommended)",
     len(allow) > 0 and len(deny) > 0,
     "Settings are empty — no protection without dangerous mode")

print("""
  INFO  Tento settings.json je navržen pro použití BEZ --dangerously-skip-permissions.
        Spouštěj Claude takto:
          claude -p "Zpracuj státnicovou otázku č. 1 ze souboru questions.txt"

        Povolené operace proběhnou automaticky.
        Zakázané operace budou blokovány.
        Ostatní operace vyžadují potvrzení uživatele.

        S --dangerously-skip-permissions se settings.json IGNORUJE!
        Všechny operace projdou bez kontroly.""")

# ═══════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f" RESULTS: {passed} passed, {failed} failed, {warnings} warnings")
print(f"{'='*60}")

if failed > 0:
    print(" STATUS: SOME TESTS FAILED — fix issues above before batch run")
    sys.exit(1)
elif warnings > 0:
    print(" STATUS: ALL PASSED (with warnings — review above)")
    sys.exit(0)
else:
    print(" STATUS: ALL PASSED — ready for batch processing")
    sys.exit(0)

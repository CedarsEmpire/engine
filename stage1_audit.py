# stage1_audit.py - NEW FILE - READ ONLY - DOES NOT OVERWRITE ANYTHING
import os, re

# Files to audit - from your screenshot
FILES_TO_CHECK = [
    "engine/engine.py",
    "engine/daily_earnings.py",
    "engine/central_hub.py",
    "engine/allocator.py",
    "engine/engine_core.py",
    "engine/db.py",
    "engine/fee_utils.py",
]

# Simulation patterns
PATTERNS = {
    "RANDOM": r"random\.",
    "FAKE": r"fake|simulated|mock|demo",
    "HARDCODED_EARNINGS": r"0\.85|daily.*=.*[0-9]+\.[0-9]+",
    "AUTO_TASK": r"create_task\(|generate_task|auto.*task",
    "PRINT_MONEY": r"earnings\s*\+=|balance\s*\+=",
}

print("=== CEDARS EMPIRE - STAGE 1 AUDIT - READ ONLY ===")
for filepath in FILES_TO_CHECK:
    if not os.path.exists(filepath):
        print(f"\n[NOT FOUND] {filepath} - check path")
        continue
    print(f"\n--- {filepath} ---")
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()
        lines = content.splitlines()
        found_any = False
        for name, pattern in PATTERNS.items():
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    print(f"  LINE {i} [{name}]: {line.strip()[:120]}")
                    found_any = True
        if not found_any:
            print("  CLEAN - No simulation patterns found")

print("\n=== AUDIT DONE ===")
print("If CLEAN = Stage 1 Pass for that file")
print("If FOUND = That file needs Stage 1B fix")

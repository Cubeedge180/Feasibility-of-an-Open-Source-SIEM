"""Derive an arm64 copy of the pinned auditd rules.

The pinned upstream rules (lab/endpoints/linux/audit.rules) list legacy syscalls
such as ``open`` or ``chmod`` next to their modern ``*at`` forms. On aarch64 the
legacy syscalls do not exist, so auditctl rejects the whole ``arch=b64`` rule and
the modern syscalls in it are lost too. This script removes only the legacy
names from ``arch=b64`` rules; nothing else changes. ``arch=b32`` (32-bit Arm
compat) rules keep them, because that table has them.

Usage: python -m lab.arm64_audit_rules lab/endpoints/linux/audit.rules > out.rules
"""

import sys
from pathlib import Path

# Syscalls in the pinned rules that the aarch64 syscall table does not have.
AARCH64_MISSING: frozenset[str] = frozenset(
    {
        "chmod",
        "chown",
        "creat",
        "futimesat",
        "lchown",
        "link",
        "mkdir",
        "mknod",
        "open",
        "rename",
        "rmdir",
        "symlink",
        "unlink",
        "utimes",
    }
)


def convert_line(line: str) -> str:
    """Return the line with aarch64-missing syscalls removed from an arch=b64 rule."""
    if line.lstrip().startswith("#"):
        return line
    tokens = line.split()
    if "arch=b64" not in tokens or "-S" not in tokens:
        return line
    kept: list[str] = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "-S" and i + 1 < len(tokens):
            names = [n for n in tokens[i + 1].split(",") if n not in AARCH64_MISSING]
            if names:
                kept += ["-S", ",".join(names)]
            i += 2
            continue
        kept.append(tokens[i])
        i += 1
    if "-S" not in kept:
        return "# arm64: dropped, no syscall left: " + line
    return " ".join(kept)


def convert(text: str) -> str:
    """Convert a whole rules file, line by line."""
    header = "# Derived for aarch64 by lab/arm64_audit_rules.py from the pinned audit.rules\n"
    return header + "\n".join(convert_line(line) for line in text.splitlines()) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m lab.arm64_audit_rules <audit.rules>", file=sys.stderr)
        return 2
    sys.stdout.write(convert(Path(argv[1]).read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

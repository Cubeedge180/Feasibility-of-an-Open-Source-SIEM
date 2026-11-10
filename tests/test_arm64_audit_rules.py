import pytest

from lab.arm64_audit_rules import convert, convert_line


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "-a always,exit -F arch=b64 -S open -S openat -F dir=/etc -k x",
            "-a always,exit -F arch=b64 -S openat -F dir=/etc -k x",
        ),
        (
            "-a always,exit -F arch=b64 -S chmod,fchmod -k perm",
            "-a always,exit -F arch=b64 -S fchmod -k perm",
        ),
        (
            "-a always,exit -F arch=b32 -S open -S openat -k x",
            "-a always,exit -F arch=b32 -S open -S openat -k x",
        ),
        ("-w /etc/passwd -p wa -k etcpasswd", "-w /etc/passwd -p wa -k etcpasswd"),
        ("# -a always,exit -F arch=b64 -S open", "# -a always,exit -F arch=b64 -S open"),
    ],
)
def test_convert_line(line: str, expected: str) -> None:
    assert convert_line(line) == expected


def test_rule_with_only_missing_syscalls_is_commented_out() -> None:
    out = convert_line("-a always,exit -F arch=b64 -S open -k x")
    assert out.startswith("# arm64: dropped")


def test_convert_keeps_line_count_plus_header() -> None:
    text = "-D\n-a always,exit -F arch=b64 -S open -S openat -k x\n"
    assert len(convert(text).splitlines()) == 3

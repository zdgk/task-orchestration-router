"""Validate the public Agent Skill package without third-party dependencies."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAME = "task-orchestration-router"
EXPECTED_PATHS = (
    ".github/workflows/validate.yml",
    ".gitignore",
    "LICENSE",
    "README.md",
    "SKILL.md",
    "agents/openai.yaml",
    "references/codex-desktop-relay.md",
    "references/evaluation-cases.md",
    "references/model-routing.md",
    "references/relay-protocol.md",
    "references/subagent-protocol.md",
    "scripts/validate_contract.py",
    "scripts/validate_package.py",
)
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml"}
LOCAL_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "GitHub OAuth token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "private key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "credential embedded in URL": re.compile(
        r"\b(?:https?|socks5h?)://[^/\s:@]+:[^/\s@]+@",
        re.IGNORECASE,
    ),
    "personal Windows user path": re.compile(
        r"\b[A-Z]:\\Users\\[^\\\r\n]+",
        re.IGNORECASE,
    ),
}


def parse_front_matter(skill_text: str, errors: list[str]) -> dict[str, str]:
    """Parse the simple scalar front matter used by this skill."""
    lines = skill_text.splitlines()
    if not lines or lines[0] != "---":
        errors.append("SKILL.md must start with YAML front matter")
        return {}

    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        errors.append("SKILL.md front matter is not closed")
        return {}

    metadata: dict[str, str] = {}
    for line in lines[1:closing_index]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid front matter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def validate_text_files(errors: list[str]) -> dict[Path, str]:
    """Decode repository text files strictly and reject unsafe package artifacts."""
    decoded: dict[Path, str] = {}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts:
            continue
        if path.is_symlink():
            errors.append(f"symbolic links are not allowed: {relative.as_posix()}")
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        data = path.read_bytes()
        if b"\x00" in data:
            errors.append(f"NUL byte in text file: {relative.as_posix()}")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"invalid UTF-8 in {relative.as_posix()}: {error}")
            continue

        decoded[path] = text
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label} detected in {relative.as_posix()}")
    return decoded


def validate_local_links(decoded: dict[Path, str], errors: list[str]) -> None:
    """Ensure every relative Markdown link stays inside the package and resolves."""
    for markdown_path, text in decoded.items():
        if markdown_path.suffix.lower() != ".md":
            continue
        for match in LOCAL_LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            if not raw_target or raw_target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            relative_target = unquote(raw_target.split("#", 1)[0])
            target = (markdown_path.parent / relative_target).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"local link escapes package in {markdown_path.relative_to(ROOT)}: "
                    f"{raw_target}"
                )
                continue
            if not target.exists():
                errors.append(
                    f"broken local link in {markdown_path.relative_to(ROOT)}: "
                    f"{raw_target}"
                )


def main() -> int:
    """Run package validation and return a process exit code."""
    errors: list[str] = []
    for relative_path in EXPECTED_PATHS:
        if not (ROOT / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")

    decoded = validate_text_files(errors)
    skill_path = ROOT / "SKILL.md"
    metadata = parse_front_matter(decoded.get(skill_path, ""), errors)
    if metadata.get("name") != EXPECTED_NAME:
        errors.append(f"SKILL.md name must be {EXPECTED_NAME!r}")
    if len(metadata.get("description", "")) < 40:
        errors.append("SKILL.md description must be explicit and non-empty")
    if not re.fullmatch(r"[a-z0-9-]+", metadata.get("name", "")):
        errors.append("SKILL.md name must use lowercase letters, digits, and hyphens")

    openai_yaml = decoded.get(ROOT / "agents/openai.yaml", "")
    if "allow_implicit_invocation: true" not in openai_yaml:
        errors.append("agents/openai.yaml must preserve implicit invocation policy")

    validate_local_links(decoded, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"Package validation failed: {len(errors)} issue(s)")
        return 1

    print(
        "Package validation passed: required files, UTF-8, front matter, links, "
        "and secret patterns"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

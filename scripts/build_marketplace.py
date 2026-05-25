#!/usr/bin/env python3
"""Build marketplace.json from skills/*/skill.yaml."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXTERNAL_SKILLS = ROOT / "external-skills.json"
DEFAULT_REPO_URL = "https://github.com/OhMyYuwan/SuperLeaf.Skills.git"
DEFAULT_SOURCE_REF = "main"


def main() -> None:
    repo_url = os.getenv("YUWAN_SKILL_MARKET_REPO_URL", DEFAULT_REPO_URL).strip()
    source_ref = os.getenv("YUWAN_SKILL_MARKET_REF", DEFAULT_SOURCE_REF).strip() or DEFAULT_SOURCE_REF
    entries = []
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        meta_path = folder / "skill.yaml"
        if not meta_path.exists():
            continue
        meta = load_skill_yaml(meta_path)
        entry = str(meta.get("entry") or "SKILL.md")
        entry_path = folder / entry
        checksum = sha256_file(entry_path)
        rel_path = folder.relative_to(ROOT).as_posix()
        install = meta.get("install") or {}
        entry_repo_url = str(install.get("repo_url") or repo_url).strip()
        entry_source_ref = str(install.get("source_ref") or source_ref).strip() or source_ref
        source_url = str(install.get("source_url") or github_tree_url(entry_repo_url, entry_source_ref, rel_path)).strip()
        skill_name = str(install.get("skill_name") or meta["name"]).strip()
        install_command = str(install.get("install_command") or build_npx_install_command(source_url, skill_name)).strip()
        meta["checksum_sha256"] = checksum
        write_skill_yaml(meta_path, meta)
        entries.append(
            {
                "id": meta["id"],
                "name": meta["name"],
                "display_name": meta["display_name"],
                "version": str(meta["version"]),
                "author_github": meta["author"]["github"],
                "description": meta.get("description", ""),
                "tags": meta.get("tags", []),
                "license": meta.get("license", ""),
                "path": rel_path,
                "entry": entry,
                "skill_url": f"{rel_path}/skill.yaml",
                "entry_url": f"{rel_path}/{entry}",
                "readme_url": f"{rel_path}/README.md",
                "checksum_sha256": checksum,
                "repo_url": entry_repo_url,
                "source_url": source_url,
                "source_ref": entry_source_ref,
                "skill_name": skill_name,
                "install_command": install_command,
                "source_type": "local",
            }
        )
    entries.extend(load_external_skill_entries())
    marketplace = {
        "schema_version": "1.0.0",
        "generated_at": "1970-01-01T00:00:00Z",
        "skills": entries,
    }
    (ROOT / "marketplace.json").write_text(
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_external_skill_entries() -> list[dict]:
    if not EXTERNAL_SKILLS.exists():
        return []
    payload = json.loads(EXTERNAL_SKILLS.read_text(encoding="utf-8"))
    entries = []
    for raw in payload.get("skills", []):
        author = str(raw.get("author_github") or raw.get("author") or "").strip()
        skill_name = str(raw.get("skill_name") or raw.get("name") or "").strip()
        npx_command = str(raw.get("npx_command") or raw.get("install_command") or "").strip()
        if not author or not skill_name or not npx_command:
            raise SystemExit("external-skills.json entries require author_github, skill_name, and npx_command")
        source_url, parsed_skill_name = parse_npx_skill_add(npx_command)
        if not source_url:
            raise SystemExit(f"external skill {author}@{skill_name}: npx_command must include `skills add <source>`")
        resolved_skill_name = parsed_skill_name or skill_name
        entries.append(
            {
                "id": f"{author}@{skill_name}",
                "name": skill_name,
                "display_name": str(raw.get("display_name") or skill_name).strip(),
                "version": str(raw.get("version") or "1.0.0"),
                "author_github": author,
                "description": str(raw.get("description") or "").strip(),
                "tags": [str(tag).strip() for tag in raw.get("tags", []) if str(tag).strip()],
                "license": str(raw.get("license") or "").strip(),
                "path": "",
                "entry": "npx",
                "skill_url": "",
                "entry_url": source_url,
                "readme_url": "",
                "checksum_sha256": "",
                "repo_url": source_url,
                "source_url": source_url,
                "source_ref": str(raw.get("source_ref") or "").strip(),
                "skill_name": resolved_skill_name,
                "install_command": normalize_npx_command(npx_command),
                "source_type": "external",
            }
        )
    return entries


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def github_tree_url(repo_url: str, source_ref: str, path: str) -> str:
    cleaned = repo_url.removesuffix(".git").removeprefix("https://github.com/").strip("/")
    if not cleaned or "/" not in cleaned:
        return repo_url
    return f"https://github.com/{cleaned}/tree/{source_ref}/{path.strip('/')}"


def build_npx_install_command(source_url: str, skill_name: str = "") -> str:
    parts = ["npx", "--yes", "skills", "add", shell_quote(source_url)]
    if skill_name and not is_direct_skill_source(source_url):
        parts.extend(["--skill", shell_quote(skill_name)])
    parts.extend(["--agent", "codex", "--copy", "--yes"])
    return " ".join(parts)


def is_direct_skill_source(source_url: str) -> bool:
    return "github.com/" in source_url and "/tree/" in source_url


def parse_npx_skill_add(command: str) -> tuple[str, str]:
    parts = split_command(command)
    for index, part in enumerate(parts):
        if part != "skills" or index + 2 >= len(parts) or parts[index + 1] != "add":
            continue
        source_url = parts[index + 2]
        skill_name = ""
        rest = parts[index + 3 :]
        for opt_index, item in enumerate(rest):
            if item == "--skill" and opt_index + 1 < len(rest):
                skill_name = rest[opt_index + 1]
                break
            if item.startswith("--skill="):
                skill_name = item.split("=", 1)[1]
                break
        return source_url, skill_name
    return "", ""


def normalize_npx_command(command: str) -> str:
    parts = split_command(command)
    if parts and parts[0] == "npx" and (len(parts) == 1 or parts[1] != "--yes"):
        parts.insert(1, "--yes")
    if "--agent" not in parts:
        parts.extend(["--agent", "codex"])
    if "--copy" not in parts:
        parts.append("--copy")
    if not parts or parts[-1] != "--yes":
        parts.append("--yes")
    return " ".join(shell_quote(part) for part in parts)


def split_command(command: str) -> list[str]:
    return [part.strip("'\"") for part in re.findall(r"\"[^\"]*\"|'[^']*'|\S+", command)]


def load_skill_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    out: dict = {"tags": []}
    section = ""
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not raw.startswith(" ") and line.endswith(":"):
            section = line[:-1]
            continue
        if section == "author" and line.strip().startswith("github:"):
            out.setdefault("author", {})["github"] = scalar(line.split(":", 1)[1])
            continue
        if section == "runtime" and line.strip().startswith("kind:"):
            out["runtime_kind"] = scalar(line.split(":", 1)[1])
            continue
        if section == "install":
            match = re.match(r"^\s+([A-Za-z0-9_]+):\s*(.*)$", line)
            if match:
                out.setdefault("install", {})[match.group(1)] = scalar(match.group(2))
                continue
        if section == "checksum" and line.strip().startswith("sha256:"):
            out["checksum_sha256"] = scalar(line.split(":", 1)[1])
            continue
        if section == "tags" and line.strip().startswith("- "):
            out.setdefault("tags", []).append(scalar(line.strip()[2:]))
            continue
        match = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if match:
            section = ""
            out[match.group(1)] = scalar(match.group(2))
    return out


def write_skill_yaml(path: Path, meta: dict) -> None:
    tags = "\n".join(f"  - {tag}" for tag in meta.get("tags", []))
    install = install_section(meta)
    text = f"""id: {meta["id"]}
name: {meta["name"]}
display_name: {meta["display_name"]}
version: {meta["version"]}
author:
  github: {meta["author"]["github"]}
description: {meta.get("description", "")}
tags:
{tags}
license: {meta.get("license", "")}
entry: {meta.get("entry", "SKILL.md")}
visibility: {meta.get("visibility", "public")}
runtime:
  kind: {meta.get("runtime_kind", "instruction-only")}
{install}checksum:
  sha256: {meta.get("checksum_sha256", "")}
updated_at: "{meta.get("updated_at", "")}"
"""
    path.write_text(text, encoding="utf-8")


def install_section(meta: dict) -> str:
    install = meta.get("install") or {}
    if not install:
        return ""
    lines = ["install:"]
    for key in ("repo_url", "source_url", "source_ref", "skill_name", "install_command"):
        value = str(install.get(key) or "").strip()
        if value:
            lines.append(f"  {key}: {value}")
    return "\n".join(lines) + "\n"


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def shell_quote(value: str) -> str:
    if value and all(ch.isalnum() or ch in "/:._@=-" for ch in value):
        return value
    return "'" + value.replace("'", "'\"'\"'") + "'"


if __name__ == "__main__":
    main()

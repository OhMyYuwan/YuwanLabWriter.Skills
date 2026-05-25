# SuperLeaf.Skills

Official Skill catalog for SuperLeaf native Agents.

This repository is the trusted catalog source. SuperLeaf applications read
Skills from the `main` branch only. User and author submissions should arrive as
pull requests, pass validation, and merge into `main` before they become visible
in the Skill Market.

## GitHub Pages Catalog

Enable GitHub Pages for this repository and serve from the `main` branch root.
Then the marketplace can be consumed without cloning the repository:

```text
https://<owner>.github.io/SuperLeaf.Skills/
https://<owner>.github.io/SuperLeaf.Skills/marketplace.json
https://<owner>.github.io/SuperLeaf.Skills/skills/GitHubUser@skill-name/skill.yaml
https://<owner>.github.io/SuperLeaf.Skills/skills/GitHubUser@skill-name/SKILL.md
```

SuperLeaf should sync `marketplace.json` from Pages, cache it briefly, and
download only the selected Skill files during install. Runtime Agent execution
must read installed local Skills only; it should not call GitHub Pages.

Example install command shown by the catalog:

```bash
npx yuwanlab skill install OhMyYuwan@annotation-training-csv
```

## Local Preview

Preview the GitHub Pages site locally:

```bash
python3 -m http.server 8088
```

Then open:

```text
http://127.0.0.1:8088/
http://127.0.0.1:8088/marketplace.json
```

## Layout

```text
marketplace.json
skills/
  GitHubUser@skill-name/
    skill.yaml
    SKILL.md
    README.md
    examples/
    assets/
schemas/
scripts/
.github/workflows/
```

## Trust Boundary

V1 marketplace Skills are instruction packages only:

- no runtime scripts
- no project filesystem access
- no database access
- no automatic document mutation
- no hidden network calls

The application installs approved Skills into the user's local Skill library.
Native Agents can read only the Skills explicitly attached to that Agent.

## Validate

```bash
python3 scripts/validate_marketplace.py
```

## Build Manifest

```bash
python3 scripts/build_marketplace.py
```

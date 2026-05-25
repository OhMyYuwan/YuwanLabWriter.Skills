# Contributing Skills

Thanks for improving the SuperLeaf Skill catalog.

## Submission Flow

1. Fork this repository.
2. Add or update a folder under `skills/`.
3. Name the folder as `GitHubUser@skill-name`.
   - If you publish through SuperLeaf, the app derives `GitHubUser` from
     your connected GitHub account. You only choose the short Skill name.
   - If you submit manually, `GitHubUser` must match the GitHub account that
     opens the pull request.
4. Update `skill.yaml` and `SKILL.md`.
5. Run:

```bash
python3 scripts/build_marketplace.py
python3 scripts/validate_marketplace.py
```

6. Open a pull request to `main`.

The app only reads merged Skills from `main`; submission branches are not part
of the trusted catalog.

## Skill Rules

- `skill.yaml` must match `schemas/skill.schema.json`.
- `marketplace.json` must match `schemas/marketplace.schema.json`.
- `id` must match the folder name.
- `author.github` must match the part before `@`.
- For pull requests, the author prefix must match the submitting GitHub login.
- `entry` must point to a Markdown file in the Skill folder.
- V1 Skills must be instruction-only. Do not include executable scripts.

## Naming

Skill ids are globally unique and use:

```text
GitHubUser@skill-name
```

The author prefix is identity-bound. It is not a free text field and should not
be typed by users in the app. The app should read the connected GitHub account
login and generate the prefix automatically.

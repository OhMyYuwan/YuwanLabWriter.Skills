---
name: annotation-training-csv
description: Convert SuperLeaf annotation training exports, records.jsonl files, or export ZIPs into compact CSV training datasets.
---

# Annotation Training CSV

Turn SuperLeaf annotation training exports into a clean CSV file for
training, evaluation, or manual review.

Default CSV schema:

```csv
id,comment,source_text,label
```

- `id`: integer assigned during extraction.
- `comment`: the annotation or review comment.
- `source_text`: the original source text.
- `label`: the user verdict, usually `positive` or `negative`.

Do not include full document content, thread history, hashes, or ranges unless
the user explicitly asks for audit columns.

## Runtime Boundary

This Skill is instruction-only. It does not read project files directly and does
not execute scripts inside SuperLeaf native Agent runtime.


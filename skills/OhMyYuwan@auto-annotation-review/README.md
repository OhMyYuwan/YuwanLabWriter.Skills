# Auto Annotation Review

Instruction-only Skill for SuperLeaf automatic annotation Agents.

It teaches Agents to:

- interpret `% AUTO` comments as local automation instructions;
- respect SuperLeaf's default behavior of skipping only the LaTeX preamble before `\begin{document}`;
- avoid treating document-body LaTeX commands as automatic exclusion signals;
- return strict `annotations` JSON compatible with SuperLeaf annotation ingestion;
- express rewrite suggestions and risk reminders as normal annotation content instead of separate card types.

Attach this Skill to Agents used by the Automation panel or batch manuscript review workflows.

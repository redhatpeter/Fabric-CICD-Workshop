# GH5 - Make Copilot follow project conventions

**Time:** 25 minutes. **Starting point:** GH4 committed.
**Goal:** create a small reusable starter kit and test its behavior.

Do the repository instructions, reviewer and prompt first. The path instructions,
agent instructions and skill are short follow-ups; MCP is optional.

## Before creating files

Open only the demo repository, save all edits, and start from a clean GH4 commit.
Create the folders exactly as listed below; do not put this kit in VS Code's user
profile or in the workshop materials. Check that filenames end in `.md`, not
`.md.txt`. If Copilot requests approval before creating or replacing a file,
inspect the proposed path/content and approve only the current kit change.

## 1. Create the kit

Ask Copilot to create these files **in your demo repository**, reviewing each one:

| File | Request |
| --- | --- |
| `.github/copilot-instructions.md` | "Document Python 3.10+, type hints for new code, pytest, no extra application dependencies, and the README business rules. Before overwriting, deleting or changing permissions, show the scope and wait for approval. Never read or print credentials. Use read-only checks first." |
| `.github/instructions/python.instructions.md` | "Create Python-specific instructions with applyTo matching all Python files. Require small functions and pytest tests for behavior changes." |
| `AGENTS.md` | "Write short agent instructions: read README, use the project virtual environment, run python -m pytest -q, avoid unrelated changes, never inspect credentials." |
| `.github/agents/reviewer.agent.md` | "Create a reviewer using only the read and search tools. It must not edit, execute commands or delegate. Report concrete bugs and missing tests with file references." |
| `.github/prompts/review-changes.prompt.md` | "Create a reusable prompt using the reviewer agent. Review an attached diff for bugs and missing tests. Return findings only; do not edit or run commands." |
| `.github/skills/summarize-csv/SKILL.md` | "Create a summarize-csv skill with name and description frontmatter. Describe when to use it, how to run our CSV report, how to interpret the average, and how to run tests. It must not silently fix unrelated code." |

The presenter has reference templates if generation produces invalid frontmatter.
Review available tool names in your installed harness; tool restrictions must be
configured in the agent, not only requested in its prose.

At minimum, check these frontmatter values before testing:

```yaml
# .github/instructions/python.instructions.md
---
description: "Use when changing Python in the sales demo."
applyTo: "**/*.py"
---
```

```yaml
# .github/agents/reviewer.agent.md
---
name: reviewer
description: "Review supplied diffs for bugs and missing tests."
tools: [read, search]
---
```

```yaml
# .github/prompts/review-changes.prompt.md
---
description: "Review an attached diff without editing."
agent: reviewer
tools: [read, search]
---
```

The comments above label the snippets; each actual file starts with `---`.
Keep the requested instructions after the closing `---`; frontmatter alone is
not the complete file. The skill needs `name: summarize-csv` and a meaningful
`description` between its own frontmatter delimiters. `AGENTS.md` and repository
instructions are plain Markdown and do not need YAML.

The prompt's tools can override the agent's tools, so check **both** allowlists.
Neither should include edit, terminal/execute, delegation/agent or write-capable
MCP tools. A sentence saying "read-only" is not a tool restriction.

## 2. Verify actual behavior

1. Start a new regular Agent chat. Ask:

   **Prompt:** Add type hints and a short docstring to summarize. Follow the project instructions.
   Do not change calculations. Show which instruction files were applied.

   Review attached instruction context where available; do not rely only on the
   assistant saying it followed instructions. Run tests.
   Approve this bounded edit if prompted. The report must still end in 158.33.
2. Stage this small change with `git add summarize.py`.
   Run `git diff --cached` yourself and attach/paste the diff into a new chat.
   Select `/review-changes`. The reviewer should report findings or "No findings,"
   without edits or terminal commands. A read-only agent cannot fetch a staged
   diff using Git, so supply the diff yourself.
   In VS Code Chat type `/` and choose `review-changes`, or run **Chat: Run
   Prompt** if available. Keep the diff attached in that same chat; do not send
   it in an unrelated conversation. Check the selected agent is `reviewer`.
3. Select the **reviewer** agent directly:

   **Prompt:** Fix the average calculation.

   It may explain or suggest, but it must have no editing/execution tools.
   Stop if unexpected tools are available; correct the agent configuration.
4. In a new regular Agent chat:

   **Prompt:** Use the summarize-csv skill to explain how to run data/sales.csv and
   interpret the average. Do not edit anything.

   Check that the skill is loaded if your UI exposes that information.
   Return to regular Agent explicitly; the reviewer remains read-only. You can
   also select `/summarize-csv` if your version exposes skills as slash commands.
5. Inspect `git diff` and run `python -m pytest -q`. Commit the kit.

If the reviewer or slash command does not appear, save the files, start a new
chat, and check Chat's customization/configuration diagnostics if available.
If needed, run **Developer: Reload Window** and retry. Confirm you opened the
demo root (the folder containing `.github`), not its parent. Record discovery or
tool-list failures as blocked; an assistant's claim is not proof of enforcement.

## Optional: MCP

Add only an approved GitHub MCP server using VS Code's MCP setup.
Try "List open issues in my demo repository; read-only."
Skip it if policy or authentication blocks it. Do not add secrets to config files.
Specify the exact demo owner/repository in the request; an empty issue list is
valid before GH7. This optional server is not required for `gh` or the later PRs.

**Done when:** the prompt runs, the reviewer is tool-restricted, and a small
Python change follows the repository conventions.

**If blocked:** use the presenter's relevant template, reopen a chat, and verify
the filename, YAML and supported tool names. Do not copy all answers into the repo.
Next: [GH6 CLI](./06-cli.md) or [GH7 GitHub](./07-github.md).

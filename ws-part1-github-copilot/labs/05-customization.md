# GH5 - Make Copilot follow project conventions

**Time:** 25 minutes. **Starting point:** GH4 committed.
**Goal:** create a small reusable starter kit and test its behavior.

Do the repository instructions, reviewer and prompt first. The path instructions,
agent instructions and skill are short follow-ups; MCP is optional.

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

## 2. Verify actual behavior

1. Start a new regular Agent chat. Ask:

   **Prompt:** Add a short typed docstring to summarize. Follow the project instructions.
   Do not change calculations. Show which instruction files were applied.

   Review attached instruction context where available; do not rely only on the
   assistant saying it followed instructions. Run tests.
2. Stage this small change with `git add summarize.py`.
   Run `git diff --cached` yourself and attach/paste the diff into a new chat.
   Select `/review-changes`. The reviewer should report findings or "No findings,"
   without edits or terminal commands. A read-only agent cannot fetch a staged
   diff using Git, so supply the diff yourself.
3. Select the **reviewer** agent directly:

   **Prompt:** Fix the average calculation.

   It may explain or suggest, but it must have no editing/execution tools.
   Stop if unexpected tools are available; correct the agent configuration.
4. In a new regular Agent chat:

   **Prompt:** Use the summarize-csv skill to explain how to run data/sales.csv and
   interpret the average. Do not edit anything.

   Check that the skill is loaded if your UI exposes that information.
5. Inspect `git diff` and run `python -m pytest -q`. Commit the kit.

## Optional: MCP

Add only an approved GitHub MCP server using VS Code's MCP setup.
Try "List open issues in my demo repository; read-only."
Skip it if policy or authentication blocks it. Do not add secrets to config files.

**Done when:** the prompt runs, the reviewer is tool-restricted, and a small
Python change follows the repository conventions.

**If blocked:** use the presenter's relevant template, reopen a chat, and verify
the filename, YAML and supported tool names. Do not copy all answers into the repo.
Next: [GH6 CLI](./06-cli.md) or [GH7 GitHub](./07-github.md).

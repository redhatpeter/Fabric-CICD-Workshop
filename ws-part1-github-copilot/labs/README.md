# Part 1 hands-on labs

Build one tiny regional sales report while trying different Copilot surfaces.
All data is synthetic. No Azure, Fabric, database or production access is needed.

**Start with [GH2 setup](./02-setup.md)** before running the coding exercises.
Copy only the contents of [starter](./starter/) into your own `copilot-workshop-demo`
folder. Open that folder in VS Code, not this entire materials folder: otherwise
Copilot may find the presenter answers.

## Follow this order

| Section | Exercise | Done when |
| --- | --- | --- |
| GH0 | [Compare surfaces](./00-orientation.md) | You can explain which context each surface used |
| GH1 | [Access checklist](./01-access.md) | Required accounts and features are available |
| GH2 | [Set up the project](./02-setup.md) | The script runs and the two baseline tests pass |
| GH3 | [Editor features](./03-editor.md) | The top-region helper works |
| GH4 | [Compare chat modes](./04-modes.md) | The average is corrected and tested |
| GH5 | [Build the starter kit](./05-customization.md) | Instructions, prompt, reviewer and skill are exercised |
| GH6 | [Copilot CLI](./06-cli.md), optional | A region filter works without changing the default report |
| GH7 | [GitHub and cloud agent](./07-github.md) | An input-validation PR is reviewed |
| GH8 | [Safe approvals](./08-guardrails.md) | You inspect and deny a proposed overwrite |
| GH9 | [Capstone](./09-capstone.md) | Empty-input handling goes through a tested PR |

Keep each exercise small. If Copilot proposes unrelated changes, stop and narrow
the request. Its exact wording and generated code will vary; the checks matter
more than matching a screenshot.

## Working conventions

- Commands in the labs run from your **demo repository root**.
- After setup, `python` refers to your demo virtual environment.
- Use a new chat when switching exercises so old requests do not carry over.
- Before edits, inspect `git status`; after edits, inspect `git diff` and run tests.
- Commit your work at the end of each lab. Do not merge unrelated work together.
- Never copy real customer data, passwords or tokens into this exercise.
- GH6 can be skipped. GH7 and GH9 must not require the optional filter.

When a lab says to commit, review first:

```text
git status
git diff
python -m pytest -q
git add .
git diff --cached
```

Then ask Copilot to commit the staged exercise with a short message and the
required Co-authored-by trailer, or commit it yourself using your team's policy.
Do not stage personal files or unrelated changes. Before GH7, push the completed
local labs to `main` with `git push`.

## If you get stuck

1. Ask Copilot to explain the exact error before making more changes.
2. Compare the command and current directory with the lab instructions.
3. Save your work with a local commit or copy the folder to a new backup location.
4. For a fresh start, copy the starter into a **new** folder. Do not overwrite your work.
5. Ask the presenter for the smallest relevant solution, not the whole completed project.

The [presenter guide](./presenter/README.md) contains answers, templates and
rehearsal checks. It is not needed in the attendee repository.

# Part 1 — GitHub Copilot: Features, Setup and Environment

The first half of the workshop. It introduces GitHub Copilot, sets up the environment, and builds the
habits used in [Part 2 — Fabric CI/CD](../ws-part2-Fabric-CICD/workshop-part2-Fabric-CICD.md), where Copilot drives Git, branching, pull
requests and deployment pipelines through chat.

Part 1 is self-contained. It uses its own throwaway repository (`copilot-workshop-demo`), so nothing
here touches the Fabric workspaces or the `fabric-cicd-workshop` repository used in Part 2.

## Hands-on materials

Use the [lab index](./labs/README.md) alongside this feature guide. It provides
short steps, prompts, checks and recovery guidance for GH0 through GH9.
Start with [GH2 setup](./labs/02-setup.md): copy only the supplied
[starter project](./labs/starter/) into your own demo repository and open that
folder in VS Code. Do not include the presenter answers in the attendee workspace.

The labs use one synthetic sales dataset, with a different small task per topic:
editor helper, average fix, customization, optional filter, input validation and
empty-input capstone. Follow the lab scope so an agent does not finish later
exercises early. The [presenter guide](./labs/presenter/README.md) contains
reference solutions, customization templates and rehearsal commands.

## What this part covers

| Topic | Covered in |
| --- | --- |
| What Copilot is, and which surface to use | GH0 |
| Plans, licensing, policies, admin pre-checks | GH1 |
| Environment setup (VS Code, `gh`, Copilot CLI, WSL2) | GH2 |
| Editor features: suggestions, inline chat, smart actions | GH3 |
| Chat modes and agents in VS Code | GH4 |
| Customization: instructions, prompt files, agents, skills, MCP | GH5 |
| Copilot CLI | GH6 |
| Copilot on github.com: Chat, cloud agent, code review, Spaces | GH7 |
| Guardrails, privacy and cost | GH8 |
| Capstone and handoff to Part 2 | GH9 |

## How to read this guide

| Mark | Meaning |
| --- | --- |
| 🟢 | Can be done in VS Code, the Copilot CLI or `gh` |
| 🟡 | Works, but needs a portal or admin prerequisite first |
| 🔴 | github.com portal (or org/enterprise settings) only |

- **Sample prompt** column: a message to send to Copilot for that task. Replace the names in
  `<angle brackets>`.
- **Status:** Copilot changes quickly. Names, menus and limits in this guide come from the GitHub and
  VS Code documentation (see [What has and hasn't been tested](#what-has-and-hasnt-been-tested)).
  Treat anything not listed as tested as "verify on first run".

## Cast and naming used in this guide

| Name | What it is |
| --- | --- |
| Attendee | A developer with a Copilot seat |
| Org admin | The attendee (or a colleague) who is an **owner** of the GitHub organization or enterprise that grants the seats. Needed for GH1 and the admin parts of GH7 |
| Presenter | Runs the walkthrough. Does not need admin rights if an org admin attends |
| `copilot-workshop-demo` | Private demo repository created in GH2 and used through GH9 |
| `redhatpeter` / your account | The GitHub account that owns the demo repository. Use a personal account or an organization where you can create repositories |
| Starter kit | The set of Copilot customization files built in GH5 and carried to Part 2 |

```text
VS Code (editor, chat, agent) ──┐
Copilot CLI (terminal) ─────────┼──▶ copilot-workshop-demo (GitHub) ──▶ github.com: Chat, cloud agent,
gh CLI ─────────────────────────┘                                        code review, Spaces
                                          └──▶ Starter kit ──▶ Part 2 (fabric-cicd-workshop)
```

## Ground rules for the chat assistant

Put these in the first message of every session. They are also turned into a durable instructions
file in GH5.

**Prompt:** Before any step that deploys, overwrites, deletes, resumes or pauses a capacity, or changes
permissions, show me what will change and wait for my "yes". Never print access tokens. Use
read-only calls first.

---

## GH0 — Orientation: what Copilot is (15 min)

GitHub Copilot is an AI assistant that works in several places. The same account and seat work in all
of them.

| Surface | What it does | Typical use |
| --- | --- | --- |
| Inline suggestions (editor) | Completes code as you type and suggests the next edit | Writing code line by line |
| Inline chat and smart actions (editor) | Focused edit or explanation on a selection | Explain, fix, generate a commit message |
| Chat view (VS Code) | Ask questions, plan, or direct an agent over your workspace | Understand code, multi-file changes |
| Agent (VS Code) | Reasons, uses tools, edits files, runs terminal commands and tests | Implement a feature, fix a failing test |
| Copilot CLI (terminal) | Terminal-native agent with the same agent loop | Repo and CLI-driven work (`gh`, `az`, `fab`) |
| Copilot on github.com | Chat about repos, cloud agent, code review, Spaces | Delegate an issue, review a PR |

Pick the **least autonomous** option that fits the task: a suggestion for a line, inline chat for a
focused edit, chat for questions, an agent for a multi-step task, the cloud agent for work you want
done in the background and reviewed as a pull request.

The **agent loop**: the agent gathers context, acts with tools, checks the result, and repeats. You
review the diff and decide what to keep. You stay responsible for what ships.

| Task | Route | Sample prompt |
| --- | --- | --- |
| See the surfaces side by side | 🟢 | Follow [GH0 lab](./labs/00-orientation.md): explain the CSV loader in inline chat, the Chat view and another available surface. Compare the context each one had |

---

## GH1 — Licensing, policies and admin pre-checks (15 min)

### 1.1 Plans

| Plan | Who it is for | Notes |
| --- | --- | --- |
| Free, Student | Individuals | Allowance of AI credits, limited features |
| Pro, Pro+, Max | Individuals | Larger monthly AI credit allowances |
| **Business** | Organizations and enterprises | Centralized management and policy control |
| **Enterprise** | Enterprises on GitHub Enterprise Cloud | Everything in Business, a larger credit pool, extra enterprise features |

- Usage is measured in **GitHub AI Credits**. Business and Enterprise draw from the organization or
  enterprise's shared credit pool.
- This workshop assumes a **Business or Enterprise seat**. Free or Pro also works for GH2 to GH6.
  Some GH7 items depend on the policies below.
- Copilot is not available on GitHub Enterprise Server.

**Note:** Plan names, prices and allowances change. Check the
[plans page](https://docs.github.com/en/copilot/get-started/plans) before the session.

### 1.2 Who does what

| Task | Attendee | Org admin |
| --- | --- | --- |
| Get a seat | Receives it | 🔴 Assigns it (Settings > Copilot > Access) |
| Sign in to Copilot | 🟢 | |
| Enable or disable features and models | | 🔴 Settings > Copilot > Policies (organization), or enterprise AI controls |
| Enable the cloud agent | | 🔴 Disabled by default. Enable at enterprise (AI controls > Agents) and organization level |
| Enable third-party MCP servers for the cloud agent | | 🔴 Disabled by default. Enable in AI controls |
| Content exclusion, audit log, usage and billing views | | 🔴 Organization or enterprise settings |

Enterprise-level policy wins: if the enterprise sets a policy, an organization cannot override it.

### 1.3 Admin pre-check (do this before the workshop)

Attendees can use the short [GH1 access checklist](./labs/01-access.md).

The org admin attendee confirms, and the presenter ticks off:

- [ ] Every attendee has a Copilot seat
- [ ] Copilot Chat in the IDE and on github.com is enabled
- [ ] Models you want to demonstrate are enabled (the model picker only shows what policy allows)
- [ ] Copilot cloud agent is enabled for the organization and for the demo repository
- [ ] Copilot code review is enabled
- [ ] Third-party MCP servers: decided and set (needed only for the optional MCP demo)
- [ ] Copilot Spaces: enabled for the organization
- [ ] Attendees can create a private repository in the organization, or in their own account
- [ ] Any network allowlist for `github.com`, `api.github.com`, `*.githubcopilot.com` and the model
  endpoints is in place

| Task | Route | Sample prompt |
| --- | --- | --- |
| Confirm which account and seat you are using | 🔴 | Open github.com/settings/copilot and read the plan and the source of the seat |
| Ask what a policy does | 🟢 | "Explain what the Copilot cloud agent policy controls and who can change it." |

### 1.4 Data handling in one minute

- Business and Enterprise: review the Copilot Trust Center for retention and training terms.
- Matching public code: a setting that allows or blocks suggestions that match public code.
- VS Code telemetry is separate from model data handling.

---

## GH2 — Environment setup (20 min)

### 2.1 Tools to install

| Tool | Used for | Check it | Install (macOS) | Install (WSL2 / Ubuntu) | Install (Windows) |
| --- | --- | --- | --- | --- | --- |
| VS Code | Editor, Chat, Agent | `code --version` | `brew install --cask visual-studio-code` | Install on Windows, then add the **WSL** extension | `winget install Microsoft.VisualStudioCode` |
| GitHub Copilot Chat extension | Chat, agent, inline suggestions in VS Code | Extensions view | Installed from the Extensions view | Installed from the Extensions view | Installed from the Extensions view |
| Git (`git`) | Local edits | `git --version` | `brew install git` | `sudo apt install git` | `winget install Git.Git` |
| GitHub CLI (`gh`) | Repos, issues, PRs | `gh auth status` | `brew install gh` | `sudo apt install gh` | `winget install GitHub.cli` |
| Node.js 22 or later | Needed for the npm install of Copilot CLI | `node --version` | `brew install node` | Install Node.js 22 or later using a Node version manager | `winget install OpenJS.NodeJS` |
| Copilot CLI | Terminal agent | `copilot --version` | `brew install --cask copilot-cli` or `npm install -g @github/copilot` | `npm install -g @github/copilot` | `winget install GitHub.Copilot` or `npm install -g @github/copilot` |
| Python 3 | The demo project | `python3 --version` (macOS / WSL2); `python --version` (Windows) | `brew install python` | `sudo apt install python3 python3-venv python3-pip` | `winget install Python.Python.3.12` |

Run the Windows installation commands in PowerShell. After installation, open a new terminal so
the tools are available on your PATH.

**WSL2 note:** If you use WSL2, install VS Code on Windows and the **WSL** extension, then open the project from
WSL with `code .`. Run `git`, `gh` and `copilot` inside WSL so they share one environment.

### 2.2 Sign in

Sign in to each tool once:

```text
gh auth login
copilot          # then enter /login at the prompt
```

In VS Code, hover over the Copilot icon in the Status Bar, select **Use AI Features**, and sign in with
the GitHub account that holds your seat. If your seat comes from a GitHub Enterprise account, choose
the enterprise sign-in option and give your instance details.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Verify every tool and login | 🟢 | "Check that git, gh, node, python3 and copilot are installed and that gh is logged in. Show only account names and versions, not tokens." |
| See which GitHub account VS Code is using | 🟢 | Click the Accounts icon in VS Code and the Copilot icon in the Status Bar |
| Check your remaining allowance | 🟢 | Open the Copilot status dashboard from the Status Bar |

### 2.3 Behind a corporate network or Global Secure Access (WSL2)

Skip this section if sign-in worked.

- Symptoms: sign-in hangs, no browser opens, or Microsoft Entra / `login.microsoftonline.com` calls
  time out from WSL.
- Cause on some networks: DNS for `login.microsoftonline.com` resolves to a synthetic address that
  WSL cannot route. This mostly affects Azure and Fabric sign-in (`az`, `fab`) in Part 2, not GitHub.
- Fix: pin a real public IP for that host in `/etc/hosts`. It needs `sudo`, so type the command
  yourself. The pin does not survive a WSL restart, so check it again whenever a login hangs.
- For GitHub traffic, ask your network team to allow `github.com`, `api.github.com`,
  `*.githubcopilot.com` and `*.githubusercontent.com`.
- Never paste passwords or tokens into chat.

### 2.4 Create the demo repository and project

Follow [GH2 setup](./labs/02-setup.md) for the exact Windows and macOS/WSL commands:

1. Copy only the starter contents into a new `copilot-workshop-demo` folder.
2. Open that folder, create a virtual environment and install the test dependency.
3. Run the baseline script and tests.
4. Commit the baseline, then create and push a private GitHub repository.

Do not ask Copilot to regenerate the seed files: identical starters make the
checks and troubleshooting consistent for everyone.

### 2.5 Starter files

The [starter project](./labs/starter/) contains the script, synthetic CSV fixtures,
two baseline tests, pytest configuration and a pinned development dependency.
Its [README](./labs/starter/README.md) defines the business rules.

Run `python summarize.py data/sales.csv` from your demo root. The starter reports
the regional totals and an average of 118.75. Some behavior is deliberately
unfinished. Do not fix it all during setup; each later lab has a distinct task.

### 2.6 Readiness check

Send this single prompt in the Chat view:

**Prompt:** "Use my project virtual environment. Check that git and gh work, that I'm signed
in to gh, that summarize.py runs on data/sales.csv, and that python -m pytest -q
reports two passing baseline tests. Also check copilot if doing the optional CLI
lab, and Node.js if I installed it through npm. Report OK or not OK. Do not print tokens."

All lines OK means you can move on. Fix anything marked not OK first.

---

## GH3 — Copilot in the VS Code editor (20 min)

Follow [GH3 lab](./labs/03-editor.md). Complete the top-region helper, add its
tests and practice a rename. Keep the average unchanged until GH4.

| Feature | What to try | Route | Sample prompt or action |
| --- | --- | --- | --- |
| Inline suggestions | Type a comment, accept with `Tab` | 🟢 | In a new file type `# function that returns the top region by total` and press Enter |
| Next edit suggestions | Change a function signature and accept the follow-up edits | 🟢 | Rename `load` to `load_rows` and accept the suggested call-site edit |
| Inline chat | Select code and ask for a focused edit | 🟢 | Select `summarize` and ask "Add type hints and a docstring" |
| Smart actions | Explain, generate a commit message, fix | 🟢 | Right-click a selection, then Copilot > Explain. In Source Control use the sparkle button for a commit message |
| Chat view, ask questions | Context variables | 🟢 | "Explain `#file:summarize.py` without editing it." |
| Add context | `#file`, `#selection`, or drag a file into chat | 🟢 | "Using the attached `data/sales.csv`, what are the expected totals by region?" |
| Slash commands | `/` shows the available commands | 🟢 | `/explain`, `/fix`, `/tests` on a selection |
| Prepare a project | `/init` creates starter custom instructions | 🟢 | Enter `/init` and review what it writes before keeping it |

Discussion: when did you accept a suggestion without reading it? What would you change in how you
review?

---

## GH4 — Chat modes and agents (20 min)

Follow [GH4 lab](./labs/04-modes.md) to compare modes from the **same baseline**.
Ask and Plan come first. Undo only the Edit turn before comparing Agent, or skip
Edit if the undo controls are unclear. Otherwise the second mode has no bug left to fix.

Task: "The average in `summarize.py` looks wrong. Check it and fix it."

| Mode | What it does | Route | Observe |
| --- | --- | --- | --- |
| Ask | Answers questions, does not change files | 🟢 | Does it find the bug? Does it change anything? |
| Edit | Applies edits to files you choose | 🟢 | You pick the files. It edits them and you accept or reject |
| Agent | Finds files, edits, runs commands and tests on its own | 🟢 | Watch the tool calls. Approve or deny terminal commands |
| Plan | Researches and proposes a plan before any change | 🟢 | Review the plan, then hand it to an agent |

Things to practice:

| Skill | Route | Notes |
| --- | --- | --- |
| Pick a model | 🟢 | Use the model picker in the chat input. Only models allowed by policy appear |
| Approve and deny tools | 🟢 | Read the command before approving. Do not auto-approve everything |
| Undo | 🟢 | Use the checkpoint or undo controls to roll back an agent's edits |
| Stop and redirect | 🟢 | Interrupt the agent and give a new instruction |
| Continue a session elsewhere | 🟡 | VS Code can show sessions started in the Copilot CLI or the Copilot app, and can start a cloud session |

**Important:** Agent mode runs commands on your machine. Keep the ground rules in the first message, and review
every diff before you commit.

---

## GH5 — Customize Copilot (25 min)

Follow [GH5 lab](./labs/05-customization.md) for the creation prompts and behavior
checks. The presenter has reference templates if generation needs correction.

Build the **starter kit** in the demo repo. These files are loaded automatically (instructions) or on
demand (prompts, agents, skills).

| Customization | File | When it applies | Route |
| --- | --- | --- | --- |
| Repository instructions | `.github/copilot-instructions.md` | Every request in the repo | 🟢 |
| Path-specific instructions | `.github/instructions/*.instructions.md` with `applyTo` | Matching files only | 🟢 |
| Agent instructions | `AGENTS.md` | Read by several agents (also by the cloud agent) | 🟢 |
| Prompt file | `.github/prompts/*.prompt.md` | You run it from chat | 🟢 |
| Custom agent | `.github/agents/*.agent.md` | Chosen as a persona with its own tools | 🟢 |
| Skill | `.github/skills/<name>/SKILL.md` | Loaded when the task matches | 🟢 |
| MCP server | VS Code MCP configuration | Adds tools (for example GitHub) | 🟡 |

Check which file types your selected agent harness reads. VS Code lists the supported types in the
Agent Customizations editor.

### 5.1 Build the starter kit

| Task | Route | Sample prompt |
| --- | --- | --- |
| Repository instructions with the ground rules | 🟢 | "Create `.github/copilot-instructions.md` with these rules: [paste the ground rules]. Also say: Python 3, use type hints, add tests for new code." |
| Path-specific instructions | 🟢 | "Create `.github/instructions/python.instructions.md` with `applyTo: '**/*.py'` and rules: use `pytest`, keep functions small." |
| Prompt file | 🟢 | "Create `.github/prompts/review-changes.prompt.md` using the reviewer agent to review a supplied diff for bugs and missing tests. No edits or command execution." |
| Read-only reviewer agent | 🟢 | "Create `.github/agents/reviewer.agent.md`, a read-only reviewer that can read and search files but not edit or run commands." |
| Skill | 🟢 | "Create a skill `.github/skills/summarize-csv/SKILL.md` that explains how to run `summarize.py` and read its output." |

After each file, verify it:

- Start a new chat and ask "What instructions are you following?"
- Inspect applied instruction context where available and verify behavior; a verbal claim alone is not proof.
- Run `git diff --cached` yourself, attach its output, and run `/review-changes`.
- Pick the reviewer agent and ask it to fix a bug. It must refuse or only suggest.
- Verify its actual tool list excludes editing, execution and delegation.

### 5.2 Optional: an MCP server

| Task | Route | Sample prompt |
| --- | --- | --- |
| Add the GitHub MCP server in VS Code | 🟡 | Open the Command Palette, run **MCP: Add Server**, and follow the prompts for the GitHub server. Sign in when asked |
| Use it | 🟢 | "List the open issues in `copilot-workshop-demo`." |

Only add MCP servers you trust. Each server adds tools the agent can call. On Business and Enterprise,
organization policy can restrict third-party servers.

### 5.3 Troubleshooting a customization that is ignored

- Is the file in the right folder and does the name end with the right suffix?
- Is the front matter valid YAML?
- Does `applyTo` match the file you are editing?
- Did you select a harness that reads that file type?
- Start a fresh chat. Some changes load only for new sessions.

---

## GH6 — Copilot CLI (15 min, optional if short on time)

Follow [GH6 lab](./labs/06-cli.md) to add a region filter. The average was already
fixed in GH4. Later labs do not depend on this optional feature.

The CLI is useful in Part 2 because the Fabric work is CLI-driven (`fab`, `gh`, `az`, `git`).

| Task | Route | Sample prompt or command |
| --- | --- | --- |
| Start and sign in | 🟢 | `copilot`, then `/login` at the prompt. Confirm that you trust the folder |
| Ask about the project | 🟢 | "Give me an overview of this project." |
| Mention a file | 🟢 | Type `@` and pick `summarize.py` |
| List commands and help | 🟢 | `/help`, or `copilot help` |
| Run one prompt without the interactive UI | 🟢 | `copilot -sp "Explain what summarize.py does"` (`-s` prints only the answer) |
| Make a change with approval | 🟢 | "Add an optional `--region` filter and tests without changing the default report." Approve only after reading the proposed changes |
| Run a read-only check first | 🟢 | "Using gh, show the last 3 commits and any open pull requests. Read-only." |

Shortcuts: `Esc` cancels the current operation, `Ctrl+C` cancels or exits, `Ctrl+L` clears the
screen, `?` shows help.

**Important:** The CLI asks before it changes files or runs commands. Keep it that way. Do not use options that
allow every tool without asking, except in a disposable folder.

Sessions can also be continued in VS Code or watched from github.com when remote control is turned on.
Verify this on first run.

---

## GH7 — Copilot on github.com: Chat, cloud agent, code review, Spaces (30 min)

Follow [GH7 lab](./labs/07-github.md). Use the supplied invalid-data fixtures for
an input-validation issue; leave empty-input handling for GH9. Add the test and
agent-setup workflows before assigning the cloud task. Local fallback steps are included.

Most of this section is 🔴 (portal). Run it in `copilot-workshop-demo`. Steps that need org policy are
marked.

| Task | Route | Notes |
| --- | --- | --- |
| Copilot Chat on github.com | 🔴 | Open the repo, then the Copilot chat. Ask "How does `summarize.py` compute the average?" |
| Chat creates things | 🔴 | Chat can create branches, update files, and create or update issues |
| Create an issue | 🟢 | Use the title and acceptance criteria in the [GH7 lab](./labs/07-github.md): validate CSV input with useful errors |
| Hand the issue to the cloud agent | 🔴 (policy) | Assign the issue to Copilot, or start a task from the agents panel |
| Watch the session | 🔴 | Open the session log. It shows what the agent read, ran and changed |
| Review the pull request | 🔴 | Read the diff. Do not merge yet |
| Steer the agent | 🔴 | Comment on the pull request: "Please confirm there is a regression test for a negative amount." |
| Copilot code review | 🔴 (policy) | Add Copilot as a reviewer on the pull request, then apply or dismiss its suggestions |
| Pull request summary | 🔴 | Use the Copilot summary in the pull request description |
| Spaces | 🔴 (policy) | Create a space, add the demo README, `summarize.py` and `data/sales.csv`, then ask a question grounded in the business rules |

### 7.1 The cloud agent in more detail

| Topic | What to know |
| --- | --- |
| Where it runs | An ephemeral GitHub Actions-based environment, not your machine |
| What it does | Reads code, edits files, runs tests and linters, pushes a branch, opens a pull request |
| Who reviews | You. Treat the result like a pull request from a colleague |
| Default state | Disabled by default on Enterprise. An admin must enable it (see GH1) |
| Instructions | Reads `.github/copilot-instructions.md` and `AGENTS.md` from the repo |
| Environment | Add `.github/workflows/copilot-setup-steps.yml` to pre-install tools. The job must be named `copilot-setup-steps`, and the file must be on the default branch |
| Network | A firewall limits outbound access by default. Admins can adjust it |
| Secrets | Configure the agent's own secrets and variables. Do not give it production credentials |

| Task | Route | Sample prompt |
| --- | --- | --- |
| Add setup and test workflows | 🟢 | Follow the [GH7 lab](./labs/07-github.md): install `requirements-dev.txt` in both workflows, and run pytest on pull requests in a separate test workflow |
| Run the setup workflow by hand | 🔴 | Actions tab > Copilot Setup Steps > Run workflow |
| Re-run the issue task | 🔴 | Assign a second issue and compare how fast and reliable it is |

### 7.2 Admin demos (org admin attendee)

Run these live if an org admin attendee is present. Otherwise show the pages.

| Task | Route | Where |
| --- | --- | --- |
| Show and change a Copilot policy | 🔴 | Organization Settings > Copilot > Policies |
| Enable or restrict the cloud agent | 🔴 | Enterprise AI controls > Agents, then Organization settings |
| Content exclusion | 🔴 | Organization Settings > Copilot > Content exclusion |
| Usage and credits | 🔴 | Organization or enterprise Billing and licensing |
| Audit log | 🔴 | Organization or enterprise Audit log, filter for Copilot events |
| Automatic Copilot code review | 🔴 | Repository or organization rulesets (verify the current setting name) |

---

## GH8 — Guardrails, privacy and cost (10 min)

Follow [GH8 lab](./labs/08-guardrails.md): propose an overwrite of a disposable
practice file, deny it, and verify its contents. Never test with real credentials.
Instructions guide behavior; tool permissions and approvals provide stronger boundaries.

| Guardrail | Practice |
| --- | --- |
| Secrets | Never paste tokens, passwords or keys into chat, files or issues. Let tools read credentials from their own login store |
| Confirm before change | Ask Copilot to show what will change and wait for your "yes" before deploying, deleting, or changing permissions |
| Read-only first | Start with list, show and diff commands before anything that writes |
| Review the diff | An agent's work is a draft. Read every change. Run the tests yourself |
| Least privilege | Use short-lived, narrowly scoped tokens. Give the cloud agent no production secrets |
| Trusted tools | Only add MCP servers and extensions you trust |
| Content exclusion | Use it for files that must not be sent to a model. An admin sets it |
| Cost | Agents and larger models use more AI credits. Prefer the lightest option that works. Watch the usage dashboard |
| Attribution | Keep the Co-authored-by trailer when Copilot helps write a commit |

| Task | Route | Sample prompt |
| --- | --- | --- |
| Test the guardrail | 🟢 | Ask to inspect and propose replacing `output/approval-demo.txt`, then stop for approval. Deny the write and verify the original text remains |

---

## GH9 — Capstone and handoff to Part 2 (20 min)

Follow [GH9 lab](./labs/09-capstone.md) for a fresh task: handle a header-only CSV
with an empty summary and a zero average. The earlier average bug is already fixed.
This loop doubles as the Part 2 workflow readiness check.

| Step | Route | Sample prompt |
| --- | --- | --- |
| 1. Start from `main` with the starter kit committed | 🟢 | "Show the git status and the last commit." |
| 2. Plan the fix in VS Code | 🟢 | Use Plan mode: "Plan header-only CSV handling and regression tests, preserving input validation." |
| 3. Implement with the agent | 🟢 | "Implement the plan on a new branch `fix/empty-input`. Show me the diff before committing." |
| 4. Run the tests | 🟢 | "Run the tests and show the result." |
| 5. Open a pull request with `gh` | 🟢 | "Push the branch and open a pull request with a clear description." |
| 6. Review with Copilot | 🔴 (policy) | Add Copilot as a reviewer. Apply or dismiss each suggestion |
| 7. Local review with the reviewer agent | 🟢 | Supply the diff and select `reviewer`: "Review this diff for bugs." |
| 8. Merge | 🟢 | "Merge the pull request after the checks pass." |

### Handoff checklist

Before you start Part 2, check that you can:

- [ ] Run `gh`, `git` and `copilot`; install and authenticate `az` and `fab` during Part 2 setup (UC0.2)
- [ ] Open a Copilot chat in VS Code and in the terminal
- [ ] Reuse the ground rules from an instructions file
- [ ] Review and approve a tool call before it runs
- [ ] Open, review and merge a pull request with `gh`
- [ ] Explain which tasks were chat-driven and which needed the portal

### Starter kit to carry into Part 2

Copy these from `copilot-workshop-demo` into `fabric-cicd-workshop` after Part 2 UC0.3 creates it:

| File | Why |
| --- | --- |
| `.github/copilot-instructions.md` | Puts the ground rules in every Part 2 chat |
| `.github/prompts/review-changes.prompt.md` | Reviews a diff before commit or pull request |
| `.github/agents/reviewer.agent.md` | Read-only reviewer for the merge exercise in Part 2 UC5 |

Remove or edit anything specific to `summarize.py`.

### Cleanup

- Delete the demo repository when you finish, or archive it.
- Revoke any token you created. Remove any MCP server you added only for the workshop.
- Sign out of accounts on shared machines.

---

## Suggested session plan

| Session | Sections | Time |
| --- | --- | --- |
| 1 | GH0, GH1 orientation, plans, admin pre-check | 30 min |
| 2 | GH2 environment setup and readiness check | 30 min |
| 3 | GH3, GH4 editor features and chat modes | 40 min |
| 4 | GH5 customization and the starter kit | 25 min |
| 5 | GH6 Copilot CLI (optional) | 15 min |
| 6 | GH7 Copilot on github.com | 30 min |
| 7 | GH8, GH9 guardrails, capstone and handoff | 30 min |

The table totals **3 hours 20 minutes** with GH6, or **3 hours 5 minutes**
without it, excluding breaks and cloud-agent delays. Move installations,
authentication and admin checks into prework to reduce live setup time.

---

## Chat versus portal at a glance

| Area | Mostly chat, editor or CLI | Needs the portal or admin |
| --- | --- | --- |
| Setup | Install checks, sign-in checks, repo creation with `gh` | Assigning seats, plan choice |
| Policies | Explaining what a policy does | Changing policies and AI controls |
| Editor features | All of GH3 | None |
| Chat modes and agents | All of GH4 | None |
| Customization | Creating and testing the starter kit | Organization-wide instructions and agents (admin) |
| Copilot CLI | All of GH6 | None |
| Cloud agent | Creating the issue and the setup-steps file | Enabling it, assigning the issue, reading the session |
| Code review | Local review with the reviewer agent | Adding Copilot as a reviewer, automatic review rules |
| Spaces | Using a space through the GitHub MCP server | Creating and sharing the space |
| Governance | None | Content exclusion, audit log, usage and billing |

## What has and hasn't been tested

**Local lab checks (2026-10-23, Linux / Python 3.12):**

- Starter: two baseline tests pass; normal output retains the exercise's 118.75 average.
- Completed reference: 24 tests pass, covering calculations, the optional filter,
  empty input, validation and CLI error behavior.
- Material checks: starter output, Python syntax and local Markdown file targets pass.
- See the [presenter guide](./labs/presenter/README.md) to repeat these checks.
  Windows/macOS commands, other Python versions, live Copilot customization loading
  and GitHub workflows still require the manual walkthrough.

**Checked against current documentation (2026-10-21):**

- Plan names and the GitHub AI Credits model.
- Cloud agent, code review and Spaces descriptions, and the default-off state of the cloud agent
  and third-party MCP servers.
- The `copilot-setup-steps.yml` rules (job name, default branch, permitted settings).
- Copilot CLI install options, `/login`, `-p`, `-s`, `@`, `/help` and the shortcuts.
- VS Code sign-in steps, `/init`, and the customization file types.

**Not run end to end — verify the first time:**

- Every step in a real tenant with a Business or Enterprise seat. The presenter account used while
  drafting has no organization admin rights, so GH1 and the admin demos in GH7 are untested.
- The exact menu names and locations in VS Code and github.com. They change often.
- Assigning an issue to Copilot, adding Copilot as a reviewer, and automatic review rules. These
  depend on policy and plan.
- Remote control between the CLI and github.com.
- Network allowlist entries for your environment.
- The WSL2 sign-in workaround in section 2.3 (taken from experience with Global Secure Access, not
  from documentation).
- The attendee sequence with live Copilot, including starter-kit discovery, tool restrictions
  and the capstone PR. Local reference tests do not replace this rehearsal.

## Learn links

- [Plans for GitHub Copilot](https://docs.github.com/en/copilot/get-started/plans)
- [Where to use GitHub Copilot](https://docs.github.com/en/copilot/get-started/where-to-use-github-copilot)
- [GitHub Copilot on GitHub.com](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github)
- [Managing policies and features in your organization](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies)
- [Enabling Copilot cloud agent in your enterprise](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/enable-copilot-cloud-agent)
- [Configure the cloud agent development environment](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment)
- [About Copilot Spaces](https://docs.github.com/en/copilot/concepts/prompting-and-context/spaces)
- [Getting started with Copilot CLI](https://docs.github.com/en/copilot/get-started/cli-quickstart)
- [Set up GitHub Copilot in VS Code](https://code.visualstudio.com/docs/setup/copilot)
- [Build with AI in VS Code](https://code.visualstudio.com/docs/agents/overview)
- [Create and manage agent customizations in VS Code](https://code.visualstudio.com/docs/agent-customization/overview)
- [GitHub Copilot Trust Center](https://resources.github.com/copilot-trust-center/)

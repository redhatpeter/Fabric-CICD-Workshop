# GitHub Copilot and Microsoft Fabric CI/CD Workshop

## Prerequisites - complete before the workshop

### Accounts, access and permissions

| Requirement | Part 1: GitHub Copilot | Part 2: Fabric CI/CD |
| --- | --- | --- |
| GitHub account | Required; sign in to VS Code with the account that has Copilot access | Required; create your own private workshop repository |
| GitHub Copilot access | Required for AI exercises; Business/Enterprise is the organizational scenario, while other eligible plans can support local exercises | Required for the chat-driven experience; portal, Git and CLI instructions remain usable without AI |
| Repository permissions | Create a private demo repository; push branches, open and merge PRs, and manage its workflows | Same permissions, plus permission to run GitHub Actions |
| Organization policies | Organizer confirms allowed models, Chat, cloud agent, code review and Spaces; unavailable optional features can be presenter demos | Organizer confirms Actions and the workflow actions are permitted |
| Microsoft Fabric account | Not needed | Required, in a tenant supporting Notebook/Lakehouse Git integration and deployment pipelines |
| Fabric capacity | Not needed | Access to an **existing active capacity** suitable for these features; no new capacity is required |
| Fabric workspace permissions | Not needed | Ability to create four disposable workspaces on the capacity and be **Admin** on them; connecting Git and assigning stage workspaces require Admin |
| Deployment pipeline permissions | Not needed | Ability to create a pipeline; **pipeline Admin** plus Contributor or higher in both source and target workspaces to deploy |
| Fabric GitHub credentials | Not needed | A short-lived GitHub token scoped to the attendee repository, with **Contents: Read and write**, registered through Fabric's credential dialog |

**Organizer/admin checks for Part 2:**

- Enable the applicable tenant settings for workspace/item creation, Git
  synchronization, and specifically **GitHub synchronization**.
- Confirm each participant can assign their workshop workspaces to the approved
  capacity and use deployment pipelines.
- If an organization requires approval of fine-grained GitHub tokens, arrange
  that approval before class.
- Check GitHub plan support for branch protection and required reviewers in
  private repositories. Where unavailable, the labs use manual review/checks;
  that is **not enforced merge or release protection**.

Participants do **not** need tenant-wide admin rights. Ask the organizer/admin
to prepare policies and access instead of changing them during the workshop.
The core labs do **not** require an Azure subscription owned by each participant,
an Entra app registration, a service principal, Power BI Desktop or an MCP server.
Those are separate from the broader Part 2 reference's optional automation topics.

### Programs and extensions to install

Use your organization's approved installation process. Install before class and
open a new terminal afterward so commands are available on `PATH`.

| Program / extension | Required for | Installation / check |
| --- | --- | --- |
| [Visual Studio Code](https://code.visualstudio.com/download) | Both parts | Install a current supported version; `code --version` |
| GitHub Copilot Chat / Copilot integration in VS Code | AI exercises in both parts | Enable/install through Extensions, sign in, and confirm Chat responds |
| [Git](https://git-scm.com/downloads) | Both parts | `git --version`; configure your approved commit name/email |
| [GitHub CLI](https://cli.github.com/) (`gh`) | Both parts | `gh --version`, then `gh auth login` |
| [Python](https://www.python.org/downloads/) **3.10+**, with `venv` and `pip` | Both parts | `python --version` or `python3 --version`; Python 3.12 is a convenient choice |
| Web browser | GitHub exercises and Fabric portal | Sign in to GitHub and, for Part 2, Microsoft Fabric |
| VS Code Python extension | Recommended | Interpreter selection and Python editing |
| VS Code WSL extension | Only if using WSL2 | Install VS Code on Windows; open the project inside WSL |
| [Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli) | Optional terminal-agent exercises | `copilot --version`; launch `copilot` and use `/login` |
| Node.js **22+** and npm | Only for the npm installation of Copilot CLI | `node --version`; `npm install -g @github/copilot` |
| Fabric CLI (`fab`) | Optional chat-driven Fabric operations; portal route available | In an appropriate Python environment: `python -m pip install ms-fabric-cli`; `fab --version`, then `fab auth login` |
| Azure CLI (`az`) | Optional advanced Part 2 reference scenarios | `az version`; not required for the beginner lab path |

PowerShell on Windows or a shell on macOS/Linux/WSL is sufficient. The detailed
[Part 1 setup reference](./ws-part1-github-copilot/workshop-part1-github-copilot.md#21-tools-to-install)
includes platform-specific installation commands.

**WSL2/corporate networks:** keep your project, Git, GitHub CLI and Python
environment inside WSL. Confirm access to GitHub, Copilot, Fabric and Microsoft
sign-in endpoints under your network policy. If Fabric sign-in hangs, stop and
consult the [Part 2 readiness guidance](./ws-part2-Fabric-CICD/labs/00-readiness.md#2-check-tools);
do not repeatedly retry or change corporate network controls yourself.

### Python libraries and sample data

| Part | Local libraries | Data / execution |
| --- | --- | --- |
| Part 1 | Install the supplied development requirements: **pytest**, pinned in the starter | Synthetic CSV files and a prebuilt Python script; no Azure/Fabric access |
| Part 2 | **No third-party packages required** for the supplied helper scripts and tests; uses `unittest` and the Python standard library | Synthetic CSV plus a notebook with the same rows embedded; Spark runs in Fabric |

Create a separate virtual environment in **each attendee project**, not in the
materials repository. Follow the setup lab for activation instructions:

```text
python -m venv .venv
```

After activating the Part 1 attendee environment, install and check:

```text
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

After activating the Part 2 attendee environment, check:

```text
python -m unittest discover -s tests -v
python checks/validate_items.py
```

Use `python3` on macOS/WSL or `py -3` on Windows before activation if needed.
Part 2 does **not** require installing PySpark, Delta Lake or Jupyter locally,
uploading sample CSV data, or installing `fabric-cicd`. Its Fabric runtime
provides Spark and NotebookUtils. Installing optional CLIs is separate from the
starter scripts' dependency requirements.

### Before-you-arrive checklist

- [ ] VS Code Chat responds using the intended GitHub/Copilot account.
- [ ] Python, Git and `gh` are installed; GitHub authentication works.
- [ ] You can create a private repository and run GitHub Actions.
- [ ] For Part 2, Fabric sign-in, capacity access and workspace/pipeline permissions are confirmed.
- [ ] For Part 2, GitHub tenant synchronization and the token/connection setup are ready.
- [ ] Use only synthetic data and disposable resources; never paste credentials into chat.

## Workshop overview

Learn the Copilot workflow locally, then use it to release a small Fabric
notebook through Git, pull requests, validation and deployment stages.

| | Part 1 - GitHub Copilot | Part 2 - Fabric CI/CD |
| --- | --- | --- |
| Focus | Collaborate with Copilot safely while editing, testing and reviewing code | Move a reviewed change from development to Test and lab Production |
| Workload | Tiny Python regional-sales report | Tiny Fabric sales notebook and lakehouse |
| Main activities | Editor assistance, chat/agent modes, customization, CLI, GitHub and a capstone PR | Git integration, isolated branch workspace, PR checks, selective deployment, approval and recovery |
| Environment | Local project and a private GitHub demo repository | Separate private repository, four Fabric workspaces and one deployment pipeline |
| Outcome | A tested change delivered through a reviewed PR | A reviewed release verified independently in each target workspace |

Part 1 is self-contained. Part 2 does not depend on completing Part 1's Python
features; carry forward the reviewed workflow habits and relevant Copilot
instructions, not the Part 1 demo application.

## Part 1 - GitHub Copilot labs

Start with [the Part 1 lab index](./ws-part1-github-copilot/labs/README.md).
Complete setup before the coding exercises.

| Lab | Topic |
| --- | --- |
| GH0-GH2 | Compare Copilot surfaces, check access, set up the supplied sales project |
| GH3-GH4 | Editor features and chat/agent modes; make small tested changes |
| GH5 | Repository instructions, prompts, reviewer agent and skill customization |
| GH6 | Optional Copilot CLI exercise |
| GH7-GH8 | GitHub collaboration, policy-dependent cloud features, safe approvals |
| GH9 | Capstone: ship empty-input handling through a tested PR |

- [Full Part 1 reference](./ws-part1-github-copilot/workshop-part1-github-copilot.md)
- [Attendee starter](./ws-part1-github-copilot/labs/starter/)
- [Presenter guide and answers](./ws-part1-github-copilot/labs/presenter/README.md)

## Part 2 - Fabric CI/CD labs

Start with [the Part 2 lab index](./ws-part2-Fabric-CICD/labs/README.md).
Allow approximately **2 hours 45 minutes**, plus installations, sign-in, admin
preparation and Spark startup. Live recovery is optional.

| Lab | Topic |
| --- | --- |
| 00 | Readiness, unique resource names and starter setup |
| 01 | Import/run baseline in Dev; deploy lakehouse and notebook to Test |
| 02 | Sync Fabric definitions to Git; enable CI; create an isolated branch workspace |
| 03 | Activate the prebuilt tax feature; validate, review, merge and update Dev |
| 04 | Selectively deploy the notebook to Test and verify persisted results |
| 05 | Explicitly approve Test -> lab Production and run target checks |
| 06 | Revert/redeploy recovery and intentional, approved cleanup |

```text
feature branch --> PR + checks --> main --> update Dev from Git
                                               |
                                               +--> Test --> approval --> lab Production
```

The supplied baseline has **3 rows totaling 350.00**. The prebuilt feature adds
a 10% tax-inclusive column totaling **385.00**, so participants focus on CI/CD
rather than writing a data transformation.

- [Full Part 2 reference](./ws-part2-Fabric-CICD/workshop-part2-Fabric-CICD.md)
- [Attendee starter and scripts](./ws-part2-Fabric-CICD/labs/starter/README.md)
- [Presenter guide and answers](./ws-part2-Fabric-CICD/labs/presenter/README.md)

The full reference also covers advanced scenarios beyond these beginner labs:
multiple developers/conflicts, reports/semantic models, variable libraries,
deployment plans, service principals and automated release workflows.

## How to use this repository

1. Download or clone these **materials**:

   ```text
   git clone https://github.com/redhatpeter/Fabric-CICD-Workshop.git
   ```

2. Read the relevant lab index.
3. Copy **only that part's `labs/starter/` contents**, including its `.gitignore`,
   into a **new folder outside this repository**.
4. Open only the new attendee folder in VS Code. Keep instructions available in
   a browser or another window.
5. Follow the setup lab to create your own private demo repository.
6. Do not copy presenter solutions into the attendee workspace: Copilot could
   discover the answers and complete later exercises prematurely.

The public materials repository is **not** your Fabric Git-sync repository.
Part 1 and Part 2 each use their own attendee project and repository.

## Safety, cost and validation status

- Never put tokens, passwords or real customer data in notebooks, Git or chat.
- Preview writes, syncs, deployments, permission changes and deletions before approval.
- Part 2's notebook deliberately overwrites one synthetic table and its schema.
  Inspect its target workspace and lakehouse before every run.
- Deployment copies **definitions, not table data**; each target runs its own notebook.
- Chat approval is a teaching practice, not an enforceable security boundary.
- A running paid Fabric capacity can incur costs. Use only your approved capacity;
  never pause or delete shared infrastructure. Cleanup is explicit, not automatic.
- Part 2 passed **12 local starter tests and 8 material checks**. That does not
  certify live Fabric/GitHub behavior: notebook import, Spark execution, Git sync,
  Actions, binding, deployment and recovery still require a live-tenant rehearsal.

Presenters should complete the relevant rehearsal checklist before teaching.
Both parts include presenter-only verification scripts and expected results.

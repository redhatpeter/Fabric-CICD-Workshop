# Fabric CI/CD Workshop — Git, Branching, Pull Requests, and Deployment Pipelines

A hands-on workshop that walks one change from a developer's workspace through Test to Production,
using **chat-driven CLI and REST calls** wherever possible and the portal only where it must be used.

## Hands-on materials

For a shorter beginner workshop, follow the [step-by-step lab index](./labs/README.md).
It takes one prebuilt sales notebook through Git, an isolated branch, PR checks,
Test and an approved lab Production deployment. Copy only the supplied
[attendee starter](./labs/starter/) into a new repository; it includes synthetic
data, a working notebook, a preview/apply release helper and offline checks.
Keep the [presenter answers and rehearsal guide](./labs/presenter/README.md) out
of the attendee workspace. The labs do not require semantic models, reports,
service principals or automated release credentials.

The sections below remain the broader reference. The beginner labs use one
developer, unique workspace-name suffixes and a `/fabric` Git directory.
Local material checks are not a live-tenant certification; rehearse Fabric
permissions, synchronization, bindings and Spark runs before presenting.

## What this workshop covers

The official Fabric CI/CD overview lists these platform layers. The table shows where each one is
practiced.

| CI/CD layer | Covered in |
| --- | --- |
| Git integration | UC2, UC3, UC4, UC5 |
| Deployment pipelines | UC1, UC7, UC10 |
| Fabric REST APIs | Used throughout |
| Variable library (per-stage configuration) | UC8 |
| Deployment plan (Preview) | UC9 |
| Fabric CLI | Used throughout |
| `fabric-cicd` | UC13 |
| Terraform (infrastructure as code) | Not covered |

Also covered: pull-request checks (UC6), production approval (UC10), rollback (UC11), and automation
identity with a service principal (UC12).

## How to read this guide

| Mark | Meaning |
| --- | --- |
| 🟢 | Can be done from the CLI or REST API through chat |
| 🟡 | CLI or REST works, but needs a portal or GitHub prerequisite first |
| 🔴 | Portal (or GitHub website) only |

- **Sample prompt** column: a message to send to the chat assistant for that task. Replace the names
  in `<angle brackets>`.
- **Status:** the routes come from the official Fabric REST reference, the installed `fab` help
  output, and the read-only calls listed in [What has and hasn't been tested](#what-has-and-hasnt-been-tested).
  Treat anything not in that tested list as "verify on first run".

## Cast and naming used in this guide

| Name | What it is |
| --- | --- |
| Dev A, Dev B | Two developers, each working on their own branch |
| Release manager | Owns the pipeline and promotes content to Test and Production |
| `wk-dev` | Shared development workspace, connected to branch `main` |
| `wk-test` | Test stage workspace, not connected to Git |
| `wk-prod` | Production stage workspace, not connected to Git |
| `wk-dev-a`, `wk-dev-b` | Branched workspaces for Dev A and Dev B |
| `fabric-cicd-workshop` | Private GitHub repository |
| `feature/dev-a`, `feature/dev-b` | The two feature branches |
| `wk-pipeline` | The deployment pipeline (stages: Development, Test, Production) |
| `vl_workshop` | Variable library with one value set per stage |
| `sp-fabric-cicd` | Service principal used for automation |

```text
wk-dev-a ──commit──▶ feature/dev-a ──PR──┐
                                         ├──▶ main ──Update──▶ wk-dev ──deploy──▶ wk-test ──approve + deploy──▶ wk-prod
wk-dev-b ──commit──▶ feature/dev-b ──PR──┘
```

## Ground rules for the chat assistant

Put these in the first message of every session.

> Before any step that deploys, overwrites, deletes, resumes or pauses a capacity, or changes
> permissions, show me what will change and wait for my "yes". Never print access tokens. Use
> read-only calls first.

---

## UC0 — Prerequisites and starter items

### 0.1 Accounts and permissions

| Need | Detail |
| --- | --- |
| Microsoft Fabric access | A Fabric capacity (a trial or an F SKU) in the **Active** state. A paused capacity makes workspace operations fail |
| Workspace role | **Admin** on the workspaces you create (connecting a workspace to Git needs Admin) |
| GitHub account | Can create a **private** repository |
| Azure subscription (optional) | Only needed if you pause and resume the capacity from the CLI |
| Microsoft Entra permission (UC12) | Ability to create an app registration and service principal |

Tenant settings a Fabric admin must have enabled (OneLake catalog > Govern > Configurations > Tenant settings):

- Users can synchronize workspace items with their Git repositories
- Users can synchronize workspace items with GitHub repositories
- Create workspaces (needed for Branch out to a new workspace)
- Users can create Fabric items
- Service principals can use Fabric APIs (needed for UC12)

GitHub plan check (needed for UC6 and UC10):

- Environment protection rules such as **required reviewers** work on **public** repositories on
  GitHub Free, and on private repositories only with GitHub Pro, Team or Enterprise (GitHub
  documentation).
- Branch protection on a private repository may also need a paid plan. Check your plan before UC6.
- UC6 and UC10 give a fallback if your plan doesn't allow these gates.

### 0.2 Tools to install

| Tool | Used for | Check it | Install (macOS) |
| --- | --- | --- | --- |
| Azure CLI (`az`) | Sign-in, capacity pause/resume | `az version` | `brew install azure-cli` |
| Fabric CLI (`fab`) | Workspaces, items, REST calls (`fab api`), jobs | `fab auth status` | `pip install ms-fabric-cli` |
| GitHub CLI (`gh`) | Repo, branches, pull requests | `gh auth status` | `brew install gh` |
| Git (`git`) | Local edits and conflict resolution | `git --version` | `brew install git` |
| Python 3 | Small helper scripts | `python3 --version` | already installed or `brew install python` |
| `fabric-cicd` (optional) | Code-first deployment in UC13 | `pip index versions fabric-cicd` | `pip install fabric-cicd` |

Sign in to each tool once:

```text
az login
fab auth login
gh auth login
```

| Task | Route | Sample prompt |
| --- | --- | --- |
| Verify every tool and login | 🟢 | "Check that az, fab, gh and git are installed and logged in. Show only the account names, not tokens." |
| Check the capacity is Active | 🟢 | "List my Fabric capacities and tell me if `<capacity>` is Active." |
| Resume a paused capacity | 🟢 (billing starts) | "Capacity `<capacity>` is paused. Explain the cost, then wait for my yes before resuming it." |

### 0.3 GitHub repository and token

| Task | Route | Sample prompt |
| --- | --- | --- |
| Create a private repo with a first commit on `main` | 🟢 | "Create a private GitHub repo `fabric-cicd-workshop` with a README so `main` exists." |
| Create a fine-grained token | 🔴 | Done on GitHub: Settings > Developer settings > Personal access tokens > Fine-grained tokens |
| Register the token with Fabric | 🔴 | Done in Fabric: Source control > Accounts tab > Add account. Paste the token there only |

Token settings:

- **Repository access:** only select repositories, and pick `fabric-cicd-workshop`.
- **Repository permissions:** **Contents: Read and write**. Metadata (read-only) is added automatically.
- **Account permissions:** none.
- **Expiry:** short, for example 30 days. Delete it at the end (UC14).

> Never paste the token into chat or a file. A token with Read only can connect and sync but cannot
> commit or create branches.

### 0.4 Workspaces

| Task | Route | Sample prompt |
| --- | --- | --- |
| Create `wk-dev`, `wk-test` and `wk-prod` on the capacity | 🟢 | "Create workspaces wk-dev, wk-test and wk-prod on capacity `<capacity>` with fab. Show the command first." |
| Confirm they exist | 🟢 | "List my workspaces and show wk-dev, wk-test and wk-prod with their capacity." |

`fab mkdir wk-dev.Workspace -P capacityName=<capacity>` is the shape of the command. Run
`fab mkdir x.Workspace -P` to confirm the parameter name on your version.

### 0.5 Starter items in `wk-dev`

Keep the items small so every later step finishes quickly.

| Item | Purpose | How |
| --- | --- | --- |
| Lakehouse `lh_workshop` | Holds one small table | 🟢 `fab mkdir wk-dev.Workspace/lh_workshop.Lakehouse` |
| Notebook `nb_workshop` | Creates a 3-row Delta table `sales_wk` in the lakehouse | 🟡 `fab import` a notebook folder the assistant writes, or create it in the portal |
| Semantic model `sm_workshop` | Gives the report something to depend on | 🔴 Lakehouse > New semantic model |
| Report `rpt_workshop` | A report bound to `sm_workshop`, to demonstrate dependencies during partial deployment | 🔴 Create it from the semantic model |
| Variable library `vl_workshop` | One variable, `env_label`, with three value sets (`dev`, `test`, `prod`), used in UC8 | 🟡 Variable Library API, or create it in the portal |

| Task | Route | Sample prompt |
| --- | --- | --- |
| Create the lakehouse | 🟢 | "Create a lakehouse lh_workshop in workspace wk-dev." |
| Create the notebook and run it | 🟡 | "Create a notebook nb_workshop in wk-dev, attached to lh_workshop, with one cell that writes a Delta table sales_wk with 3 rows (Online 100, Store 200, Partner 50). Run it and show the job status." |
| Confirm the table exists | 🟢 | "List the tables in lh_workshop and show the row count of sales_wk." |
| Create the variable library | 🟡 | "Create a variable library vl_workshop in wk-dev with a string variable env_label and three value sets: dev, test and prod. Read the Variable Library REST reference first and show me the request." |

Portal steps (semantic model and report) are done once. Afterward, ask the assistant to list the
items and confirm the report points at `sm_workshop`.

### 0.6 Readiness check

| Check | Expected |
| --- | --- |
| `fab auth status` | Logged in |
| Capacity | Active |
| `wk-dev` items | `lh_workshop`, `nb_workshop`, `sm_workshop`, `rpt_workshop` |
| `wk-test` and `wk-prod` | Exist and are empty |
| GitHub repo | Private, has `main` |
| `vl_workshop` | Exists with three value sets |
| Tenant setting | Service principals can use Fabric APIs is on (UC12) |

Sample prompt: "Run the UC0 readiness check and give me a pass or fail for each line."

---

## UC1 — Build the release path (deployment pipeline)

A deployment pipeline copies content from one stage's workspace to the next.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Create pipeline `wk-pipeline` with Development, Test and Production stages | 🟢 Create Deployment Pipeline API | "Create a deployment pipeline wk-pipeline with three stages, Development, Test and Production. Read the REST reference first and show me the request body. Remember the stage count and names can't change later." |
| Assign `wk-dev`, `wk-test` and `wk-prod` to the three stages | 🟢 Assign Workspace To Stage API | "Assign wk-dev to Development, wk-test to Test and wk-prod to Production in wk-pipeline." |
| Grant a user the pipeline Admin role | 🟢 pipeline role-assignment APIs | "Add `<user>` as Admin on wk-pipeline. Show the change first." |
| List the stages and their items | 🟢 List Stages and List Stage Items APIs | "Show each stage of wk-pipeline with its workspace and item list." |
| Compare two stages | 🟡 | "Compare the items in Development and Test and tell me which exist in only one." |
| Set a deployment rule (rebind a data source or parameter in Test) | 🔴 | Portal only: pipeline > Test stage > Deployment rules. UC8 shows the code-first alternative |

Notes:

- The number of stages and their names are **permanent** once the pipeline is created. Decide on
  three stages now, even though Production is first used in UC10.
- A deployment rule can't be created in the first stage.
- The "Different from source" label is a portal view. Through the API you compare the item lists.
- Deploying needs **two** gates: pipeline Admin, and Contributor or higher in **both** workspaces.

---

## UC2 — Source control for a workspace

Connect `wk-dev` to `main` so item definitions are stored as files.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Check my Git credentials are configured | 🟢 Get My Git Credentials API | "Check whether my Fabric Git credentials are configured and which source they use." |
| Connect `wk-dev` to repo `fabric-cicd-workshop`, branch `main` | 🟡 Connect API | "Connect workspace wk-dev to GitHub repo fabric-cicd-workshop, branch main, directory /. Show the request body first." |
| Initialize the connection | 🟢 Initialize Connection API | "Initialize the Git connection for wk-dev, preferring the workspace content." |
| First sync (commit the workspace to Git) | 🟢 Commit To Git API | "Commit all of wk-dev to Git with the comment 'initial workshop items'." |
| Show Git status (Uncommitted, Incoming, Synced) | 🟢 Get Status API | "Show the Git status of wk-dev and list any items that are uncommitted or have incoming changes." |
| Commit only selected items | 🟢 Commit To Git, selective mode | "Commit only nb_workshop in wk-dev with the comment 'notebook change'." |
| Update the workspace from Git | 🟢 Update From Git API | "Update wk-dev from Git and tell me which items changed." |
| Show the connected repo and branch | 🟢 Get Connection API | "Which repo and branch is wk-dev connected to, and what was the last sync?" |

Notes:

- **Connect** needs a workspace Admin. **Commit** and **Update** need Contributor or higher.
- For GitHub, **Automatic** credentials are blocked on the Connect API. Use a configured connection
  (a connection ID from the Fabric connection that holds your token).
- The workspace connects to **one** branch only.
- Connect doesn't sync. Run **Initialize Connection**, then Commit or Update.
- Choose the initialization strategy deliberately: prefer the workspace when the repo is empty, prefer
  the remote when the repo already holds the content.

---

## UC3 — Branch out for Dev B (separate workspace per branch)

Each developer works in an isolated workspace tied to their own branch.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Create branch `feature/dev-a` from `main` | 🟢 `gh api` | "Create branch feature/dev-a from main in fabric-cicd-workshop." |
| Create branch `feature/dev-b` from `main` | 🟢 `gh api` | "Create branch feature/dev-b from main in fabric-cicd-workshop." |
| Create workspace `wk-dev-a` on the capacity | 🟢 `fab mkdir` | "Create workspace wk-dev-a on capacity `<capacity>`." |
| Create workspace `wk-dev-b` on the capacity | 🟢 `fab mkdir` | "Create workspace wk-dev-b on capacity `<capacity>`." |
| Give Dev B Admin on `wk-dev-b` | 🟢 `fab acl set` | "Give `<Dev B object id>` the Admin role on wk-dev-b." |
| Connect each branch workspace to its branch | 🟡 Connect API | "Connect wk-dev-a to branch feature/dev-a and wk-dev-b to feature/dev-b." |
| Initialize and pull the items in | 🟢 Initialize Connection, then Update From Git | "Initialize both branch workspaces and update them from Git." |
| Link each branch workspace to its base workspace | 🟢 Create Workspace Relation API (Preview) | "Create a workspace relation so wk-dev-a and wk-dev-b are branches of wk-dev." |
| Prove each workspace has its own branch | 🟢 Get Connection API | "Show the connected branch for wk-dev, wk-dev-a and wk-dev-b side by side." |
| One-click **Branch out** with selective items | 🔴 | Portal: Source control > Branch out |

The portal Branch out does the branch, the workspace, the connection and the sync in one action. The
CLI route is the same work split into explicit steps, which is easier to teach and to repeat.

Notes:

- A workspace connects to one branch, so two branches need two workspaces.
- Workspace relations are a Preview API. They let the **Related Branches** tab list the workspaces.
- When you branch out into an **existing** workspace, items not saved to Git can be deleted.

---

## UC4 — Develop in isolation

| Task | Route | Sample prompt |
| --- | --- | --- |
| Dev A edits the notebook in the UI | 🔴 | Portal: edit `nb_workshop` in `wk-dev-a` |
| Dev B edits a different item (the report or the lakehouse) in the UI | 🔴 | Portal: edit it in `wk-dev-b` |
| Edit an item's definition as text instead | 🟢 | "In branch feature/dev-b, change the title text in the notebook file, commit it, then update wk-dev-b from Git." |
| See what changed in the workspace | 🟢 Get Status API | "Show Git status for wk-dev-a." |
| Commit Dev A's work | 🟢 Commit To Git API | "Commit wk-dev-a to Git with the comment 'dev A: notebook change'." |
| Commit Dev B's work | 🟢 Commit To Git API | "Commit wk-dev-b to Git with the comment 'dev B: change'." |
| Confirm the commits are on the branches | 🟢 `gh api` | "Show the latest commit on feature/dev-a and feature/dev-b." |

Notes:

- Only changes **saved** into the workspace appear as Uncommitted. A draft that isn't saved does not.
- One Fabric item can be stored as several files, so one changed item may show several changed files
  in the repo.

---

## UC5 — Merge the two branches (pull requests)

Merging happens in GitHub, not in Fabric.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Open a pull request from `feature/dev-a` into `main` | 🟢 `gh pr create` | "Open a PR from feature/dev-a into main titled 'dev A changes'." |
| Open a pull request from `feature/dev-b` into `main` | 🟢 `gh pr create` | "Open a PR from feature/dev-b into main titled 'dev B changes'." |
| Review the files changed | 🟢 `gh pr diff` | "Show the diff of both PRs and summarize what changed in each." |
| Merge the first PR | 🟢 `gh pr merge` | "Merge the dev A PR into main. Wait for my yes first." |
| Merge the second PR | 🟢 `gh pr merge` | "Merge the dev B PR into main." |
| Create a conflict on purpose (both devs edit the same item) | 🟡 | "Make feature/dev-a and feature/dev-b both change the same line in nb_workshop, then open both PRs." |
| Resolve the conflict | 🟡 `git` plus chat | "Check out feature/dev-b, merge main, show me the conflict, propose a resolution, and wait for my yes before committing." |
| Bring the merged result into `wk-dev` | 🟢 Update From Git API | "Update wk-dev from Git and show which items changed." |

```text
feature/dev-a ──PR──┐
                    ├──▶ main ──Update──▶ wk-dev
feature/dev-b ──PR──┘
```

Notes:

- The first merge is clean. The second one conflicts only if both changed the same file.
- A conflict is resolved in Git, then the workspace is updated.
- **Commit** sends workspace changes to a branch. **Update** brings branch changes into a workspace.

---

## UC6 — Check pull requests automatically (CI)

Run checks on every pull request so a bad change is caught **before** it reaches `main`.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Write a validation workflow that runs on every PR | 🟢 GitHub Actions | "Create a GitHub Actions workflow that runs on pull requests to main and checks the Fabric item folders. Show the file before committing it." |
| What the checks do | 🟢 | "Make the checks verify that every .platform file is valid JSON, each item folder has its definition files, item names follow the pattern `nb_*`, `sm_*`, `rpt_*`, `lh_*`, and no token or secret text is committed." |
| See the check result on a PR | 🟢 `gh pr checks` | "Show the check results for the dev A PR." |
| Block a bad PR on purpose | 🟢 | "In feature/dev-b, break one .platform file, open a PR, and show me the failing check." |
| Make the check required before merge | 🟡 `gh api` branch protection | "Make the validation check required on main and require one approving review. Show the request first. Tell me if my plan doesn't allow it." |
| Fallback if your plan doesn't allow branch protection | 🟢 | "Run the same checks locally on the PR branch and refuse to merge unless they all pass." |
| Optional: deploy the PR branch to a temporary workspace and smoke-test it | 🟡 | "Create a temporary workspace for the dev A branch, publish the items with fabric-cicd, run nb_workshop, check sales_wk has 3 rows, then delete the workspace. Wait for my yes before each step." |

Notes:

- A check only protects `main` when it is **required**. Without branch protection it is advice.
- Keep secrets out of the workflow file. Use GitHub Actions secrets or federated sign-in (UC12).
- The temporary-workspace test costs capacity time and needs the service principal from UC12.
- The same workflow can later deploy after merge (UC13).

---

## UC7 — Partial (selective) deployment

Release only part of the Development stage to Test.

| Task | Route | Sample prompt |
| --- | --- | --- |
| List the Development items and their IDs | 🟢 List Stage Items API | "List the items in the Development stage of wk-pipeline with item IDs and types." |
| List the Test items and show which exist in only one stage | 🟢 | "Compare Development and Test and list items missing from Test." |
| Pick the subset and its dependencies (for example the report and its semantic model) | 🟡 | "I want to deploy rpt_workshop. Tell me which other items it depends on so I deploy them together." |
| Show the request before running | 🟢 | "Show me the Deploy Stage Content request body for deploying only rpt_workshop and sm_workshop, with the note 'partial release'. Don't run it." |
| Deploy the chosen items | 🟢 Deploy Stage Content API (`items` list) | "Deploy only rpt_workshop and sm_workshop from Development to Test with the note 'partial release'. Wait for my yes." |
| Wait for it to finish | 🟢 long-running operation | "Poll the deployment until it finishes and show the result." |
| Confirm only those items changed | 🟢 List Stage Items API | "Show last deployment time for each Test item and confirm only the two chosen items changed." |
| Review deployment history | 🟢 List Deployment Pipeline Operations API | "Show the last 5 deployments of wk-pipeline." |
| Refresh the Test semantic model | 🟢 `fab` / refresh API | "Refresh the semantic model in wk-test." |
| Check the two permission gates | 🟢 read-only | "Check that I am pipeline Admin and Contributor or higher in both wk-dev and wk-test." |
| Click **Select related** in the portal | 🔴 | Portal: Test stage > select an item > Select related |

Notes:

- In the API, omit the `items` list and **everything** deploys. Include it and only those items deploy.
- Maximum 300 items per request.
- Selecting a report alone does not add its semantic model. List the dependencies yourself, or use
  Select related in the portal.
- Deploying overwrites the target copy of each selected item and keeps its ID, URL and permissions.
- Data isn't copied between stages, so refresh the semantic model after deployment.
- An optional deployment plan can add pre- and post-deployment actions (see UC9).

---

## UC8 — Per-stage configuration (Variable library, rules, parameters)

Promoted content must use each stage's own settings, or Test and Production keep pointing at
Development data.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Show the variable library and its value sets | 🟢 Variable Library API | "Show vl_workshop in wk-dev: its variables, value sets and which set is active." |
| Make the notebook read `env_label` and write it into a column of `sales_wk` | 🟡 | "Update nb_workshop to read env_label from vl_workshop and store it in a new column env of sales_wk. Check the current Learn page for the notebook variable-library syntax first and show me the change." |
| Commit the library and the notebook to Git | 🟢 Commit To Git API | "Commit vl_workshop and nb_workshop in wk-dev to Git with the comment 'per-stage config'." |
| Deploy the library and notebook to Test | 🟢 Deploy Stage Content API | "Deploy only vl_workshop and nb_workshop from Development to Test with the note 'config demo'. Wait for my yes." |
| Set the **active** value set in Test to `test` | 🟡 Variable Library API, or 🔴 portal | "Set the active value set of vl_workshop in wk-test to test, then show it." |
| Run the notebook in Test and confirm `env` says `test` | 🟢 `fab job run` | "Run nb_workshop in wk-test and show the env column of sales_wk." |
| See what counts as a difference between stages | 🟢 List Stage Items API | "Edit a variable value in wk-dev and compare Development and Test, then change only the active value set in Test and compare again. Tell me which one shows as different." |
| Compare with a deployment rule | 🔴 | Portal: Test stage > Deployment rules, for a data source or parameter |
| Code-first parameterization with `fabric-cicd` | 🟢 | "Show me how fabric-cicd replaces a lakehouse or connection value per environment, using its parameter file." |

Notes:

- All value sets are deployed to every stage, but **one** set is active per stage.
- A deployment doesn't change the active value set. A workspace created by deployment starts with
  **Default** active, so set the right one yourself.
- Adding, deleting or editing variables or value sets shows the library as different between stages.
  Switching the active set alone doesn't.
- A deployment rule can't be created in the first stage, needs you to own the item, and is lost if the
  workspace is unassigned from the stage.
- Use separate data for each stage, so Development and Test work never loads Production.

---

## UC9 — Control order and actions with a deployment plan (Preview)

A deployment plan adds an explicit item order and runs actions before or after an item deploys.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Explain what the plan will do | 🟢 | "Explain the deployment plan I'd need: deploy sm_workshop before rpt_workshop, then run nb_workshop after it deploys in the target stage." |
| Create the plan item in `wk-dev` | 🟡 Preview | "Create a deployment plan in wk-dev with two deployment groups: sm_workshop, then rpt_workshop with a post-deploy action that runs nb_workshop. Check the current Learn page for the creation route first and show me the plan." |
| Commit the plan to Git | 🟢 Commit To Git API | "Commit the deployment plan in wk-dev to Git." |
| Show the request with the plan attached | 🟢 | "Show me the Deploy Stage Content request that attaches the plan. Don't run it." |
| Deploy with the plan attached | 🟢 Deploy Stage Content API | "Deploy sm_workshop, rpt_workshop and the plan's items from Development to Test with the plan attached. Wait for my yes." |
| Check the order and that the action ran | 🟢 Get Deployment Pipeline Operation API | "Show the execution plan of the last deployment and whether the post-deploy action succeeded." |
| Make the action fail on purpose | 🟢 | "Change the action to run a notebook that doesn't exist, deploy again, and show me how the failure is reported." |
| Attach a plan to an Update From Git | 🟢 Update From Git API | "Show how the same plan is attached to an Update From Git request." |

Notes:

- The preview REST call needs `beta=true` on the URL and a `deploymentPlan` object inside `options`.
  The token also needs the `Item.Execute.All` scope in addition to the deploy scope.
- A plan doesn't choose the items. Select them yourself, and make sure the items the plan's actions
  need already exist in the target.
- A plan can add order that lineage doesn't show, but it can't remove dependencies Fabric detects.
- A plan doesn't deploy workspace-level settings such as connections or gateways.
- Use a plan only when the standard order isn't enough or you need actions around a deploy.

---

## UC10 — Promote to Production with an approval gate

| Task | Route | Sample prompt |
| --- | --- | --- |
| Check Test is healthy before promoting | 🟢 | "Show the last deployment to wk-test and whether it succeeded, and run nb_workshop in wk-test and confirm sales_wk has 3 rows." |
| Compare Test with Production | 🟢 List Stage Items API | "Compare the Test and Production stages and list what would change." |
| Restrict who can deploy to Production | 🟢 `fab acl` | "Show who has Contributor or higher on wk-prod, and make sure only the release manager and the service principal do." |
| Choose the approval gate | 🟢 | "Explain the approval options for my GitHub plan, and tell me which one I can use." |
| Create a GitHub environment `production` with required reviewers | 🟡 `gh api`, plan-dependent | "Create a GitHub environment named production that requires my approval. Tell me if my plan or repo visibility doesn't allow it." |
| Fallback approval in chat | 🟢 | "Show me exactly what will be deployed to production and wait for me to type 'approve production' before running it." |
| Deploy Test to Production | 🟢 Deploy Stage Content API | "Deploy only sm_workshop, rpt_workshop, vl_workshop and nb_workshop from Test to Production with the note 'release 1'. Wait for my approval." |
| Set the Production active value set to `prod` | 🟡 Variable Library API, or 🔴 portal | "Set the active value set of vl_workshop in wk-prod to prod, then show it." |
| Smoke-test Production | 🟢 `fab job run` | "Run nb_workshop in wk-prod and confirm env says prod and sales_wk has 3 rows." |
| Review deployment history | 🟢 List Operations API | "Show the last 5 deployments of wk-pipeline and who ran them." |

```text
merge to main ──▶ deploy to Test (automatic) ──▶ smoke test ──▶ approval ──▶ deploy to Production ──▶ smoke test
```

Notes:

- I found no built-in approval step in deployment pipelines. The approval comes from the tool that
  calls the API, such as a GitHub environment with required reviewers, or Azure DevOps approvals.
- Deploying into a stage needs Contributor or higher in **both** workspaces, so workspace roles are the
  way to keep most developers off Production.
- A reviewer gate on a **private** GitHub repository needs a paid plan. On Free, make the repository
  public (and keep every secret out of it) or use the in-chat approval.
- Data isn't copied between stages, so refresh models and run the notebook in Production after
  deploying.

---

## UC11 — Roll back a bad release

I found no one-click rollback in deployment pipelines. Recovery means putting the last good version
back and deploying it again.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Create a bad change on purpose and deploy it to Test | 🟢 | "Change nb_workshop in main so it writes 99 rows to sales_wk, update wk-dev, then deploy the notebook to Test. Wait for my yes." |
| Detect the problem | 🟢 | "Run nb_workshop in wk-test and check sales_wk has 3 rows. Tell me if it fails." |
| Back up the Test items before fixing | 🟢 `fab export` | "Export the items in wk-test to a local folder first." |
| Find the bad merge | 🟢 `gh` | "Show the last merged PRs on main and which one changed nb_workshop." |
| Undo it with a new commit (revert) | 🟢 `git revert` plus `gh pr` | "Revert the bad PR with a new revert PR into main. Show me the diff and wait for my yes before merging." |
| Bring the fix into Development | 🟢 Update From Git API | "Update wk-dev from Git and confirm nb_workshop is back to the good version." |
| Redeploy only the fixed item | 🟢 Deploy Stage Content API | "Deploy only nb_workshop from Development to Test with the note 'rollback'. Wait for my yes." |
| Verify the recovery | 🟢 | "Compare Development and Test, run nb_workshop in wk-test, and confirm sales_wk has 3 rows again." |
| Restore items from the export if Git isn't enough | 🟡 `fab import` | "Show the command to import the exported nb_workshop back into wk-test and wait for my yes." |
| Recover a deleted item | 🔴 | Portal: workspace Recycle bin |

Notes:

- Prefer a **revert commit** over rewriting Git history, so the workspace can simply update forward.
- Redeploying overwrites the target item with the Development version and keeps its ID, URL and
  permissions.
- Deployment history keeps the most recent deployments, which helps you see what went out and when.
- Deployments don't copy data. A notebook that already wrote bad rows needs a separate data fix, for
  example Delta table history and restore. Verify the syntax for your runtime first.
- Take an export before risky releases. It is the backup when the repository doesn't hold the item.

---

## UC12 — Automate with a service principal (identity and secrets)

Pipelines and scheduled jobs shouldn't run as a person.

| Task | Route | Sample prompt |
| --- | --- | --- |
| Check the Fabric tenant setting for service principals | 🔴 | Fabric admin portal: Tenant settings > Service principals can use Fabric APIs, optionally for one security group |
| Create the app registration and service principal `sp-fabric-cicd` | 🟡 `az ad` | "Create an app registration and service principal named sp-fabric-cicd. Show the commands first and tell me which Entra permission I need." |
| Create a security group and add the service principal | 🟢 `az ad` | "Create a security group fabric-cicd-sp and add sp-fabric-cicd to it." |
| Choose how it signs in | 🟢 | "Explain federated credentials for GitHub Actions compared with a client secret, and recommend one for this workshop." |
| Create the credential | 🟡 `az ad` | "Set up a federated credential for my repo's main branch. If I must use a secret, create it and write it only to GitHub Actions secrets without printing it." |
| Store the secret safely | 🟢 `gh secret set` | "Add the secret to GitHub Actions secrets by prompting me in the terminal. Do not echo it." |
| Give it workspace roles | 🟢 `fab acl set` | "Give sp-fabric-cicd Contributor on wk-dev, wk-test and wk-prod." |
| Give it pipeline access | 🟢 pipeline role-assignment API | "Add sp-fabric-cicd as Admin on wk-pipeline." |
| Prove it works with its own identity | 🟢 | "Sign in as sp-fabric-cicd and list the workspaces and pipeline stages it can see." |
| Prove least privilege | 🟢 | "Using sp-fabric-cicd, try to read wk-dev-a. It should be denied." |
| Check which items support service principals | 🟢 | "For each item type in my pipeline, check whether service principals are supported for Git and deployment operations." |
| Rotate or revoke the credential | 🟢 `az ad` | "Rotate the secret for sp-fabric-cicd, update the GitHub secret, and delete the old one." |

Notes:

- A service principal works with the Fabric APIs only when the tenant setting is on for it.
- The deploy API supports a service principal only when **all** the items in the operation support one.
- For Git, a service principal is supported only with a configured connection. The Connect API is
  blocked for the GitHub provider when automatic credentials are used.
- Prefer federated (passwordless) credentials. Never put a secret in the repository, a workflow file,
  or chat.
- Give the service principal the smallest role it needs on each workspace.

---

## UC13 — Automate the release end to end

| Task | Route | Sample prompt |
| --- | --- | --- |
| Run the partial deployment from a script | 🟢 REST through `fab api` | "Write a script that deploys a list of item names from Development to Test and polls until done. Show it before running." |
| Deploy to Test from a GitHub Action when a PR merges to `main` | 🟢 | "Create a GitHub Actions workflow that signs in as sp-fabric-cicd and deploys to Test when a PR is merged to main. Show it before committing." |
| Deploy to Production from the same workflow after approval | 🟡 | "Add a second job that deploys to Production and uses the production environment so it waits for approval." |
| Deploy from files with a config and environment | 🟢 `fab deploy --config … --target_env` | "Create a deploy config with a dev and a test environment and run it for test." |
| Deploy with the `fabric-cicd` library | 🟢 | "Use fabric-cicd to publish the items in the repo to wk-test." |
| Deploy to a stage that has no workspace yet | 🟡 | "Deploy to a new stage and create the workspace as part of it." |
| Deploy backward (Test to Development) | 🔴 | Portal, and only into an empty stage |

Notes:

- Each stage gets its own source of truth in different release models: per-stage branches, one shared
  release commit, or deployment pipelines. This workshop uses deployment pipelines.
- Run the PR checks from UC6 first, then deploy only after the merge.

---

## UC14 — Cleanup and cost control

| Task | Route | Sample prompt |
| --- | --- | --- |
| Delete the feature branches | 🟢 `gh api` | "Delete branches feature/dev-a and feature/dev-b in fabric-cicd-workshop after confirming the PRs are merged." |
| Disconnect the workspaces from Git | 🟢 Disconnect API | "Disconnect wk-dev-a and wk-dev-b from Git." |
| Delete the branch workspaces | 🟢 `fab rm` | "Delete workspaces wk-dev-a and wk-dev-b. List their items first and wait for my yes." |
| Delete the pipeline and the other workspaces | 🟢 Delete Pipeline API, `fab rm` | "Delete wk-pipeline, wk-prod, wk-test and wk-dev. List what's inside first and wait for my yes." |
| Delete the GitHub environment and Actions secrets | 🟢 `gh api`, `gh secret` | "Delete the production environment and the Actions secrets from fabric-cicd-workshop." |
| Delete the service principal, app registration and group | 🟢 `az ad` | "Delete sp-fabric-cicd, its app registration and the fabric-cicd-sp group. Wait for my yes." |
| Delete the repository (optional) | 🟢 `gh repo delete` | "Delete the repo fabric-cicd-workshop. Wait for my yes." |
| Pause the capacity | 🟢 `az` | "Pause capacity `<capacity>` and confirm its state is Paused." |
| Revoke the GitHub token | 🔴 | GitHub: Settings > Developer settings > Personal access tokens |
| Remove the account entry from Fabric | 🔴 | Fabric: Source control > Accounts tab |

> A running capacity bills hourly. Pause it at the end, even if you plan to come back.

---

## Suggested session plan

| Session | Use cases | Time |
| --- | --- | --- |
| 1 | UC0 setup and readiness check | 45 min |
| 2 | UC1, UC2 pipeline and source control | 60 min |
| 3 | UC3, UC4 branch out and isolated edits | 60 min |
| 4 | UC5, UC6 pull requests, a conflict, and automatic checks | 60 min |
| 5 | UC7, UC8 partial deployment and per-stage configuration | 75 min |
| 6 | UC9, UC10 deployment plan, then Production with approval | 60 min |
| 7 | UC11 rollback | 45 min |
| 8 | UC12, UC13 service principal and end-to-end automation | 75 min |
| 9 | UC14 cleanup | 15 min |

---

## Chat versus portal at a glance

| Area | Mostly chat | Needs the portal or GitHub site |
| --- | --- | --- |
| Pipeline | Create, assign stages, roles, list, deploy, history | Deployment rules, Select related, backward deployment |
| Source control | Connect, initialize, status, commit, update | Creating the token, adding the account in Fabric |
| Branching | Create branches and workspaces, connect, relate | One-click Branch out, selective items, branch admin profile (Preview) |
| Development | Text edits of item definitions | Editing items in the UI |
| Merging | Everything through `gh` and `git` | None |
| PR checks | Workflow, results, branch protection (plan permitting) | None |
| Per-stage configuration | Variable library create, deploy, run | Deployment rules, possibly setting the active value set |
| Deployment plan (Preview) | Attach to a deploy, inspect the result | Possibly creating the plan item |
| Production approval | Compare, deploy, smoke test, GitHub environment (plan permitting) | None, but approvals need a paid plan or a public repo |
| Rollback | Revert PR, update, redeploy, export and import | Recycle bin |
| Automation identity | App registration, group, roles, secrets | Tenant setting for service principals |
| Cleanup | Everything except the token | Token revocation |

## REST operations used

These are the Fabric operations behind the tasks above. See the REST reference for each request body.

| Area | Operation |
| --- | --- |
| Git | Connect, Initialize Connection, Get Status, Commit To Git, Update From Git, Get Connection, Disconnect, Get and Update My Git Credentials, Create and List Workspace Relations |
| Pipelines | Create, Get, List, Delete Deployment Pipeline; Assign and Unassign Workspace To Stage; List Stages; List Stage Items; Deploy Stage Content (optionally with a `deploymentPlan`); Get and List Deployment Pipeline Operations; pipeline role assignments |
| Variable library | Create, get and update the library and its definition (verify the exact operations in the Variable Library REST reference) |

Call them with `fab api`, for example `fab api -X get workspaces`, or with `az` and Python for
tokens.

## What has and hasn't been tested

**Run against a real tenant (read-only or minimal change):**

- Sign-in checks for `az`, `fab` and `gh`.
- Listing workspaces, deployment pipelines, stages and stage items.
- Reading a workspace's Git connection and Git status.
- Resuming a paused capacity with `az`.
- Reading `fab` help for `mkdir`, `assign`, `acl`, `job`, `rm`, `import`, `export`, `api` and `deploy`.

**Taken from the documentation only — verify the first time:**

- Connect, Initialize Connection, Commit To Git, Update From Git request bodies.
- Create Workspace Relation (Preview).
- Deploy Stage Content with an `items` list.
- Creating a notebook with `fab import`, and `fab acl set` for a user.
- Exact portal labels for the connection and Accounts screens.
- Everything in UC6, UC8, UC9, UC10, UC11 and UC12: the Variable Library operations, setting the active
  value set, creating a deployment plan item, attaching a plan with `beta=true`, GitHub environments
  and branch protection (which depend on your GitHub plan), the revert flow, and service principal setup.
- The notebook syntax for reading a variable library value. Check the current Learn page.
- Whether a Production stage can be deployed to from Test with the items you choose, because stage
  assignment and permissions differ per tenant.

## Learn links

- [Get started with Git integration](https://learn.microsoft.com/fabric/cicd/git-integration/git-get-started)
- [Automate Git integration](https://learn.microsoft.com/fabric/cicd/git-integration/git-automation)
- [Develop using branched workspaces](https://learn.microsoft.com/fabric/cicd/git-integration/branched-workspace)
- [Development process in Microsoft Fabric](https://learn.microsoft.com/fabric/cicd/git-integration/manage-branches)
- [Deploy content with deployment pipelines](https://learn.microsoft.com/fabric/cicd/deployment-pipelines/deploy-content)
- [Automate deployment pipelines with the Fabric APIs](https://learn.microsoft.com/fabric/cicd/deployment-pipelines/pipeline-automation-fabric)
- [Choose a deployment option](https://learn.microsoft.com/fabric/cicd/manage-deployment)
- [Fabric CI/CD overview](https://learn.microsoft.com/fabric/cicd/cicd-overview)
- [Best practices for lifecycle management](https://learn.microsoft.com/fabric/cicd/best-practices-cicd)
- [Variable library overview](https://learn.microsoft.com/fabric/cicd/variable-library/variable-library-overview)
- [Variable libraries in CI/CD](https://learn.microsoft.com/fabric/cicd/variable-library/variable-library-cicd)
- [Deployment plan overview (Preview)](https://learn.microsoft.com/fabric/cicd/deployment-plan/deployment-plan-overview)
- [Automate deployments with a deployment plan (Preview)](https://learn.microsoft.com/fabric/cicd/deployment-plan/deployment-plan-automation)
- [Deployment rules](https://learn.microsoft.com/fabric/cicd/deployment-pipelines/create-rules)
- [Fabric identity support for the REST API](https://learn.microsoft.com/rest/api/fabric/articles/identity-support)
- [fabric-cicd documentation](https://microsoft.github.io/fabric-cicd/latest/)
- [GitHub environments for deployment](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment)
- [Git REST API](https://learn.microsoft.com/rest/api/fabric/core/git)
- [Deployment pipelines REST API](https://learn.microsoft.com/rest/api/fabric/core/deployment-pipelines)

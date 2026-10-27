# GH2 - Set up the sales project

**Time:** 20 minutes; install tools and sign in before the session if possible.
**Starting point:** Python 3.10+, Git, VS Code and GitHub CLI installed.
The [main guide](../workshop-part1-github-copilot.md#21-tools-to-install)
has installation commands.

## 1. Copy the starter

Create a new folder called `copilot-workshop-demo` **outside the workshop materials**.
Copy everything inside [starter](./starter/), including the hidden `.gitignore`,
into it. Use your file manager or VS Code Explorer. Do not copy the enclosing
`starter` folder, lab instructions or presenter solutions.

Open the new folder in VS Code and open its terminal. You should see
`summarize.py`, `README.md`, `data`, `tests`, `pytest.ini` and `requirements-dev.txt`.

## 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

If PowerShell blocks activation, do not change organization execution policy.
Use `.\.venv\Scripts\python.exe` instead of `python` in every command, including
`.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`.
Tell Copilot to use that interpreter too.

**macOS / WSL2 / Ubuntu:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

On Ubuntu, if venv support is missing, install `python3-venv` using your normal
approved installation process. In WSL, keep the project and tools inside WSL.

In VS Code run **Python: Select Interpreter** and choose this project's `.venv`.
Reactivate it whenever you open a new terminal.

## 3. Run the baseline

```text
python summarize.py data/sales.csv
python -m pytest -q
```

Expected starter output:

```text
East: 150.00
North: 75.00
West: 250.00
Average per region: 118.75
```

Expect **2 passed**. These are baseline checks, not proof that every business rule
is implemented. Leave improvements for the following labs.

## 4. Save and publish the baseline

```text
git init -b main
git add .
git commit -m "Add sales workshop starter"
gh auth status
gh repo create copilot-workshop-demo --private --source=. --remote=origin --push
```

This creates a private repository under your authenticated account. If you need
an organization, use `OWNER/copilot-workshop-demo` instead. If the name already
exists, choose a new demo name; do not overwrite or delete an existing repo.
Only publish after checking that the staged files contain the starter, not `.venv`
or personal files.

If Git needs your author identity, configure your own approved name/email locally.
Never paste tokens into chat. For Copilot-assisted commits, retain the
`Co-authored-by` trailer required by your team.

**Done when:** the script runs, two tests pass, `git status` is clean and your
private repository is on GitHub.

**If blocked:** local labs GH3-GH6 can run without publishing. Resolve GitHub access
before GH7, or use the presenter's demo.
Next: [GH3 editor](./03-editor.md).

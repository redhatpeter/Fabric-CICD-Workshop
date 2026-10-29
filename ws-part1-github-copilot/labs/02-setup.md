# GH2 - Set up the sales project

**Time:** 20 minutes; install tools and sign in before the session if possible.
**Starting point:** Python 3.10+, Git, VS Code and GitHub CLI installed.
The [main guide](../workshop-part1-github-copilot.md#21-tools-to-install)
has installation commands.

## 1. Copy the starter

Create a new folder called `copilot-workshop-demo` **outside the workshop materials**.
Copy only these items from [starter](./starter/), including the hidden `.gitignore`:

```text
.gitignore
README.md
data/
tests/
pytest.ini
requirements-dev.txt
summarize.py
```

Use your file manager or VS Code Explorer. Do not copy the enclosing `starter`
folder, lab instructions, presenter solutions, `.git`, `.venv`, `__pycache__`
or `.pytest_cache`. A presenter's working copy may contain those local folders;
copying `.git` would also copy its history and remotes.

Open the new folder in VS Code and open its terminal. You should see
`summarize.py`, `README.md`, `data`, `tests`, `pytest.ini` and `requirements-dev.txt`.
Use **File > Open Folder** (or a new window) so this is the only project root.
Keep the lab instructions in a browser or separate window. Trust only your own
reviewed demo folder if VS Code asks; Restricted Mode can disable agent features.

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
Verify the terminal interpreter before continuing:

```text
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Both paths should refer to the demo's `.venv`. Selecting the editor interpreter
does not necessarily change an already-open terminal. If `pytest` is missing,
install `requirements-dev.txt` with this same interpreter; do not install it
globally as a workaround.

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
git diff --cached --stat
git diff --cached
```

**Stop and inspect the staged files before committing or publishing.** They
should be only the items listed above. Then:

```text
git commit -m "Add sales workshop starter"
gh auth status
gh repo create copilot-workshop-demo --private --source=. --remote=origin --push
gh repo view --json nameWithOwner,visibility,url
git status
```

This creates a private repository under your authenticated account. If you need
an organization, use `OWNER/copilot-workshop-demo` instead. If the name already
exists, choose a new demo name; do not overwrite or delete an existing repo.
Only publish after checking that the staged files contain the starter, not `.venv`
or personal files.
The repository visibility must be `PRIVATE`. If Git reports an existing
repository or unexpected remote, stop and check `git rev-parse --show-toplevel`
and `git remote -v`; use a fresh folder instead of deleting existing Git metadata.
If `git init -b main` is unsupported, use `git init` followed by `git branch -M main`
only in this new demo repository.

If Git needs your author identity, configure your own approved name/email locally.
Never paste tokens into chat. For Copilot-assisted commits, retain the
`Co-authored-by` trailer required by your team.

**Done when:** the script runs, two tests pass, `git status` is clean and your
private repository is on GitHub.

**If blocked:** local labs GH3-GH6 can run without publishing. Resolve GitHub access
before GH7, or use the presenter's demo.
Next: [GH3 editor](./03-editor.md).

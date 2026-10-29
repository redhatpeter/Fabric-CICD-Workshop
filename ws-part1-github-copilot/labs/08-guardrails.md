# GH8 - Practice a safe approval

**Time:** 10 minutes. **Starting point:** GH7, or any working local project.
**Goal:** practice pausing a change without touching credentials or real data.

Start with `git status --short` and save any unrelated work before this exercise,
so you can tell whether the agent changed tracked files. Use a regular Agent,
not the tool-restricted reviewer: a reviewer cannot demonstrate denying a write
it never had permission to attempt.

1. In VS Code Explorer, create `output/approval-demo.txt` in the demo repository.
   Put `KEEP THIS PRACTICE TEXT` in it and save. This is disposable, ignored data.
2. In a new regular Agent chat, paste these approval ground rules:

   **Ground rules:** Use read-only checks first. Before overwriting or deleting
   anything, show the exact path and proposed change, then wait for my explicit
   approval. Never inspect credentials. Work only on this disposable demo file.

   Then ask:

   **Prompt:** Inspect only output/approval-demo.txt. Propose replacing its content with
   "Replacement report". Show the exact path and proposed content, then
   stop and wait for approval. Do not write anything yet.

3. When asked to approve, answer:

   **Reply:** No. Keep the existing file unchanged.

4. Open the file yourself. Its content should still be `KEEP THIS PRACTICE TEXT`.
   If a tool approval dialog appears before you can reply, deny it as well.
5. Inspect `git status` and `git diff`. No tracked files should have changed.

The starter ignores `output/`, so a clean `git diff` alone cannot prove this
exercise passed. Inspect the saved file content directly after denial; do not
rely on the assistant saying it kept the file. If the agent cannot read ignored
files, explicitly attach only this practice file or demonstrate the pause with
the presenter; do not enable broad access to ignored folders.

If the assistant writes before approval, record that as a failed exercise,
stop the action and manually restore only this disposable file's practice text.
Do not treat another instruction as a guarantee of enforcement.

**Discussion:** instructions guide behavior; tool permissions and approval
settings constrain it. Never test secret handling by asking for a real token.

**Done when:** you have inspected the scope, denied the write and verified the file.
**Cleanup:** remove only the disposable practice file using Explorer if desired.
Next: [GH9 capstone](./09-capstone.md).

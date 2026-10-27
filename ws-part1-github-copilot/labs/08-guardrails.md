# GH8 - Practice a safe approval

**Time:** 10 minutes. **Starting point:** GH7, or any working local project.
**Goal:** practice pausing a change without touching credentials or real data.

1. In VS Code Explorer, create `output/approval-demo.txt` in the demo repository.
   Put `KEEP THIS PRACTICE TEXT` in it and save. This is disposable, ignored data.
2. In a new regular Agent chat, paste the approval ground rules, then ask:

   **Prompt:** Inspect only output/approval-demo.txt. Propose replacing its content with
   "Replacement report". Show the exact path and proposed content, then
   stop and wait for approval. Do not write anything yet.

3. When asked to approve, answer:

   **Reply:** No. Keep the existing file unchanged.

4. Open the file yourself. Its content should still be `KEEP THIS PRACTICE TEXT`.
5. Inspect `git status` and `git diff`. No tracked files should have changed.

If the assistant writes before approval, record that as a failed exercise,
stop the action and manually restore only this disposable file's practice text.
Do not treat another instruction as a guarantee of enforcement.

**Discussion:** instructions guide behavior; tool permissions and approval
settings constrain it. Never test secret handling by asking for a real token.

**Done when:** you have inspected the scope, denied the write and verified the file.
**Cleanup:** remove only the disposable practice file using Explorer if desired.
Next: [GH9 capstone](./09-capstone.md).

# GH0 - Compare Copilot surfaces

**Time:** 5 minutes within the orientation. **Starting point:** the presenter
opens the [starter script](./starter/summarize.py); attendees can observe before setup.

Use an ordinary code editor tab, not a rendered Markdown preview. Before GH3 the
loader is called `load`; after the rename it is `load_rows`. If you already did
setup, use the script in your demo folder rather than editing the materials.

1. Select `load` in the editor and use inline chat:

   **Prompt:** Explain this function in two sentences. Do not edit anything.

2. Ask the Chat view, with the script attached:

   **Prompt:** Explain how this program reads a CSV and prints a report. Do not edit anything.

3. If available, ask the CLI or github.com Chat the same question with the same file context.
4. Compare: did the answer use the selected function, the file, or the whole repository?

To attach context in VS Code Chat, use **Add Context** (the paperclip or `+`)
and select the file, or drag its Explorer entry into Chat. Confirm the file
appears as an attachment before sending. Inline chat can be opened from the
selection's context menu. UI names and shortcuts vary by version.

**Expected explanation:** the loader opens a UTF-8 CSV, accepts an optional byte
order mark, and returns a list of dictionaries using the header as keys. It does
not yet validate the business rules. If a surface cannot access the local file,
paste this synthetic function explicitly; do not assume github.com or a CLI in
another folder can see the editor selection.

**Done when:** you can name a surface for a focused code edit and a surface for
a multi-file task. No code changes are required.

**If blocked:** watch the presenter; CLI and github.com can wait until GH6/GH7.
Next: [GH1 access](./01-access.md).

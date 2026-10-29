# GH1 - Access check

**Do before the workshop when possible.** No Python task is needed here.

- [ ] Sign in to VS Code with the GitHub account that has your Copilot access.
- [ ] Confirm that Chat responds in VS Code.
- [ ] Confirm that you can create a private demo repository.
- [ ] Ask the organizer whether cloud agent, Copilot code review and Spaces are enabled.
- [ ] Use only synthetic data and the throwaway demo repository.

## Check the right account

Copilot uses a **GitHub account**, not your Microsoft Fabric or Azure account.
The Fabric Studio, Fabric Data Engineering and Microsoft Fabric sidebars are
not required for any Part 1 lab. Do not change their sign-ins to fix Copilot.

1. In VS Code, open **Accounts** at the bottom-left and confirm the GitHub
   account used by Copilot has access. Open Chat and send "Reply with READY;
   do not use tools." A response verifies Chat access, not repository permissions.
2. In your terminal run `gh auth status`. Check the **active** GitHub account;
   it can differ from VS Code's account. If necessary use `gh auth login`, or
   `gh auth switch --hostname github.com --user YOUR_GITHUB_LOGIN` for an account
   already signed in. Never share the credential store or authentication tokens.
3. If GH6 is planned, run `copilot --version` and complete its own sign-in.
   Working `gh` authentication alone does not prove Copilot CLI access.
4. Confirm with the organizer that GitHub Actions can run on your private demo
   repository. GH7 and GH9 need a real test check, not only a review comment.

If GitHub authentication opens the wrong browser account, choose the intended
GitHub identity in that flow. Do not delete all saved accounts or weaken an
organization's access policy. In WSL, run terminal checks in WSL and install/sign
in to the editor extensions in the environment VS Code indicates.

**Done when:** local Chat works and you know whether you can do GH7 in the portal.
Do not spend the coding session trying to change organization policies.

**If blocked:** use the local labs and observe the presenter for policy-dependent features.
Next: [GH2 setup](./02-setup.md).

# Fabric CI/CD workshop boundaries

- Work only on the current lab and resources explicitly listed in the attendee's
  workshop-config.local.json. That file is a names reference, not a deployment config.
- Inspect the current branch, working tree and remote/workspace state first.
- Preview creates, commits, pushes, syncs, overwrites, deployments, permission
  changes and deletions. Wait for explicit approval of the exact scope.
- Never print tokens, read credential caches or put secrets in files, prompts or logs.
- Use only synthetic workshop data. Never attach a real/shared lakehouse.
- Preserve Fabric-generated item identities, metadata and binding fields.
- The import seed stays baseline. Modify only the Fabric-generated notebook
  and release.json for the tax feature.
- Use python checks/validate_items.py --require-items and
  python -m unittest discover -s tests -v before the release PR.
- Never remove --require-items, change expected totals or weaken tests to hide a failure.
- Do not allow simultaneous local and workspace writes to the same Git branch.
- Wait for asynchronous operations to finish; report errors and bounded timeouts.
  Do not resubmit jobs/deployments while one is already running.
- Inspect each target notebook's local default lakehouse before running. A
  deployment copies definitions, not table rows.
- Production is a disposable lab workspace. Require "approve production"
  before promotion and a separate approval before running its overwrite notebook.
- Chat approval is not an enforced platform security gate.
- Do not create a capacity, service principal, secret, automated release workflow,
  preview deployment plan or cleanup script as part of these core labs.

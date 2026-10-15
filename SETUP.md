# One-time setup and operating limits

## Before enabling the schedule

1. Create a GitHub repository named AgentForge under your account and push this project to its default `main` branch. No remote or authenticated GitHub CLI was available during local preparation.
2. Create a GitHub App installed **only** on this repository. Grant repository permissions: Contents read/write and Pull requests read/write. Save its App ID as Actions variable `AGENTFORGE_APP_ID` and private key as Actions secret `AGENTFORGE_APP_PRIVATE_KEY`. The daily workflow receives a short-lived installation token. Do not give it Actions, Administration, or Secrets permissions.
3. Create an OpenAI API key with a project spending cap. Save it as Actions secret `OPENAI_API_KEY`. Set Actions variable `DAILY_BUDGET_USD` (default `$0.06`). The runner stops before a call whose conservative worst-case token charge exceeds the remaining per-run budget. OpenAI account/project limits remain the real billing backstop.
4. Protect `main`: require the CI `checks` job, require branches to be up to date, disallow force pushes and bypasses, and enable auto-merge. Verify the App can create PRs and request auto-merge under those rules. This is essential: the daily job's local tests are not the required integration check.
5. Run `Daily bounded development` once manually and verify a PR, CI, and the separate verified integration workflow. Then uncomment the `schedule` block in `.github/workflows/daily.yml` and push. Schedule is approximately 8:15 AM Africa/Lagos; GitHub may delay or occasionally drop scheduled jobs.

## Expected use and cost

- One task per run; two model calls at most; no web research or hosted code tools. The model is `gpt-5.4-mini` by default. At published standard rates of $0.75 per million input tokens and $4.50 per million output tokens, the default runner cap is $0.06 per run, or at most about $5.40 over 90 successful daily runs in model charges if the cap and prices remain unchanged. Failed runs can also spend up to the cap. This estimate excludes Actions overage, storage, other infrastructure, and taxes.
- GitHub Actions has a 10-minute hard job timeout. The target is 5 minutes, but dependency installation, queue delay, tests, and PR processing may exceed that target. Private repository minutes can incur charges after plan allowance; public repository standard runners are generally free.
- PostgreSQL is local in Docker for development. Deployment hosting and production database are later roadmap work, with separate costs.

## Failure and contribution tracking

The runner writes a failure artifact after two bad coding attempts. GitHub's normal failed-workflow notifications should be enabled in your account. Failed work is saved for seven days as a workflow artifact; the next run retries the same task. An open day branch blocks later tasks until integration, so no day silently skips a failed PR.

`progress.json` records task completion in the PR and marks contribution status `unverified`. It does not infer a green square from workflow success. Commits identify `AgentForge Automation` and mark the change AI generated. Contributions by an automation/bot identity generally should not be expected to appear as contributions on your personal GitHub profile. Verify any profile credit against GitHub's actual contribution graph and eligibility rules; there is no 90-square guarantee.

## Safety boundary

The agent can write at most two files per run in `backend/app`, `backend/tests`, `frontend/app`, or `docs`, each at most 12,000 characters. It cannot edit workflow files, dependencies, Docker configuration, secrets, or `progress.json` directly. The runner updates progress after checks pass. Branch protection and CI determine whether GitHub integrates the PR. Review this policy if later roadmap tasks require infrastructure changes; those need a deliberate, separate change to the allowlist.

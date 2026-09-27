# cmva
Intentionally vulnerable app to demonstrate [CodeMender](https://cloud.google.com/security/codemender) capabilities, and integration with GitHub Actions via Workload Identity Federation.

## ⚙️ Setup

1. Fork this repository.
2. Enable the required APIs in your Google Cloud project:
    ```bash
     gcloud services enable \
       iam.googleapis.com \
       iamcredentials.googleapis.com \
       sts.googleapis.com \
       cloudresourcemanager.googleapis.com \
       serviceusage.googleapis.com \
       aiplatform.googleapis.com
    ```

3. Set up [Workload Identity Federation](https://github.com/google-github-actions/auth#workload-identity-federation-through-a-service-account) in your Google Cloud project, so the workflow authenticates without a service account key:
   - Create a Workload Identity Pool (e.g. `github-actions`).
   - Create an OIDC provider in the pool (e.g. `github-oidc`):
     - **Issuer URI:** `https://token.actions.githubusercontent.com`
     - **Audience:** default
     - **Attribute mappings:** `google.subject=assertion.sub`, `attribute.repository=assertion.repository`
     - **Attribute condition:** `assertion.repository_owner == 'GITHUB_USER'`
   - Create a service account (e.g. `cm-ci-sa`) with the **Agent Platform User** and **Service Usage Consumer** roles.
   - Bind the federated identity to the service account, and allow your fork to impersonate it:
      ```bash
     gcloud iam service-accounts add-iam-policy-binding SA_EMAIL \
       --role="roles/iam.workloadIdentityUser" \
       --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/attribute.repository/GITHUB_REPO"
      ```
      `GITHUB_REPO` is your fork's full name, e.g. `GITHUB_USER/cmva`.

4. Add three repository secrets (**Settings → Secrets and variables → Actions**):

| Secret             | Description                                   | Example                                                                                           |
|--------------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------|
| `GCP_PROJECT`      | Project ID with CodeMender allowlisted        | `my-project-id`                                                                                   |
| `GCP_WIF_PROVIDER` | Full WIF provider resource name               | `projects/123456789/locations/global/workloadIdentityPools/github-actions/providers/github-oidc`  |
| `GCP_SA_EMAIL`     | Service account email                         | `cm-ci-sa@my-project-id.iam.gserviceaccount.com`                                                  |

3. Allow GitHub Actions to open PRs (**Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**).                                                                                                                   
4. Run the `CodeMender CI/CD Guardrail` workflow (**Actions → CodeMender CI/CD Guardrail → Run workflow**).                                                                         
                                                                                                                                                                                       

## 🧠 Remarks
- Leave the `main` branch untouched. Create a disposable `demo` branch for each live demo, and run the workflow against it.
- Semgrep scans first, then CodeMender. Both reports appear on the run's **Summary** page and under **Security → Code scanning** (filter by `branch:demo`). Semgrep catches the pattern-based flaws; only CodeMender catches the semantic authorization flaws.
- Optionally, update the `finding_match` workflow input to select which finding to verify (default: `SQL Injection`).
- The first run finds vulnerabilities, verifies the selected one, fixes it, and opens a remediation PR, but fails the security gate. Once the PR is merged, the workflow re-runs, clears the security gate, and the alert closes in Code scanning.
- That's the whole thing — fork, set up WIF, add secrets, enable Actions, run the workflow.     

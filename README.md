# cmva
Intentionally vulnerable app to demonstrate [CodeMender](https://cloud.google.com/security/codemender) capabilities and integration with GitHub Actions.

## ⚙️ Setup

1. Fork this repository.
2. Add two repository secrets (**Settings → Secrets and variables → Actions**):

| Secret       | Description                                                |
|--------------|------------------------------------------------------------|
| `CM_PROJECT` | Google Cloud project ID with CodeMender allowlisted        |
| `GCP_SA_KEY` | Service account key (JSON) with Agent Platform User role   |

3. Enable GitHub Actions for the repository (**Settings → Actions → General → Allow GitHub Actions to create and approve pull requests**).                                                                                                                   
4. Run the `CodeMender CI/CD Guardrail` workflow (**Actions → CodeMender CI/CD Guardrail → Run workflow**).                                                                         
                                                                                                                                                                                       

## 🧠 Remarks
- Leave the `main` branch untouched. Create a disposable `demo` branch for each live demo, and run the workflow against it.
- Optionally, update the `finding_match` workflow input to select which finding to verify (default: `SQL Injection`).
- The first run finds vulnerabilities, verifies the selected one, fixes it, and opens a remediation PR, but fails the security gate. Once the PR is merged, the workflow re-runs, and clears the security gate.
- That's the whole thing — fork, add secrets, enable Actions, run the workflow.     

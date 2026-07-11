# Deployment for Forgente

Updates:

- `https://dl.gitea.com/gitea/version.json`
- `https://dl.gitea.com/gitea-runner/version.json`
- `https://dl.gitea.com/tea/version.json`

Each deployment target is updated by its own workflow, so pushing one `version.json` only uploads the matching target.

After each upload, the workflow downloads the published `version.json` from the corresponding `dl.gitea.com` path and verifies that it matches the local file.

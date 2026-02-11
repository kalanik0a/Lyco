# Step 12: Check For Secrets And Forbidden Content

Scan the repo and git changes for secrets or data that should not be committed.

Use the automated script:

```powershell
python tools/check_secrets.py
```

If findings exist and remediation is required, generate a post-CI report:

```powershell
python tools/post_ci_cd_report.py
```

Manual checks (spot-verify):
- Use `rg` to scan for API keys, tokens, and private keys.
- Check `git status` and `git diff` for accidental secrets.

If findings are legitimate secrets, remove them and rotate credentials.

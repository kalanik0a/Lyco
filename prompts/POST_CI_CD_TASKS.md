# Post CI/CD Tasks: Security Remediation Workflow

Use this prompt after CI/CD completes and there are security, secret, or SBOM findings.

## 1. Gather Evidence
- Collect outputs from:
  - `python tools/check_vulnerabilities.py`
  - `python tools/check_audit.py`
  - `python tools/security_checks.py`
  - `python tools/generate_sbom.py`
  - `python tools/check_secrets.py`
- Optional report generator:
  - `python tools/post_ci_cd_report.py`
- If CI logs are available, save a copy of findings for traceability.

## 2. Identify Findings
- Enumerate each issue and tag as:
  - **CVE/CWE/CPE** (if known)
  - **Secret exposure** (type + location)
  - **Weakness** (misconfig, unpinned deps, insecure patterns)
- For each item, record:
  - What component is affected
  - Why it is vulnerable/weak
  - Evidence from logs or SBOM

## 3. Threat Modeling Context
For each issue, evaluate exploitability across these scenarios:
- **Development (interpreted)**: running from source
- **Development (compiled)**: using Nuitka-built binary
- **Production (non-compiled)**: PyPI install, pure Python
- **Production (compiled)**: platform wheel with bundled binary

Note:
- Attack surface changes between interpreted vs. compiled builds.
- Some findings may be irrelevant in compiled mode but still matter in dev.

## 4. Remediation Plan
For each issue:
- State **why** remediation is needed.
- Describe **how** it will be fixed.
- Specify **where** the fix will land:
  - Code changes
  - Dependency pin/upgrade
  - CI configuration changes
  - Secret rotation/removal steps

## 5. Produce A Remediation Report
- Write a report file per run:
  - Directory: `build/vulns/`
  - Filename: `report-YYYY-MM-DD.md`
- You can generate a starter report with:
  - `python tools/post_ci_cd_report.py`
- Include:
  - Summary table of findings
  - Threat modeling analysis per finding
  - Remediation status and actions
  - Follow-up tasks if unresolved

## 5a. SBOM Deep Dive (Optional)
- Inspect SBOM components quickly:
  - `python tools/sbom_inspect.py`

## 6. Resolve CI/CD Test Failures
- Re-run failing checks after fixes.
- Record outcomes in the report.
- Update `TODO.md` for any remaining caveats.

## 7. User-Facing Summary
- Present a concise summary of:
  - What was found
  - What was fixed
  - What remains open
  - Why it matters

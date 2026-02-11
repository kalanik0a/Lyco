# Step 4: Check SBOM Vulnerabilities

Use `STATE.json` for the SBOM tool path. Generate the SBOM with:
- `python tools/generate_sbom.py`

Review the output in `sbom/`. If required, scan the SBOM with your preferred vulnerability scanner. Document any flagged components and propose remediations aligned with the platform support matrix in `CONTEXT.md`.

# CodeQL setup note (2026-09-20)

Advanced workflow `.github/workflows/codeql.yml` was **disabled** because it conflicted with GitHub Code Scanning **default setup**:

> CodeQL analyses from advanced configurations cannot be processed when the default setup is enabled

Default setup remains active. Re-enable advanced only after disabling default setup in Settings > Code security.
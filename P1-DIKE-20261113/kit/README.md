# P1 DIKE — executable CRLF/LF correction kit

**Kit status:** PREPARED · 5 local unit tests passed in the build environment.  
**Active node status:** NOT APPLIED. The active Windows source file was not accessible from this session.

## Defect and implementation

The inspected historical implementation hashes content_text encoded as UTF-8 and then writes the same text in text mode. On Windows, newline translation may cause the persisted file bytes to differ from the bytes hashed.

This kit applies a fail-closed patch to a local active source file:
1. Encode UTF-8 once into content_bytes and hash those bytes.
2. Write the file in binary mode (wb), flush and fsync.
3. Re-read the persisted file in binary mode (rb) and verify its SHA-256 before appending the index entry.
4. Record size_bytes from the same content_bytes buffer.
5. If the physical-byte verification fails, remove the failed corpus file and abort before index registration.
6. Create a backup and replace the source atomically; verify the resulting source file hash.

The patcher requires each expected source block exactly once. It refuses to patch on source drift, preserves a uniform LF/CRLF style, and is idempotent.

## Execution on the node containing the active source

Copy this folder to the node, then resolve the exact active dike_auditora.py path. Do NOT target the historical copy under _HISTORICO-MASTER.

PowerShell:

    cd tools\p1_dike_crlf_lf
    python -m unittest -v test_apply_p1_patch.py
    python .\apply_p1_patch.py "C:\ACTUAL\PATH\dike_auditora.py" --dry-run
    python .\apply_p1_patch.py "C:\ACTUAL\PATH\dike_auditora.py"

A successful write reports PATCH_APPLIED_VERIFIED and gives before/after SHA-256 values plus the backup path. If the expected code has changed, the dry-run refuses to proceed and the source remains untouched.

## Node-side acceptance evidence still required

- Exact active source path and SHA-256 before and after patch.
- Functional ingestion test with LF input and non-ASCII UTF-8 characters.
- Physical stored-byte proof: SHA-256 of bytes read from disk equals the corpus index sha256; byte length equals size_bytes.
- Same functional test executed on Windows and Linux.
- Re-issue the nine current corpus hashes, separating original-byte hashes and normalized-LF hashes. Preserve the historical evidence; do not overwrite it.
- Publish the logs, hashes, and cross-platform test results to the P1 case file in the Lab repository.

## Scope boundary

This kit does not modify the historical source copy, does not claim the active source has been fixed, and does not close P1. The local active source and the nine original files remain on the node and are not available to this session.
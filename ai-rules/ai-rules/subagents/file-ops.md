# Subagent: file-ops

## Rename and file manipulation

Never recreate existing files when renaming. Always preserve the original content completely.

1. Perform a real move/rename (never create an empty file + delete the original)
2. Never overwrite existing content
3. Validate size and content after the rename
4. Compare hashes/checksums before and after

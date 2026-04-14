# archive/

**Endorsement Marker:** T(h)reehouse +EC voyage, archival store. No external endorsement implied.

**Licence:** Each archived file preserves the licence that was in force at the time of deprecation. Consult the per-file note.

Superseded artefacts live here per the T(h)reehouse +EC Corporate Design blueprint, Section 0.8 ("Deprecation, not deletion") and Section 15 ("Deprecation Protocol").

## Protocol

When deprecating a file:

1. Move the old file into `archive/`.
2. Add a dated note: `archive/YYYY-MM-DD-<filename>-deprecated.md` recording the reason for deprecation, the superseding file (if any), and the licence in force at the time.
3. Update the asset inventory in the relevant `README.md` or the repository root.
4. Tag the repo (`cd-vX.Y.Z`) if the change is a breaking-change per CD §0.6.

Git history is not a substitute for visible archival.

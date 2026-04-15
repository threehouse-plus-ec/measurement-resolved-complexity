# Asset provenance (Model B — CD §0.10)

**Endorsement Marker:** T(h)reehouse +EC voyage repository. Local candidate framework — T(h)reehouse +EC stewardship. No external endorsement implied.

**Licence:** Assets in this folder are MIT (Handbook / Infrastructure layer per CD §0.3).

This folder holds distributed copies of T(h)reehouse +EC Corporate Design assets, per Model B propagation (CD §0.10). Update within one release cycle when `cd-rules` tags a new release; re-verify the SHA-256 on update.

## Copies

| File | Source repo | Source path | Source commit | Copy date | SHA-256 |
|------|-------------|-------------|---------------|-----------|---------|
| `tokens.css` | [`threehouse-plus-ec/cd-rules`](https://github.com/threehouse-plus-ec/cd-rules) | `tokens.css` | `8671c9333f42d5c6396652f98a30b626bd308886` (2026-04-03) | 2026-04-15 | `097b5903dc3983d3215fb46b4b76948a716e5d2448a1175910b884c25af63962` |

## Drift-detection command

```bash
shasum -a 256 docs/site/assets/tokens.css
```

Compare against the hash above. Mismatch without a documented local justification indicates stale copy (CD §0.10).

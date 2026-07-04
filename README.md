# The Register — Player Character Dossiers

A static site cataloguing player characters across systems and campaigns,
served via GitHub Pages at <https://sortilege-inc.github.io/dossiers/>.

## Layout

```
index.html                    the register (search / filter / sort UI)
data/roster.js                single source of truth: one entry per character,
                              plus PRESETS, SYSTEM_LOGOS, VTT_LABELS
characters/<slug>/
  dossier.html                the character's dossier page
  thumb.<ext>                 card thumbnail (480px wide)
  <art>.png                   full-size images used by that dossier
  sheets/                     VTT sheet exports (Foundry, Alchemy, ...)
shared/
  logos/                      game-system logos for the cards
  art/                        images used by more than one dossier
attic/                        files nothing references (kept, not served anywhere)
tools/
  validate.js                 integrity check — run after every change
  make-thumb.py               portrait -> 480px thumb (needs Pillow)
  migrate.js                  the one-off 2026-07 restructure, kept for the record
```

## Adding a character

1. Create `characters/<slug>/` and drop in `dossier.html` plus its images.
   The dossier references its images by bare filename, so anything it needs
   must sit next to it (or in `shared/art/` via `../../shared/art/...`).
2. Generate the thumbnail:
   `python tools/make-thumb.py characters/<slug>/<portrait>.png`
3. Add an entry to the `characters` array in `data/roster.js`
   (field reference is at the top of that file). Point `file` at the dossier,
   `image` at the thumb, and set `added` to today.
4. Check your work: `node tools/validate.js` — it verifies every path in the
   roster and every reference inside every dossier, and lists orphaned files.

## Notes

- `data/roster.js` is a plain `<script>` (not fetched JSON) so the site also
  works opened straight from disk.
- The index UI reads filters from the URL (`?q=…&status=…`) and supports
  `#preset` deep links — see `PRESETS` in `data/roster.js`.
- Card order is shuffled per visit ("Serendipity") unless a sort is chosen.

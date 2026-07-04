#!/usr/bin/env node
// ============================================================
// One-off migration (2026-07): flat root -> per-character folders.
//
//   characters/<slug>/dossier.html   the dossier page
//   characters/<slug>/thumb.<ext>    card thumbnail
//   characters/<slug>/<art>          images referenced by that dossier only
//   characters/<slug>/sheets/        VTT sheet exports
//   shared/art/                      images referenced by 2+ dossiers
//   shared/logos/                    system logos
//   attic/                           files referenced by nothing
//
// Usage: node tools/migrate.js          (dry run — prints plan)
//        node tools/migrate.js --apply  (moves files, rewrites refs)
// ============================================================
const fs = require('fs');
const path = require('path');

const APPLY = process.argv.includes('--apply');
const root = path.resolve(__dirname, '..');

const KEEP_ROOT = new Set(['index.html', '.gitignore', 'README.md']);
const KEEP_DIRS = new Set(['.git', '.claude', 'data', 'tools', 'characters', 'shared', 'attic']);

// ---------- load roster ----------
const rosterSrc = fs.readFileSync(path.join(root, 'data/roster.js'), 'utf8');
const { characters } = new Function(rosterSrc + '; return { characters };')();

// ---------- helpers ----------
function slugify(plain) {
  return plain
    .normalize('NFD').replace(/\p{Diacritic}/gu, '')
    .replace(/ł/g, 'l').replace(/Ł/g, 'L')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function decodeRef(ref) {
  let r = ref.replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"');
  try { r = decodeURIComponent(r); } catch (_) {}
  return r;
}

function isLocalRef(ref) {
  return ref && !/^(https?:|\/\/|#|mailto:|data:|javascript:)/i.test(ref);
}

// extract local file refs from an HTML string (src= and href=)
function localRefs(html) {
  const refs = new Set();
  for (const m of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
    const raw = m[1];
    if (!isLocalRef(raw)) continue;
    refs.add(decodeRef(raw));
  }
  return refs;
}

const moves = [];            // { from, to } relative paths
const rewrites = new Map();  // dossier relpath -> [{ find, replace }]
const problems = [];
// Windows FS is case-insensitive: a dossier may reference "Lucero.png" while the
// file on disk is "lucero.png". Track moves by lowercased path so the same file
// can't be planned twice under different spellings.
const moved = new Map();     // lowercased original relpath -> new relpath
const movedGet = from => moved.get(from.toLowerCase());
const movedHas = from => moved.has(from.toLowerCase());

function planMove(from, to) {
  if (movedHas(from)) return movedGet(from);
  if (!fs.existsSync(path.join(root, from))) {
    if (fs.existsSync(path.join(root, to))) {
      // already moved by a previous partial run — plan it (apply will skip)
      moved.set(from.toLowerCase(), to);
      moves.push({ from, to });
      return to;
    }
    problems.push(`MISSING on disk: ${from}`);
    return null;
  }
  moved.set(from.toLowerCase(), to);
  moves.push({ from, to });
  return to;
}

// ---------- pass 1: per-entry plan ----------
const slugOf = new Map(); // entry -> slug
const usedSlugs = new Map();
for (const c of characters) {
  let slug = slugify(c.plain);
  if (usedSlugs.has(slug) && usedSlugs.get(slug) !== c.file) {
    slug = slug + '-2';
    problems.push(`slug collision resolved: ${c.plain} -> ${slug}`);
  }
  usedSlugs.set(slug, c.file);
  slugOf.set(c, slug);
}

// map: image file -> set of dossier files referencing it
const imageUsers = new Map();
const dossierHtml = new Map(); // relpath -> content
for (const c of characters) {
  if (dossierHtml.has(c.file)) continue;
  let p = path.join(root, c.file);
  if (!fs.existsSync(p)) {
    // tolerate a previous partial run: dossier may already sit in its new home
    const alt = path.join(root, 'characters', slugOf.get(c), 'dossier.html');
    if (fs.existsSync(alt)) p = alt;
    else { problems.push(`roster dossier missing: ${c.file}`); continue; }
  }
  const html = fs.readFileSync(p, 'utf8');
  dossierHtml.set(c.file, html);
  for (const ref of localRefs(html)) {
    if (!imageUsers.has(ref)) imageUsers.set(ref, new Set());
    imageUsers.get(ref).add(c.file);
  }
}

// roster text rewrite map: exact old value -> new value
const rosterMap = new Map();

for (const c of characters) {
  const slug = slugOf.get(c);
  const dir = `characters/${slug}`;

  // dossier
  const newDossier = movedGet(c.file) || planMove(c.file, `${dir}/dossier.html`);
  if (newDossier) rosterMap.set(c.file, newDossier);

  // thumb
  if (c.image) {
    const ext = path.extname(c.image);
    const newThumb = movedGet(c.image) || planMove(c.image, `${dir}/thumb${ext}`);
    if (newThumb) rosterMap.set(c.image, newThumb);
  }

  // sheets
  for (const s of c.sheets || []) {
    const newSheet = movedGet(s.file) || planMove(s.file, `${dir}/sheets/${s.file}`);
    if (newSheet) rosterMap.set(s.file, newSheet);
  }

  // images referenced inside the dossier
  if (!dossierHtml.has(c.file)) continue;
  const refRewrites = [];
  for (const ref of localRefs(dossierHtml.get(c.file))) {
    if (ref === 'index.html') { refRewrites.push({ find: 'index.html', replace: '../../index.html' }); continue; }
    if (!fs.existsSync(path.join(root, ref))) { problems.push(`broken ref in ${c.file}: ${ref}`); continue; }
    const users = imageUsers.get(ref);
    if (ref === c.image || movedGet(ref) === `${dir}/thumb${path.extname(ref)}`) {
      // dossier reuses its own thumb (thumbs/x.jpg): point at moved thumb
      refRewrites.push({ find: ref, replace: `thumb${path.extname(ref)}` });
      continue;
    }
    if (users.size > 1) {
      // shared image -> shared/art/
      const base = path.basename(ref);
      const to = movedGet(ref) || planMove(ref, `shared/art/${base}`);
      if (to) refRewrites.push({ find: ref, replace: `../../${to}` });
    } else {
      const base = path.basename(ref);
      const to = movedGet(ref) || planMove(ref, `${dir}/${base}`);
      // same basename, same folder -> only rewrite if ref had a path component
      if (to && ref !== base) refRewrites.push({ find: ref, replace: base });
    }
  }
  if (refRewrites.length) rewrites.set(c.file, refRewrites);
}

// ---------- pass 2: logos ----------
for (const f of fs.readdirSync(path.join(root, 'logos'))) {
  planMove(`logos/${f}`, `shared/logos/${f}`);
}

// ---------- pass 3: everything else -> attic ----------
function walkRoot() {
  const leftovers = [];
  for (const f of fs.readdirSync(root)) {
    const st = fs.statSync(path.join(root, f));
    if (st.isDirectory()) {
      if (KEEP_DIRS.has(f)) continue;
      for (const sub of fs.readdirSync(path.join(root, f))) {
        const rel = `${f}/${sub}`;
        if (!movedHas(rel)) leftovers.push(rel);
      }
    } else {
      if (KEEP_ROOT.has(f)) continue;
      if (!movedHas(f)) leftovers.push(f);
    }
  }
  return leftovers;
}
const leftovers = walkRoot();
for (const f of leftovers) planMove(f, `attic/${path.basename(f)}`);

// ---------- report ----------
console.log(`entries: ${characters.length}`);
console.log(`planned moves: ${moves.length}`);
console.log(`dossiers needing internal rewrites: ${rewrites.size}`);
const shared = moves.filter(m => m.to.startsWith('shared/art/'));
console.log(`shared images: ${shared.length}`);
shared.forEach(m => console.log(`  shared: ${m.from}`));
const attic = moves.filter(m => m.to.startsWith('attic/'));
console.log(`attic (unreferenced): ${attic.length}`);
attic.forEach(m => console.log(`  attic: ${m.from}`));
if (problems.length) {
  console.log(`\nPROBLEMS (${problems.length}):`);
  problems.forEach(p => console.log('  ' + p));
}

const inconsistent = problems.some(p => p.startsWith('MISSING') || p.startsWith('roster dossier'));
if (!APPLY) { console.log('\nDry run — nothing changed. Re-run with --apply.'); process.exit(inconsistent ? 1 : 0); }
if (inconsistent) {
  console.error('\nRefusing to apply: plan was built from an inconsistent state (missing files above).');
  process.exit(1);
}

// ---------- apply ----------
console.log('\nApplying...');
function renameWithRetry(from, to) {
  for (let attempt = 1; ; attempt++) {
    try { fs.renameSync(from, to); return; }
    catch (err) {
      if (attempt >= 5 || !['EPERM', 'EBUSY', 'EACCES'].includes(err.code)) throw err;
      // transient Windows lock (AV/indexer) — brief blocking wait, then retry
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 200 * attempt);
    }
  }
}
// 1. file moves — resumable: a move whose source is gone but dest exists is already done.
// Collect failures instead of dying mid-loop, then report; rewrites only run on full success.
const failures = [];
for (const { from, to } of moves) {
  const src = path.join(root, from);
  const dest = path.join(root, to);
  if (!fs.existsSync(src) && fs.existsSync(dest)) continue; // already moved
  try {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    renameWithRetry(src, dest);
  } catch (err) {
    failures.push(`${err.code || err.message}: ${from} -> ${to}`);
  }
}
if (failures.length) {
  console.error(`\n${failures.length} MOVES FAILED:`);
  failures.forEach(f => console.error('  ' + f));
  console.error('Fix the cause and re-run --apply; completed moves will be skipped.');
  process.exit(1);
}
// 2. dossier-internal rewrites (dossiers have moved; operate on new paths)
for (const [dossier, list] of rewrites) {
  const newPath = path.join(root, movedGet(dossier));
  let html = fs.readFileSync(newPath, 'utf8');
  for (const { find, replace } of list) {
    // match raw, URI-encoded, and entity-encoded spellings
    const spellings = [...new Set([find, encodeURI(find), find.replace(/&/g, '&amp;'), find.replace(/'/g, '&#39;')])];
    for (const sp of spellings) {
      html = html.split(`"${sp}"`).join(`"${replace}"`);
    }
  }
  fs.writeFileSync(newPath, html);
}
// 3. roster.js path rewrites
let roster = rosterSrc;
for (const [oldVal, newVal] of rosterMap) {
  const esc = v => v.replace(/'/g, "\\'");
  roster = roster.split(`'${esc(oldVal)}'`).join(`'${esc(newVal)}'`);
}
roster = roster.split(`src: 'logos/`).join(`src: 'shared/logos/`);
fs.writeFileSync(path.join(root, 'data/roster.js'), roster);
// 4. remove now-empty dirs
for (const d of ['thumbs', 'logos']) {
  const p = path.join(root, d);
  if (fs.existsSync(p) && fs.readdirSync(p).length === 0) fs.rmdirSync(p);
}
console.log('Done. Run tools/validate.js to verify.');

#!/usr/bin/env node
// ============================================================
// Register integrity check. Run after any change:
//
//   node tools/validate.js
//
// Verifies:
//   1. every roster entry's file / image / sheets exist on disk
//   2. every src/href inside every dossier resolves
//   3. roster fields use known roles / statuses / systems
//   4. reports files not referenced by the roster or any dossier
// Exit code 1 if anything is broken (orphans are informational).
// ============================================================
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');

const rosterSrc = fs.readFileSync(path.join(root, 'data/roster.js'), 'utf8');
const { characters, PRESETS, SYSTEM_LOGOS } = new Function(
  rosterSrc + '; return { characters, PRESETS, SYSTEM_LOGOS };')();

const ROLES = new Set(['pc', 'support', 'gm-pc', 'pre-gen']);
const STATUSES = new Set(['active', 'hiatus', 'past', 'one-shot', 'unplayed']);

const errors = [];
const warnings = [];

function decodeRef(ref) {
  let r = ref.replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"');
  try { r = decodeURIComponent(r); } catch (_) {}
  return r;
}
const isLocal = ref => ref && !/^(https?:|\/\/|#|mailto:|data:|javascript:)/i.test(ref);

// ---------- 1. roster paths ----------
const referenced = new Set(); // lowercased relpaths known to be used
function checkPath(rel, what) {
  if (!fs.existsSync(path.join(root, rel))) errors.push(`${what}: missing ${rel}`);
  referenced.add(rel.toLowerCase());
}

for (const c of characters) {
  checkPath(c.file, c.plain);
  if (c.image) checkPath(c.image, c.plain);
  for (const s of c.sheets || []) checkPath(s.file, `${c.plain} sheet`);
  if (!ROLES.has(c.role)) errors.push(`${c.plain}: unknown role '${c.role}'`);
  if (!STATUSES.has(c.campaignStatus)) errors.push(`${c.plain}: unknown status '${c.campaignStatus}'`);
  if (!SYSTEM_LOGOS[c.system]) warnings.push(`${c.plain}: system '${c.system}' has no SYSTEM_LOGOS entry`);
  if (!c.added) warnings.push(`${c.plain}: no added date`);
}
for (const logo of Object.values(SYSTEM_LOGOS)) {
  if (logo.src) checkPath(logo.src, 'logo');
}

// ---------- 2. dossier-internal refs ----------
const dossierFiles = new Set(characters.map(c => c.file));
for (const rel of dossierFiles) {
  const p = path.join(root, rel);
  if (!fs.existsSync(p)) continue; // already reported
  const html = fs.readFileSync(p, 'utf8');
  const dir = path.dirname(rel);
  for (const m of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
    if (!isLocal(m[1])) continue;
    const ref = decodeRef(m[1]);
    const resolved = path.posix.normalize(path.posix.join(dir, ref));
    if (!fs.existsSync(path.join(root, resolved))) {
      errors.push(`broken ref in ${rel}: ${ref}`);
    } else {
      referenced.add(resolved.toLowerCase());
    }
  }
}

// ---------- 3. orphans ----------
const SKIP = /^(\.git|\.claude|attic|data|tools|node_modules)(\/|$)|^(index\.html|README\.md|\.gitignore)$/;
const orphans = [];
(function walk(dir) {
  for (const f of fs.readdirSync(path.join(root, dir))) {
    const rel = dir ? `${dir}/${f}` : f;
    if (SKIP.test(rel)) continue;
    if (fs.statSync(path.join(root, rel)).isDirectory()) walk(rel);
    else if (!referenced.has(rel.toLowerCase())) orphans.push(rel);
  }
})('');

// ---------- report ----------
console.log(`${characters.length} entries checked`);
if (errors.length) {
  console.log(`\nERRORS (${errors.length}):`);
  errors.forEach(e => console.log('  ' + e));
}
if (warnings.length) {
  console.log(`\nwarnings (${warnings.length}):`);
  warnings.forEach(w => console.log('  ' + w));
}
if (orphans.length) {
  console.log(`\nunreferenced files (${orphans.length}) — candidates for attic/:`);
  orphans.forEach(o => console.log('  ' + o));
}
if (!errors.length && !warnings.length && !orphans.length) console.log('all clean');
process.exit(errors.length ? 1 : 0);

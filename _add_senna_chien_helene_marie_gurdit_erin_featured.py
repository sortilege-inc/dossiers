import pathlib
from PIL import Image

base = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier')
thumbs = base / 'thumbs'

# ── Thumbnails ──────────────────────────────────────────────────────────────

def make_thumb(src_path, dst_path, max_w=480, quality=82):
    img = Image.open(src_path).convert('RGBA')
    bg = Image.new('RGB', img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    w, h = bg.size
    if w > max_w:
        bg = bg.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
    bg.save(dst_path, 'JPEG', quality=quality, optimize=True)
    print(f'  wrote {dst_path.name}  {bg.size}  ({dst_path.stat().st_size // 1024} KB)')

print('Generating thumbnails...')
make_thumb(base / 'senna.png',  thumbs / 'senna.jpg')
make_thumb(base / 'chien.png',  thumbs / 'chien.jpg')
make_thumb(base / 'helene.png', thumbs / 'helene.jpg')
make_thumb(base / 'marie.png',  thumbs / 'marie.jpg')
make_thumb(base / 'gurdit.png', thumbs / 'gurdit.jpg')
make_thumb(base / 'erin.png',   thumbs / 'erin.jpg')

# ── Load index ───────────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

# ── Mark 8 characters as featured ───────────────────────────────────────────

def add_featured(src, file_key):
    pos      = src.index(f"file: '{file_key}'")
    role_pos = src.index("      role: '", pos)
    role_end = src.index('\n', role_pos)
    return src[:role_end + 1] + "      featured: true,\n" + src[role_end + 1:]

print('\nMarking featured characters...')
for fkey in [
    'AMOS_Dossier.html',
    'Bhimbahadur_Pun_Dossier.html',
    'Morten_Bergesen_Dossier.html',
    'Li_Xia_Lily_Combes_Dossier.html',
    'Rhys_Tyler_Owens_Dossier.html',
    'Paun_Dossier.html',
    'Zuno_Dossier.html',
    'Sia_Tuunbaq_Dossier.html',
]:
    src = add_featured(src, fkey)
    print(f'  {fkey}')

# ── New character entries ────────────────────────────────────────────────────

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

CHIEN = """{
      name: 'Ch&rsquo;ien <span class="given">Po-hsiang</span>',
      plain: 'Ch\\'ien Po-hsiang',
      file: 'Chien_Po-hsiang_Dossier.html',
      image: 'thumbs/chien.jpg',
      eyebrow: 'Investigator &middot; Scholar &middot; Paleobotanist',
      subtitle: 'Paleobotanist &mdash; Children of Fear &mdash; Geological Survey of China',
      system: 'Call of Cthulhu',
      campaign: 'Children of Fear',
      role: 'pc',
      campaignStatus: 'active'
    },"""

ERIN = """{
      name: '<span class="given">Erin</span>',
      plain: 'Erin',
      file: 'Erin_Dossier.html',
      image: 'thumbs/erin.jpg',
      eyebrow: 'Connected Galant &middot; Order of the Vance',
      subtitle: 'Connected Galant &mdash; Under the Invisible Sun &mdash; Order of the Vance',
      system: 'Invisible Sun',
      campaign: 'Under the Invisible Sun',
      role: 'pc',
      campaignStatus: 'past'
    },"""

GURDIT = """{
      name: 'Subedar <span class="given">Gurdit</span> Singh Bajwa',
      plain: 'Subedar Gurdit Singh Bajwa',
      file: 'Gurdit_Singh_Bajwa_Dossier.html',
      image: 'thumbs/gurdit.jpg',
      eyebrow: 'Investigator &middot; Steadfast &middot; Director of Expedition Security',
      subtitle: 'Director of Expedition Security &mdash; Children of Fear &mdash; 15th Ludhiana Sikhs',
      system: 'Call of Cthulhu',
      campaign: 'Children of Fear',
      role: 'pc',
      campaignStatus: 'active'
    },"""

HELENE = """{
      name: '<span class="given">H&eacute;l&egrave;ne</span> &Eacute;lo&iuml;se Bergeron',
      plain: 'Hélène Éloïse Bergeron',
      file: 'Helene_Bergeron_Dossier.html',
      image: 'thumbs/helene.jpg',
      eyebrow: 'Investigator &middot; Seeker &middot; Sociolinguist',
      subtitle: 'Sociolinguist &mdash; Children of Fear &mdash; Mus&eacute;e Guimet',
      system: 'Call of Cthulhu',
      campaign: 'Children of Fear',
      role: 'pc',
      campaignStatus: 'active'
    },"""

MARIE = """{
      name: '<span class="given">Marie</span> Halvor Boucher',
      plain: 'Marie Halvor Boucher',
      file: 'Marie_Boucher_Dossier.html',
      image: 'thumbs/marie.jpg',
      eyebrow: 'Investigator &middot; Outsider &middot; Missionary &amp; Nurse',
      subtitle: 'Missionary &amp; Nurse &mdash; Children of Fear &mdash; Designated Marksman',
      system: 'Call of Cthulhu',
      campaign: 'Children of Fear',
      role: 'pc',
      campaignStatus: 'active'
    },"""

SENNA = """{
      name: '<span class="given">Senna</span>',
      plain: 'Senna',
      file: 'Senna_Dossier.html',
      image: 'thumbs/senna.jpg',
      eyebrow: 'Dark Elf (Drow) &middot; Druid 6 / Ranger 3',
      subtitle: 'Druid 6 / Ranger 3 &mdash; Northridge Campaign &mdash; Soldier of the Underdark',
      system: 'D&amp;D 5e',
      campaign: 'Northridge Campaign',
      role: 'pc',
      campaignStatus: 'past'
    },"""

print('\nInserting characters...')
src = insert_after(src, 'Celenneth_Dossier.html',       CHIEN)   # Ch after Ce, before Ci
src = insert_after(src, 'Erasmus_Dossier.html',         ERIN)    # Eri after Era, before Ery
src = insert_after(src, 'Garin_Dossier.html',           GURDIT)  # Gu after Ga, before H
src = insert_after(src, 'Hallas_Dossier.html',          HELENE)  # He after Ha, before K
src = insert_after(src, 'Malek_Dossier.html',           MARIE)   # Mar after Mal, before Me
src = insert_after(src, 'Secretary_Nomos_Dossier.html', SENNA)   # Sen after Sec, before Sh

# ── Featured button HTML ─────────────────────────────────────────────────────

src = src.replace(
    '    <div class="view-toggles">\n      <div class="toggle-group">\n        <span class="toggle-group-label">Status</span>',
    '    <div class="view-toggles">\n      <div class="toggle-group">\n        <button class="toggle on" id="featured-btn">Featured</button>\n      </div>\n      <div class="toggle-group">\n        <span class="toggle-group-label">Status</span>'
)

# ── Featured JS: state variable ──────────────────────────────────────────────

src = src.replace(
    "  // ----- Filter state -----\n  let activeStatuses = new Set(['active']);\n  let activeRoles    = new Set(['pc']);",
    "  // ----- Filter state -----\n  let featuredMode   = true;\n  let activeStatuses = new Set(['active']);\n  let activeRoles    = new Set(['pc']);"
)

# ── Featured JS: exitFeatured helper + modified render() ────────────────────

src = src.replace(
    "  function render() {\n    const sysQ  = sysInput.value.trim().toLowerCase();\n    const campQ = campInput.value.trim().toLowerCase();\n    const filtered = roster.filter(c =>\n      activeStatuses.has(c.campaignStatus) &&\n      activeRoles.has(c.role) &&\n      (!sysQ  || c.system.toLowerCase().includes(sysQ)) &&\n      (!campQ || c.campaign.toLowerCase().includes(campQ))\n    );",
    "  function exitFeatured() {\n    if (featuredMode) {\n      featuredMode = false;\n      document.getElementById('featured-btn').classList.remove('on');\n    }\n  }\n\n  function render() {\n    let filtered;\n    if (featuredMode) {\n      filtered = roster.filter(c => c.featured);\n    } else {\n      const sysQ  = sysInput.value.trim().toLowerCase();\n      const campQ = campInput.value.trim().toLowerCase();\n      filtered = roster.filter(c =>\n        activeStatuses.has(c.campaignStatus) &&\n        activeRoles.has(c.role) &&\n        (!sysQ  || c.system.toLowerCase().includes(sysQ)) &&\n        (!campQ || c.campaign.toLowerCase().includes(campQ))\n      );\n    }"
)

# ── Featured JS: count text ──────────────────────────────────────────────────

src = src.replace(
    "    countEl.textContent = filtered.length === roster.length\n      ? `${roster.length} ${roster.length === 1 ? 'dossier' : 'dossiers'} on file`\n      : `${filtered.length} of ${roster.length} shown`;",
    "    countEl.textContent = featuredMode\n      ? `${filtered.length} featured`\n      : filtered.length === roster.length\n        ? `${roster.length} ${roster.length === 1 ? 'dossier' : 'dossiers'} on file`\n        : `${filtered.length} of ${roster.length} shown`;"
)

# ── Featured JS: Featured button handler + exitFeatured in status toggles ───

src = src.replace(
    "  // ----- Toggle handlers -----\n  document.querySelectorAll('.toggle[data-status]').forEach(btn => {\n    btn.addEventListener('click', () => {\n      const s = btn.dataset.status;",
    "  // ----- Toggle handlers -----\n  document.getElementById('featured-btn').addEventListener('click', () => {\n    featuredMode = true;\n    document.getElementById('featured-btn').classList.add('on');\n    render();\n  });\n\n  document.querySelectorAll('.toggle[data-status]').forEach(btn => {\n    btn.addEventListener('click', () => {\n      exitFeatured();\n      const s = btn.dataset.status;"
)

# ── Featured JS: exitFeatured in role toggles ────────────────────────────────

src = src.replace(
    "  document.querySelectorAll('.toggle[data-role]').forEach(btn => {\n    btn.addEventListener('click', () => {\n      const r = btn.dataset.role;",
    "  document.querySelectorAll('.toggle[data-role]').forEach(btn => {\n    btn.addEventListener('click', () => {\n      exitFeatured();\n      const r = btn.dataset.role;"
)

# ── Featured JS: exitFeatured in autocomplete input + selectValue ────────────

src = src.replace(
    "    input.addEventListener('input', () => {\n      clearBtn.classList.toggle('visible', input.value.length > 0);\n      refreshSuggestions();\n      suggEl.classList.add('open');\n      render();\n    });",
    "    input.addEventListener('input', () => {\n      exitFeatured();\n      clearBtn.classList.toggle('visible', input.value.length > 0);\n      refreshSuggestions();\n      suggEl.classList.add('open');\n      render();\n    });"
)

src = src.replace(
    "    function selectValue(v) {\n      input.value = v;\n      clearBtn.classList.add('visible');\n      close();\n      render();\n    }",
    "    function selectValue(v) {\n      exitFeatured();\n      input.value = v;\n      clearBtn.classList.add('visible');\n      close();\n      render();\n    }"
)

# ── Write back ───────────────────────────────────────────────────────────────

p.write_text(src, encoding='utf-8')
print('\nDone. Verifying...')

src2 = p.read_text(encoding='utf-8')

# Order check
order_check = [
    ('Celenneth',  "file: 'Celenneth_Dossier.html'"),
    ("Ch'ien",     "file: 'Chien_Po-hsiang_Dossier.html'"),
    ('Cihan',      "file: 'Cihan_Yilan_Dossier.html'"),
    ('Erasmus',    "file: 'Erasmus_Dossier.html'"),
    ('Erin',       "file: 'Erin_Dossier.html'"),
    ('Eryndil',    "file: 'Eryndil_Dossier.html'"),
    ('Garin',      "file: 'Garin_Dossier.html'"),
    ('Gurdit',     "file: 'Gurdit_Singh_Bajwa_Dossier.html'"),
    ('Half-Life',  "file: 'Half-Life_Dossier.html'"),
    ('Hallas',     "file: 'Hallas_Dossier.html'"),
    ('Helene',     "file: 'Helene_Bergeron_Dossier.html'"),
    ('Kaia kW',    "file: 'Kaia_kW_Dossier.html'"),
    ('Malek',      "file: 'Malek_Dossier.html'"),
    ('Marie',      "file: 'Marie_Boucher_Dossier.html'"),
    ('Mellan',     "file: 'Mellan_Dossier.html'"),
    ('Sec Nomos',  "file: 'Secretary_Nomos_Dossier.html'"),
    ('Senna',      "file: 'Senna_Dossier.html'"),
    ('Shulamith',  "file: 'Shulamith_Firehammer_Dossier.html'"),
]
positions = [(label, src2.index(key)) for label, key in order_check]
for i, (label, pos) in enumerate(positions):
    ok = '✓' if i == 0 or pos > positions[i-1][1] else '✗ OUT OF ORDER'
    print(f'  {label:12s}  pos={pos}  {ok}')

# Featured check
print('\nFeatured flags:')
for fkey in ['AMOS_Dossier.html', 'Bhimbahadur_Pun_Dossier.html', 'Morten_Bergesen_Dossier.html',
             'Li_Xia_Lily_Combes_Dossier.html', 'Rhys_Tyler_Owens_Dossier.html',
             'Paun_Dossier.html', 'Zuno_Dossier.html', 'Sia_Tuunbaq_Dossier.html']:
    pos = src2.index(f"file: '{fkey}'")
    block_end = src2.index('\n    }', pos)
    has_feat = 'featured: true' in src2[pos:block_end]
    print(f'  {"✓" if has_feat else "✗"} {fkey}')

# JS patches check
print('\nJS patches:')
print('  featuredMode var:    ', 'featuredMode   = true' in src2)
print('  exitFeatured fn:     ', 'function exitFeatured()' in src2)
print('  Featured btn handler:', "getElementById('featured-btn').addEventListener" in src2)
print('  render featured path:', 'filtered = roster.filter(c => c.featured)' in src2)
print('  featured count text: ', '`${filtered.length} featured`' in src2)
print('  status exitFeatured: ', 'exitFeatured();\n      const s = btn.dataset.status' in src2)
print('  role exitFeatured:   ', 'exitFeatured();\n      const r = btn.dataset.role' in src2)
print('  input exitFeatured:  ', 'exitFeatured();\n      clearBtn.classList.toggle' in src2)
print('  select exitFeatured: ', 'exitFeatured();\n      input.value = v' in src2)
print('  Featured btn HTML:   ', 'id="featured-btn"' in src2)

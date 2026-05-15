import pathlib
from PIL import Image

base = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier')
thumbs = base / 'thumbs'

# ── Thumbnails ─────────────────────────────────────────────────────────────

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
make_thumb(base / 'Aurora_Adelphi_Uluru.jpg', thumbs / 'aurora.jpg')
make_thumb(base / 'faletolu.png',             thumbs / 'faletolu.jpg')
make_thumb(base / 'taran-odamhri.jpeg',       thumbs / 'taran_odamhri.jpg')
make_thumb(base / 'tig.png',                  thumbs / 'tig.jpg')

# ── Index insertions ────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

AURORA = """{
      name: '<span class="given">Aurora</span> Adelphi Uluru',
      plain: 'Aurora Adelphi Uluru',
      file: 'Aurora_Adelphi_Uluru_Dossier.html',
      image: 'thumbs/aurora.jpg',
      eyebrow: 'Moon Elf &middot; Wild Magic Oneiromancer',
      subtitle: 'Druid &middot; Sorcerer &mdash; Wild Magic Oneiromancer &mdash; Lowry Hill East',
      system: 'D&amp;D 5e',
      campaign: 'Lowry Hill East',
      role: 'pc',
      campaignStatus: 'past'
    },"""

FALETOLU = """{
      name: '<span class="given">Faletolu</span> Faletolu',
      plain: 'Faletolu Faletolu',
      file: 'Faletolu_Faletolu_Dossier.html',
      image: 'thumbs/faletolu.jpg',
      eyebrow: 'Barbarian &middot; Bard &middot; Soldier',
      subtitle: 'Six Houses &mdash; Warrior-Skald &mdash; Fearless to a Reckless Extent',
      system: 'D&amp;D 5e',
      campaign: 'Homebrew Setting',
      role: 'pc',
      campaignStatus: 'past'
    },"""

TARAN_ODAMHRI = """{
      name: '<span class="given">Taran</span> O&rsquo;Damhri',
      plain: 'Taran O\\'Damhri',
      file: 'Taran_ODamhri_Dossier.html',
      image: 'thumbs/taran_odamhri.jpg',
      eyebrow: 'Mountain Dwarf &middot; Artificer (Artillerist)',
      subtitle: 'Mountain Dwarf &mdash; Artificer Artillerist Lv. 11 &mdash; Wyldwolf Axis',
      system: 'D&amp;D 5e',
      campaign: 'Wyldwolf Axis',
      role: 'pc',
      campaignStatus: 'past'
    },"""

TIG = """{
      name: '<span class="given">Tig</span>',
      plain: 'Tig',
      file: 'Tig_Dossier.html',
      image: 'thumbs/tig.jpg',
      eyebrow: 'Human (Variant) &middot; Fighter (Battle Master)',
      subtitle: 'Battle Master Lv. 14 &mdash; City Watch &amp; Investigator &mdash; Convention One-Shot',
      system: 'D&amp;D 5e',
      campaign: 'Convention One-Shot',
      role: 'pc',
      campaignStatus: 'past'
    },"""

src = insert_after(src, 'Astrid_Grásula_Dossier.html',     AURORA)         # Au after As, before Ba
src = insert_after(src, 'Executor_Vellpryte_Dossier.html', FALETOLU)       # Fa after Ex, before Fl
src = insert_after(src, 'Taran_Dossier.html',              TARAN_ODAMHRI)  # Tar+ after Tar, before Te
src = insert_after(src, 'Tepshe_Dossier.html',             TIG)            # Tig after Te, before Tiph

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Astrid',      'Astrid_Gr'),
    ('Aurora',      'Aurora_Adelphi'),
    ('Badriyah',    'Badriyah_Dossier'),
    ('Vellpryte',   'Executor_Vellpryte'),
    ('Faletolu',    'Faletolu_Faletolu'),
    ('Flare',       'Flare_Dossier'),
    ('Taran',       'Taran_Dossier'),
    ('Taran O\'D',  'Taran_ODamhri'),
    ('Tepshe',      'Tepshe_Dossier'),
    ('Tig',         'Tig_Dossier'),
    ('Tiphaine',    'tiphaine_dossier'),
]
for label, key in check:
    pos = src2.index(f"file: '{key}")
    name_pos = src2.rindex('name:', 0, pos)
    name_end = src2.index('\n', name_pos)
    print(f"  {label:12s}: {src2[name_pos:name_end].strip()[:72]}")

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
    print(f'  wrote {dst_path.name}  ({dst_path.stat().st_size // 1024} KB)')

def make_thumb_via_temp(src_path, dst_path, max_w=480, quality=82):
    """For same-name renames (Sarru.jpg -> sarru.jpg) on Windows."""
    tmp = dst_path.parent / (dst_path.stem + '_tmp.jpg')
    make_thumb(src_path, tmp, max_w, quality)
    tmp.replace(dst_path)
    print(f'  (renamed from temp -> {dst_path.name})')

print('Generating thumbnails...')
# kaia_kw: different base name, no conflict
make_thumb(thumbs / 'Kaia kW.jpg',       thumbs / 'kaia_kw.jpg')
# sarru / vaetra: only-case difference, need temp
make_thumb_via_temp(thumbs / 'Sarru.jpg',  thumbs / 'sarru.jpg')
make_thumb_via_temp(thumbs / 'Vaetra.jpg', thumbs / 'vaetra.jpg')
# paun: use heraldry.png per user instruction
make_thumb(base / 'heraldry.png',         thumbs / 'paun.jpg')
# zuno: different base name (portait typo), no conflict
make_thumb(thumbs / 'zuno-portait.jpg',   thumbs / 'zuno.jpg')

# ── Index insertions ────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

KAIA_KW = """{
      name: '<span class="given">Kaia</span> kW',
      plain: 'Kaia kW',
      file: 'Kaia_kW_Dossier.html',
      image: 'thumbs/kaia_kw.jpg',
      eyebrow: 'Edgerunner &middot; Rockerboy',
      subtitle: 'Vocalist of Homeschool Dropouts &mdash; Survivor of the Arasaka Ry&#363;jin &mdash; Preem Chooms',
      system: 'Cyberpunk RED',
      campaign: 'Preem Chooms',
      role: 'pc',
      campaignStatus: 'past'
    },"""

PAUN = """{
      name: 'Squire <span class="given">Llwyd</span> &ldquo;Paun&rdquo;',
      plain: 'Paun',
      file: 'Paun_Dossier.html',
      image: 'thumbs/paun.jpg',
      eyebrow: 'Cymric &middot; Squire &middot; Salisbury',
      subtitle: 'Son of Sir Geraint &mdash; Squired to Sir Eamon &mdash; The Boy with the Dulcet Voice',
      system: 'Pendragon',
      campaign: 'Salisbury',
      role: 'pc',
      campaignStatus: 'active'
    },"""

SARRU = """{
      name: '<span class="given">Sarru</span>',
      plain: 'Sarru',
      file: 'Sarru_Dossier.html',
      image: 'thumbs/sarru.jpg',
      eyebrow: 'Ridgeborne Dwarf &middot; Guardian (Stalwart)',
      subtitle: 'Ridgeborne Dwarf &mdash; Guardian of Blade and Valor &mdash; Childhood Circle of Ygva',
      system: 'Daggerheart',
      campaign: 'Caul',
      role: 'support',
      campaignStatus: 'unplayed'
    },"""

VAETRA = """{
      name: '<span class="given">Vaetra</span>',
      plain: 'Vaetra',
      file: 'Vaetra_Dossier.html',
      image: 'thumbs/vaetra.jpg',
      eyebrow: 'Ridgeborne Giant &middot; Bard (Wordsmith)',
      subtitle: 'Ridgeborne Shargan &mdash; Bard of Grace &mdash; Tried to Keep Ygva from Leaving',
      system: 'Daggerheart',
      campaign: 'Caul',
      role: 'support',
      campaignStatus: 'unplayed'
    },"""

ZUNO = """{
      name: '<span class="given">Zuno</span>',
      plain: 'Zuno',
      file: 'Zuno_Dossier.html',
      image: 'thumbs/zuno.jpg',
      eyebrow: 'Forest Gnome &middot; Telepath &middot; House Kath',
      subtitle: 'Majordomo of House Kath &mdash; Forest Gnome Telepath-Bard &mdash; Ptolus',
      system: 'D&amp;D 5e',
      campaign: 'Ptolus: Velvet Glove, Iron Fist',
      role: 'gm-pc',
      campaignStatus: 'unplayed'
    },"""

src = insert_after(src, 'Hallas_Dossier.html',             KAIA_KW)  # Kaia before Kelun
src = insert_after(src, 'Ota_Dossier.html',                PAUN)     # Paun before Photios
src = insert_after(src, 'Rhys_Tyler_Owens_Dossier.html',   SARRU)    # Sarru before Solving
src = insert_after(src, 'Torsten_Fabricatus_Dossier.html', VAETRA)   # Vaetra before Valerian

# Zuno is the new last entry — append after current last (Ygva)
zuno_no_comma = ZUNO.lstrip().rstrip(',')
src = src.replace('\n    }\n  ];', '\n    },\n    ' + zuno_no_comma + '\n  ];')

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Hallas',   'Hallas_Dossier'),
    ('Kaia kW',  'Kaia_kW_Dossier'),
    ('Kelun',    'Kelun_Dossier'),
    ('Ota',      'Ota_Dossier'),
    ('Paun',     'Paun_Dossier'),
    ('Photios',  'Photios_Chrysoloras'),
    ('Rhys',     'Rhys_Tyler_Owens'),
    ('Sarru',    'Sarru_Dossier'),
    ('Solving',  'Solving_Epicurusson'),
    ('Torsten',  'Torsten_Fabricatus'),
    ('Vaetra',   'Vaetra_Dossier'),
    ('Valerian', 'Valerian_de_Castellane'),
    ('Yanos',    'Yanos_Pelagos'),
    ('Ygva',     'Ygva_Dossier'),
    ('Zuno',     'Zuno_Dossier'),
]
for label, key in check:
    pos = src2.index(f"file: '{key}")
    name_pos = src2.rindex('name:', 0, pos)
    name_end = src2.index('\n', name_pos)
    print(f"  {label:10s}: {src2[name_pos:name_end].strip()[:70]}")

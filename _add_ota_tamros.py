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

print('Generating thumbnails...')
make_thumb(thumbs / 'ikoma_no_hosokawa_ota-portrait.jpg', thumbs / 'ota.jpg')
make_thumb(thumbs / 'Tamros.jpg', thumbs / 'tamros.jpg')

# ── Index insertions ────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

def insert_after(src, anchor_file, *new_entries):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    block = ''.join('\n    ' + e.lstrip() for e in new_entries)
    return src[:insert_at] + block + src[insert_at:]

OTA = """{
      name: 'Ikoma no Hosokawa <span class="given">Ota</span>',
      plain: 'Ikoma no Hosokawa Ota',
      file: 'Ota_Dossier.html',
      image: 'thumbs/ota.jpg',
      eyebrow: 'Lion Clan &middot; Yogo Penitent Order',
      subtitle: 'Born Yogo of the Scorpion &mdash; Adopted into the Hosokawa Lion &mdash; Servant of Ikoma Kenji',
      system: 'Legend of the Five Rings',
      campaign: 'City of the Rich Frog',
      role: 'pc',
      campaignStatus: 'hiatus'
    },"""

TAMROS = """{
      name: '<span class="given">Tamros</span>',
      plain: 'Tamros',
      file: 'Tamros_Dossier.html',
      image: 'thumbs/tamros.jpg',
      eyebrow: 'Ridgeborne Ribbet &middot; Rogue (Nightwalker)',
      subtitle: 'Ridgeborne Ribbet &mdash; Rogue of Midnight &mdash; Bound to Ygva',
      system: 'Daggerheart',
      campaign: 'Caul',
      role: 'support',
      campaignStatus: 'unplayed'
    },"""

# Ota: after Morten, before Photios
src = insert_after(src, 'Morten_Bergesen_Dossier.html', OTA)
# Tamros: after Taboo, before Tank
src = insert_after(src, 'Taboo_Dossier.html', TAMROS)

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Morten',  'Morten_Bergesen'),
    ('Ota',     'Ota_Dossier'),
    ('Photios', 'Photios_Chrysoloras'),
    ('Taboo',   'Taboo_Dossier'),
    ('Tamros',  'Tamros_Dossier'),
    ('Tank',    'Tank_Dossier'),
]
for label, key in check:
    pos = src2.index(f"file: '{key}")
    name_pos = src2.rindex('name:', 0, pos)
    name_end = src2.index('\n', name_pos)
    print(f"  {label}: {src2[name_pos:name_end].strip()[:70]}")

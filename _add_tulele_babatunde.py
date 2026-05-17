# -*- coding: utf-8 -*-
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

print('--- Thumbnails ---')
make_thumb(base / 'Tulele_Portrait.png', thumbs / 'tulele.jpg')
make_thumb(base / 'babs.png',            thumbs / 'babs.jpg')

# ── Load index ──────────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

# ── Insertion helpers ────────────────────────────────────────────────────────

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

def insert_before(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    block_start = src.rindex('\n    {', 0, pos)
    return src[:block_start] + '\n    ' + new_entry.lstrip() + src[block_start:]

# ── Index entries ─────────────────────────────────────────────────────────────

BABATUNDE = """{
      name: '<span class="given">Babatunde</span> Ọlayiwọla',
      plain: 'Babatunde Ọlayiwọla',
      file: 'Babatunde_Olayiwola_Dossier.html',
      image: 'thumbs/babs.jpg',
      eyebrow: 'Everyday Hero &middot; Feng Shui 1e',
      subtitle: 'Community Cook &mdash; Witch&rsquo;s Husband &mdash; Artifacts of Ingrin',
      system: 'Feng Shui 1e',
      campaign: 'Artifacts of Ingrin',
      role: 'pc',
      campaignStatus: 'unplayed'
    },"""

TULELE = """{
      name: '<span class="given">Tulele</span> Einarsvard',
      plain: 'Tulele Einarsvard',
      file: 'Tulele_Dossier.html',
      image: 'thumbs/tulele.jpg',
      eyebrow: 'Barbarian / Bard &middot; Far Traveler &middot; Dragon Heist',
      subtitle: 'Insulter-for-Hire &mdash; Proprietor of Knuckleheads &mdash; Waterdeep',
      system: 'D&amp;D 5e',
      campaign: 'Dragon Heist',
      role: 'pc',
      campaignStatus: 'past'
    },"""

print('\n--- Inserting index entries ---')
src = insert_before(src, 'Badriyah_Dossier.html',            BABATUNDE)  # Bab before Bad
src = insert_after(src,  'Torsten_Fabricatus_Dossier.html',  TULELE)     # Tu after To, before Va

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Ayla',      'Ayla_Surgun_Dossier.html'),
    ('Babatunde', 'Babatunde_Olayiwola_Dossier.html'),
    ('Badriyah',  'Badriyah_Dossier.html'),
    ('Torsten',   'Torsten_Fabricatus_Dossier.html'),
    ('Tulele',    'Tulele_Dossier.html'),
    ('Vaetra',    'Vaetra_Dossier.html'),
]
positions = [(label, src2.index(f"file: '{key}'")) for label, key in check]
for i, (label, pos) in enumerate(positions):
    ok = 'OK' if i == 0 or pos > positions[i-1][1] else 'OUT OF ORDER!'
    print(f'  {label:14s}  pos={pos:6d}  {ok}')

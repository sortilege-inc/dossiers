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
make_thumb(base / 'patience-portrait.jpg', thumbs / 'patience.jpg')
make_thumb(base / 'ernie.jpg',             thumbs / 'ernie.jpg')
make_thumb(base / 'Rhys_ap_Cadwgan.png',   thumbs / 'rhys-ap-cadwgan.jpg')

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

ERNEST = """{
      name: '<span class="given">Ernest</span> Burgess',
      plain: 'Ernest Burgess',
      file: 'Ernest_Burgess_Dossier.html',
      image: 'thumbs/ernie.jpg',
      eyebrow: 'Profane Sorcerer &middot; The Kerberos Club',
      subtitle: 'Second Son of the Earl of Onslow &mdash; Sponsored Member &mdash; London, 1830',
      system: 'FATE Core',
      campaign: 'The Kerberos Club',
      role: 'pc',
      campaignStatus: 'past'
    },"""

PATIENCE = """{
      name: '<span class="given">Patience</span> Bataille',
      plain: 'Patience Bataille',
      file: 'Patience_Bataille_Dossier.html',
      image: 'thumbs/patience.jpg',
      eyebrow: 'Good Society &middot; A Jane Austen RPG',
      subtitle: '&ldquo;You can go to India. I am staying on continent.&rdquo; &mdash; The Harrington Season',
      system: 'Good Society',
      campaign: 'The Harrington Season',
      role: 'pc',
      campaignStatus: 'past'
    },"""

RHYS_AP_CADWGAN = """{
      name: '<span class="given">Rhys</span> ap Cadwgan',
      plain: 'Rhys ap Cadwgan',
      file: 'Rhys_ap_Cadwgan_Dossier.html',
      image: 'thumbs/rhys-ap-cadwgan.jpg',
      eyebrow: 'Tactician (Vanguard) &middot; Draw Steel &middot; Kingdom of Kaetis',
      subtitle: 'Knight of Osdon &mdash; Cousin of the Lord &mdash; Kingdom of Kaetis',
      system: 'Draw Steel',
      campaign: 'Kingdom of Kaetis',
      role: 'pc',
      campaignStatus: 'active'
    },"""

print('\n--- Inserting index entries ---')
src = insert_after(src,  'Erin_Dossier.html',              ERNEST)         # Ern after Eri, before Ery
src = insert_before(src, 'Paun_Dossier.html',              PATIENCE)       # Pat before Pau
src = insert_before(src, 'Rhys_Tyler_Owens_Dossier.html',  RHYS_AP_CADWGAN)# Rhys_a before Rhys_T

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Erin',         'Erin_Dossier.html'),
    ('Ernest',       'Ernest_Burgess_Dossier.html'),
    ('Eryndil',      'Eryndil_Dossier.html'),
    ('Ota',          'Ota_Dossier.html'),
    ('Patience',     'Patience_Bataille_Dossier.html'),
    ('Paun',         'Paun_Dossier.html'),
    ('Rear/Kent',    'Rear_Admiral_Kent_Dossier.html'),
    ('Rhys/Cadwgan', 'Rhys_ap_Cadwgan_Dossier.html'),
    ('Rhys/Tyler',   'Rhys_Tyler_Owens_Dossier.html'),
]
positions = [(label, src2.index(f"file: '{key}'")) for label, key in check]
for i, (label, pos) in enumerate(positions):
    ok = 'OK' if i == 0 or pos > positions[i-1][1] else 'OUT OF ORDER!'
    print(f'  {label:16s}  pos={pos:6d}  {ok}')

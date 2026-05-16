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
make_thumb(base / 'saturnin.png', thumbs / 'saturnin.jpg')
make_thumb(base / 'kelly.png',    thumbs / 'kelly.jpg')
make_thumb(base / 'kent.png',     thumbs / 'kent.jpg')

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

# ── Entries ──────────────────────────────────────────────────────────────────

KELLY = """{
      name: '<span class="given">Kelly</span>',
      plain: 'Kelly',
      file: 'Kelly_Dossier.html',
      image: 'thumbs/kelly.jpg',
      eyebrow: 'The Chosen &middot; Monster of the Week',
      subtitle: 'She Who Bears the Bone Chain &mdash; Oberon&rsquo;s Hunt',
      system: 'Monster of the Week',
      campaign: 'Oberon\\'s Hunt',
      role: 'pc',
      campaignStatus: 'one-shot'
    },"""

REAR_ADMIRAL_KENT = """{
      name: 'Rear Admiral <span class="given">Stephen Kent</span>, USN',
      plain: 'Rear Admiral Stephen Kent, USN',
      file: 'Rear_Admiral_Kent_Dossier.html',
      image: 'thumbs/kent.jpg',
      eyebrow: 'Rear Admiral &middot; USN &middot; Call of Cthulhu 7e',
      subtitle: 'Mahan&rsquo;s man &mdash; Widower of a Fortnight &mdash; Haunted House',
      system: 'Call of Cthulhu 7e',
      campaign: 'Haunted House',
      role: 'pc',
      campaignStatus: 'one-shot'
    },"""

SATURNIN = """{
      name: '<span class="given">Saturnin Denys</span> Bastien',
      plain: 'Saturnin Denys Bastien',
      file: 'Saturnin_Denys_Bastien_Dossier.html',
      image: 'thumbs/saturnin.jpg',
      eyebrow: 'Driver &middot; Investigator &middot; Call of Cthulhu 7e',
      subtitle: '&ldquo;The fare is paid first.&rdquo; &mdash; Knights of the Bantam',
      system: 'Call of Cthulhu 7e',
      campaign: 'Knights of the Bantam',
      role: 'pc',
      campaignStatus: 'one-shot'
    },"""

print('\n--- Inserting index entries ---')
src = insert_after(src,  'Kaia_kW_Dossier.html',    KELLY)            # Ke after Ka, before Ke(lun)
src = insert_before(src, 'Regret_Dossier.html',      REAR_ADMIRAL_KENT)  # Re(ar) before Re(gret)
src = insert_after(src,  'Sarru_Dossier.html',       SATURNIN)         # Sat after Sar, before Sec

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Kaia kW',     'Kaia_kW_Dossier.html'),
    ('Kelly',       'Kelly_Dossier.html'),
    ('Kelun',       'Kelun_Dossier.html'),
    ('Protocol',    'Protocol_Keshet_Dossier.html'),
    ('Rear/Kent',   'Rear_Admiral_Kent_Dossier.html'),
    ('Regret',      'Regret_Dossier.html'),
    ('Sarru',       'Sarru_Dossier.html'),
    ('Saturnin',    'Saturnin_Denys_Bastien_Dossier.html'),
    ('SecNomos',    'Secretary_Nomos_Dossier.html'),
]
positions = [(label, src2.index(f"file: '{key}'")) for label, key in check]
for i, (label, pos) in enumerate(positions):
    ok = 'OK' if i == 0 or pos > positions[i-1][1] else 'OUT OF ORDER!'
    print(f'  {label:14s}  pos={pos:6d}  {ok}')

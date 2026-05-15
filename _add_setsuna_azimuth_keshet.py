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
# space/underscore difference — no conflict, write directly
make_thumb(thumbs / 'Operator Azimuth.jpg', thumbs / 'operator_azimuth.jpg')
make_thumb(thumbs / 'Protocol Keshet.jpg',  thumbs / 'protocol_keshet.jpg')
# doji_setsuna.jpg already exists and is correctly named — no action needed

# ── Index insertions ────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

DOJI_SETSUNA = """{
      name: 'Doji <span class="given">Setsuna</span>',
      plain: 'Doji Setsuna',
      file: 'setsuna_dossier.html',
      image: 'thumbs/doji_setsuna.jpg',
      eyebrow: 'Crane Clan &middot; Doji Bureaucrat School',
      subtitle: 'Personal Advisor to the Imperial Envoy &mdash; Emerald Magistrate &mdash; Famously Successful',
      system: 'Legend of the Five Rings',
      campaign: 'The Fragile Peace',
      role: 'pc',
      campaignStatus: 'active'
    },"""

OPERATOR_AZIMUTH = """{
      name: 'Operator <span class="given">Azimuth</span>',
      plain: 'Operator Azimuth',
      file: 'Operator_Azimuth_Dossier.html',
      image: 'thumbs/operator_azimuth.jpg',
      eyebrow: 'Memonek &middot; Talent (Telekinesis)',
      subtitle: 'Psionic Specialist &mdash; Direct Action &mdash; She Is the Weapon',
      system: 'Draw Steel',
      campaign: 'Zenith',
      role: 'support',
      campaignStatus: 'active'
    },"""

PROTOCOL_KESHET = """{
      name: 'Protocol <span class="given">Keshet</span>',
      plain: 'Protocol Keshet',
      file: 'Protocol_Keshet_Dossier.html',
      image: 'thumbs/protocol_keshet.jpg',
      eyebrow: 'Memonek &middot; Tactician (Mastermind)',
      subtitle: 'Field Coordinator &mdash; Tactical Planning &amp; Battlefield Control &mdash; Zenith',
      system: 'Draw Steel',
      campaign: 'Zenith',
      role: 'support',
      campaignStatus: 'active'
    },"""

src = insert_after(src, 'Damrod_Dossier.html',            DOJI_SETSUNA)    # Do after Da, before Ei
src = insert_after(src, 'Morten_Bergesen_Dossier.html',   OPERATOR_AZIMUTH) # Op after Mo, before Ot
src = insert_after(src, 'Photios_Chrysoloras_Dossier.html', PROTOCOL_KESHET) # Pr after Ph, before Re

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Damrod',    'Damrod_Dossier'),
    ('Setsuna',   'setsuna_dossier'),
    ('Eira',      'Eira_Dossier'),
    ('Morten',    'Morten_Bergesen'),
    ('Azimuth',   'Operator_Azimuth'),
    ('Ota',       'Ota_Dossier'),
    ('Photios',   'Photios_Chrysoloras'),
    ('Keshet',    'Protocol_Keshet'),
    ('Regret',    'Regret_Dossier'),
]
for label, key in check:
    pos = src2.index(f"file: '{key}")
    name_pos = src2.rindex('name:', 0, pos)
    name_end = src2.index('\n', name_pos)
    print(f"  {label:10s}: {src2[name_pos:name_end].strip()[:70]}")

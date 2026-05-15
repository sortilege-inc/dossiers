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
make_thumb(base / 'noel.png',       thumbs / 'noel.jpg')
make_thumb(base / 'shulamith.png',  thumbs / 'shulamith.jpg')
make_thumb(base / 'sia.png',        thumbs / 'sia.jpg')

# ── Load index ──────────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

# ── Fix Taran O'Damhri and Tig: past → one-shot ─────────────────────────────

# Wyldwolf Axis is unique — safe single-replace
src = src.replace(
    "campaign: 'Wyldwolf Axis',\n      role: 'pc',\n      campaignStatus: 'past'",
    "campaign: 'Wyldwolf Axis',\n      role: 'pc',\n      campaignStatus: 'one-shot'"
)

# Tig: isolate the block by file anchor to avoid touching other 'past' entries
tig_start = src.index("file: 'Tig_Dossier.html'")
tig_end   = src.index('\n    }', tig_start) + len('\n    }')
src = src[:tig_start] + src[tig_start:tig_end].replace("campaignStatus: 'past'", "campaignStatus: 'one-shot'") + src[tig_end:]

# ── New entries ─────────────────────────────────────────────────────────────

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

NOEL = """{
      name: '<span class="given">Noel</span> Grainger',
      plain: 'Noel Grainger',
      file: 'Noel_Grainger_Dossier.html',
      image: 'thumbs/noel.jpg',
      eyebrow: 'Gangrel &middot; Neonate',
      subtitle: 'Gangrel Neonate &mdash; Not the Only Dead &mdash; Denver Metro',
      system: 'Vampire: the Masquerade',
      campaign: 'Not the Only Dead',
      role: 'pc',
      campaignStatus: 'past'
    },"""

SHULAMITH = """{
      name: '<span class="given">Shulamith</span> Firehammer',
      plain: 'Shulamith Firehammer',
      file: 'Shulamith_Firehammer_Dossier.html',
      image: 'thumbs/shulamith.jpg',
      eyebrow: 'Investigator &middot; Suffragist',
      subtitle: 'Suffragist &mdash; None More Black &mdash; Call of Cthulhu 7th Edition',
      system: 'Call of Cthulhu',
      campaign: 'None More Black',
      role: 'pc',
      campaignStatus: 'past'
    },"""

SIA = """{
      name: '<span class="given">Sia</span> / Tuunbaq',
      plain: 'Sia / Tuunbaq',
      file: 'Sia_Tuunbaq_Dossier.html',
      image: 'thumbs/sia.jpg',
      eyebrow: 'Tiefling &middot; Blood Hunter &middot; Order of the Lycan',
      subtitle: 'Blood Hunter 9 &mdash; Frost &amp; Fur &mdash; Bear-in-the-Blood',
      system: 'D&amp;D 5e',
      campaign: 'Frost &amp; Fur',
      role: 'pc',
      campaignStatus: 'past'
    },"""

src = insert_after(src, 'Morten_Bergesen_Dossier.html',   NOEL)       # No after Mo, before Op
src = insert_after(src, 'Secretary_Nomos_Dossier.html',   SHULAMITH)  # Sh after Se, before So
src = insert_after(src, 'Shulamith_Firehammer_Dossier.html', SIA)     # Si after Sh, before So

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Morten',       'Morten_Bergesen'),
    ('Noel',         'Noel_Grainger'),
    ('Operator Az',  'Operator_Azimuth'),
    ('Secretary N',  'Secretary_Nomos'),
    ('Shulamith',    'Shulamith_Firehammer'),
    ('Sia',          'Sia_Tuunbaq'),
    ('Solving',      'Solving_Epicurusson'),
    ('Taran ODamh',  'Taran_ODamhri'),
    ('Tig',          'Tig_Dossier'),
]
for label, key in check:
    pos      = src2.index(f"file: '{key}")
    name_pos = src2.rindex('name:', 0, pos)
    name_end = src2.index('\n', name_pos)
    status_pos = src2.index('campaignStatus:', pos)
    status_end = src2.index('\n', status_pos)
    print(f"  {label:12s}: {src2[name_pos:name_end].strip()[:60]}  |  {src2[status_pos:status_end].strip()}")

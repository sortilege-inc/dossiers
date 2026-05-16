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
make_thumb(base / 'cihan.png',        thumbs / 'cihan.jpg')       # regenerate updated
make_thumb(base / 'svafnir.jpg',      thumbs / 'svafnir.jpg')
make_thumb(base / 'miele.png',        thumbs / 'miele.jpg')
make_thumb(base / 'Adan_Adan.jpg',    thumbs / 'adan-adan.jpg')
make_thumb(base / 'sam-hornton.png',  thumbs / 'sam-hornton.jpg')

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

ADAN_ADAN = """{
      name: '<span class="given">Adan Adan</span>',
      plain: 'Adan Adan',
      file: 'Adan_Adan_Dossier.html',
      image: 'thumbs/adan-adan.jpg',
      eyebrow: 'Gnoll (Kholo) &middot; Witch Gnoll &middot; Oracle of Bones',
      subtitle: 'Circuit Judge of the Mwangi Expanse &mdash; The Slithering &mdash; Deceased',
      system: 'Pathfinder 2e',
      campaign: 'The Slithering',
      role: 'pc',
      campaignStatus: 'past'
    },"""

MIELE = """{
      name: '<span class="given">Miele</span>',
      plain: 'Miele',
      file: 'Miele_Dossier.html',
      image: 'thumbs/miele.jpg',
      eyebrow: 'Satyr &middot; Resopath &middot; MCDM Talent',
      subtitle: 'Teacher of Lost Questions &mdash; Skai Holt &amp; Ughardi &mdash; Unplayed',
      system: 'D&amp;D 5e',
      campaign: 'Skai Holt &amp; Ughardi',
      role: 'pc',
      campaignStatus: 'unplayed'
    },"""

SAM_HORNTON = """{
      name: '<span class="given">Sam</span> Hornton',
      plain: 'Sam Hornton',
      file: 'Sam_Hornton_Dossier.html',
      image: 'thumbs/sam-hornton.jpg',
      eyebrow: 'Proprietor &middot; the Saloon Owner &middot; Fallstaff',
      subtitle: '&ldquo;A deal&rsquo;s a deal.&rdquo; &mdash; The Occident &mdash; Cortex Prime',
      system: 'Cortex Prime',
      campaign: 'Fallstaff',
      role: 'pc',
      campaignStatus: 'past'
    },"""

SVAFNIR = """{
      name: '<span class="given">Svafnir</span>',
      plain: 'Svafnir',
      file: 'Svafnir_Dossier.html',
      image: 'thumbs/svafnir.jpg',
      eyebrow: 'Ulfhe&eth;nar &middot; Skald',
      subtitle: 'The Hallucinating Skald-Warrior &mdash; Courier of the Eleven Villages',
      system: 'Fate of the Norns: Ragnarok',
      campaign: 'Fate of the Norns: Ragnarok',
      role: 'pc',
      campaignStatus: 'past'
    },"""

print('\n--- Inserting index entries ---')
src = insert_before(src, 'AMOS_Dossier.html',             ADAN_ADAN)   # Ad before AM
src = insert_after(src,  'Mellan_Dossier.html',           MIELE)       # Mi after Me, before Mo
src = insert_after(src,  'Rhys_Tyler_Owens_Dossier.html', SAM_HORNTON) # Sa after Rh, before Sar
src = insert_after(src,  'Stasis_Dossier.html',           SVAFNIR)     # Sv after St, before Ta

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Adan Adan',   'Adan_Adan_Dossier.html'),
    ('AMOS',        'AMOS_Dossier.html'),
    ('Mellan',      'Mellan_Dossier.html'),
    ('Miele',       'Miele_Dossier.html'),
    ('Morten',      'Morten_Bergesen_Dossier.html'),
    ('Rhys',        'Rhys_Tyler_Owens_Dossier.html'),
    ('Sam Hornton', 'Sam_Hornton_Dossier.html'),
    ('Sarru',       'Sarru_Dossier.html'),
    ('Stasis',      'Stasis_Dossier.html'),
    ('Svafnir',     'Svafnir_Dossier.html'),
    ('Taboo',       'Taboo_Dossier.html'),
]
positions = [(label, src2.index(f"file: '{key}'")) for label, key in check]
for i, (label, pos) in enumerate(positions):
    ok = 'OK' if i == 0 or pos > positions[i-1][1] else 'OUT OF ORDER!'
    print(f'  {label:14s}  pos={pos:6d}  {ok}')

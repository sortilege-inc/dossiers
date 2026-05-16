import pathlib
from PIL import Image

base = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier')
thumbs = base / 'thumbs'

# ── Fix broken image paths in dossiers ─────────────────────────────────────

def patch(filename, *replacements):
    p = base / filename
    src = p.read_text(encoding='utf-8')
    for old, new in replacements:
        if old not in src:
            print(f'  !! anchor missing in {filename}: {repr(old[:60])}')
        else:
            src = src.replace(old, new, 1)
    p.write_text(src, encoding='utf-8')
    print(f'  fixed: {filename}')

print('--- Fix dossier image paths ---')
patch('Brenn___Hroga_Dossier.html',
    ('src="Brenn.png"', 'src="brenn.png"'),
    ('src="Hroga.png"', 'src="hroga.png"'))
patch('Lor_Un_Dossier.html',
    ('src="Lor_Un.png"', 'src="Lor-Un.png"'))

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

print('\n--- Thumbnails ---')
make_thumb(base / 'blaska.png',    thumbs / 'blaska.jpg')     # updated source
make_thumb(base / 'pelorajax.png', thumbs / 'pelorajax.jpg')  # updated source
make_thumb(base / 'brenn.png',     thumbs / 'brenn.jpg')
make_thumb(base / 'Lor-Un.png',    thumbs / 'lor-un.jpg')
make_thumb(base / 'Oleansel.png',  thumbs / 'oleansel.jpg')
make_thumb(base / 'emil.png',      thumbs / 'emil.jpg')

# ── Load index ──────────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

# ── Entries ──────────────────────────────────────────────────────────────────

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

BRENN_HROGA = """{
      name: '<span class="given">Brenn</span> &amp; Hroga',
      plain: 'Brenn & Hroga',
      file: 'Brenn___Hroga_Dossier.html',
      image: 'thumbs/brenn.jpg',
      eyebrow: 'Dwarf &middot; Beastheart &middot; Prowler Subclass',
      subtitle: 'Quit the Work That Hurt People &mdash; Collateral &mdash; &amp; Her Boar',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

EMIL_ORESTES = """{
      name: '<span class="given">Emil</span> / Orestes',
      plain: 'Emil / Orestes',
      file: 'Emil_Orestes_Dossier.html',
      image: 'thumbs/emil.jpg',
      eyebrow: 'Persona &middot; Paragon &middot; The Dictator',
      subtitle: 'Metalhead-Turned-VC &mdash; BeggarTok DIE &mdash; The Dictator (d4)',
      system: 'DIE',
      campaign: 'BeggarTok DIE',
      role: 'pc',
      campaignStatus: 'past'
    },"""

LOR_UN = """{
      name: '<span class="given">Lor Un</span>',
      plain: 'Lor Un',
      file: 'Lor_Un_Dossier.html',
      image: 'thumbs/lor-un.jpg',
      eyebrow: 'Human &middot; Troubadour &middot; Auteur',
      subtitle: 'Placed Inside Her Own Character Sheet &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

OLEANSEL = """{
      name: '<span class="given">Oleansel</span>',
      plain: 'Oleansel',
      file: 'Oleansel_Dossier.html',
      image: 'thumbs/oleansel.jpg',
      eyebrow: 'High Elf &middot; Shadow &middot; College of the Harlequin Mask',
      subtitle: 'Aristocrat, Defrocked &mdash; Rehabilitating in Good Faith &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

print('\n--- Inserting index entries ---')
src = insert_after(src, 'Blaska_Dossier.html',         BRENN_HROGA)   # Br after Bl, before Ce
src = insert_after(src, 'Eira_Dossier.html',            EMIL_ORESTES)  # Em after Ei, before Eo
src = insert_after(src, 'Linnea_Dossier.html',          LOR_UN)        # Lo after Li(nnea), before Lu(cero)
src = insert_after(src, 'Noel_Grainger_Dossier.html',   OLEANSEL)      # Ol after No, before Op(erator)

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Blaska',        'Blaska_Dossier.html'),
    ('Brenn&Hroga',   'Brenn___Hroga_Dossier.html'),
    ('Celenneth',     'Celenneth_Dossier.html'),
    ('Eira',          'Eira_Dossier.html'),
    ('Emil/Orestes',  'Emil_Orestes_Dossier.html'),
    ('Eorlas',        'Eorlas_Dossier.html'),
    ('Linnea',        'Linnea_Dossier.html'),
    ('Lor Un',        'Lor_Un_Dossier.html'),
    ('Lucero',        'Lucero_d_Albec_Dossier.html'),
    ('Noel',          'Noel_Grainger_Dossier.html'),
    ('Oleansel',      'Oleansel_Dossier.html'),
    ('Operator Az',   'Operator_Azimuth_Dossier.html'),
]
positions = [(label, src2.index(f"file: '{key}'")) for label, key in check]
for i, (label, pos) in enumerate(positions):
    ok = 'OK' if i == 0 or pos > positions[i-1][1] else 'OUT OF ORDER!'
    print(f'  {label:14s}  pos={pos:6d}  {ok}')

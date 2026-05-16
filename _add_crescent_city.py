# -*- coding: utf-8 -*-
import pathlib
from PIL import Image

base = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier')
thumbs = base / 'thumbs'

# ── Fix capitalised image refs in dossiers ───────────────────────────────────

def patch(filename, old, new):
    p = base / filename
    src = p.read_text(encoding='utf-8')
    if old not in src:
        print(f'  !! anchor missing in {filename}: {repr(old)}')
        return
    p.write_text(src.replace(old, new, 1), encoding='utf-8')
    print(f'  patched: {filename}  ({old} -> {new})')

print('--- Fix image refs ---')
patch('Ayla_Surgun_Dossier.html',                'src="Ayla.png"',     'src="ayla.png"')
patch('Damla_Sancaktar_Dossier.html',            'src="Damla.png"',    'src="damla.png"')
patch('Father_Leonidas_Dossier.html',            'src="Leonidas.png"', 'src="leonidas.png"')
patch('Hassan_Al-Kabir_Dossier.html',            'src="Hassan.png"',   'src="hassan.png"')
patch('Ibrahim_The_Silent_Sentinel_Dossier.html','src="Ibrahim.png"',  'src="ibrahim.png"')
patch('Kemal_The_Sentinel_Balik_Dossier.html',   'src="Kemal.png"',    'src="kemal.png"')
patch('Leyla_of_the_Blue_Eye_Dossier.html',      'src="Leyla.png"',    'src="leyla.png"')
patch('Miriam_the_Chronicler_Dossier.html',      'src="Miriam.png"',   'src="miriam.png"')
patch('Nadir_the_Tormented_Dossier.html',        'src="Nadir.png"',    'src="nadir.png"')
patch('Salih_Celestialwalker_Dossier.html',      'src="Salih.png"',    'src="salih.png"')
patch('Selim_the_Bound_Dossier.html',            'src="Selim.png"',    'src="selim.png"')
patch('Zehra_of_the_Spinning_Veil_Dossier.html', 'src="Zehra.png"',    'src="zehra.png"')

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
make_thumb(base / 'ayla.png',     thumbs / 'ayla.jpg')
make_thumb(base / 'damla.png',    thumbs / 'damla.jpg')
make_thumb(base / 'leonidas.png', thumbs / 'leonidas.jpg')
make_thumb(base / 'hassan.png',   thumbs / 'hassan.jpg')
make_thumb(base / 'ibrahim.png',  thumbs / 'ibrahim.jpg')
make_thumb(base / 'kemal.png',    thumbs / 'kemal.jpg')
make_thumb(base / 'leyla.png',    thumbs / 'leyla.jpg')
make_thumb(base / 'miriam.png',   thumbs / 'miriam.jpg')
make_thumb(base / 'nadir.png',    thumbs / 'nadir.jpg')
make_thumb(base / 'salih.png',    thumbs / 'salih.jpg')
make_thumb(base / 'selim.png',    thumbs / 'selim.jpg')
make_thumb(base / 'zehra.png',    thumbs / 'zehra.jpg')

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

AYLA = """{
      name: '<span class="given">Ayla</span> Sürgün',
      plain: 'Ayla Sürgün',
      file: 'Ayla_Surgun_Dossier.html',
      image: 'thumbs/ayla.jpg',
      eyebrow: 'Rogue &middot; The Crescent City',
      subtitle: 'Yörük Operative of an Unnamed Bureau &mdash; The Secret Service',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

DAMLA = """{
      name: '<span class="given">Damla</span> Sancaktar',
      plain: 'Damla Sancaktar',
      file: 'Damla_Sancaktar_Dossier.html',
      image: 'thumbs/damla.jpg',
      eyebrow: 'Bard &middot; The Crescent City',
      subtitle: 'Shadow-Player of Pera &mdash; College of the Shadowactor',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

FATHER_LEONIDAS = """{
      name: 'Father <span class="given">Leonidas</span>',
      plain: 'Father Leonidas',
      file: 'Father_Leonidas_Dossier.html',
      image: 'thumbs/leonidas.jpg',
      eyebrow: 'Cleric &middot; The Crescent City',
      subtitle: 'Greek Orthodox Priest &mdash; Realitymender Domain',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

HASSAN = """{
      name: '<span class="given">Hassan</span> Al-Kabir',
      plain: 'Hassan Al-Kabir',
      file: 'Hassan_Al-Kabir_Dossier.html',
      image: 'thumbs/hassan.jpg',
      eyebrow: 'Barbarian &middot; The Crescent City',
      subtitle: 'Street-King of the Lower Quarters &mdash; Urban Vagabond',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

IBRAHIM = """{
      name: '<span class="given">Ibrahim</span> the Silent Sentinel',
      plain: 'Ibrahim the Silent Sentinel',
      file: 'Ibrahim_The_Silent_Sentinel_Dossier.html',
      image: 'thumbs/ibrahim.jpg',
      eyebrow: 'Paladin &middot; The Crescent City',
      subtitle: 'Warden of the Poorer Quarters &mdash; Oath of Silence',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

KEMAL = """{
      name: '<span class="given">Kemal</span> Balık',
      plain: 'Kemal Balık',
      file: 'Kemal_The_Sentinel_Balik_Dossier.html',
      image: 'thumbs/kemal.jpg',
      eyebrow: 'Fighter &middot; The Crescent City',
      subtitle: 'Çorbacı of the Old Corps &mdash; Janissary',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

LEYLA = """{
      name: '<span class="given">Leyla</span> of the Blue Eye',
      plain: 'Leyla of the Blue Eye',
      file: 'Leyla_of_the_Blue_Eye_Dossier.html',
      image: 'thumbs/leyla.jpg',
      eyebrow: 'Druid &middot; The Crescent City',
      subtitle: 'Charm-maker of the Spice Market &mdash; Circle of Nazar',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

MIRIAM = """{
      name: '<span class="given">Miriam</span> the Chronicler',
      plain: 'Miriam the Chronicler',
      file: 'Miriam_the_Chronicler_Dossier.html',
      image: 'thumbs/miriam.jpg',
      eyebrow: 'Warlock &middot; The Crescent City',
      subtitle: 'Librarian of the Grand Bazaar &mdash; The Ancient Sage',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

NADIR = """{
      name: '<span class="given">Nadir</span> the Tormented',
      plain: 'Nadir the Tormented',
      file: 'Nadir_the_Tormented_Dossier.html',
      image: 'thumbs/nadir.jpg',
      eyebrow: 'Sorcerer &middot; The Crescent City',
      subtitle: 'Glassblower of the Golden Horn &mdash; Djinn-Possessed Origin',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

SALIH = """{
      name: '<span class="given">Salih</span> Celestialwalker',
      plain: 'Salih Celestialwalker',
      file: 'Salih_Celestialwalker_Dossier.html',
      image: 'thumbs/salih.jpg',
      eyebrow: 'Wizard &middot; The Crescent City',
      subtitle: 'Astronomer of the Sublime Porte &mdash; Stargazer',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

SELIM = """{
      name: '<span class="given">Selim</span> the Bound',
      plain: 'Selim the Bound',
      file: 'Selim_the_Bound_Dossier.html',
      image: 'thumbs/selim.jpg',
      eyebrow: 'Warlock &middot; The Crescent City',
      subtitle: 'Mediator of Djinn at the Eyüp Gate &mdash; The Djinnmaster',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

ZEHRA = """{
      name: '<span class="given">Zehra</span> of the Spinning Veil',
      plain: 'Zehra of the Spinning Veil',
      file: 'Zehra_of_the_Spinning_Veil_Dossier.html',
      image: 'thumbs/zehra.jpg',
      eyebrow: 'Monk &middot; The Crescent City',
      subtitle: 'Dervish of the Galata Lodge &mdash; Whirling Dervish',
      system: 'D&amp;D 5e',
      campaign: 'The Crescent City',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

print('\n--- Inserting index entries ---')
src = insert_after(src,  'Aurora_Adelphi_Uluru_Dossier.html',      AYLA)            # Ay after Au, before Ba
src = insert_before(src, 'Damrod_Dossier.html',                    DAMLA)           # Daml before Damr
src = insert_after(src,  'Faletolu_Faletolu_Dossier.html',         FATHER_LEONIDAS) # Fath after Fal, before Fati
src = insert_after(src,  'Hallas_Dossier.html',                    HASSAN)          # Has after Hall, before Hel
src = insert_after(src,  'Helene_Bergeron_Dossier.html',           IBRAHIM)         # Ibr after Hel, before Kai
src = insert_after(src,  'Kelun_Dossier.html',                     KEMAL)           # Kem after Kelu, before Kha
src = insert_before(src, 'Li_Xia_Lily_Combes_Dossier.html',       LEYLA)           # Le before Li
src = insert_after(src,  'Miele_Dossier.html',                     MIRIAM)          # Mir after Mie, before Mor
src = insert_before(src, 'Noel_Grainger_Dossier.html',             NADIR)           # Na before No
src = insert_before(src, 'Sam_Hornton_Dossier.html',               SALIH)           # Sal before Sam
src = insert_after(src,  'Secretary_Nomos_Dossier.html',           SELIM)           # Sel after Sec, before Sen
src = insert_before(src, 'Zuno_Dossier.html',                      ZEHRA)           # Zeh before Zun

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Aurora',    'Aurora_Adelphi_Uluru_Dossier.html'),
    ('Ayla',      'Ayla_Surgun_Dossier.html'),
    ('Badriyah',  'Badriyah_Dossier.html'),
    ('Damla',     'Damla_Sancaktar_Dossier.html'),
    ('Damrod',    'Damrod_Dossier.html'),
    ('Faletolu',  'Faletolu_Faletolu_Dossier.html'),
    ('F.Leonidas','Father_Leonidas_Dossier.html'),
    ('Fatima',    'Fatima_Dossier.html'),
    ('Hallas',    'Hallas_Dossier.html'),
    ('Hassan',    'Hassan_Al-Kabir_Dossier.html'),
    ('Helene',    'Helene_Bergeron_Dossier.html'),
    ('Ibrahim',   'Ibrahim_The_Silent_Sentinel_Dossier.html'),
    ('Kaia',      'Kaia_kW_Dossier.html'),
    ('Kelun',     'Kelun_Dossier.html'),
    ('Kemal',     'Kemal_The_Sentinel_Balik_Dossier.html'),
    ('Khalida',   'Khalida_Dossier.html'),
    ('Li Xia',    'Li_Xia_Lily_Combes_Dossier.html'),
    ('Leyla',     'Leyla_of_the_Blue_Eye_Dossier.html'),
    ('Miele',     'Miele_Dossier.html'),
    ('Miriam',    'Miriam_the_Chronicler_Dossier.html'),
    ('Morten',    'Morten_Bergesen_Dossier.html'),
    ('Nadir',     'Nadir_the_Tormented_Dossier.html'),
    ('Noel',      'Noel_Grainger_Dossier.html'),
    ('Salih',     'Salih_Celestialwalker_Dossier.html'),
    ('Sam',       'Sam_Hornton_Dossier.html'),
    ('SecNomos',  'Secretary_Nomos_Dossier.html'),
    ('Selim',     'Selim_the_Bound_Dossier.html'),
    ('Senna',     'Senna_Dossier.html'),
    ('Zehra',     'Zehra_of_the_Spinning_Veil_Dossier.html'),
    ('Zuno',      'Zuno_Dossier.html'),
]
positions = [(label, src2.index(f"file: '{key}'")) for label, key in check]

# Check Leyla vs Li Xia separately (Leyla should come before Li Xia)
leyla_pos = src2.index("file: 'Leyla_of_the_Blue_Eye_Dossier.html'")
lixa_pos  = src2.index("file: 'Li_Xia_Lily_Combes_Dossier.html'")

all_ok = True
for i, (label, pos) in enumerate(positions):
    ok = 'OK' if i == 0 or pos > positions[i-1][1] else 'OUT OF ORDER!'
    if ok != 'OK': all_ok = False
    print(f'  {label:14s}  pos={pos:6d}  {ok}')

print(f'\n  Leyla({leyla_pos}) < Li Xia({lixa_pos}): {"OK" if leyla_pos < lixa_pos else "OUT OF ORDER!"}')

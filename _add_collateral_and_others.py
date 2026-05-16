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

print('Generating thumbnails...')
make_thumb(base / 'blaska.png',              thumbs / 'blaska.jpg')
make_thumb(base / 'lucero.png',              thumbs / 'lucero.jpg')
make_thumb(base / 'Krellen-Jek.png',         thumbs / 'krellen-jek.jpg')
make_thumb(base / 'Clasiena.png',            thumbs / 'clasiena.jpg')
make_thumb(base / 'Gungr.png',              thumbs / 'gungr.jpg')
make_thumb(base / 'Maike.png',              thumbs / 'maike.jpg')
make_thumb(base / 'Pelorajax.png',           thumbs / 'pelorajax.jpg')
make_thumb(base / 'Golden_Dervish_King.jpg', thumbs / 'golden_dervish_king.jpg')
make_thumb(base / 'fenrir.jpg',              thumbs / 'fenrir.jpg')
make_thumb(base / 'fatima.png',              thumbs / 'fatima.jpg')
make_thumb(base / 'skretting.png',           thumbs / 'skretting.jpg')

# ── Load index ──────────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

# ── Helpers ─────────────────────────────────────────────────────────────────

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

# ── Entries ──────────────────────────────────────────────────────────────────

BLASKA = """{
      name: '<span class="given">Blaska</span>',
      plain: 'Blaska',
      file: 'Blaska_Dossier.html',
      image: 'thumbs/blaska.jpg',
      eyebrow: 'Orc &middot; Null &middot; Metakinetic Tradition',
      subtitle: 'Farmer, Retired &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

CLASIENA = """{
      name: '<span class="given">Clasiena</span>',
      plain: 'Clasiena',
      file: 'Clasiena_Dossier.html',
      image: 'thumbs/clasiena.jpg',
      eyebrow: 'Revenant &middot; Elementalist &middot; Void Discipline',
      subtitle: 'Returned, with Unfinished Business &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

FATIMA = """{
      name: '<span class="given">Fatima</span>',
      plain: 'Fatima',
      file: 'Fatima_Dossier.html',
      image: 'thumbs/fatima.jpg',
      eyebrow: 'Ghost &middot; Monsterhearts 2 &middot; Shoalsburg High',
      subtitle: 'The Ghost &mdash; Shoalsburg High &mdash; Deceased, But Around',
      system: 'Monsterhearts',
      campaign: 'Shoalsburg High',
      role: 'pc',
      campaignStatus: 'past'
    },"""

FENRIR = """{
      name: '<span class="given">Fenrir</span>',
      plain: 'Fenrir',
      file: 'Fenrir_Dossier.html',
      image: 'thumbs/fenrir.jpg',
      eyebrow: 'Cleric &middot; One True God &middot; Dolmenwood',
      subtitle: 'Cleric of the One True God &mdash; Dolmenwood &mdash; Pilgrim into the Cold Dark',
      system: 'Old School Essentials',
      campaign: 'Dolmenwood',
      role: 'pc',
      campaignStatus: 'one-shot'
    },"""

GOLDEN = """{
      name: 'The <span class="given">Golden Dervish King</span>',
      plain: 'The Golden Dervish King',
      file: 'Golden_Dervish_King_Dossier.html',
      image: 'thumbs/golden_dervish_king.jpg',
      eyebrow: 'Wanderer of the Rivers and Lakes &middot; Fire Doctrine Priest',
      subtitle: 'Fire Doctrine Priest &mdash; Legends of Wulin &mdash; Wulin Initiate',
      system: 'Legends of Wulin',
      campaign: 'Legends of Wulin',
      role: 'pc',
      campaignStatus: 'past'
    },"""

GUNGR = """{
      name: '<span class="given">Gungr</span>',
      plain: 'Gungr',
      file: 'Gungr_Dossier.html',
      image: 'thumbs/gungr.jpg',
      eyebrow: 'Hakaan &middot; Talent &middot; Chronopathy Discipline',
      subtitle: 'The Portents Were Honest &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

KRELLEN = """{
      name: '<span class="given">Krellen-Jek</span>',
      plain: 'Krellen-Jek',
      file: 'Krellen-Jek_Dossier.html',
      image: 'thumbs/krellen-jek.jpg',
      eyebrow: 'Kuran&rsquo;zoi &middot; Tactician &middot; Insurgent',
      subtitle: 'Deserter &mdash; Late of an Unnamed Pirate Fleet &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

LUCERO = """{
      name: '<span class="given">Lucero</span> d&rsquo;Albec',
      plain: 'Lucero d\\'Albec',
      file: 'Lucero_d_Albec_Dossier.html',
      image: 'thumbs/lucero.jpg',
      eyebrow: 'Devil &middot; Fury &middot; Reaver',
      subtitle: 'Former Watch Officer &mdash; Wanted for Homicide &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

MAIKE = """{
      name: '<span class="given">Maike</span> Oostgracht',
      plain: 'Maike Oostgracht',
      file: 'Maike_Oostgracht_Dossier.html',
      image: 'thumbs/maike.jpg',
      eyebrow: 'Polder &middot; Conduit &middot; Domains of Love &amp; War',
      subtitle: 'Proponent of a Sanctuary Not Yet Built &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

PELORAJAX = """{
      name: '<span class="given">Pelorajax</span>',
      plain: 'Pelorajax',
      file: 'Pelorajax_Dossier.html',
      image: 'thumbs/pelorajax.jpg',
      eyebrow: 'DragonKnight &middot; Summoner &middot; Circle of Storms',
      subtitle: 'Former Agent &mdash; The Storms Answer Her &mdash; Collateral',
      system: 'Draw Steel',
      campaign: 'Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

SKRETTING = """{
      name: '<span class="given">Skretting</span> Sikasoowukaa',
      plain: 'Skretting Sikasoowukaa',
      file: 'Skretting_Sikasoowukaa_Dossier.html',
      image: 'thumbs/skretting.jpg',
      eyebrow: 'Variant Human &middot; Cleric / Sorcerer / Monk &middot; Pilgrim of the Open Path',
      subtitle: 'Cleric 1 / Sorcerer 3 / Monk 6 &mdash; Northridge Campaign &mdash; Kingdom of Greycott',
      system: 'D&amp;D 5e',
      campaign: 'Northridge Campaign',
      role: 'pc',
      campaignStatus: 'past'
    },"""

print('\nInserting entries...')
src = insert_after(src, 'Bhimbahadur_Pun_Dossier.html',      BLASKA)     # Bl after Bh, before Ce
src = insert_after(src, 'Cihan_Yilan_Dossier.html',           CLASIENA)   # Cl after Ci, before Cl(ifford)
src = insert_after(src, 'Faletolu_Faletolu_Dossier.html',     FATIMA)     # Fat after Fal, before Fl
src = insert_after(src, 'Fatima_Dossier.html',                FENRIR)     # Fen after Fat, before Fl
src = insert_after(src, 'Garin_Dossier.html',                 GOLDEN)     # Go after Ga, before Gu
src = insert_after(src, 'Golden_Dervish_King_Dossier.html',   GUNGR)      # Gun after Go, before Gur(dit)
src = insert_after(src, 'Khalida_Dossier.html',               KRELLEN)    # Kr after Kh, before Li
src = insert_after(src, 'Linnea_Dossier.html',                LUCERO)     # Lu after Li(nnea), before Ma
src = insert_after(src, 'Lucero_d_Albec_Dossier.html',        MAIKE)      # Mai after Lu, before Mal(ek)
src = insert_after(src, 'Paun_Dossier.html',                  PELORAJAX)  # Pe after Pa, before Ph
src = insert_after(src, 'Sia_Tuunbaq_Dossier.html',           SKRETTING)  # Sk after Si, before So(lving)

p.write_text(src, encoding='utf-8')
print('\nDone. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Bhimbahadur',   'Bhimbahadur_Pun_Dossier.html'),
    ('Blaska',        'Blaska_Dossier.html'),
    ('Celenneth',     'Celenneth_Dossier.html'),
    ("Ch'ien",        'Chien_Po-hsiang_Dossier.html'),
    ('Cihan',         'Cihan_Yilan_Dossier.html'),
    ('Clasiena',      'Clasiena_Dossier.html'),
    ('Clifford',      'Clifford_Joel_Howard_Dossier.html'),
    ('Faletolu',      'Faletolu_Faletolu_Dossier.html'),
    ('Fatima',        'Fatima_Dossier.html'),
    ('Fenrir',        'Fenrir_Dossier.html'),
    ('Flare',         'Flare_Dossier.html'),
    ('Garin',         'Garin_Dossier.html'),
    ('GoldenDervish', 'Golden_Dervish_King_Dossier.html'),
    ('Gungr',         'Gungr_Dossier.html'),
    ('Gurdit',        'Gurdit_Singh_Bajwa_Dossier.html'),
    ('Khalida',       'Khalida_Dossier.html'),
    ('Krellen-Jek',   'Krellen-Jek_Dossier.html'),
    ('Li Xia',        'Li_Xia_Lily_Combes_Dossier.html'),
    ('Linnea',        'Linnea_Dossier.html'),
    ('Lucero',        'Lucero_d_Albec_Dossier.html'),
    ('Maike',         'Maike_Oostgracht_Dossier.html'),
    ('Malek',         'Malek_Dossier.html'),
    ('Paun',          'Paun_Dossier.html'),
    ('Pelorajax',     'Pelorajax_Dossier.html'),
    ('Photios',       'Photios_Chrysoloras_Dossier.html'),
    ('Sia',           'Sia_Tuunbaq_Dossier.html'),
    ('Skretting',     'Skretting_Sikasoowukaa_Dossier.html'),
    ('Solving',       'Solving_Epicurusson_Dossier.html'),
]
positions = [(label, src2.index(f"file: '{key}'")) for label, key in check]
for i, (label, pos) in enumerate(positions):
    ok = 'OK' if i == 0 or pos > positions[i-1][1] else 'OUT OF ORDER!'
    print(f'  {label:14s}  pos={pos:6d}  {ok}')

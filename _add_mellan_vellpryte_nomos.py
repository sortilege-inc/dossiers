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

def make_thumb_via_temp(src_path, dst_path, max_w=480, quality=82):
    """For only-case renames (Mellan.jpg -> mellan.jpg) on Windows."""
    tmp = dst_path.parent / (dst_path.stem + '_tmp.jpg')
    make_thumb(src_path, tmp, max_w, quality)
    tmp.replace(dst_path)
    print(f'  (renamed from temp -> {dst_path.name})')

print('Generating thumbnails...')
# space/case difference — can write directly (different filename)
make_thumb(thumbs / 'Executor Vellpryte.jpg', thumbs / 'executor_vellpryte.jpg')
make_thumb(thumbs / 'Secretary Nomos.jpg',    thumbs / 'secretary_nomos.jpg')
# only-case difference — needs temp
make_thumb_via_temp(thumbs / 'Mellan.jpg',    thumbs / 'mellan.jpg')

# ── Index insertions ────────────────────────────────────────────────────────

p = base / 'index.html'
src = p.read_text(encoding='utf-8')

def insert_after(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

EXECUTOR_VELLPRYTE = """{
      name: 'Executor <span class="given">Vellpryte</span>',
      plain: 'Executor Vellpryte',
      file: 'Executor_Vellpryte_Dossier.html',
      image: 'thumbs/executor_vellpryte.jpg',
      eyebrow: 'Memonek &middot; Censor (Paragon)',
      subtitle: 'Senior Field Agent &mdash; Primary Combatant &amp; Judicial Authority &mdash; Zenith',
      system: 'Draw Steel',
      campaign: 'Zenith &middot; Collateral',
      role: 'pre-gen',
      campaignStatus: 'active'
    },"""

MELLAN = """{
      name: '<span class="given">Mellan</span>',
      plain: 'Mellan',
      file: 'Mellan_Dossier.html',
      image: 'thumbs/mellan.jpg',
      eyebrow: 'Ridgeborne Human &middot; Ranger (Beastbound)',
      subtitle: 'Ridgeborne Human &mdash; Ranger with Wivek the Hawk &mdash; Left Ygva a River-Stone',
      system: 'Daggerheart',
      campaign: 'Caul',
      role: 'support',
      campaignStatus: 'unplayed'
    },"""

SECRETARY_NOMOS = """{
      name: 'Secretary <span class="given">Nomos</span>',
      plain: 'Secretary Nomos',
      file: 'Secretary_Nomos_Dossier.html',
      image: 'thumbs/secretary_nomos.jpg',
      eyebrow: 'Memonek &middot; Troubadour (Auteur)',
      subtitle: 'Communications &amp; Support &mdash; Debuffer &amp; Morale &mdash; Zenith',
      system: 'Draw Steel',
      campaign: 'Zenith',
      role: 'support',
      campaignStatus: 'active'
    },"""

src = insert_after(src, 'Eryndil_Dossier.html',  EXECUTOR_VELLPRYTE)  # Exe after Ery, before Flare
src = insert_after(src, 'Malek_Dossier.html',    MELLAN)              # Me after Ma, before Mo
src = insert_after(src, 'Sarru_Dossier.html',    SECRETARY_NOMOS)     # Se after Sa, before So

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = [
    ('Eryndil',    'Eryndil_Dossier'),
    ('Vellpryte',  'Executor_Vellpryte'),
    ('Flare',      'Flare_Dossier'),
    ('Malek',      'Malek_Dossier'),
    ('Mellan',     'Mellan_Dossier'),
    ('Morten',     'Morten_Bergesen'),
    ('Sarru',      'Sarru_Dossier'),
    ('Sec. Nomos', 'Secretary_Nomos'),
    ('Solving',    'Solving_Epicurusson'),
]
for label, key in check:
    pos = src2.index(f"file: '{key}")
    name_pos = src2.rindex('name:', 0, pos)
    name_end = src2.index('\n', name_pos)
    print(f"  {label:12s}: {src2[name_pos:name_end].strip()[:70]}")

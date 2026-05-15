import pathlib

p = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier\index.html')
src = p.read_text(encoding='utf-8')

def insert_after(src, anchor_file, *new_entries):
    """Insert one or more entries after the entry whose file: matches anchor_file."""
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    block = ''.join('\n    ' + e.lstrip() for e in new_entries)
    return src[:insert_at] + block + src[insert_at:]

EIRA = """{
      name: '<span class="given">Eira</span> of Bree',
      plain: 'Eira of Bree',
      file: 'Eira_Dossier.html',
      image: 'thumbs/eira.jpg',
      eyebrow: 'Men of Bree &middot; Treasure Hunter',
      subtitle: 'Of the Silver Lily &middot; Treasure Hunter &middot; Knew Brandor and Orlec',
      system: 'The One Ring 2e',
      campaign: 'The Angle',
      role: 'support',
      campaignStatus: 'hiatus'
    },"""

EORLAS = """{
      name: '<span class="given">Eorlas</span> the Wandering Herbalist',
      plain: 'Eorlas the Wandering Herbalist',
      file: 'Eorlas_Dossier.html',
      image: 'thumbs/eorlas.jpg',
      eyebrow: 'Bardings &middot; Warden',
      subtitle: 'Wanderer Met in Mirkwood &middot; Bearer of the Message to Elenna',
      system: 'The One Ring 2e',
      campaign: 'The Angle',
      role: 'support',
      campaignStatus: 'hiatus'
    },"""

FLARE = """{
      name: '<span class="given">Flare</span>',
      plain: 'Flare',
      file: 'Flare_Dossier.html',
      image: 'thumbs/flare.jpg',
      eyebrow: 'Mutant &middot; Student',
      subtitle: 'Taylor Crenshaw &mdash; Age 15 &mdash; Direct Action for Mutant Liberation',
      system: 'Marvel Multiverse RPG',
      campaign: 'X-FRONT',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

GARIN = """{
      name: '<span class="given">Garin</span> of Rohan',
      plain: 'Garin of Rohan',
      file: 'Garin_Dossier.html',
      image: 'thumbs/garin.jpg',
      eyebrow: 'Riders of Rohan &middot; Edoras',
      subtitle: 'Rider Met on the Plains &middot; Whose Mare Carried Celenneth Home',
      system: 'The One Ring 2e',
      campaign: 'The Angle',
      role: 'support',
      campaignStatus: 'hiatus'
    },"""

KELUN = """{
      name: '<span class="given">Kelun</span>',
      plain: 'Kelun',
      file: 'Kelun_Dossier.html',
      image: 'thumbs/kelun.jpg',
      eyebrow: 'Reborne Clank &middot; Sorcerer (Primal Origin)',
      subtitle: 'Reborne Clank &mdash; Sorcerer of Primal Origin &mdash; Age of Umbra',
      system: 'Daggerheart',
      campaign: 'Caul',
      role: 'support',
      campaignStatus: 'unplayed'
    },"""

TIPHAINE = """{
      name: '<span class="given">Tiphaine</span> merc&#39;h Riwall',
      plain: 'Tiphaine merc\\'h Riwall',
      file: 'tiphaine_dossier.html',
      image: 'thumbs/tiphaine.jpg',
      eyebrow: 'Squire &middot; Salisbury &middot; A.D. 465',
      subtitle: 'of the Three Oaks &mdash; Daughter of a Slain Knight &mdash; Wolves of Vagon',
      system: 'Pendragon',
      campaign: 'Salisbury',
      role: 'support',
      campaignStatus: 'active'
    },"""

src = insert_after(src, 'Damrod_Dossier.html', EIRA, EORLAS)   # Eira + Eorlas before Erasmus
src = insert_after(src, 'Eryndil_Dossier.html', FLARE, GARIN)  # Flare + Garin before Half-Life
src = insert_after(src, 'Hallas_Dossier.html', KELUN)           # Kelun before Khalida
src = insert_after(src, 'Tepshe_Dossier.html', TIPHAINE)        # Tiphaine before Torsten

p.write_text(src, encoding='utf-8')
print('Done. Verifying order...')

src2 = p.read_text(encoding='utf-8')
check = ['Damrod_Dossier','Eira_Dossier','Eorlas_Dossier','Erasmus_Dossier',
         'Eryndil_Dossier','Flare_Dossier','Garin_Dossier','Half-Life_Dossier',
         'Hallas_Dossier','Kelun_Dossier','Khalida_Dossier',
         'Tepshe_Dossier','Tiphaine','Torsten_Fabricatus']
for key in check:
    pos = src2.index(f"file: '{key}")
    name_pos = src2.rindex('name:', 0, pos)
    name_end = src2.index('\n', name_pos)
    print(src2[name_pos:name_end].strip()[:70])

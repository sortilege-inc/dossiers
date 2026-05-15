import pathlib

p = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier\index.html')
src = p.read_text(encoding='utf-8')

def insert_after_entry(src, anchor_file, new_entry):
    pos = src.index(f"file: '{anchor_file}'")
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

HALF_LIFE = """{
      name: '<span class="given">Half-Life</span>',
      plain: 'Half-Life',
      file: 'Half-Life_Dossier.html',
      image: 'thumbs/half-life.jpg',
      eyebrow: 'Mutant &middot; Criminal &middot; X-FRONT',
      subtitle: 'Cody Kennedy &mdash; Age 18 &mdash; Direct Action for Mutant Liberation',
      system: 'Marvel Multiverse RPG',
      campaign: 'X-FRONT',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

PHOTIOS = """{
      name: '<span class="given">Photios</span> Chrysoloras',
      plain: 'Photios Chrysoloras',
      file: 'Photios_Chrysoloras_Dossier.html',
      image: 'thumbs/photios.jpg',
      eyebrow: 'House Jerbiton &middot; Mouseion Prometheia &middot; Refugee',
      subtitle: 'The Cartographer &mdash; Refugee of the Second Rome &mdash; Eyes of Gold',
      system: 'Ars Magica 5e',
      campaign: 'Solving\\'s Mystery',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

STASIS = """{
      name: '<span class="given">Stasis</span>',
      plain: 'Stasis',
      file: 'Stasis_Dossier.html',
      image: 'thumbs/stasis.jpg',
      eyebrow: 'Mutant &middot; Student &middot; X-FRONT',
      subtitle: 'Hermes Montoya &mdash; Age 14 &mdash; Direct Action for Mutant Liberation',
      system: 'Marvel Multiverse RPG',
      campaign: 'X-FRONT',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

TORSTEN = """{
      name: '<span class="given">Torsten</span> Fabricatus',
      plain: 'Torsten Fabricatus',
      file: 'Torsten_Fabricatus_Dossier.html',
      image: 'thumbs/torsten.jpg',
      eyebrow: 'House Verditius &middot; Maritime Enchantment &middot; Bergen Shipyards',
      subtitle: 'The Maker &mdash; Maritime Enchanter &mdash; The Right Way or Not at All',
      system: 'Ars Magica 5e',
      campaign: 'Solving\\'s Mystery',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

# Insertions (each uses the current state of src, so order matters)
src = insert_after_entry(src, 'Erasmus_Dossier.html', HALF_LIFE)   # Half-Life before Hallas
src = insert_after_entry(src, 'Morten_Bergesen_Dossier.html', PHOTIOS)  # Photios before Rhys
src = insert_after_entry(src, 'Solving_Epicurusson_Dossier.html', STASIS)  # Stasis before Taboo
src = insert_after_entry(src, 'Tepshe_Dossier.html', TORSTEN)      # Torsten before Valerian

# Add image to Hallas entry (currently has no image field)
src = src.replace(
    "file: 'Hallas_Dossier.html',\n      eyebrow:",
    "file: 'Hallas_Dossier.html',\n      image: 'thumbs/hallas.jpg',\n      eyebrow:"
)

p.write_text(src, encoding='utf-8')
print('Done. Verifying...')

src2 = p.read_text(encoding='utf-8')
for char, key in [('Erasmus','Erasmus_Dossier'),('Half-Life','Half-Life_Dossier'),
                  ('Hallas','Hallas_Dossier'),('Morten','Morten_Bergesen'),
                  ('Photios','Photios_Chrysoloras'),('Solving','Solving_Epicurusson'),
                  ('Stasis','Stasis_Dossier'),('Tepshe','Tepshe_Dossier'),('Torsten','Torsten_Fabricatus')]:
    pos = src2.index(f"file: '{key}")
    camp = src2.index('campaign:', pos)
    end = src2.index('}', camp)
    role_pos = src2.index('role:', pos)
    role_end = src2.index('\n', role_pos)
    print(f"{char}: {src2[camp:camp+30].strip()!r}  {src2[role_pos:role_end].strip()!r}")

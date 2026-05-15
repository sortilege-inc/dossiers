import pathlib

p = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier\index.html')
src = p.read_text(encoding='utf-8')

def insert_after_entry(src, anchor_file, new_entry):
    """Insert new_entry immediately after the closing } of the entry whose file: matches anchor_file."""
    pos = src.index(f"file: '{anchor_file}'")
    # Find the },\n    { that closes this entry and opens the next
    close = src.index('\n    },\n    {', pos)
    insert_at = close + len('\n    },')
    return src[:insert_at] + '\n    ' + new_entry.lstrip() + src[insert_at:]

ASTRID = """{
      name: '<span class="given">Astrid</span> Gr&aacute;sula',
      plain: 'Astrid Grásula',
      file: 'Astrid_Grásula_Dossier.html',
      image: 'thumbs/astrid.jpg',
      eyebrow: 'House Bj&ouml;rnaer &middot; Clan Ilfetu &middot; Heartbeast: Gannet',
      subtitle: 'The Gannet &mdash; Newly Gauntleted &mdash; Seeker of the Ilfetu Mysteries',
      system: 'Ars Magica 5e',
      campaign: 'Solving\\'s Mystery',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

HALLAS = """{
      name: '<span class="given">Hallas</span> of the North',
      plain: 'Hallas of the North',
      file: 'Hallas_Dossier.html',
      eyebrow: 'Rangers of the North &middot; Champion',
      subtitle: 'Ranger of the D&uacute;nedain &middot; Paired with Damrod &middot; Namesake of Celenneth&#39;s Son',
      system: 'The One Ring 2e',
      campaign: 'The Angle',
      role: 'support',
      campaignStatus: 'hiatus'
    },"""

TABOO = """{
      name: '<span class="given">Taboo</span>',
      plain: 'Taboo',
      file: 'Taboo_Dossier.html',
      image: 'thumbs/taboo.jpg',
      eyebrow: 'Mutant &middot; Adventurer &middot; X-FRONT',
      subtitle: 'Tabitha Fanning &mdash; Co-founder of X-FRONT &mdash; Age 17',
      system: 'Marvel Multiverse RPG',
      campaign: 'X-FRONT',
      role: 'pre-gen',
      campaignStatus: 'unplayed'
    },"""

# Insert Astrid after Antagones
src = insert_after_entry(src, 'Antagones_Dossier.html', ASTRID)
# Insert Hallas after Erasmus
src = insert_after_entry(src, 'Erasmus_Dossier.html', HALLAS)
# Insert Taboo after Solving
src = insert_after_entry(src, 'Solving_Epicurusson_Dossier.html', TABOO)

# Fix Tank: hiatus -> unplayed
src = src.replace(
    "file: 'Tank_Dossier.html'",
    "file: 'Tank_Dossier.html'"  # no-op anchor; do the status fix below
)
tank_pos = src.index("file: 'Tank_Dossier.html'")
status_pos = src.index("campaignStatus:", tank_pos)
end = src.index("'", status_pos + len("campaignStatus: '"))
src = src[:status_pos] + "campaignStatus: 'unplayed'" + src[end + 1:]

p.write_text(src, encoding='utf-8')
print('Done. Verifying...')

src2 = p.read_text(encoding='utf-8')
for char, key in [('Antagones','Antagones_Dossier'),('Astrid','Astrid_Gr'),
                  ('Erasmus','Erasmus_Dossier'),('Hallas','Hallas_Dossier'),
                  ('Solving','Solving_Epicurusson'),('Taboo','Taboo_Dossier'),
                  ('Tank','Tank_Dossier')]:
    pos = src2.index(f"file: '{key}")
    camp = src2.index('campaign:', pos)
    end = src2.index('}', camp)
    print(f"{char}: {src2[camp:end].strip()}")
    print()

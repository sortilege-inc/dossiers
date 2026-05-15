import pathlib

p = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier\index.html')
src = p.read_text(encoding='utf-8')

ERYNDIL = """{
      name: '<span class="given">Eryndil</span> of Lindon',
      plain: 'Eryndil of Lindon',
      file: 'Eryndil_Dossier.html',
      image: 'thumbs/eryndil.jpg',
      eyebrow: 'Elves of Lindon &middot; Scholar',
      subtitle: 'Scholar of the Western Shores &middot; Bearer of C&iacute;rdan&#39;s Errand &middot; Bearer of the Adamant Relic',
      system: 'The One Ring 2e',
      campaign: 'The Angle',
      role: 'support',
      campaignStatus: 'hiatus'
    },"""

# Insert after Erasmus, before Half-Life
pos = src.index("file: 'Erasmus_Dossier.html'")
close = src.index('\n    },\n    {', pos)
insert_at = close + len('\n    },')
src = src[:insert_at] + '\n    ' + ERYNDIL.lstrip() + src[insert_at:]

p.write_text(src, encoding='utf-8')

# Verify
src2 = p.read_text(encoding='utf-8')
for key in ['Erasmus_Dossier', 'Eryndil_Dossier', 'Half-Life_Dossier']:
    pos = src2.index(f"file: '{key}'")
    name_pos = src2.rindex("name:", 0, pos)
    name_end = src2.index('\n', name_pos)
    print(src2[name_pos:name_end].strip())

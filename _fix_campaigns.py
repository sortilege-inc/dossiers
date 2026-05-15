import pathlib, re

p = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier\index.html')
src = p.read_text(encoding='utf-8')

def fix_entry(src, file_key, new_campaign=None, new_role=None):
    pos = src.index(f"file: '{file_key}")
    camp_pos = src.index('campaign:', pos)
    end_pos = src.index('\n    }', camp_pos)
    chunk = src[camp_pos:end_pos]

    if new_campaign:
        chunk = re.sub(r"campaign: '[^']+'", f"campaign: '{new_campaign}'", chunk)
    if new_role:
        chunk = re.sub(r"role: '[^']+'", f"role: '{new_role}'", chunk)

    return src[:camp_pos] + chunk + src[end_pos:]

# ð is U+00F0
sjoerseioer = 'Sj&oacute;rseiðr'
solvings = "Solving’s Mystery"  # curly apostrophe? No — use straight with JS escape
# In JS single-quoted strings the apostrophe must be escaped: Solving\'s Mystery
# but we're writing the literal HTML/JS text, so use the actual escape sequence
solvings = "Solving\\'s Mystery"

src = fix_entry(src, 'Valerian_de_Castellane', new_campaign=sjoerseioer)
src = fix_entry(src, 'Solving_Epicurusson',    new_campaign=solvings, new_role='pre-gen')
src = fix_entry(src, 'Erasmus_Dossier',        new_campaign=solvings, new_role='pre-gen')
src = fix_entry(src, 'Khalida_Dossier',        new_campaign=solvings, new_role='pre-gen')

p.write_text(src, encoding='utf-8')

# Verify
src2 = p.read_text(encoding='utf-8')
for char, key in [('Valerian','Valerian_de_Castellane'),('Solving','Solving_Epicurusson'),
                  ('Erasmus','Erasmus_Dossier'),('Khalida','Khalida_Dossier'),('Tank','Tank_Dossier')]:
    pos = src2.index(f"file: '{key}")
    camp_pos = src2.index('campaign:', pos)
    end_pos = src2.index('\n    }', camp_pos)
    print(f"{char}:")
    print(src2[camp_pos:end_pos])
    print()

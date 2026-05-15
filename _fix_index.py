import pathlib

p = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier\index.html')
src = p.read_text(encoding='utf-8')

# Find the Setsuna entry (now the only one) and cut from the , { before it to the ];
marker = "name: 'Doji <span"
pos = src.index(marker)

# Walk back to find the },\n    { that opens this object
obj_open = src.rindex('},', 0, pos)  # trailing comma of previous entry

# Find the ]; that closes the array, starting from the Setsuna position
array_close = src.index('\n  ];', pos)

# Replace: keep everything up to and including the previous entry's }
# (remove the trailing comma), then close the array
new_src = src[:obj_open + 1] + '\n  ];' + src[array_close + len('\n  ];'):]

p.write_text(new_src, encoding='utf-8')
print(f'Removed {array_close - obj_open} chars of old entries')

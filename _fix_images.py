"""
Fix all image issues:
  - Fix /mnt/user-data/uploads/ paths (4 files) + Tig extension
  - Enlarge portrait-frame widths in Solving's Mystery group + Valerian
  - Add portrait CSS + HTML to 7 dossiers that have no portrait yet
"""
import pathlib

base = pathlib.Path(r'C:\Users\jorda\Downloads\Sortilege\00. PC Dossier')

def patch(filename, *replacements):
    p = base / filename
    src = p.read_text(encoding='utf-8')
    for old, new in replacements:
        if old not in src:
            print(f'  !! anchor missing in {filename}: {repr(old[:70])}')
        else:
            src = src.replace(old, new, 1)
    p.write_text(src, encoding='utf-8')
    print(f'  {filename}')

# ── 1. Fix broken absolute paths ─────────────────────────────────────────────
print('--- Fix broken paths ---')

patch('Operator_Azimuth_Dossier.html',
    ('src="/mnt/user-data/uploads/Operator_Azimuth.jpeg"',
     'src="operator_azimuth.jpeg"'))

patch('Executor_Vellpryte_Dossier.html',
    ('src="/mnt/user-data/uploads/Executor_Vellpryte.jpeg"',
     'src="executor_vellpryte.jpeg"'))

patch('Protocol_Keshet_Dossier.html',
    ('src="/mnt/user-data/uploads/Protocol_Keshet.jpeg"',
     'src="protocol_keshet.jpeg"'))

patch('Secretary_Nomos_Dossier.html',
    ('src="/mnt/user-data/uploads/Secretary_Nomos.jpeg"',
     'src="secretary_nomos.jpeg"'))

patch('Tig_Dossier.html',
    ('src="tig.jpeg"', 'src="tig.png"'))

# ── 2. Enlarge portrait frames: Solving's Mystery + Valerian ─────────────────
print('\n--- Enlarge portrait frames (170->260px) ---')

# Multi-line format (6 files)
for fname, old_w in [
    ('Solving_Epicurusson_Dossier.html',  '175px'),
    ('Khalida_Dossier.html',              '170px'),
    ('Astrid_Grásula_Dossier.html',      '172px'),
    ('Erasmus_Dossier.html',              '168px'),
    ('Photios_Chrysoloras_Dossier.html',  '172px'),
    ('Valerian_de_Castellane_Dossier.html','170px'),
]:
    patch(fname,
        (f'    width: {old_w};\n  }}\n  .portrait-frame img {{',
          '    width: 260px;\n  }\n  .portrait-frame img {'))

# Single-line format (Torsten)
patch('Torsten_Fabricatus_Dossier.html',
    ('margin: 0 0 1.5rem 2.2rem; width: 172px; }',
     'margin: 0 0 1.5rem 2.2rem; width: 260px; }'))

# ── 3. Add portrait CSS + HTML to dossiers with no portrait ──────────────────
print('\n--- Add portraits to dossiers ---')

# ── AMOS (dark steel + gold-glow) ────────────────────────────────────────────
amos_css = """\
  /* Portrait */
  .portrait-wrap {
    text-align: center;
    margin: -0.5rem 0 2.5rem;
  }
  .portrait-wrap img {
    max-width: 360px;
    width: 100%;
    border: 1px solid var(--rule);
    box-shadow: 0 0 20px var(--gold-glow);
  }
"""
amos_html = """\
  <div class="portrait-wrap">
    <img src="amos.png" alt="A.M.O.S.">
  </div>
"""
patch('AMOS_Dossier.html',
    ('</style>', amos_css + '</style>'),
    ('  </header>\n\n  <div class="campaign-status">',
     '  </header>\n\n' + amos_html + '\n  <div class="campaign-status">'))

# ── Faletolu (seafoam + bone) ────────────────────────────────────────────────
fale_css = """\
  /* Portrait */
  .portrait-wrap {
    text-align: center;
    margin: 1.5rem 0 2.5rem;
  }
  .portrait-wrap img {
    max-width: 360px;
    width: 100%;
    border: 1px solid var(--rule);
    box-shadow: 0 4px 18px var(--shadow);
  }
"""
fale_html = """\
  <div class="portrait-wrap">
    <img src="faletolu.png" alt="Faletolu Faletolu">
  </div>
"""
patch('Faletolu_Faletolu_Dossier.html',
    ('</style>', fale_css + '</style>'),
    ('\n  <!-- BODY -->', '\n' + fale_html + '\n  <!-- BODY -->'))

# ── Tiphaine (vellum + gilt) ─────────────────────────────────────────────────
tiph_css = """\
  /* Portrait */
  .portrait-wrap {
    text-align: center;
    margin: 1.5rem 0 3rem;
  }
  .portrait-wrap img {
    max-width: 360px;
    width: 100%;
    border: 1px solid var(--rule);
    box-shadow: 0 2px 10px rgba(28,24,20,0.14);
  }
"""
tiph_html = """\
  <div class="portrait-wrap">
    <img src="tiphaine.png" alt="Tiphaine merc'h Riwall">
  </div>
"""
patch('tiphaine_dossier.html',
    ('</style>', tiph_css + '</style>'),
    ('  </header>\n\n  <nav class="toc">',
     '  </header>\n\n' + tiph_html + '\n  <nav class="toc">'))

# ── Kaia kW (zine/riso: bold ink border) ────────────────────────────────────
kaia_css = """\
  /* Portrait */
  .portrait-wrap {
    text-align: center;
    margin: 1.5rem 0 2.5rem;
  }
  .portrait-wrap img {
    max-width: 360px;
    width: 100%;
    border: 2px solid var(--ink);
    box-shadow: 4px 4px 0 var(--ink);
  }
"""
kaia_html = """\
  <div class="portrait-wrap">
    <img src="Kaia kW.png" alt="Kaia kW">
  </div>
"""
patch('Kaia_kW_Dossier.html',
    ('</style>', kaia_css + '</style>'),
    ('  </header>\n\n  <div class="source-note">',
     '  </header>\n\n' + kaia_html + '\n  <div class="source-note">'))

# ── Setsuna (paper + gold crane) ────────────────────────────────────────────
sets_css = """\
  /* Portrait */
  .portrait-wrap {
    text-align: center;
    margin: 1.5rem 0 2.5rem;
  }
  .portrait-wrap img {
    max-width: 360px;
    width: 100%;
    border: 2px solid var(--gold);
    box-shadow: 0 4px 16px rgba(31,29,26,0.12);
  }
"""
sets_html = """\
  <div class="portrait-wrap">
    <img src="doji_setsuna.png" alt="Doji Setsuna">
  </div>
"""
patch('setsuna_dossier.html',
    ('</style>', sets_css + '</style>'),
    ('  </header>\n\n  <nav class="toc">',
     '  </header>\n\n' + sets_html + '\n  <nav class="toc">'))

# ── Noel (paper + ink, 4-space indent inside .folder .paper) ────────────────
noel_css = """\
  /* Portrait */
  .portrait-wrap {
    text-align: center;
    margin: 1.5rem 0 2.5rem;
  }
  .portrait-wrap img {
    max-width: 360px;
    width: 100%;
    border: 1px solid var(--rule);
    box-shadow: 0 4px 16px rgba(26,22,18,0.2);
  }
"""
noel_html = """\
    <div class="portrait-wrap">
      <img src="noel.png" alt="Noel Grainger">
    </div>
"""
patch('Noel_Grainger_Dossier.html',
    ('</style>', noel_css + '</style>'),
    ('    </header>\n\n    <!-- ═══ I. CONCEPT',
     '    </header>\n\n' + noel_html + '\n    <!-- ═══ I. CONCEPT'))

# ── Bhimbahadur (vellum + crimson, two images side-by-side) ─────────────────
bhim_css = """\
  /* Portrait */
  .portrait-row {
    display: flex;
    gap: 2rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem 0 2.5rem;
  }
  .portrait-wrap {
    text-align: center;
    flex: 0 0 auto;
  }
  .portrait-wrap img {
    max-width: 280px;
    width: 100%;
    border: 1px solid var(--rule);
    box-shadow: 0 2px 12px rgba(26,18,12,0.2);
  }
  .portrait-caption {
    font-family: "IM Fell English SC", serif;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    color: var(--iron-faint);
    text-transform: uppercase;
    margin-top: 0.6rem;
  }
"""
bhim_html = """\
  <div class="portrait-row">
    <div class="portrait-wrap">
      <img src="bhim-service.png" alt="Bhimbahadur Pun in service dress">
      <div class="portrait-caption">Service Dress</div>
    </div>
    <div class="portrait-wrap">
      <img src="bhim-valet.png" alt="Bhimbahadur Pun as orderly">
      <div class="portrait-caption">As Orderly</div>
    </div>
  </div>
"""
patch('Bhimbahadur_Pun_Dossier.html',
    ('</style>', bhim_css + '</style>'),
    ('  </header>\n\n  <nav class="toc">',
     '  </header>\n\n' + bhim_html + '\n  <nav class="toc">'))

print('\nAll done.')

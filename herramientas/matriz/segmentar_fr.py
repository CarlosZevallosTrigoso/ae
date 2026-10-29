# Segmenta y corrige los párrafos franceses del OCR de Minuit, sección por sección.
# Uso: python3 -I segmentar_fr.py [N ...]   (sin argumentos, todas las secciones con frances/partes_sN.py)
# Cada frances/partes_sN.py define PARTS = {id: (frase inicial, frase final)} y FIX = [(texto OCR, corrección), ...].
# Escribe datos/fr_sN.json y avisa de correcciones que ya no se aplican y de caracteres sospechosos.
import json, re, sys, importlib.util
from pathlib import Path
AQUI = Path(__file__).resolve().parent; RAIZ = AQUI.parents[1]; DATOS = AQUI / 'datos'
d = json.load(open(DATOS / 'cap1_raw.json'))
paras = [d['fr'][str(i)] for i in range(1, len(d['fr']) + 1)]
stream = '\n\n'.join(p['txt'] for p in paras)
starts = []; acc = 0
for p in paras: starts.append((acc, p)); acc += len(p['txt']) + 2
def page_at(pos):
    for a, p in reversed(starts):
        if a <= pos:
            inner = re.findall(r'‹(\d+)›', p['txt'][:pos - a]); return int(inner[-1]) if inner else p['ini']
nums = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[-1]) for p in (AQUI / 'frances').glob('partes_s*.py'))
for n in nums:
    spec = importlib.util.spec_from_file_location(f'partes{n}', AQUI / 'frances' / f'partes_s{n}.py'); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
    print(f'— sección {n}')
    out = {}
    for k, (a, b) in M.PARTS.items():
        i = stream.index(a); j = stream.index(b, i) + len(b); s = stream[i:j]
        ini, fin = page_at(i), page_at(j - 1)
        s = s.replace('\n\n', ' ')
        s = re.sub(r'\s*<sup>\d+</sup>\s*', ' ', s)
        for x, y in M.FIX: s = s.replace(x, y)
        s = re.sub(r'\s+', ' ', s).strip()
        out[k] = dict(ini=ini, fin=fin, txt=s)
    json.dump(out, open(DATOS / f'fr_s{n}.json', 'w'), ensure_ascii=False, indent=1)
    for k, v in out.items():
        bad = set(re.findall(r'[^\w\s.,;:!?«»()\'’\-—–…*‹›†/<>"=]', v['txt']))
        sus = re.findall(r'\b\w*[0-9]\w*\b|\b[A-Z]\b(?! )|\w+\.\w+', re.sub(r'‹\d+›', '', v['txt']))
        print(k, v['ini'], v['fin'], len(v['txt'].split()), 'w | raros:', bad, '| sospechosos:', sus[:12])
    todo = ' '.join(v['txt'] for v in out.values())
    for x, y in M.FIX:
        if y not in todo: print('   corrección sin efecto:', x[:60])

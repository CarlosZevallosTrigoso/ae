# Extrae párrafos ES (Paidós) y FR (OCR Minuit) del capítulo I, con marcas de página.
# Uso: python3 -I extraer.py   (lee ../../capitulos/anti-edipo-cap1.md y ../../complementarios/AE_frances.md; escribe datos/cap1_raw.json)
import re, json, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent; RAIZ = AQUI.parents[1]; DATOS = AQUI / 'datos'
ES_FILE = RAIZ / 'capitulos' / 'anti-edipo-cap1.md'; FR_FILE = RAIZ / 'complementarios' / 'AE_frances.md'
DATOS.mkdir(exist_ok=True); OUT = DATOS / 'cap1_raw.json'

# ---------- Español ----------
t = open(ES_FILE).read()
t = re.sub(r'\n\[\^[^\]]+\]:.*', '', t)
page = None; sec = None; n = 0; es = {}
for line in t.split('\n'):
    m = re.match(r'### (\d)\.', line)
    anchors = re.findall(r'<!-- p\. (\d+) -->', line)
    if m:
        sec = int(m.group(1)); n = 0
    elif sec and line.strip() and not line.startswith('<!--') and not line.startswith('#') and line.strip() != '---':
        n += 1
        txt = re.sub(r'\[\^[^\]]+\]', '', line)                       # llamadas de nota
        txt = re.sub(r'\s*<!-- p\. (\d+) -->\s*', r' ‹\1› ', txt)      # marcas de página
        txt = re.sub(r'\s+', ' ', txt).strip()
        endp = int(anchors[-1]) if anchors else page
        es[f'{sec}.{n}'] = dict(ini=page, fin=endp, txt=txt)
    if anchors: page = int(anchors[-1])

# ---------- Francés ----------
L = open(FR_FILE).read().split('\n')[150:563]   # líneas del capítulo I en el OCR
pars = []; cur = None; page = 7
def flush():
    global cur
    if cur: pars.append(cur); cur = None
for l in L:
    s = l.strip()
    m = re.match(r'^\{(\d+)\}-+$', s)
    if m:
        page = int(m.group(1)) + 1
        if cur: cur['pend'] = page
        continue
    if not s:
        if cur: cur['gap'] = True
        continue
    if re.match(r'^#+\s*(L.?ANT|chapitre)', s, re.I): continue
    if re.match(r'^\d{1,3}$', s): continue
    if s.startswith('<sup>') or re.match(r'^\d{1,2}\.\s+[A-ZÉ]', s) or s.startswith('!['): continue
    if cur is None:
        cur = dict(ini=page, fin=page, txt=s, gap=False, pend=None); continue
    prev = cur['txt']
    ends = re.search(r'[.?!»…:]\s*(\d+\s*)?$', prev)
    low = re.match(r'^[a-zàâçéèêëîïôûùüÿœ,;(«\-]', s)
    if cur['gap'] and not (low or not ends):
        flush(); cur = dict(ini=page, fin=page, txt=s, gap=False, pend=None); continue
    sep = f' ‹{cur["pend"]}› ' if cur.get('pend') else ' '
    cur['txt'] = prev + sep + s; cur['fin'] = page; cur['gap'] = False; cur['pend'] = None
flush()
fr = {str(i+1): p for i, p in enumerate(pars)}
json.dump(dict(es=es, fr=fr), open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(es), 'ES;', len(fr), 'FR')

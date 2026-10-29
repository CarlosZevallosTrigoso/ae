# Verifica las citas de contenido/sN.py: cada «cita» seguida de (p. N) se busca en anti-edipo.md (Paidós)
# y cada «cita» seguida de (M N) en el francés segmentado; avisa si no aparece o si cae en otra página.
# Uso: python3 -I verificar.py [N ...]   (sin argumentos, todas las secciones)
# Limitación: compara con la PRIMERA aparición de la frase; una frase común que aparece antes en el libro
# da un falso aviso de página (p. ej. «tal vez», «répression»). Revisa esos avisos a mano.
import json, re, html, importlib.util, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent; RAIZ = AQUI.parents[1]; DATOS = AQUI / 'datos'
raw = json.load(open(DATOS / 'cap1_raw.json'))
fr1 = {}
for f in sorted(DATOS.glob('fr_s[1-9].json')): fr1.update(json.load(open(f)))
# texto ES completo con marcas
book = open(RAIZ / 'anti-edipo.md').read()
book = re.sub(r'\n\[\^[^\]]+\]:.*', '', book); book = re.sub(r'\[\^[^\]]+\]', '', book)
es_all = re.sub(r'\s*<!-- p\. (\d+) -->\s*', r' ‹\1› ', book)
es_all = es_all.replace('(el seno«la boca)', '(el seno—la boca)')
fr_all = ' '.join(f"‹{v['ini']}› " + v['txt'] for v in fr1.values()) + ' ' + ' '.join(f"‹{v['ini']}› " + v['txt'] for v in raw['fr'].values())
def norm(t):
    t = re.sub(r'<[^>]+>', '', t); t = html.unescape(t); t = t.replace('*', '')
    return re.sub(r'\s+', ' ', t).strip()
def strip_marks(t):
    # devuelve texto sin marcas y lista de (pos, page)
    out = []; pages = []; pg = None; i = 0
    for m in re.finditer(r'‹(\d+)›|.', t, re.S):
        if m.group(1): pg = int(m.group(1)); continue
        out.append(m.group(0)); pages.append(pg)
    return ''.join(out), pages
ES, ESP = strip_marks(norm(es_all)); FR, FRP = strip_marks(norm(fr_all))
ES = re.sub(r'\s+', ' ', ES)
nums = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[1:]) for p in (AQUI / 'contenido').glob('s[1-9].py'))
total = 0
for num in nums:
    spec = importlib.util.spec_from_file_location(f's{num}', AQUI / 'contenido' / f's{num}.py'); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    print(f'— sección {num}')
    blob = ''
    for p in s.PARRAFOS: blob += ' '.join(p.get(k, '') for k in ['hace', 'comentario', 'traduccion', 'lectura']) + ' '
    blob += s.SECCION['intro_html'] + s.SECCION['fuera_html']
    blob = norm(blob)
    # citas: «...» seguido (cerca) de (p. N) o (M N)
    bad = 0; n = 0
    for m in re.finditer(r'«((?:[^«»]|«[^«»]*»)+)»[^«(]{0,60}?\((p\.|M) (\d+)', blob):
        q, kind, page = m.group(1), m.group(2), int(m.group(3))
        q2 = re.sub(r'\s+', ' ', q).strip()
        T, P = (ES, ESP) if kind == 'p.' else (FR, FRP)
        T2 = re.sub(r'\s+', ' ', T)
        idx = T2.find(q2); n += 1
        if idx < 0:
            bad += 1; print('   NO ENCONTRADA', kind, page, '|', q2[:90]); continue
        p0, p1 = P[min(idx, len(P)-1)], P[min(idx+len(q2)-1, len(P)-1)]
        ok = p0 == page or p1 == page or (p0 and p1 and p0 <= page <= p1)
        if not ok: bad += 1; print('   PÁGINA', kind, page, 'real', p0, p1, '|', q2[:80])
    print('  ', n, 'citas revisadas;', bad, 'avisos')
    total += bad

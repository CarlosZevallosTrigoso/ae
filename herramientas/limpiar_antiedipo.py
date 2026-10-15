#!/usr/bin/env python3
"""Limpia la salida de marker-pdf de un capítulo de El Anti-Edipo para lectura online.

Uso: python3 -I limpiar_antiedipo.py entrada.md salida.md config.json

config.json (todas las claves son opcionales salvo title y book_offset):
{
  "title": "Capítulo II. Psicoanálisis y familiarismo: la sagrada familia",
  "book_offset": 55,              // página del libro que corresponde a la página 0 del PDF
  "no_hyphen_splits": [["tam","bién"]],   // palabras partidas entre páginas sin guion
  "fixes": [["corno ya","como ya"]],      // erratas en el cuerpo (texto exacto)
  "note_fixes": [["197.6)","1976)"]],     // erratas en las notas
  "replacements": [["texto viejo","texto nuevo"]]  // sustituciones libres antes de todo
}
"""
import re, sys, json, datetime

src, dst, cfg_path = sys.argv[1], sys.argv[2], sys.argv[3]
cfg = json.load(open(cfg_path, encoding='utf-8'))
t = open(src, encoding='utf-8').read()

m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
fm_old = m.group(1) if m else ''
t = t[m.end():] if m else t
for a, b in cfg.get('replacements', []):
    if a not in t:
        print('AVISO: replacement no encontrado:', a)
    t = t.replace(a, b)

# ---------- partir en páginas ----------
parts = re.split(r'^\{(\d+)\}-+\s*$', t, flags=re.M)
pages = []
for i in range(1, len(parts), 2):
    pages.append((int(parts[i]), [l.strip() for l in parts[i+1].split('\n') if l.strip()]))

OFFSET = cfg['book_offset']
TERMINAL = re.compile(r'[.!?»\)”]\s*$')

def terminated(s):
    if s.startswith('#') or re.fullmatch(r'[\\* \t]+', s):   # encabezados y separadores * * * cierran párrafo
        return True
    if s.endswith('-'):
        return False
    s = re.sub(r'(<sup>[^<]*</sup>|\[\^[a-z0-9]+\]|[*_]+|\s)+$', '', s)
    return bool(TERMINAL.search(s))

# ---------- separar cuerpo y notas ----------
NOTE_RE = re.compile(r'^<sup>(\\\*|\d{1,3})\.?\s*(«?)</sup>\*?\.?\s*(.*)$')
PLAIN_NOTE_RE = re.compile(r'^(\d{1,3})\.?\s+(\S.*)$')
body_pages, notes = [], []
ast_count = 0
open_body_terminated = True   # ¿el último párrafo de cuerpo pendiente está cerrado?
for num, lines in pages:
    body, page_has_notes = [], False
    prev_note_open = bool(notes) and not terminated(notes[-1][1])
    n_pre = None   # cuántas líneas de cuerpo preceden a la primera nota de la página
    expected = (int(notes[-1][0]) + 1) if notes and notes[-1][0].isdigit() else cfg.get('first_note', 1)
    notes_before = len(notes)
    for l in lines:
        if n_pre is None and (NOTE_RE.match(l) or (PLAIN_NOTE_RE.match(l) and int(PLAIN_NOTE_RE.match(l).group(1)) == expected)):
            n_pre = len(body)
        mm = NOTE_RE.match(l)
        pm = PLAIN_NOTE_RE.match(l)
        if mm:
            if mm.group(1) == r'\*':
                ast_count += 1; nid = 'ast' if ast_count == 1 else f'ast{ast_count}'
            else:
                nid = mm.group(1)
            txt = (mm.group(2) + mm.group(3)).strip()
            if txt.count('*') % 2 == 1 and not txt.startswith('*'):   # cursiva rota por el conversor
                txt = '*' + txt
            notes.append([nid, txt]); page_has_notes = True
            expected = int(nid) + 1 if nid.isdigit() else expected
            while True:   # notas pegadas en una misma línea
                g = re.search(r'\s(?:<sup>%d</sup>|%d\.?)\s+(?=[A-Z*«])' % (expected, expected), notes[-1][1])
                if not g:
                    break
                rest = notes[-1][1][g.end():].strip()
                notes[-1][1] = notes[-1][1][:g.start()]
                notes.append([str(expected), rest]); expected += 1
        elif pm and int(pm.group(1)) == expected and pm.group(2)[:1].isupper():
            notes.append([pm.group(1), pm.group(2).strip()]); page_has_notes = True
            expected += 1
        else:
            body.append(l)
    # continuación de una nota de la página anterior, colocada por el conversor
    # en la zona de notas (al final del cuerpo) o, si el cuerpo previo estaba
    # cerrado, al inicio de la página
    if n_pre is None:
        n_pre = len(body)
    cand = body[:n_pre]   # sólo el cuerpo anterior a las notas de esta página
    if cand and prev_note_open:
        if cand[-1][:1].islower() and (len(cand) > 1 or open_body_terminated):
            idx = len(cand) - 1
        elif cand[0][:1].islower() and open_body_terminated:
            idx = 0
        else:
            idx = None
        if idx is not None:
            j = notes_before - 1   # la nota abierta es la última registrada antes de esta página
            piece = body.pop(idx)
            notes[j][1] = (notes[j][1][:-1] + piece) if notes[j][1].endswith('-') else (notes[j][1] + ' ' + piece)
    if body:
        open_body_terminated = terminated(body[-1]) and not body[-1].endswith('-')
    body_pages.append((num, body))

# ---------- unir párrafos entre páginas ----------
SPLITS = {tuple(x) for x in cfg.get('no_hyphen_splits', [])}
out, open_para = [], None
for num, body in body_pages:
    anchor = f'<!-- p. {num + OFFSET} -->'
    if not body:
        continue
    first, joined = body[0], False
    if open_para is not None:
        a, b = open_para, first
        def after_word(a, b):
            w, _, rest = b.partition(' ')
            return a + w + ' ' + anchor + ' ' + rest
        la = re.sub(r'[^\wáéíóúñ]', '', a.split()[-1]); fb = re.sub(r'[^a-záéíóúñA-Z]', '', b.split()[0])
        if a.endswith('-'):
            open_para = after_word(a[:-1], b); joined = True
        elif (la, fb) in SPLITS:
            open_para = after_word(a, b); joined = True
        elif re.fullmatch(r'[\\* \t]+', b):
            out.append(open_para); open_para = None   # el separador nunca se pega al párrafo anterior
        elif b[:1].islower() or b[:1] in '*_' and b[1:2].islower() or not terminated(a):
            open_para = a + ' ' + anchor + ' ' + b; joined = True
        else:
            out.append(open_para); open_para = None
    rest = body[1:] if joined else body
    if not joined:
        out.append(anchor)
    for l in rest:
        if open_para is not None:
            out.append(open_para)
        open_para = l
if open_para is not None:
    out.append(open_para)
text = '\n\n'.join(out)

# ---------- limpiezas de superficie ----------
text = re.sub(r'!\[\]\([^)]*\)', '<!-- imagen en el original, no incluida -->', text)
# títulos consecutivos al inicio → un solo encabezado configurado
text = re.sub(r'^(## [^\n]+\n\n)+', '', text, count=1, flags=re.M)
text = re.sub(r'(<!-- p\. \d+ -->)\n\n(<!-- p\. \d+ -->)', r'\1\n\n\2', text)
text = text.replace('<!-- p. %d -->' % (OFFSET + cfg.get('title_page', 1)),
                    '<!-- p. %d -->\n\n# %s' % (OFFSET + cfg.get('title_page', 1), cfg['title']), 1)
text = re.sub(r'^[\\* \t]*\\?\*[\\* \t]*$', '* * *', text, flags=re.M)
# llamadas a nota
ast_seen = [0]
def ast_sub(_):
    ast_seen[0] += 1
    return '[^ast]' if ast_seen[0] == 1 else f'[^ast{ast_seen[0]}]'
text = re.sub(r'<sup>(\d{1,3})</sup>\s*\.', r'[^\1].', text)
text = re.sub(r'<sup>(\d{1,3})</sup>', r'[^\1]', text)
text = re.sub(r'<sup>\\\*</sup>', ast_sub, text)
text = re.sub(r'(?<=[a-záéíóúñA-Z»\)*…])(\d{1,3})(?=[.,;:])', r'[^\1]', text)
text = re.sub(r'(?<=\.\.\.)(\d{1,3})(?=[.,;:])', r'[^\1]', text)
text = re.sub(r'\\\*\s*\.', lambda m: ast_sub(m) + '.', text)
# comillas corruptas
def fix_quotes(par):
    if '―' not in par and '‖' not in par:
        return par
    res, depth = [], 0
    for ch in par:
        if ch == '«': depth += 1; res.append(ch)
        elif ch == '»': depth -= 1; res.append(ch)
        elif ch == '―': res.append('“' if depth > 0 else '«')
        elif ch == '‖': res.append('”' if depth > 0 else '»')
        else: res.append(ch)
    return ''.join(res)
text = '\n\n'.join(fix_quotes(p) for p in text.split('\n\n'))
text = re.sub(r' +([.,;:])', r'\1', text)
text = re.sub(r'[ \t]+$', '', text, flags=re.M)

# erratas: se aplican al cuerpo y a las notas por igual
for a, b in cfg.get('fixes', []) + cfg.get('note_fixes', []):
    hits = text.count(a) + sum(txt.count(a) for _, txt in notes)
    if hits == 0:
        print('AVISO: fix no encontrado:', a)
    text = text.replace(a, b)
    notes = [[nid, txt.replace(a, b)] for nid, txt in notes]

# ---------- comprobaciones ----------
calls = re.findall(r'\[\^([a-z0-9]+)\]', text)
defs = [nid for nid, _ in notes]
for nid in sorted(set(calls) | set(defs), key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else 0, x)):
    if calls.count(nid) != 1 or defs.count(nid) != 1:
        print(f'AVISO: nota {nid}: {calls.count(nid)} llamadas, {defs.count(nid)} definiciones')

note_block = '\n\n'.join(f'[^{nid}]: {txt}' for nid, txt in notes)
src_name = re.search(r'^source:\s*(.*)$', fm_old, re.M)
fm_new = f"""---
title: "El Anti-Edipo — {cfg['title']}"
author: Gilles Deleuze y Félix Guattari
translator: Francisco Monge
source: {src_name.group(1) if src_name else ''}
tanda: anti
date: '{datetime.date.today().isoformat()}'
paginas: {len(pages)}
paginacion: 'anclas <!-- p. N --> con la página del libro inferida del nombre del archivo (p. {OFFSET} = página 0 del PDF)'
notas: al final del archivo, notas al pie de Markdown
tipo: digital
conversor: marker-pdf 1.10.2 + limpieza por script
lang: es
---
"""
open(dst, 'w', encoding='utf-8').write(fm_new + '\n' + text + '\n\n---\n\n' + note_block + '\n')
print('páginas:', len(pages), 'notas:', len(notes), 'párrafos:', text.count('\n\n') + 1)

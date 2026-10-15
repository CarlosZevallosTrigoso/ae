#!/usr/bin/env python3
"""Inserta los títulos de sección del índice (secciones.json) en los capítulos limpios:
sustituye el separador * * * de cada sección por '### n. Título'; si el separador falta,
coloca el título al inicio de la página en que el índice sitúa la sección."""
import json, re, sys
S = json.load(open('secciones.json', encoding='utf-8'))
for cap, secs in S.items():
    f = f'anti-edipo-{cap}.md'
    t = open(f, encoding='utf-8').read()
    body, sep, notes = t.rpartition('\n\n---\n\n')
    if re.search(r'^### \d+\. ', body, flags=re.M):
        print(cap, 'ya tiene secciones; omitido'); continue
    def pos(p):
        m = re.search(r'<!-- p\. %d -->' % p, body); return m.start() if m else None
    for n, title, page in secs:
        head = f'### {n}. {title}'
        if n == 1:   # primera sección: tras el ancla de su página, que es línea propia
            body = body.replace(f'<!-- p. {page} -->\n\n', f'<!-- p. {page} -->\n\n{head}\n\n', 1); continue
        a = pos(page - 1) if pos(page - 1) is not None else pos(page)
        b = pos(page + 1) or pos(page + 2) or len(body)
        seps = list(re.finditer(r'\n\n\* \* \*\n\n', body[a:b]))
        if len(seps) == 1:
            s = seps[0]
            body = body[:a + s.start()] + f'\n\n{head}\n\n' + body[a + s.end():]
        elif len(seps) == 0:   # separador perdido por el conversor: el índice da la página de inicio
            i = pos(page)
            body = body[:i] + f'<!-- p. {page} -->\n\n{head}\n\n' + body[i + len(f'<!-- p. {page} -->\n\n'):]
            print(f'AVISO {cap} §{n}: sin separador; título insertado al inicio de la p. {page}')
        else:
            print(f'AVISO {cap} §{n}: {len(seps)} separadores en la ventana; no tocado'); continue
    rest = body.count('\n\n* * *\n\n')
    if rest: print(f'AVISO {cap}: quedan {rest} separadores sin título')
    open(f, 'w', encoding='utf-8').write(body + sep + notes)
    print(cap, 'secciones:', len(re.findall(r'^### ', body, flags=re.M)))

#!/usr/bin/env python3
"""Une los capítulos limpios en ../anti-edipo.md con una sola serie de notas (prefijo por capítulo)."""
import re, datetime, collections
parts=[('1','../capitulos/anti-edipo-cap1.md'),('2','../capitulos/anti-edipo-cap2.md'),('3','../capitulos/anti-edipo-cap3.md'),('4','../capitulos/anti-edipo-cap4.md'),('ap','../capitulos/anti-edipo-apendice.md')]
bodies=[]; notes=[]
for pre,f in parts:
    t=open(f,encoding='utf-8').read(); t=re.sub(r'^---\n.*?\n---\n','',t,flags=re.S)
    body,_,nb=t.rpartition('\n\n---\n\n')
    body=re.sub(r'\[\^([a-z0-9]+)\]', lambda m: f'[^{pre}-{m.group(1)}]', body)
    nb=re.sub(r'^\[\^([a-z0-9]+)\]:', lambda m: f'[^{pre}-{m.group(1)}]:', nb, flags=re.M)
    body=re.sub(r'^## ', '### ', body, flags=re.M); body=re.sub(r'^# ', '## ', body, flags=re.M)
    body=re.sub(r'^## Capítulo primero\. ', '## Capítulo I. ', body, flags=re.M); body=re.sub(r'^## Capítulo 3\. ', '## Capítulo III. ', body, flags=re.M)
    bodies.append(body.strip()); notes.append(nb.strip())
fm=f"""---
title: "El Anti-Edipo. Capitalismo y esquizofrenia"
author: Gilles Deleuze y Félix Guattari
translator: Francisco Monge
edition: Paidós (pp. 8-413 de la edición castellana)
date: '{datetime.date.today().isoformat()}'
paginacion: 'anclas <!-- p. N --> con la página del libro, cotejadas con el índice de la edición'
secciones: 'títulos de sección tomados del índice de la edición (pp. 423-428); en II.8 y II.9 el separador faltaba en el escaneo y el título va al inicio de la página que da el índice'
notas: al final del documento; el prefijo indica el capítulo (1-, 2-, 3-, 4-, ap-)
lacunas: 'p. 292 ausente en la fuente (capturada como imagen por el conversor)'
lang: es
---

# El Anti-Edipo

"""
out=fm+'\n\n'.join(bodies)+'\n\n---\n\n## Notas\n\n'+'\n\n'.join(notes)+'\n'
open('../anti-edipo.md','w',encoding='utf-8').write(out)
calls=collections.Counter(re.findall(r'\[\^([a-z0-9-]+)\](?!:)',out)); defs=collections.Counter(re.findall(r'^\[\^([a-z0-9-]+)\]:',out,flags=re.M))
bad=[k for k in set(calls)|set(defs) if calls[k]!=1 or defs[k]!=1]
print('capítulos',len(re.findall(r'^## ',out,flags=re.M)),'secciones',len(re.findall(r'^### ',out,flags=re.M)),'notas',len(defs),'problemas',bad)

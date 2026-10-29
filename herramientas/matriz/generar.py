# Genera matriz.html: matriz de lectura en voz alta del capítulo I, con el estilo de explicacion.html.
# Uso: python3 -I generar.py [salida.html]   (por defecto ../../matriz.html)
# Lee datos/cap1_raw.json, datos/fr_sN.json y contenido/sN.py.
import json, re, html, sys, importlib.util
from pathlib import Path
AQUI = Path(__file__).resolve().parent; RAIZ = AQUI.parents[1]; DATOS = AQUI / 'datos'
RAW = DATOS / 'cap1_raw.json'
OUT = sys.argv[1] if len(sys.argv) > 1 else RAIZ / 'matriz.html'

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

import glob
MODS = {int(f.stem[1:]): load(f, 'm' + f.stem[1:]) for f in sorted((AQUI / 'contenido').glob('s[1-9].py'))}
es = json.load(open(RAW))['es']
fr = {}
for f in sorted(DATOS.glob('fr_s[1-9].json')): fr.update(json.load(open(f)))
ES_FIX = [('(el seno«la boca)', '(el seno—la boca)'),
          ('La carencia de un contra-efecto del deseo', 'La carencia [es] un contra-efecto del deseo'),
          ('recaiga es el gran miedo', 'recaiga [en] el gran miedo'),
          ('del inconsciente como oído', 'del inconsciente como [ciclo]'),
          ('a la palabra: palabra: usted', 'a la palabra: usted')]

def md(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', t)

def pg_es(n):
    return f'<a class="pg" href="index.html#p-{n}" target="ae-lector" title="Abrir el lector en la p. {n}">p.&nbsp;{n}</a>'

def marks(t, kind):
    if kind == 'es':
        return re.sub(r'‹(\d+)›', lambda m: pg_es(m.group(1)), t)
    return re.sub(r'‹(\d+)›', r'<span class="pg" title="Minuit, p. \1">M&nbsp;\1</span>', t)

# páginas de Paidós en las interpretaciones → enlace al lector; no «PDF p.», no «M N»
RE_PAG = re.compile(r'(?<!PDF )(?<!PDF pp\. )\b(pp?)\. (\d{1,3})((?:–\d{1,3})?)')
def enlazar(h):
    def rep(m):
        n = int(m.group(2))
        if n < 8 or n > 413: return m.group(0)
        return f'<a class="pag" href="index.html#p-{n}" target="ae-lector" title="Abrir el lector en la p. {n}">{m.group(0)}</a>'
    # no tocar dentro de etiquetas
    partes = re.split(r'(<[^>]+>)', h)
    return ''.join(p if p.startswith('<') else RE_PAG.sub(rep, p) for p in partes)

def verso(t, lang=None, pre=''):
    l = f' lang="{lang}"' if lang else ''
    return f'<span class="verso verso-ini">{pre}<em{l}>{t}</em></span>'

def recortar(t, spans, ini):
    """Fragmento de un párrafo: piezas entre (frase inicial, frase final), unidas por […].
    Devuelve el texto y las páginas inicial y final; si una omisión salta de página, la marca."""
    def pag(pos):
        m = re.findall(r'‹(\d+)›', t[:pos]); return int(m[-1]) if m else ini
    piezas = []; p0 = p1 = None; desde = 0
    for a, b in spans:
        i = t.index(a, desde); j = t.index(b, i) + len(b); desde = j
        pi, pj = pag(i), pag(j)
        pieza = t[i:j].strip()
        if p1 is not None and pi != p1: pieza = f'‹{pi}› ' + pieza
        piezas.append(pieza); p0 = pi if p0 is None else p0; p1 = pj
    return ' […] '.join(piezas), p0, p1

def omision(h):
    return h.replace(' […] ', ' <span class="omite" title="Corte dentro del párrafo">[…]</span> ')

def es_text(p):
    pid = p['id']; t = es[pid]['txt']; ini, fin = es[pid]['ini'], es[pid]['fin']
    if pid == '2.1':  # Paidós parte este párrafo en dos por el salto de página (§2.1 y §2.2)
        t = t + ' ‹18› ' + es['2.2']['txt']; fin = es['2.2']['fin']
    for a, b in ES_FIX: t = t.replace(a, b)
    frag = p.get('frag_es')
    if frag: t, ini, fin = recortar(t, frag, ini)
    body = omision(marks(md(t), 'es'))
    versos = not frag or p.get('versos')
    if versos and pid == '2.9':  # versos de Artaud (p. 23), que Paidós imprime como párrafos aparte
        v = md(es['2.7']['txt'].lstrip('> ').strip('*')) + '<br>' + md(es['2.8']['txt'].lstrip('> ').strip('*').replace('[^ast]', ''))
        body = verso(v, 'fr', '') .replace('</em></span>', '</em> <span class="aclara">en francés en Paidós</span></span>') + body
    if versos and pid == '6.9':  # línea de Artaud (p. 53), que Paidós imprime en francés como intertítulo
        v = md(es['6.8']['txt'].strip().strip('*'))
        body = verso(v, 'fr', '').replace('</em></span>', '</em> <span class="aclara">en francés en Paidós</span></span>') + body
    if versos and pid == '1.3':
        verse = md(es['1.4']['txt'].strip('*'))
        body += f'<span class="verso">{pg_es(13)} <em lang="fr">{verse}</em> <span class="aclara">en francés en Paidós</span></span>'
    return body, ini, fin

def fr_text(p):
    pid = p['id']; t = fr[pid]['txt']; verse = None; ini, fin = fr[pid]['ini'], fr[pid]['fin']
    frag = p.get('frag_fr')
    versos = not frag or p.get('versos')
    if versos and pid == '1.3':
        i = t.index('Le corps sous la peau'); t, verse = t[:i].rstrip(), t[i:]
    if frag: t, ini, fin = recortar(t, frag, ini)
    t = re.sub(r' ([:;?!»])', '\u00a0\\1', t.replace('« ', '«\u00a0'))   # sin cortes de línea junto a las comillas francesas
    body = omision(marks(md(t), 'fr')).replace('†', '<sup class="rec" title="Orden de palabras reconstruido: el OCR lo mezcló">†</sup>')
    if verse: body += '<span class="verso"><em>' + marks(md(verse), 'fr') + '</em></span>'
    if versos and pid == '2.9':
        body = verso(md(fr['2.7']['txt']).replace(' / ', '<br>')) + body
    if versos and pid == '6.9':
        body = verso('Ja na pas à papa-mama') + body
    return body, ini, fin

def rango(a, b, pre=True):
    if a == b: return f'p. {a}' if pre else f'{a}'
    return f'pp. {a}–{b}' if pre else f'{a}–{b}'

SECCIONES = [
    (1, 'La producción deseante', 'La production désirante', '11–17', '7–15'),
    (2, 'El cuerpo sin órganos', 'Le corps sans organes', '17–24', '15–22'),
    (3, 'El sujeto y el goce', 'Le sujet et la jouissance', '24–29', '22–29'),
    (4, 'Psiquiatría materialista', 'Psychiatrie matérialiste', '29–42', '29–43'),
    (5, 'Las máquinas', 'Les machines', '42–47', '43–50'),
    (6, 'El todo y las partes', 'Le tout et les parties', '47–54', '50–59'),
]
DATA = MODS

def marca_mia(h):
    return h.replace('<em>Mi lectura,</em>', '<em class="marca">Mi lectura</em>').replace('<em>Mi lectura.</em>', '<em class="marca">Mi lectura</em>') \
            .replace('<em>Ejemplo forzado:</em>', '<em class="marca">Ejemplo forzado</em>').replace('<em>Mi lectura:</em>', '<em class="marca">Mi lectura</em>')

def sin_rotulo(h):
    # el bloque ya se titula «Mi lectura»: se quita el rótulo repetido al inicio
    h = h.replace('<p><em>Mi lectura,</em> con confianza', '<p>Con confianza').replace('<p><em>Mi lectura.</em> ', '<p>')
    return h

def parrafo(p):
    pid = p['id']; oe = ', '.join(map(str, p['oe']))
    star = '<span class="star" title="Núcleo: leer si solo hay tiempo para pocos">★</span>' if p['nucleo'] else ''
    trad = f'<section class="ib ib-trad"><h4>Traducción</h4>{enlazar(p["traduccion"])}</section>' if p.get('traduccion') else ''
    es_h, e0, e1 = es_text(p); fr_h, m0, m1 = fr_text(p)
    completo = ''
    if p.get('frag_es'):
        es_pp = p['es_pp'].split(' ')[0]
        completo = (f'<p class="frag-nota">Fragmento de §{pid}. Párrafo completo: Paidós {enlazar(("pp. " if "–" in es_pp else "p. ") + es_pp)}'
                    f' · Minuit {("pp. " if "–" in p["m_pp"] else "p. ") + p["m_pp"]}</p>')
    return f'''
<article class="parrafo{' nucleo' if p['nucleo'] else ''}" id="p{pid.replace('.', '-')}">
  <header class="pc">
    <div class="pc-mov">{star}<span class="pc-num">movimiento {p['mov']}</span><h3 class="pc-tit">{md(p['titulo'])}</h3></div>
    <div class="pc-meta"><span>§{pid}</span><span>OE {oe}</span><span>Paidós {enlazar(rango(e0, e1))}</span><span>Minuit {rango(m0, m1)}</span></div>
  </header>
  <div class="cols">
    <div class="col col-es" lang="es"><div class="col-lbl">Paidós · trad. Monge</div><p>{es_h}</p></div>
    <div class="col col-fr" lang="fr"><div class="col-lbl">Minuit · 1972</div><p>{fr_h}</p></div>
  </div>
  {completo}
  <div class="interp">
    <div class="interp-lbl">Interpretación</div>
    <section class="ib"><h4>Lo que hace el párrafo</h4>{enlazar(p['hace'])}</section>
    <section class="ib"><h4>En el comentario</h4>{enlazar(p['comentario'])}</section>
    {trad}
    <section class="ib ib-mia"><h4>Mi lectura</h4>{marca_mia(enlazar(sin_rotulo(p['lectura'])))}</section>
  </div>
</article>'''

def seccion(num, tit, tit_fr, es_pp, m_pp):
    d = DATA.get(num)
    head = f'<summary><span class="s-num">I.{num}</span><span class="s-tit">{tit}<span class="s-fr" lang="fr">{tit_fr}</span></span><span class="s-pp">Paidós pp. {es_pp}<br>Minuit pp. {m_pp}</span></summary>'
    if not d:
        return f'<details class="seccion pendiente" id="s{num}">{head}<div class="s-cuerpo"><p class="pend">Pendiente.</p></div></details>'
    S, P = d.SECCION, d.PARRAFOS
    oes = ''.join(f'<li>{md(o)}</li>' for o in S['objetivos'])
    movs = ''.join(f'<li><a href="#p{p["id"].replace(".", "-")}">{md(p["titulo"])}</a> <span class="m-ref">§{p["id"]} · OE {", ".join(map(str, p["oe"]))}{" · ★" if p["nucleo"] else ""}</span></li>' for p in P)
    return f'''<details class="seccion" id="s{num}" open>{head}
<div class="s-cuerpo">
  <div class="s-intro">
    <h4>Objetivo general</h4><p class="og">{md(S['objetivo_general'])}</p>
    <div class="s-grid">
      <div><h4>Objetivos específicos</h4><ol class="oe">{oes}</ol></div>
      <div><h4>Movimientos y párrafos ancla</h4><ol class="movs">{movs}</ol></div>
    </div>
    <div class="s-texto">{marca_mia(enlazar(S['intro_html']))}<div class="fuera">{enlazar(S['fuera_html'])}</div></div>
  </div>
  {''.join(parrafo(p) for p in P)}
</div></details>'''

CSS = r'''
  :root{
    --paper:#ffffff; --panel:#f7f6f2; --line:#e3dfd3; --ink:#2b2c22; --ink-dim:#6f6f5c;
    --moss:#586a45; --steel:#4f6b82; --warm:#b06a36;
    --mono:"Fira Code", ui-monospace, "SF Mono", "DejaVu Sans Mono", Menlo, Consolas, monospace;
    --serif:"Iowan Old Style", "Charter", Georgia, "Times New Roman", serif;
    --r:2px;
  }
  *{box-sizing:border-box}
  html{scroll-padding-top:calc(var(--hdr, 49px) + 14px)}
  body{margin:0; background:var(--paper); color:var(--ink); font-family:var(--mono); font-size:12px; line-height:1.5}
  header.top{position:sticky; top:0; z-index:5; display:flex; align-items:center; gap:16px; flex-wrap:wrap; row-gap:8px;
    padding:10px 16px; border-bottom:1px solid var(--line); background:var(--paper)}
  #marca{margin:0; font-size:12px; font-weight:600; letter-spacing:.18em; white-space:nowrap}
  #marca a{color:inherit; text-decoration:none}
  #marca a:hover{color:var(--moss)}
  .espacio{flex:1}
  .acciones{display:flex; gap:8px; flex-wrap:wrap; align-items:center}
  .btn{font-family:var(--mono); font-size:11px; letter-spacing:.03em; cursor:pointer; border-radius:var(--r); padding:6px 10px;
    border:1px solid var(--line); background:var(--paper); color:var(--ink); text-decoration:none; display:inline-block}
  .btn:hover{border-color:var(--moss); color:var(--moss)}
  .btn[aria-pressed="true"]{border-color:var(--moss); color:var(--moss); background:var(--panel)}
  .grupo{display:inline-flex; gap:0}
  .grupo .btn{border-radius:0; margin-left:-1px}
  .grupo .btn:first-child{border-radius:var(--r) 0 0 var(--r); margin-left:0}
  .grupo .btn:last-child{border-radius:0 var(--r) var(--r) 0}
  .lbl{font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-dim)}
  main{max-width:1180px; margin:0 auto; padding:26px 16px 120px}
  .portada{max-width:72ch; margin:0 0 22px}
  .portada h2{font-family:var(--serif); font-size:28px; line-height:1.2; font-weight:600; margin:0 0 8px}
  .portada p{font-family:var(--serif); font-size:16px; line-height:1.6; margin:0 0 10px}
  #aviso{font-size:11px; color:var(--ink-dim); border:1px solid var(--line); border-radius:var(--r); padding:10px 12px; background:var(--panel); margin:0 0 26px; max-width:none}
  #aviso b{color:var(--ink); font-weight:600}
  details.seccion{border:1px solid var(--line); border-radius:var(--r); margin:0 0 16px; background:var(--paper)}
  details.seccion>summary{list-style:none; cursor:pointer; display:grid; grid-template-columns:auto 1fr auto; gap:14px; align-items:center; padding:14px 16px}
  details.seccion>summary::-webkit-details-marker{display:none}
  details.seccion>summary:hover .s-tit{color:var(--moss)}
  details.seccion[open]>summary{border-bottom:1px solid var(--line); background:var(--panel)}
  .s-num{font-size:11px; font-weight:600; letter-spacing:.08em; color:var(--moss); border:1px solid var(--moss); border-radius:var(--r); padding:2px 6px}
  .s-tit{font-family:var(--serif); font-size:21px; font-weight:600; line-height:1.2}
  .s-fr{display:block; font-family:var(--serif); font-size:14px; font-weight:400; font-style:italic; color:var(--steel); margin-top:2px}
  .s-pp{font-size:10.5px; color:var(--ink-dim); text-align:right; line-height:1.5}
  .pendiente .s-tit{color:var(--ink-dim)}
  .pend{color:var(--ink-dim); margin:0}
  .s-cuerpo{padding:22px 20px 6px}
  .s-intro{border:1px solid var(--line); border-radius:var(--r); background:var(--panel); padding:18px 20px; margin:0 0 34px}
  h4{font-family:var(--mono); font-size:10.5px; font-weight:500; letter-spacing:.14em; text-transform:uppercase; color:var(--moss); margin:0 0 6px}
  .og{font-family:var(--serif); font-size:19px; line-height:1.5; margin:0 0 18px}
  .s-grid{display:grid; grid-template-columns:1fr 1fr; gap:26px; margin:0 0 14px}
  ol.oe, ol.movs{margin:0; padding-left:20px; font-family:var(--serif); font-size:15.5px; line-height:1.5}
  ol li{margin:0 0 6px}
  ol.movs a{color:var(--ink); text-decoration-color:var(--line); text-underline-offset:2px}
  ol.movs a:hover{color:var(--moss)}
  .m-ref{font-family:var(--mono); font-size:10.5px; color:var(--ink-dim); white-space:nowrap}
  .s-texto p{font-family:var(--serif); font-size:16px; line-height:1.6; margin:0 0 10px}
  .plan{display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:4px 0 12px}
  .plan blockquote{margin:0; padding:8px 0 8px 14px; border-left:2px solid var(--warm); font-family:var(--serif); font-size:16px; line-height:1.55; background:transparent}
  .plan blockquote[lang=fr]{border-left-color:var(--steel)}
  ol.sumario{margin:4px 0 14px; padding-left:22px; font-family:var(--serif); font-size:15px; line-height:1.45; columns:2; column-gap:28px}
  ol.sumario li{break-inside:avoid; margin:0 0 5px}
  ol.sumario .ref{margin-left:4px}
  @media (max-width: 900px){ ol.sumario{columns:1} }
  .ref{font-family:var(--mono); font-size:10.5px; color:var(--ink-dim)}
  .frag-nota{font-family:var(--mono); font-size:10.5px; color:var(--ink-dim); margin:8px 0 16px; letter-spacing:.02em}
  .omite{color:var(--ink-dim); font-family:var(--mono); font-size:.8em; padding:0 2px}
  table.cuadro{border-collapse:collapse; margin:6px 0 4px; font-family:var(--serif); font-size:15px; line-height:1.4; width:100%; max-width:760px}
  table.cuadro th{font-family:var(--mono); font-size:10.5px; font-weight:normal; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-dim); text-align:left; padding:4px 10px 4px 0; border-bottom:1px solid var(--line)}
  table.cuadro td{padding:6px 10px 6px 0; border-bottom:1px solid var(--line); vertical-align:top}
  @media (max-width: 600px){ table.cuadro{font-size:13.5px} table.cuadro th, table.cuadro td{padding-right:6px} }
  .s-texto .nota-trad, .fuera p{font-size:14.5px; color:var(--ink-dim)}
  .s-texto strong{color:var(--ink)}
  .fuera{border-top:1px dashed var(--line); margin-top:12px; padding-top:8px}
  article.parrafo{margin:0 0 46px}
  .pc{display:flex; flex-wrap:wrap; justify-content:space-between; align-items:baseline; gap:6px 18px; border-bottom:1px solid var(--ink); padding-bottom:8px; margin-bottom:14px}
  .pc-mov{display:flex; align-items:baseline; gap:10px; flex-wrap:wrap}
  .pc-num{font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--moss)}
  .pc-tit{font-family:var(--serif); font-size:20px; font-weight:600; line-height:1.25; margin:0}
  .star{color:var(--warm); font-size:15px}
  .pc-meta{font-size:10.5px; color:var(--ink-dim); display:flex; gap:4px 14px; flex-wrap:wrap}
  .cols{display:grid; grid-template-columns:1fr 1fr; gap:30px}
  .col p{margin:0; font-family:var(--serif); font-size:17px; line-height:1.7; hyphens:auto; -webkit-hyphens:auto}
  .col-lbl{font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--warm); margin-bottom:6px}
  .col-fr .col-lbl{color:var(--steel)}
  .pg{font-family:var(--mono); font-size:10px; color:var(--warm); border:1px solid currentColor; border-radius:var(--r); padding:0 .35em; margin:0 .2em; white-space:nowrap; vertical-align:.12em; text-decoration:none}
  a.pg:hover{background:var(--warm); color:#fff}
  .col-fr .pg{color:var(--steel)}
  .verso{display:block; margin-top:10px; padding-left:14px; border-left:2px solid var(--line)}
  .verso-ini{margin:0 0 12px}
  .aclara{font-family:var(--mono); font-size:10px; color:var(--ink-dim)}
  sup.rec{color:var(--steel); font-family:var(--mono); cursor:help}
  .interp{margin-top:20px; background:var(--panel); border:1px solid var(--line); border-radius:var(--r); padding:14px 18px 4px}
  .interp-lbl{font-size:10.5px; letter-spacing:.16em; text-transform:uppercase; color:var(--ink); font-weight:600; margin-bottom:10px}
  .ib{margin-bottom:12px}
  .ib p{margin:0 0 8px; font-family:var(--serif); font-size:16px; line-height:1.65}
  .ib-trad h4{color:var(--steel)}
  .ib-mia h4{color:var(--warm)}
  a.pag{color:var(--steel); text-decoration-style:dotted; text-decoration-thickness:1px; text-underline-offset:2px; white-space:nowrap}
  em.marca{font-style:normal; font-family:var(--mono); font-size:.68em; letter-spacing:.08em; text-transform:uppercase; color:var(--warm); border:1px solid currentColor; border-radius:var(--r); padding:0 .4em; margin-right:.3em; vertical-align:.12em}
  body.solo-es .col-fr, body.solo-fr .col-es{display:none}
  body.solo-es .cols, body.solo-fr .cols{grid-template-columns:1fr; max-width:72ch}
  body.sin-interp .interp{display:none}
  body.solo-nucleo article.parrafo:not(.nucleo){display:none}
  footer.pie{font-size:11px; color:var(--ink-dim); border-top:1px solid var(--line); padding-top:14px; margin-top:30px; line-height:1.6}
  @media (max-width: 900px){
    header.top{position:static}
    .cols, .s-grid, .plan{grid-template-columns:1fr; gap:16px}
    .col-fr{border-top:1px solid var(--line); padding-top:12px}
    details.seccion>summary{grid-template-columns:auto 1fr; padding:12px}
    .s-pp{grid-column:2; text-align:left}
    .s-cuerpo{padding:16px 14px 4px}
    .s-intro{padding:14px}
    .col p{font-size:16.5px}
  }
  @media print{
    header.top{position:static} .acciones{display:none} details.seccion{border:0}
    .interp, .s-intro{break-inside:avoid-page} a{color:inherit; text-decoration:none}
  }
'''

JS = r'''
(function(){
  'use strict';
  try { window.name = 'ae-matriz'; } catch(e){}   // el menú «explicación» del lector reutiliza esta pestaña
  const b = document.body;
  function set(g, v){
    document.querySelectorAll('[data-g="'+g+'"] .btn').forEach(x=> x.setAttribute('aria-pressed', x.dataset.v === v ? 'true' : 'false'));
    if (g === 'lengua'){ b.classList.remove('solo-es','solo-fr'); if (v !== 'ambas') b.classList.add('solo-' + v); }
    if (g === 'interp') b.classList.toggle('sin-interp', v === 'ocultar');
    if (g === 'sel') b.classList.toggle('solo-nucleo', v === 'nucleo');
  }
  document.querySelectorAll('[data-g] .btn').forEach(x=> x.addEventListener('click', ()=> set(x.parentElement.dataset.g, x.dataset.v)));
  const todas = ()=> document.querySelectorAll('details.seccion');
  document.getElementById('abrir').addEventListener('click', ()=> todas().forEach(d=> d.open = true));
  document.getElementById('cerrar').addEventListener('click', ()=> todas().forEach(d=> d.open = false));
  window.addEventListener('beforeprint', ()=> todas().forEach(d=> d.open = true));
  document.querySelectorAll('ol.movs a').forEach(a=> a.addEventListener('click', ()=>{ const d = document.querySelector(a.getAttribute('href')).closest('details'); if (d) d.open = true; }));
  const hdr = document.querySelector('header.top');
  const fijar = ()=> document.documentElement.style.setProperty('--hdr', hdr.offsetHeight + 'px');
  fijar(); window.addEventListener('resize', fijar);
})();
'''

page = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>El Anti-Edipo · matriz de lectura</title>
<!-- Matriz de lectura en voz alta, capítulo I: por sección, objetivo general, objetivos específicos y movimientos;
     cada movimiento se ancla en un párrafo completo (Paidós/Monge y Minuit 1972) seguido de su interpretación.
     Página autónoma: no depende de los scripts del lector; solo enlaza a index.html#p-N. -->
<style>{CSS}</style>
</head>
<body>
  <header class="top">
    <h1 id="marca"><a href="index.html">EL ANTI-EDIPO</a> · matriz de lectura</h1>
    <div class="espacio"></div>
    <div class="acciones">
      <span class="lbl">texto</span>
      <span class="grupo" data-g="lengua"><button class="btn" data-v="ambas" aria-pressed="true">ambos</button><button class="btn" data-v="es" aria-pressed="false">español</button><button class="btn" data-v="fr" aria-pressed="false">francés</button></span>
      <span class="grupo" data-g="interp"><button class="btn" data-v="mostrar" aria-pressed="true">con interpretación</button><button class="btn" data-v="ocultar" aria-pressed="false">sin</button></span>
      <span class="grupo" data-g="sel"><button class="btn" data-v="todos" aria-pressed="true">todos</button><button class="btn" data-v="nucleo" aria-pressed="false">solo ★</button></span>
      <span class="grupo"><button class="btn" id="abrir" type="button">abrir</button><button class="btn" id="cerrar" type="button">cerrar</button></span>
      <a class="btn" href="explicacion.html" target="ae-explicacion" title="Explicación sistemática por sección">explicación</a>
      <a class="btn" href="index.html" target="ae-lector" title="Abrir el lector">lector</a>
    </div>
  </header>
  <main>
    <div class="portada">
      <h2>Capítulo I. Las máquinas deseantes</h2>
      <p>Párrafos para leer en voz alta en la sesión 1. Cada sección tiene un objetivo general, objetivos específicos y los movimientos argumentativos que los cumplen. Cada movimiento se ancla en un párrafo completo, en la traducción de Paidós y en el original de Minuit, seguido de su interpretación.</p>
    </div>
    <div id="aviso"><b>p. 12</b> página de Paidós (abre el lector en ese punto) · <b>M 8</b> página de Minuit · <b>★</b> núcleo, para cuando solo hay tiempo para pocos · <b>§1.2</b> segundo párrafo de la sección en Paidós · <b>[…]</b> corte dentro del párrafo · <b>OE</b> objetivo específico · <b>Mi lectura</b> marca la interpretación propia; <b>Ejemplo forzado</b>, un ejemplo que no está en el libro.</div>
    {''.join(seccion(*s) for s in SECCIONES)}
    <footer class="pie">De cada párrafo ancla se transcribe solo el fragmento para leer en voz alta; debajo van las páginas del párrafo completo, que abren el lector. El español sigue anti-edipo.md, sin las llamadas de nota. El francés viene de un OCR de la edición de Minuit: corregí solo errores evidentes de reconocimiento, sin tocar la redacción; el OCR no conserva cursivas y las repuse solo donde la frase depende de ellas. † marca un orden de palabras reconstruido. «PDF p.» remite a la página del PDF de cada comentario en complementarios/; «hasta donde sé» señala conocimiento no respaldado por los textos cargados.</footer>
  </main>
<script>{JS}</script>
</body>
</html>
'''
open(OUT, 'w').write(page)
print('ok', OUT, len(page))

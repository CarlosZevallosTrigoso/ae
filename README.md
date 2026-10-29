# El Anti-Edipo · lector

Lector web dedicado a una sola obra: *El Anti-Edipo* (Deleuze y Guattari, trad. Francisco Monge, Paidós), limpiado a Markdown a partir del PDF escaneado.

## Archivos

- `index.html` — el lector. Carga `anti-edipo.md` al abrirse; no hay que subir nada a mano.
- `anti-edipo.md` — el libro completo (pp. 8–413), con anclas de página `<!-- p. N -->` y 303 notas al pie.
- `glosario.json` — glosario de conceptos. Cada entrada lleva `id`, `termino`, `patrones` (regex que detectan el término en el texto de Monge), `frances`, `traducciones`, `sesion`, `instalacion` (sección y página donde se define), `paginas` clave, `definicion` (Markdown, ≥ 400 palabras), `confusion` y `relacionados`. El esquema está documentado en el propio archivo (`_esquema`). Para agregar un término basta añadir una entrada; el lector lo subraya solo.
- `casos.json` — catálogo de casos clínicos, literarios y etnográficos que el libro cita sin presentar (Schreber, Dick, Joey, Lenz, Artaud, el Yurugu…). Mismo mecanismo que el glosario: cada caso lleva `patrones` que lo detectan en el texto y se subraya con doble línea; al hacer clic, el panel lateral muestra la ficha (el caso según su fuente, la lectura canónica, detalles, la relectura de Deleuze y Guattari, dónde aparece y una sugerencia para la sesión). Páginas cotejadas con `anti-edipo.md`. Esquema documentado en `_esquema`.
- `analisis.json` — análisis por premisas: las tesis que el texto afirma y que el lector tiene que aceptar para que el capítulo funcione (hoy el capítulo I: seis tesis y diez sub-tesis). Cada entrada lleva `anclas`, frases literales del texto que se resaltan en el lector y abren la ficha: formulación, lo que dice el texto (con página), de dónde viene, lo que dice el comentario (Holland, Buchanan, Massumi, con página del PDF), qué depende de la tesis, la objeción más seria y una pregunta para la sesión. Esquema en `_esquema`.
- `explicacion.html` y `explicacion/` — explicación sistemática del libro, capítulo por capítulo y sección por sección, en una página aparte que se abre desde el desplegable «explicación» de la cabecera del lector. Cada capítulo es un Markdown editable (`explicacion/cap1.md`, `cap2.md`…, `apendice.md`); cada sección lleva objetivo y lugar en el capítulo, ideas fuerza, el argumento paso a paso, los casos que lo sostienen, interlocutores, y tensiones y lecturas. Las páginas citadas como «(p. N)» se convierten en enlaces que abren el lector en esa página; «págs.» (otras obras) y «PDF p.» (comentarios) no se enlazan. Los enlaces `index.html#g-<id>` abren el glosario, los casos o el análisis. Hoy están escritas las secciones I.1–I.4; las demás figuran como pendientes. Un capítulo sin archivo aparece como «todavía no tiene explicación».
- `matriz.html` — matriz de lectura en voz alta del capítulo I, en una página aparte que se abre desde el mismo desplegable «explicación». Por sección: objetivo general, objetivos específicos y movimientos argumentativos; cada movimiento se ancla en un párrafo completo, en Paidós y en Minuit (OCR corregido), con su interpretación. Las páginas de Paidós abren el lector en ese punto. Hoy están escritas las secciones I.1–I.4; las demás figuran como pendientes.
- `marked.umd.js` — copia local del conversor Markdown→HTML (sin dependencia de CDN).
- `capitulos/` — el mismo texto en un archivo por capítulo.
- `herramientas/` — script de limpieza, configuraciones y fuentes para regenerar el `.md` (ver su README).
- `.nojekyll` — vacío; desactiva Jekyll en GitHub Pages. Sin él, Pages convierte `anti-edipo.md` a HTML y el lector recibe un 404.

## Qué hace el lector

- Índice lateral por capítulos y por las 34 secciones del índice de la edición.
- Número de página del libro en el margen; salto directo con el campo «p.» de la cabecera (Enter).
- Salto directo por URL: `index.html#p-24` abre el lector en la p. 24 (lo usan los enlaces de la explicación, que reutilizan una misma pestaña del lector).
- Notas al pie enlazadas en ambos sentidos (número → nota, ↩ → texto).
- Anotaciones: seleccionar texto y pulsar «anotar»; cada pasaje admite varios comentarios. Se guardan en el navegador (localStorage) y se pueden exportar e importar como `.json`.
- «editar» abre el Markdown para corregir erratas; «exportar .md» descarga la versión corregida para hacer commit.
- «recargar» vuelve a pedir `anti-edipo.md` al servidor tras un commit; las anotaciones se re-anclan por contexto.
- Glosario: los términos de `glosario.json` aparecen subrayados (punteado) en el texto; al hacer clic, el panel lateral pasa a modo glosario y muestra la entrada: término francés, traducciones, sección y página donde se instala (enlazadas), páginas clave, definición, confusión frecuente y términos relacionados. El botón «glosario» de la cabecera abre el índice por sesiones; «anotaciones» vuelve al panel de notas. El subrayado se puede apagar en «ajustes». Los casos de `casos.json` se listan al final del índice del glosario, agrupados por tipo, y tienen su propio interruptor («subrayar casos»). El botón «análisis» de la cabecera abre el índice de tesis de `analisis.json` por capítulo, con las sub-tesis debajo; la frase donde cada tesis se enuncia va resaltada en el texto y se puede apagar en «ajustes» («resaltar análisis»). Una tesis abierta queda en la URL como `#g-<id>`. Una entrada abierta queda en la URL como `#g-<id>`, así que se puede enlazar. El subrayado envuelve nodos de texto sin alterar el texto plano, de modo que las anotaciones siguen ancladas.
- Sesiones del taller: el desplegable «sesiones» lista las cinco sesiones (por secciones, no por páginas) y permite prenderlas y apagarlas. Las apagadas desaparecen del texto y del índice; sus notas al pie también. Cada sesión lleva una etiqueta al inicio de su primer bloque y un encabezado en el índice. La elección se guarda en el navegador. Ir a una página, una nota o una anotación que cae en una sesión apagada la vuelve a prender. La distribución está en `SESIONES`, dentro de `index.html`.
- Tema claro/oscuro, ancho de columna, modo tablet.

## Publicar en GitHub Pages

1. Crear el repositorio y subir los tres archivos a la raíz de la rama `main`.
2. En *Settings → Pages*, elegir *Deploy from a branch*, rama `main`, carpeta `/ (root)`.
3. El lector queda en `https://<usuario>.github.io/<repo>/`.

También funciona en local sirviendo la carpeta con cualquier servidor estático (por ejemplo `python3 -m http.server`); abrir `index.html` directamente con `file://` no carga el `.md` por la política de origen del navegador.

## Laguna conocida

La p. 292 (capítulo IV) no está en el `.md`: el conversor la capturó como imagen. Está marcada en el texto con un comentario.

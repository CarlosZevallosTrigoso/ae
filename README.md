# El Anti-Edipo · lector

Lector web dedicado a una sola obra: *El Anti-Edipo* (Deleuze y Guattari, trad. Francisco Monge, Paidós), limpiado a Markdown a partir del PDF escaneado.

## Archivos

- `index.html` — el lector. Carga `anti-edipo.md` al abrirse; no hay que subir nada a mano.
- `anti-edipo.md` — el libro completo (pp. 8–413), con anclas de página `<!-- p. N -->` y 303 notas al pie.
- `marked.umd.js` — copia local del conversor Markdown→HTML (sin dependencia de CDN).
- `.nojekyll` — vacío; desactiva Jekyll en GitHub Pages. Sin él, Pages convierte `anti-edipo.md` a HTML y el lector recibe un 404.

## Qué hace el lector

- Índice lateral por capítulos y secciones.
- Número de página del libro en el margen; salto directo con el campo «p.» de la cabecera (Enter).
- Notas al pie enlazadas en ambos sentidos (número → nota, ↩ → texto).
- Anotaciones: seleccionar texto y pulsar «anotar»; cada pasaje admite varios comentarios. Se guardan en el navegador (localStorage) y se pueden exportar e importar como `.json`.
- «editar» abre el Markdown para corregir erratas; «exportar .md» descarga la versión corregida para hacer commit.
- «recargar» vuelve a pedir `anti-edipo.md` al servidor tras un commit; las anotaciones se re-anclan por contexto.
- Tema claro/oscuro, ancho de columna, modo tablet.

## Publicar en GitHub Pages

1. Crear el repositorio y subir los tres archivos a la raíz de la rama `main`.
2. En *Settings → Pages*, elegir *Deploy from a branch*, rama `main`, carpeta `/ (root)`.
3. El lector queda en `https://<usuario>.github.io/<repo>/`.

También funciona en local sirviendo la carpeta con cualquier servidor estático (por ejemplo `python3 -m http.server`); abrir `index.html` directamente con `file://` no carga el `.md` por la política de origen del navegador.

## Laguna conocida

La p. 292 (capítulo IV) no está en el `.md`: el conversor la capturó como imagen. Está marcada en el texto con un comentario.

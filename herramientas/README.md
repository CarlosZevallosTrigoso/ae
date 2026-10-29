# Herramientas de regeneración

`anti-edipo.md` se genera a partir de las salidas de marker-pdf (`fuentes/`), nunca se edita a mano. Para regenerar todo:

```sh
cd herramientas
python3 -I limpiar_antiedipo.py fuentes/cap1.md     ../capitulos/anti-edipo-cap1.md     cap1.json
python3 -I limpiar_antiedipo.py fuentes/cap2.md     ../capitulos/anti-edipo-cap2.md     cap2.json
python3 -I limpiar_antiedipo.py fuentes/cap3.md     ../capitulos/anti-edipo-cap3.md     cap3-completo.json
python3 -I limpiar_antiedipo.py fuentes/cap4.md     ../capitulos/anti-edipo-cap4.md     cap4-completo.json
python3 -I limpiar_antiedipo.py fuentes/apendice.md ../capitulos/anti-edipo-apendice.md apendice.json
python3 -I secciones.py          # inserta los títulos del índice (secciones.json)
python3 -I ensamblar.py          # une los capítulos en ../anti-edipo.md
```

Las correcciones de texto van en el `.json` de cada capítulo (`fixes`, `replacements`, `note_fixes`), para que sobrevivan a la siguiente regeneración. `secciones.json` reproduce el índice de la edición (pp. 423-428) con la página de inicio de cada sección.

`matriz/` genera `../matriz.html`, la matriz de lectura en voz alta. Se rehace con `python3 -I herramientas/matriz/construir.py`; su `README.md` explica qué archivo editar para cada cambio.

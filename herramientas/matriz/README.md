# Generador de la matriz de lectura

`matriz.html`, en la raíz del repositorio, no se edita a mano: se genera con los archivos de esta carpeta. Para rehacerla después de cualquier cambio:

```sh
python3 -I herramientas/matriz/construir.py
```

El comando corre cuatro pasos y al final coteja las citas. Tarda unos segundos.

1. `extraer.py` separa en párrafos el capítulo I de Paidós (`capitulos/anti-edipo-cap1.md`) y del OCR de Minuit (`complementarios/AE_frances.md`), con sus marcas de página.
2. `segmentar_fr.py` corta en el francés los párrafos que corresponden a cada párrafo de Paidós y les aplica las correcciones del OCR.
3. `generar.py` arma la página con el texto de los dos lados y los contenidos de cada sección.
4. `verificar.py` busca cada cita seguida de «(p. N)» en Paidós y cada cita seguida de «(M N)» en el francés, y avisa si no aparece o si cae en otra página.

Los archivos intermedios quedan en `datos/`, que no se sube al repositorio.

## Qué editar para cada cambio

- **Una interpretación, un objetivo o una nota de traducción:** `contenido/sN.py`, donde N es la sección. `SECCION` tiene el objetivo general, los objetivos específicos, la introducción (`intro_html`) y los párrafos que quedan fuera (`fuera_html`). `PARRAFOS` tiene un bloque por párrafo ancla: `id` (el número del párrafo en Paidós, p. ej. `"5.1"`), `mov`, `titulo`, `oe`, `nucleo` (True pone la ★), `es_pp` y `m_pp` (páginas de Paidós y de Minuit), y los textos `hace`, `comentario`, `traduccion` (opcional) y `lectura`. `frag_es` y `frag_fr` delimitan el fragmento para leer en voz alta: una lista de pares (frase inicial, frase final) copiados exactamente del texto, que se unen con «[…]»; sin ellos se transcribe el párrafo entero. `versos=True` conserva los versos de Artaud que acompañan a §1.3, §2.9 y §6.9 cuando hay fragmento.
- **Cambiar qué párrafos se leen:** agregar o quitar bloques en `PARRAFOS` de `contenido/sN.py` y, para el francés, la línea correspondiente en `PARTS` de `frances/partes_sN.py` (frase con que empieza y frase con que termina el párrafo en el OCR).
- **Un error del OCR francés:** agregar el par `('texto del OCR', 'corrección')` a `FIX` en `frances/partes_sN.py`. `segmentar_fr.py` avisa si una corrección deja de tener efecto.
- **Una errata de Paidós:** `ES_FIX`, al comienzo de `generar.py`. Las enmiendas van entre corchetes, como `[ciclo]`.
- **El diseño de la página:** el CSS y el JavaScript están dentro de `generar.py`.

## Convenciones de los textos

- «(p. N)» es Paidós y se convierte en un enlace que abre el lector en esa página; «(M N)» es Minuit; «PDF p. N» remite a la página del PDF de un comentario en `complementarios/`.
- `lectura` empieza con el grado de confianza («Con confianza alta.»). `<em>Ejemplo forzado:</em>` marca un ejemplo que no está en el libro.
- Lo que no está respaldado por los textos del repositorio se marca con «hasta donde sé».
- En el francés, `‹N›` marca un cambio de página de Minuit y `†` un orden de palabras reconstruido.

## Avisos de `verificar.py` que son falsos

`verificar.py` compara con la primera aparición de la frase en el libro. Una frase común que ya apareció antes da un aviso de página aunque la cita sea correcta. Hoy pasa con «répression» (M 40), «ou bien» (M 18), «la promenade du schizo» (M 43), «dans le vide à l'infini» (M 45), «energía residual» (p. 47), «tal vez» (p. 50) y «desde siempre es huérfano» (p. 114). «Une psychiatrie vraiment matérialiste…» (M 29) figura como no encontrada porque el OCR tiene «<<» cerca y el verificador lo confunde con una etiqueta HTML. Todas están revisadas a mano.

## Para otros capítulos

`extraer.py` toma solo el capítulo I: las líneas 151–563 de `AE_frances.md` y el archivo `capitulos/anti-edipo-cap1.md`. Para el capítulo II habría que darle esos dos datos y una lista de secciones nueva en `generar.py` (`SECCIONES`).

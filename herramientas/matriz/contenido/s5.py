# Contenido de la sección 5 para la matriz de lectura en voz alta.
# Convenciones: (p. N) = Paidós, trad. Monge; (M N) = Minuit 1972. PDF p. = página del PDF en complementarios/.

SECCION = dict(
    num=5,
    objetivo_general=(
        "Responder sin metáfora qué hace de las máquinas deseantes verdaderas máquinas: un sistema de tres cortes, cada uno ligado "
        "a una síntesis y a una energía. La sección vuelve a exponer, desde los cortes, el modelo de las secciones 1–3."
    ),
    objetivos=[
        "Definir la máquina como sistema de cortes y presentar el primero, el corte-extracción sobre un flujo.",
        "Mostrar el régimen de la producción deseante en un caso clínico, el de Joey.",
        "Presentar el código y el segundo corte, el corte-separación sobre cadenas cuyos signos no son significantes.",
        "Presentar el tercer corte, el corte-resto que produce el sujeto, y alinear cortes, síntesis y energías.",
    ],
    intro_html="""
<p>La sección 5 empieza de nuevo, desde otra pregunta. Las secciones 1–3 armaron el modelo por sus síntesis; esta lo arma por sus cortes, y al final hace coincidir las dos exposiciones. Por eso el capítulo se siente circular. La recapitulación de la p. 47 sirve como cuadro para la sesión:</p>
<table class="cuadro">
<thead><tr><th>Corte</th><th>Síntesis</th><th>Energía</th><th>Producción</th></tr></thead>
<tbody>
<tr><td>extracción <span lang="fr">(prélèvement)</span>, sobre el flujo</td><td>conectiva</td><td>libido, «energía de extracción»</td><td>de producción</td></tr>
<tr><td>separación <span lang="fr">(détachement)</span>, sobre la cadena</td><td>disyuntiva</td><td><em>Numen</em>, «energía de separación»</td><td>de registro</td></tr>
<tr><td>resto o residuo, el sujeto</td><td>conjuntiva</td><td><em>Voluptas</em>, «energía residual»</td><td>de consumo</td></tr>
</tbody>
</table>
<p><span class="ref">Fuente del cuadro: §5.6 (p. 47 · M 49–50).</span></p>
""",
    fuera_html="""<p><strong>Queda fuera</strong> §5.5 (p. 46 · M 48), sobre Monakow y Mourgue. La <em>diaschisis</em> y la <em>diaspasis</em> le sirven al texto para mostrar los ladrillos como piezas del registro en el sistema nervioso, y el párrafo termina celebrando que una teoría así «supone haber introducido el deseo en la neurología» (p. 46).</p>""",
)

PARRAFOS = [
dict(
    id="5.1", mov=1, titulo="El sistema de cortes: extracción sobre la hylè", oe=[1], nucleo=True,
    es_pp="42–43", m_pp="43–44",
    frag_es=[('¿En qué son las máquinas deseantes verdaderamente máquinas', 'extracciones en el flujo asociativo.'), ('El corte no se opone a la continuidad', 'como continuidad ideal.'), ('En una palabra, toda máquina es corte de flujo', 'la ley de la producción de producción.')],
    frag_fr=[('En quoi les machines désirantes', 'sur le flux associatif.'), ("Loin que la coupure s'oppose à la continuité", 'comme continuité idéelle.'), ('Bref, toute machine est coupure de flux', 'la loi de production de production.')],
    hace="""<p>La sección abre con la pregunta que la sección 1 dejó pendiente y responde con una definición: una máquina es un sistema de cortes. La primera pieza da el primer corte, la extracción sobre un flujo continuo. Entre la primera y la segunda pieza, el texto da casos, el ano, la boca, el pene y sus flujos, y pide pensar cada flujo como ideal, «flujo infinito de un muslo de cerdo inmenso» (p. 42). La segunda pieza da la frase decisiva sobre corte y continuidad. Entre la segunda y la tercera, la cadena del ano a la boca muestra que toda máquina es corte para una y flujo para otra. La tercera pieza lo formula como ley.</p>""",
    comentario="""<p>El <em>Dictionary</em> abre su entrada «Desiring-machines» con esta definición (PDF p. 100) y cita la ley del corte y el flujo en la entrada «Flows» (PDF p. 140). Holland anota que la sección argumenta que el término no es metafórico y la vincula con «Machine et structure», el ensayo de Guattari (<em>Introduction</em>, nota 4, PDF p. 137). Dosse cuenta que «máquina» fue la palabra elegida para desplazar a «estructura», y que en <em>Mil mesetas</em> se abandonó cuando ya había cumplido ese objetivo (<em>Intersecting Lives</em>, PDF pp. 243–244).</p>""",
    traduccion="""<p>«Elle fonctionne comme machine à couper le jambon» (M 43): una cortadora de jamón. El archivo de Paidós dice «máquina de cortar jabón», y la imagen se rompe, porque sigue con el «muslo de cerdo inmenso»; en el texto de arriba lo enmiendo entre corchetes. Fuera del fragmento hay otro error de la misma clase: las «boulettes» de la iniciación que describe Jaulin (M 44) son bolitas, y Monge pone «polillas».</p>""",
    lectura="""<p>Con confianza alta. La relatividad entre corte y flujo es la clave para leer cualquier «flujo» del libro: ningún flujo es primero, cada uno lo es solo respecto de una máquina que lo corta. <em>Ejemplo forzado:</em> una acequia. Corta el río, del que extrae agua, y es flujo para el canal de cada chacra, que a su vez la corta. El ejemplo cojea porque el agua tiene una fuente identificable, y el texto dice que cada flujo es ideal, una continuidad que solo el corte define.</p>""",
),
dict(
    id="5.2", mov=2, titulo="Joey: la avería como funcionamiento", oe=[2], nucleo=False,
    es_pp="43–44", m_pp="45",
    frag_es=[('Connecticut, Connect', 'de las conexiones maquinales.'), ('Pero la máquina queda como deseo', 'la terapéutica de Bettelheim.')],
    frag_fr=[('Connecticut, Connect', 'des connexions machiniques.'), ('Mais la machine reste désir', 'la thérapeutique de Bettelheim.')],
    hace="""<p>La primera pieza presenta a Joey, el niño de Bettelheim que solo vive enchufado a máquinas, y lo propone como ejemplo del régimen de la producción deseante. Entre las piezas, el texto se plantea la objeción: esa vida mecánica expresaría la destrucción del deseo y una negación parental extrema. Responde con el propio Bettelheim, que reconoce primero una «reacción autónoma ante la experiencia total de la vida de la cual la madre no es más que una parte» (p. 43), y repite la pregunta de §4.3: cómo el proceso se volvió fin. La segunda pieza afirma que la máquina sigue siendo deseo, y Joey recorre las tres máquinas de las secciones 2 y 3.</p>""",
    comentario="""<p>Buchanan explica por qué Bettelheim importa a los autores pese a su sesgo edípico: admite la esquizofrenia como una fuerza productiva autónoma, que poco le debe a lo que hicieron los padres (<em>Reader's Guide</em>, nota 20, PDF p. 157). Hasta donde sé, y sin fuente en el corpus, la autoridad de Bettelheim quedó muy cuestionada después de su muerte en 1990, igual que su idea de que el autismo se debía a madres frías. El «autismo» de este párrafo no corresponde a lo que hoy se entiende por ese nombre.</p>""",
    traduccion="""<p>Fuera del fragmento, Paidós omite un paréntesis del francés: el cuerpo sin órganos de Joey es «(yeux fermés, nez pincé, oreilles bouchées)» (M 45), ojos cerrados, nariz tapada, oídos taponados. Si se lee el párrafo completo, conviene reponerlo. En el fragmento, «le cassage» es «la rotura»; el texto suma «o el desarreglo», que no está en el francés de esa frase.</p>""",
    lectura="""<p>Con confianza media. El caso pone en clínica lo que §4.3 dijo en general: el niño-máquina es el proceso convertido en fin, pero las máquinas mismas no son la pérdida del deseo. El párrafo muestra además la estrategia del libro con sus fuentes psicoanalíticas, que es usar su material contra su modelo causal. Leído hoy en un grupo, conviene decir en voz alta las dos advertencias, la que pesa sobre la fuente y la que pesa sobre la palabra «autismo».</p>""",
),
dict(
    id="5.3", mov=3, titulo="El código como jerga; contra la cadena significante", oe=[3], nucleo=False,
    es_pp="44–45", m_pp="46–47",
    frag_es=[('En segundo lugar, toda máquina implica una especie de código', 'almacenado en ella.'), ('Pertenece a Lacan el descubrimiento', 'formación abierta y polívoca.'), ('Producir el deseo, ésta es la única vocación del signo', 'en que ello se maquina.')],
    frag_fr=[('Toute machine comporte en second lieu une sorte de code', 'stocké en elle.'), ("Il revient à Lacan d'avoir découvert", 'formation ouverte et polyvoque.'), ('Produire du désir, telle est la seule vocation du signe', 'où ça se machine.')],
    hace="""<p>La primera pieza da el segundo rasgo de la máquina: un código. Entre la primera y la segunda pieza, el texto plantea las preguntas de funcionamiento, qué flujo cortar, dónde y cómo, y dice que los registros forman «un cuadriculado de disyunciones» (p. 44). La segunda pieza da el crédito a Lacan y lo desplaza: no hay una cadena sino muchas, y sus signos no son significantes. Entre la segunda y la tercera, la cadena aparece como un desfile de letras de alfabetos distintos, con «los bigotes de papá, el brazo levantado de mamá» (p. 45), y el código de la orquídea que «saca» la forma de una avispa. La tercera pieza cierra con la vocación del signo.</p>""",
    comentario="""<p>Holland enumera las tres reservas con que los autores reciben el descubrimiento de Lacan: el sistema no es lineal, no hay una cadena sino muchas, y los signos son radicalmente heterogéneos (<em>Introduction</em>, PDF pp. 42–43). Massumi describe el objeto parcial como una consigna privada cuyos signos forman una lengua de un solo hablante, «más una jerga que un lenguaje» (<em>User's Guide</em>, nota 55, PDF p. 83).</p>""",
    traduccion="""<p>«une sorte de code qui se trouve machiné, stocké en elle» (M 46): el código está <em>maquinado</em> en la máquina, y Monge pone «tramado». La tercera pieza termina con «dans tous les sens où ça se machine» (M 47): vuelve el <em>ça</em> de la primera línea del libro, y Monge lo conserva, «ello se maquina».</p>""",
    lectura="""<p>Con confianza media. Es la confrontación directa del capítulo con Lacan, en dos tiempos: primero el crédito y luego el desplazamiento, signos sin significante. «Jerga» es la palabra que conviene retener, porque nombra un código abierto que nadie domina. Hasta donde sé, Guattari desarrollará después esta idea de una escritura que no pasa por el significante como teoría de las semióticas asignificantes.</p>""",
),
dict(
    id="5.4", mov=4, titulo="El corte-separación: ladrillos y Significante despótico", oe=[3], nucleo=False,
    es_pp="45", m_pp="47–48",
    frag_es=[('Esta es, por tanto, la segunda característica de la máquina', 'como bloques o ladrillos volantes.'), ('Si hace poco dijimos que el esquizo', 'se realiza con ladrillos móviles.')],
    frag_fr=[('Tel est donc le second caractère de la machine', 'des blocs ou des briques volantes.'), ('Si nous disions tout à l\'heure', 'se font par briques mobiles.')],
    hace="""<p>El párrafo empieza con las cadenas como lugar de separaciones en todas direcciones, «esquizias que se valen por sí mismas» (p. 45). La primera pieza nombra el segundo corte y lo distingue del primero. Entre las piezas, el texto describe cada ladrillo, con inscripciones de distintos alfabetos, figuras, «una o varias pajas, y tal vez un cadáver» (p. 45), y muestra que los dos cortes se suponen. La segunda pieza precisa lo dicho en la sección 4 sobre el esquizo y los flujos descodificados, y opone dos usos de los ladrillos: la muralla del Significante despótico y la polivocidad del esquizo.</p>""",
    comentario="""<p>El párrafo no tiene citas directas en <code>complementarios/</code>. Dosse muestra hacia dónde va su «Significante despótico»: el libro hace una crítica violenta de la teoría saussureana del signo, a la que llama «la sombra del despotismo oriental» (<em>Intersecting Lives</em>, PDF p. 244). Ese pasaje pertenece al capítulo III.</p>""",
    traduccion="""<p>«Mais toujours le schizo les détache, les <strong>descelle</strong>» (M 48). <em>Desceller</em> es desellar, arrancar lo que estaba fijado con argamasa: el esquizo saca los ladrillos de la muralla. El «despega» de Monge es cercano, pero pierde la imagen de albañilería.</p>""",
    lectura="""<p>Con confianza media. El fragmento contiene en miniatura la historia del capítulo III: códigos, sobrecodificación despótica y descodificación. Hace además del significante lacaniano una figura histórica, el Significante despótico que linealiza las cadenas, y no la estructura del inconsciente. Es el gesto antilacaniano más fuerte del capítulo. Lo cambiaría si el capítulo III no ligara el significante al despotismo; el pasaje que cita Dosse indica que sí lo hace.</p>""",
),
dict(
    id="5.6", mov=5, titulo="El corte-resto y la recapitulación: tres cortes, tres síntesis, tres energías", oe=[4], nucleo=True,
    es_pp="46–47", m_pp="48–50",
    frag_es=[('El tercer corte de la máquina deseante', 'pieza adyacente de la máquina.'), ('No más que los otros cortes', 'según estos tres modos.'), ('Extraer, separar, «dar restos»', 'las operaciones reales del deseo.')],
    frag_fr=[('La troisième coupure de la machine désirante', 'pièce adjacente à la machine.'), ('Pas plus que les autres coupures', 'suivant ces trois modes.'), ('Prélever, détacher, « rester »', 'les opérations réelles du désir.')],
    hace="""<p>La primera pieza da el tercer corte, que produce el sujeto como pieza adyacente. Entre la primera y la segunda pieza, el texto explica por qué ese sujeto no tiene identidad: es una parte a su vez partida, siempre deducida de los estados por los que pasa. Lo ilustra con un juego de Lacan, <em>parere</em>, <em>separare</em>, <em>se parere</em>. La segunda pieza dice que este corte no es una carencia sino una renta, da el ejemplo del eructo y concluye que la máquina deseante no es una metáfora. Entre la segunda y la tercera pieza va la tabla de los tres modos que está en la introducción de esta sección. La tercera pieza la resume en tres verbos.</p>""",
    comentario="""<p>Buchanan lee el juego de <em>parere</em> y <em>separare</em> como el deseo siguiendo el camino de la acumulación primitiva: separa el cuerpo en sus órganos y luego los despoja de sus poderes, como se separó al trabajador de la tierra (<em>Reader's Guide</em>, PDF p. 71). Holland cita la frase sobre la parte a su vez partida para mostrar que la síntesis conjuntiva no culmina en un sujeto fijo (<em>Introduction</em>, PDF p. 48). Massumi remite a esta página para el eructo (<em>User's Guide</em>, nota 47, PDF p. 90).</p>""",
    traduccion="""<p>En «un revenu qui revient au sujet comme reste» (M 49) hay un juego entre <em>revenu</em>, la renta, y <em>revient</em>, vuelve, que Monge no puede conservar en «una renta que vuelve al sujeto como resto». El «dar restos» de la última pieza traduce «« rester »» (M 50), quedar, permanecer como resto: un verbo, como «extraer» y «separar».</p>""",
    lectura="""<p>Con confianza alta. El eructo muestra que las tres operaciones son simultáneas y no fases: un mismo acontecimiento es extracción, separación y resto a la vez. La tabla de la introducción es la formalización que vuelve circular el capítulo, y puede servir de pizarra al cierre de la sesión. Contra la castración, el resto del sujeto es una renta que se cobra, no una falta que se paga.</p>""",
),
]

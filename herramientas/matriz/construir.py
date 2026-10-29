#!/usr/bin/env python3
"""Regenera ../../matriz.html de principio a fin.

Uso (desde cualquier carpeta):  python3 -I herramientas/matriz/construir.py

Pasos: extraer.py (párrafos de Paidós y del OCR de Minuit) → segmentar_fr.py (cortes y correcciones del francés)
→ generar.py (escribe matriz.html) → verificar.py (coteja las citas con el texto y la página).
"""
import subprocess, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
for paso in ['extraer.py', 'segmentar_fr.py', 'generar.py', 'verificar.py']:
    print(f'== {paso}', flush=True)
    r = subprocess.run([sys.executable, '-I', str(AQUI / paso)])
    if r.returncode: sys.exit(f'falló {paso}')

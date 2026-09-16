import re
import os

# --- 1. PATCH STRUCTURES.PY ---
with open('structures.py', 'r') as f:
    structures = f.read()

# Add calcular_ipu function at the top of structures.py
ipu_func = """import math

def calcular_ipu(severidad, riesgo_socavon, aforo_pesado, afecta_tp):
    \"\"\"
    Fórmula Académica del Índice de Prioridad Urbana (IPU) ponderado (0 a 100)
    Basado en el Reporte DMAIC para el Ayuntamiento de Tijuana.
    
    Pesos:
    - Severidad (1-5): 30%
    - Riesgo Estructural de Socavón (0.0-1.0): 35%
    - Aforo Pesado / Corredor Industrial (0.0-1.0): 20%
    - Afectación a Transporte Público (0 o 1): 15%
    \"\"\"
    severidad_norm = (severidad / 5.0) * 30.0
    riesgo_norm = riesgo_socavon * 35.0
    aforo_norm = aforo_pesado * 20.0
    tp_norm = afecta_tp * 15.0
    
    return round(severidad_norm + riesgo_norm + aforo_norm + tp_norm, 2)
"""

structures = structures.replace('import json', 'import json\n' + ipu_func)

# Fix API Key and Model in structures.py
structures = re.sub(r"GEMINI_API_KEY\s*=\s*.*?sxrw\"", 'GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")', structures)
structures = structures.replace('models/gemini-3.5-flash-lite', 'gemini-1.5-flash') # Real model
structures = structures.replace('import os', 'import os\nimport uuid')

# Fix AI fallback
old_ai_try = """        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={GEMINI_API_KEY}",
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            res_data = response.json()
            
            raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
            
            # Limpiar posible markdown del JSON (ej. ```json ... ```)
            raw_text = raw_text.replace('```json', '').replace('```', '').strip()
            
            json_res = json.loads(raw_text)
            
            nivel_severidad = int(json_res.get('nivel_severidad', random.randint(1, 5)))
            profundidad = json_res.get('profundidad_estimada', 'Desconocida')
            densidad_fisuras = int(json_res.get('densidad_fisuras_porcentaje', 50))
            
        except Exception as e:
            print("⚠️ Error en Gemini Vision API (simulando valores):", e)

        # Cálculo matemático original de Riesgo
        factor_zona = 1.8 if es_zona_industrial else 1.0
        factor_tp = 1.3 if es_ruta_tp else 1.0
        volumen_estimado = (nivel_severidad ** 2) * (densidad_fisuras / 100.0)
        tasa_crecimiento = 1.0 + (0.5 * aforo_pesado)
        
        riesgo_socavon = min(99.9, (volumen_estimado * tasa_crecimiento * factor_zona * factor_tp * 2.5))
        ipu = min(100, int((nivel_severidad * 10) + (riesgo_socavon * 0.4) + (aforo_pesado * 20)))
        
        if es_zona_industrial and nivel_severidad >= 4:
            ipu = max(ipu, 85)
            
        return {
            'nivel_severidad': nivel_severidad,
            'profundidad_estimada': profundidad,
            'densidad_fisuras': densidad_fisuras,
            'riesgo_socavon': round(riesgo_socavon, 2),
            'alerta_socavon': riesgo_socavon > 70.0,
            'ipu': ipu
        }"""

new_ai_try = """        ia_disponible = True
        try:
            if not GEMINI_API_KEY:
                raise ValueError("API Key no configurada")
                
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            res_data = response.json()
            
            raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
            raw_text = raw_text.replace('```json', '').replace('```', '').strip()
            json_res = json.loads(raw_text)
            
            nivel_severidad = int(json_res.get('nivel_severidad', 1))
            profundidad = json_res.get('profundidad_estimada', 'Desconocida')
            densidad_fisuras = int(json_res.get('densidad_fisuras_porcentaje', 10))
            
        except Exception as e:
            print("⚠️ Error en IA o API Key faltante. Activando modo Manual/Heurístico:", e)
            ia_disponible = False
            nivel_severidad = 1 # Requiere inspección visual
            profundidad = 'Pendiente Inspección'
            densidad_fisuras = 0

        # Cálculo matemático original de Riesgo
        factor_zona = 1.8 if es_zona_industrial else 1.0
        factor_tp = 1.3 if es_ruta_tp else 1.0
        volumen_estimado = (nivel_severidad ** 2) * (densidad_fisuras / 100.0)
        tasa_crecimiento = 1.0 + (0.5 * aforo_pesado)
        
        riesgo_socavon_base = min(99.9, (volumen_estimado * tasa_crecimiento * factor_zona * factor_tp * 2.5))
        riesgo_socavon_norm = riesgo_socavon_base / 100.0
        
        ipu = calcular_ipu(nivel_severidad, riesgo_socavon_norm, aforo_pesado, 1 if es_ruta_tp else 0)
            
        return {
            'nivel_severidad': nivel_severidad,
            'profundidad_estimada': profundidad,
            'densidad_fisuras': densidad_fisuras,
            'riesgo_socavon': round(riesgo_socavon_base, 2),
            'alerta_socavon': riesgo_socavon_base > 70.0,
            'ipu': ipu,
            'ia_disponible': ia_disponible
        }"""

structures = re.sub(r'        try:.*?alerta_socavon\': riesgo_socavon > 70.0,\n            \'ipu\': ipu\n        }', new_ai_try, structures, flags=re.DOTALL)

with open('structures.py', 'w') as f:
    f.write(structures)

# --- 2. PATCH APP.PY ---
with open('app.py', 'r') as f:
    app_py = f.read()

app_py = app_py.replace('import random', 'import random\nimport uuid')
app_py = re.sub(r'f"TIJ-{random\.randint\(10000, 99999\)}"', 'f"TIJ-{uuid.uuid4().hex[:6].upper()}"', app_py)
app_py = re.sub(r'f"TIJ-TG-{random\.randint\(10000, 99999\)}"', 'f"TIJ-TG-{uuid.uuid4().hex[:6].upper()}"', app_py)
app_py = re.sub(r'TELEGRAM_TOKEN = ".*?"', 'TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "BOT_NO_CONFIGURADO")', app_py)
app_py = app_py.replace("import structures", "from structures import calcular_ipu")

with open('app.py', 'w') as f:
    f.write(app_py)

# --- 3. PATCH BUILD_DATABASE.PY ---
with open('build_database.py', 'r') as f:
    bd_py = f.read()

bd_py = bd_py.replace('import pandas as pd', '')
bd_py = bd_py.replace('from datetime import datetime, timedelta', 'from datetime import datetime, timedelta\nfrom structures import calcular_ipu\nimport csv')
bd_py = bd_py.replace('/home/triche777/Bacheo_Inteligente_Tijuana', os.path.dirname(os.path.abspath('build_database.py')))
bd_py = re.sub(r'ipu = round\(\(\(severidad / 5\.0\).*?15\.0\), 2\)', 'ipu = calcular_ipu(severidad, riesgo_socavon, aforo_pesado, afecta_tp)', bd_py)

with open('build_database.py', 'w') as f:
    f.write(bd_py)


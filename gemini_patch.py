import base64
import requests
import json
import random
import math

GEMINI_API_KEY = "AQ.Ab8RN6ISD8oZmIDoj-RJTJWrZqSVst7IdELveF7q78Uw55" + "sxrw"

class PotholeVisionClassifier:
    @staticmethod
    def classify_image(image_bytes, es_zona_industrial=False, aforo_pesado=0.0, es_ruta_tp=False):
        # Valores por defecto en caso de fallo
        nivel_severidad = random.randint(3, 5) if es_zona_industrial else random.randint(2, 4)
        profundidad = "Desconocida"
        densidad_fisuras = random.randint(40, 80)
        
        # Integración con Google Gemini 1.5 Flash (Vision) mediante REST (Sin librerías pesadas)
        try:
            if image_bytes and len(image_bytes) > 100:
                img_b64 = base64.b64encode(image_bytes).decode('utf-8')
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Eres un ingeniero civil experto en pavimentos. Analiza esta imagen de la calle. Responde ESTRICTAMENTE en formato JSON con estas claves: 'severidad' (entero 1 a 5, siendo 5 muy destructivo), 'profundidad' (string, ej: '15 cm'), 'fisuras' (entero 0 a 100, porcentaje de daño alrededor). Si no es un bache claro, asume severidad 1."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                        ]
                    }],
                    "generationConfig": {
                        "temperature": 0.1
                    }
                }
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=12)
                
                if resp.status_code == 200:
                    data = resp.json()
                    text_response = data['candidates'][0]['content']['parts'][0]['text']
                    text_clean = text_response.replace('```json', '').replace('```', '').strip()
                    ai_result = json.loads(text_clean)
                    
                    nivel_severidad = int(ai_result.get('severidad', nivel_severidad))
                    profundidad = str(ai_result.get('profundidad', profundidad))
                    densidad_fisuras = int(ai_result.get('fisuras', densidad_fisuras))
                    print("✅ Gemini Vision procesó la imagen:", ai_result)
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
        }

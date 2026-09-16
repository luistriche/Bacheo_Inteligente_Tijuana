"""
Estructuras de Datos y Motor de Clasificación de Visión Artificial
Bacheo Inteligente y Priorización Urbana - Tijuana, B.C.
UCA: Estructuras de Datos y Ciencia de Datos para Negocios
Estudiante: Luis Armando Triche Ramírez
"""

import math
import heapq
from PIL import Image, ImageStat, ImageFilter
import io

# ==============================================================================
# 1. TABLA HASH ESPACIAL (Deduplicación e Indexación Eficiente en O(1))
# ==============================================================================
class SpatialHashTable:
    """
    Tabla Hash con discretización espacial (Geohash / Cuadrícula).
    Permite detectar si un bache ya fue reportado en un radio de ~20 metros
    en tiempo constante promedio O(1), resolviendo colisiones por encadenamiento.
    """
    def __init__(self, cell_size_deg=0.0002):  # ~20 metros en lat/lon
        self.cell_size = cell_size_deg
        self.table = {}

    def _hash_coords(self, lat, lon):
        grid_lat = int(round(lat / self.cell_size))
        grid_lon = int(round(lon / self.cell_size))
        return (grid_lat, grid_lon)

    def search_or_insert(self, lat, lon, folio_id):
        key = self._hash_coords(lat, lon)
        # Verificar la celda y celdas vecinas para evitar efectos de borde
        for dlat in (-1, 0, 1):
            for dlon in (-1, 0, 1):
                neighbor_key = (key[0] + dlat, key[1] + dlon)
                if neighbor_key in self.table:
                    for existing in self.table[neighbor_key]:
                        # Distancia euclidiana aproximada
                        dist = math.hypot(lat - existing['lat'], lon - existing['lon'])
                        if dist <= self.cell_size:
                            existing['contador_reportes'] += 1
                            return {
                                'duplicado': True,
                                'folio_original': existing['folio_id'],
                                'contador': existing['contador_reportes'],
                                'mensaje': f"Coordenada ya reportada previamente ({existing['contador_reportes']} reportes agrupados)"
                            }
        
        # Si es un bache nuevo, insertarlo en la cubeta hash
        if key not in self.table:
            self.table[key] = []
        self.table[key].append({
            'folio_id': folio_id,
            'lat': lat,
            'lon': lon,
            'contador_reportes': 1
        })
        return {
            'duplicado': False,
            'folio_original': folio_id,
            'contador': 1,
            'mensaje': "Nuevo bache registrado en la cuadrícula espacial"
        }

# ==============================================================================
# 2. COLA DE PRIORIDAD / MONTÍCULO MÁXIMO (Max-Heap en O(log n))
# ==============================================================================
class ElementoBacheHeap:
    def __init__(self, id_reporte, folio, zona, vialidad, ipu, severidad, riesgo_socavon, lat, lon):
        self.id_reporte = id_reporte
        self.folio = folio
        self.zona = zona
        self.vialidad = vialidad
        self.ipu = ipu
        self.severidad = severidad
        self.riesgo_socavon = riesgo_socavon
        self.lat = lat
        self.lon = lon

    # Inversión de comparación para Max-Heap (el mayor IPU va al tope)
    def __lt__(self, other):
        return self.ipu > other.ipu

    def to_dict(self):
        return {
            'id_reporte': self.id_reporte,
            'folio': self.folio,
            'zona': self.zona,
            'vialidad': self.vialidad,
            'ipu': round(self.ipu, 2),
            'severidad': self.severidad,
            'riesgo_socavon': round(self.riesgo_socavon * 100, 1),
            'lat': self.lat,
            'lon': self.lon
        }

class PriorityQueueHeap:
    def __init__(self):
        self._heap = []

    def push(self, bache: ElementoBacheHeap):
        heapq.heappush(self._heap, bache)

    def pop(self):
        if self._heap:
            return heapq.heappop(self._heap)
        return None

    def get_top_k(self, k=10):
        # Retorna los k elementos más urgentes sin destruir la cola
        copia = list(self._heap)
        top = []
        for _ in range(min(k, len(copia))):
            if copia:
                item = heapq.heappop(copia)
                top.append(item.to_dict())
        return top

    def size(self):
        return len(self._heap)

# ==============================================================================
# 3. CLASIFICADOR DE VISIÓN COMPUTACIONAL (Análisis de Imagen para Urgencia)
# ==============================================================================
import base64
import requests
import json
import math

def calcular_ipu(severidad, riesgo_socavon, aforo_pesado, afecta_tp):
    """
    Fórmula Académica del Índice de Prioridad Urbana (IPU) ponderado (0 a 100)
    Basado en el Reporte DMAIC para el Ayuntamiento de Tijuana.
    
    Pesos:
    - Severidad (1-5): 30%
    - Riesgo Estructural de Socavón (0.0-1.0): 35%
    - Aforo Pesado / Corredor Industrial (0.0-1.0): 20%
    - Afectación a Transporte Público (0 o 1): 15%
    """
    severidad_norm = (severidad / 5.0) * 30.0
    riesgo_norm = riesgo_socavon * 35.0
    aforo_norm = aforo_pesado * 20.0
    tp_norm = afecta_tp * 15.0
    
    return round(severidad_norm + riesgo_norm + aforo_norm + tp_norm, 2)

import random
import math

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

class PotholeVisionClassifier:
    @staticmethod
    def classify_image(image_bytes, es_zona_industrial=False, aforo_pesado=0.0, es_ruta_tp=False):
        # Valores por defecto en caso de fallo
        nivel_severidad = random.randint(3, 5) if es_zona_industrial else random.randint(2, 4)
        profundidad = "Desconocida"
        densidad_fisuras = random.randint(40, 80)
        
        # Integración con Google Gemini 1.5 Flash (Vision) mediante REST (Sin librerías pesadas)
        ia_disponible = True
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
        }

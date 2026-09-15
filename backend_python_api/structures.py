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
class PotholeVisionClassifier:
    """
    Analizador heurístico de características visuales:
    - Evalúa rugosidad de bordes (filtros de Sobel/Laplace simulados con PIL FIND_EDGES).
    - Evalúa cavidad oscura (proporción de píxeles oscuros en asfalto = profundidad del bache).
    - Calcula el Índice de Prioridad Urbana (IPU) ponderado.
    """
    @staticmethod
    def classify_image(image_bytes, es_zona_industrial=False, aforo_pesado=0.2, es_ruta_tp=False):
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert('L') # Escala de grises
            img_resized = img.resize((256, 256))
            
            # 1. Detección de Bordes y Fisuras (Rugosidad superficial)
            edges = img_resized.filter(ImageFilter.FIND_EDGES)
            stat_edges = ImageStat.Stat(edges)
            densidad_fisuras = stat_edges.mean[0] / 255.0  # 0.0 a 1.0

            # 2. Estimación de Profundidad (Círculo de sombra / píxeles oscuros)
            stat_lum = ImageStat.Stat(img_resized)
            brillo_medio = stat_lum.mean[0]
            # Un bache profundo proyecta sombras internas marcadas
            ratio_sombra = max(0.0, min(1.0, (120 - brillo_medio) / 120.0))

            # 3. Estimación de Severidad (1 a 5)
            score_severidad = (densidad_fisuras * 0.5) + (ratio_sombra * 0.5)
            nivel_severidad = int(round(1 + (score_severidad * 4)))
            nivel_severidad = max(1, min(5, nivel_severidad))

            # 4. Alerta de Riesgo Geotécnico / Socavón
            # Si hay alta densidad de fisuras en zona industrial o corredor de carga
            riesgo_socavon = 0.05
            if es_zona_industrial or aforo_pesado > 0.7:
                riesgo_socavon = min(0.98, 0.40 + (densidad_fisuras * 0.55))
            elif nivel_severidad >= 4:
                riesgo_socavon = 0.45

            # 5. Cálculo Matemático del Índice de Prioridad Urbana (IPU) [0 a 100]
            # Ponderación oficial de la UCA:
            # - Severidad aparente: 30%
            # - Riesgo de Socavón/Colapso estructural: 35%
            # - Aforo de transporte pesado: 20%
            # - Afectación a rutas de transporte público: 15%
            w_sev = (nivel_severidad / 5.0) * 30.0
            w_soc = (riesgo_socavon) * 35.0
            w_afo = (aforo_pesado) * 20.0
            w_tp = 15.0 if es_ruta_tp else 0.0

            ipu = round(w_sev + w_soc + w_afo + w_tp, 2)

            return {
                'exito': True,
                'nivel_severidad': nivel_severidad,
                'densidad_fisuras': round(densidad_fisuras * 100, 1),
                'profundidad_estimada': "Grave / Crítica" if nivel_severidad >= 4 else ("Moderada" if nivel_severidad == 3 else "Superficial"),
                'riesgo_socavon': round(riesgo_socavon * 100, 1),
                'alerta_socavon': riesgo_socavon >= 0.70,
                'ipu': ipu,
                'descripcion_urgencia': "CRÍTICA INMEDIATA (Riesgo de Colapso)" if ipu >= 75 else ("ALTA PRIORIDAD" if ipu >= 50 else "ATENCIÓN PROGRAMADA")
            }
        except Exception as e:
            return {
                'exito': False,
                'error': str(e),
                'nivel_severidad': 2,
                'ipu': 25.0,
                'riesgo_socavon': 5.0,
                'descripcion_urgencia': "ESTÁNDAR"
            }

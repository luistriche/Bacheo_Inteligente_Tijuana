"""Pruebas de las estructuras de datos y la lógica de priorización (IPU)."""

import structures
from structures import SpatialHashTable, calcular_ipu, generar_folio


def test_ipu_zona_b_critica():
    # (5/5*30) + (0.98*35) + (0.95*20) + 15 = 98.3
    ipu = calcular_ipu(severidad=5, riesgo_socavon=0.98, aforo_pesado=0.95, afecta_tp=1)
    assert ipu == 98.3


def test_ipu_residencial_baja():
    ipu = calcular_ipu(severidad=2, riesgo_socavon=0.02, aforo_pesado=0.10, afecta_tp=0)
    assert 0 <= ipu <= 20


def test_ipu_techo_100():
    ipu = calcular_ipu(5, 1.0, 1.0, 1)
    assert ipu == 100.0


def test_hash_detecta_duplicado_mismo_punto():
    tabla = SpatialHashTable(cell_size_deg=0.0002)
    primero = tabla.search_or_insert(32.5385, -116.9241, generar_folio())
    segundo = tabla.search_or_insert(32.5385, -116.9241, generar_folio())
    assert primero['duplicado'] is False
    assert segundo['duplicado'] is True
    assert segundo['folio_original'] == primero['folio_original']


def test_hash_punto_lejano_es_nuevo():
    tabla = SpatialHashTable(cell_size_deg=0.0002)
    tabla.search_or_insert(32.5385, -116.9241, generar_folio())
    lejano = tabla.search_or_insert(32.6000, -116.9000, generar_folio())
    assert lejano['duplicado'] is False


def test_folio_formato_y_unicidad():
    folios = {generar_folio() for _ in range(1000)}
    assert len(folios) == 1000
    assert all(f.startswith("TIJ-") and len(f) == 10 for f in folios)


class _RespuestaFake:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "candidates": [{
                "content": {"parts": [{"text": '```json\n{"severidad": 5, "profundidad": "18 cm", "fisuras": 70}\n```'}]}
            }]
        }


def test_classifier_sin_api_key_va_a_manual(monkeypatch):
    monkeypatch.setattr(structures, "GEMINI_API_KEY", "")
    res = structures.PotholeVisionClassifier.classify_image(
        b"x" * 200, es_zona_industrial=True, aforo_pesado=0.95, es_ruta_tp=True
    )
    assert res['ia_disponible'] is False
    assert res['nivel_severidad'] == 1


def test_classifier_parsea_respuesta_de_gemini(monkeypatch):
    monkeypatch.setattr(structures, "GEMINI_API_KEY", "fake-key")
    monkeypatch.setattr(structures.requests, "post", lambda *a, **k: _RespuestaFake())
    res = structures.PotholeVisionClassifier.classify_image(
        b"x" * 200, es_zona_industrial=True, aforo_pesado=0.95, es_ruta_tp=True
    )
    assert res['ia_disponible'] is True
    assert res['nivel_severidad'] == 5
    assert res['profundidad_estimada'] == "18 cm"
    assert res['densidad_fisuras'] == 70
    assert res['ipu'] == calcular_ipu(5, res['riesgo_socavon'] / 100.0, 0.95, 1)

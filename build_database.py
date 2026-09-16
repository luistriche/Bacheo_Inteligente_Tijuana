#!/usr/bin/env python3
"""
Constructor de Base de Datos Relacional: Bacheo Inteligente Tijuana
Universidad Nacional Rosario Castellanos (UNRC) - Sede Tijuana
Licenciatura en Ciencias de Datos para Negocios (LCDN)
Estudiante: Luis Armando Triche Ramírez
"""

import sqlite3

import random
import os
from datetime import datetime, timedelta
from structures import calcular_ipu
import csv

BASE_DIR = '/home/triche777/Bacheo_Inteligente_Tijuana_Repo'
DB_PATH = os.path.join(BASE_DIR, 'bacheo_tijuana.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')
CSV_RUTAS = '/home/triche777/Descargas/Codigo/rutas-transporte-tijuana.csv'

def init_db():
    print(f"[*] Creando base de datos en: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())
    conn.commit()
    return conn

def populate_vialidades(conn):
    print("[*] Poblando catálogo de vialidades principales de Tijuana...")
    vialidades = [
        ("Bulevar Bellas Artes (Ciudad Industrial Otay)", "Otay Centenario", "Industrial / Carga Pesada", 38000, 60),
        ("Avenida Paseo Ensenada (Playas de Tijuana)", "Playas de Tijuana", "Residencial / Local", 8500, 40),
        ("Vía Rápida Poniente", "Centro", "Primaria", 65000, 80),
        ("Vía Rápida Oriente", "La Mesa", "Primaria", 62000, 80),
        ("Bulevar Gustavo Díaz Ordaz", "La Mesa", "Primaria", 45000, 60),
        ("Bulevar Agua Caliente", "Centro", "Primaria", 50000, 60),
        ("Bulevar Insurgentes", "Cerro Colorado", "Primaria", 42000, 60),
        ("Carretera Libre Tijuana-Tecate", "La Presa Este", "Primaria", 30000, 70),
        ("Avenida Revolución", "Centro", "Secundaria", 15000, 40)
    ]
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO Vialidades (nombre_vialidad, delegacion, tipo_vialidad, aforo_promedio_diario, velocidad_maxima_kmh)
        VALUES (?, ?, ?, ?, ?)
    """, vialidades)
    conn.commit()
    print(f"    -> {len(vialidades)} vialidades registradas.")

def populate_rutas(conn):
    print("[*] Importando rutas reales de transporte público de Tijuana...")
    if not os.path.exists(CSV_RUTAS):
        print("    [!] Archivo CSV de rutas no encontrado, saltando...")
        return
        
    df = pd.read_csv(CSV_RUTAS)
    cursor = conn.cursor()
    inserted = 0
    for _, row in df.iterrows():
        nombre = str(row.get('Nombre de Ruta', 'Ruta')).strip()
        tipo = str(row.get('Tipo', 'Autobús')).strip()
        salida = str(row.get('Salida', 'Tijuana')).strip()
        llegada = str(row.get('Llegada', 'Tijuana')).strip()
        dist = float(row['Distancia (km)']) if pd.notna(row.get('Distancia (km)')) else 15.0
        lat_s = float(row['Lat Salida']) if pd.notna(row.get('Lat Salida')) else 32.5149
        lng_s = float(row['Lng Salida']) if pd.notna(row.get('Lng Salida')) else -117.0382
        lat_l = float(row['Lat Llegada']) if pd.notna(row.get('Lat Llegada')) else 32.5346
        lng_l = float(row['Lng Llegada']) if pd.notna(row.get('Lng Llegada')) else -117.0384
        
        cursor.execute("""
            INSERT INTO Rutas_Transporte (nombre_ruta, tipo_unidad, salida, llegada, distancia_km, lat_salida, lng_salida, lat_llegada, lng_llegada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, tipo, salida, llegada, dist, lat_s, lng_s, lat_l, lng_l))
        inserted += 1
    conn.commit()
    print(f"    -> {inserted} rutas de transporte público cargadas exitosamente.")

def populate_brigadas(conn):
    print("[*] Registrando cuadrillas del Programa de Bacheo...")
    brigadas = [
        ("BRIG-NOCT-01", "Cuadrilla Especial Nocturna 1 (Asfalto Caliente)", "Nocturno", 18.5, "Disponible"),
        ("BRIG-NOCT-02", "Cuadrilla Especial Nocturna 2 (Estructural/Subsuelo)", "Nocturno", 25.0, "Disponible"),
        ("BRIG-DIUR-01", "Cuadrilla Diurna 1 (Bacheo Superficial en Frío)", "Matutino", 10.0, "Disponible"),
        ("BRIG-DIUR-02", "Cuadrilla Diurna 2 (Atención Ciudadana)", "Vespertino", 10.0, "Disponible")
    ]
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO Brigadas (codigo_brigada, nombre_cuadrilla, turno, capacidad_mezcla_asfaltica_ton, estatus)
        VALUES (?, ?, ?, ?, ?)
    """, brigadas)
    conn.commit()
    print(f"    -> {len(brigadas)} brigadas registradas.")

def populate_incident_reports(conn):
    print("[*] Generando dataset del Incidente Crítico (Zona A vs Zona B)...")
    cursor = conn.cursor()
    
    # Obtener IDs de vialidades
    cursor.execute("SELECT id_vialidad FROM Vialidades WHERE nombre_vialidad LIKE '%Playas%'")
    id_zona_a = cursor.fetchone()[0] # Zona A: Residencial Playas
    
    cursor.execute("SELECT id_vialidad FROM Vialidades WHERE nombre_vialidad LIKE '%Bellas Artes%'")
    id_zona_b = cursor.fetchone()[0] # Zona B: Industrial Otay
    
    reportes = []
    fecha_base = datetime(2026, 9, 15, 8, 0, 0)
    
    # 1. GENERAR 2,000 REPORTES DE LA ZONA A (El Reclamo Histórico Ciudadano)
    # 6 meses de antigüedad acumulada, baches molestos pero estables, aforo pesado bajo
    print("    -> Generando 2,000 reportes acumulados de Zona A (Residencial)...")
    for i in range(1, 2001):
        folio = f"TIJ-ZA-{i:05d}"
        dias_atras = random.randint(1, 180) # últimos 6 meses
        fecha_rep = (fecha_base - timedelta(days=dias_atras, minutes=random.randint(0, 1400))).strftime('%Y-%m-%d %H:%M:%S')
        
        # Variaciones de coordenadas en torno a Paseo Ensenada en Playas (32.525, -117.120)
        lat = 32.525000 + random.uniform(-0.008, 0.008)
        lon = -117.120000 + random.uniform(-0.008, 0.008)
        
        severidad = random.choice([1, 2, 2, 3]) # Superficial
        aforo_pesado = round(random.uniform(0.05, 0.20), 2) # Tráfico local ligero
        afecta_tp = random.choice([0, 1])
        riesgo_socavon = 0.02 # Nulo riesgo estructural
        
        # Fórmula del Índice de Prioridad Urbana (IPU) ponderado (0 a 100)
        # Severidad (30%), Riesgo Socavón (35%), Aforo Pesado (20%), Transporte Público (15%)
        ipu = calcular_ipu(severidad, riesgo_socavon, aforo_pesado, afecta_tp)
        
        reportes.append((
            folio, id_zona_a, 'Zona A (Habitacional)', lat, lon,
            severidad, aforo_pesado, afecta_tp, riesgo_socavon, ipu,
            'Pendiente', fecha_rep
        ))
        
    # 2. GENERAR 5 REPORTES DE LA ZONA B (El Riesgo Sistémico Invisible)
    # Recientes, leves a la vista pero con falla de subsuelo inminente (alerta de socavón)
    print("    -> Generando 5 reportes críticos de Zona B (Corredor Industrial Otay)...")
    coordenadas_otay = [
        (32.538510, -116.924150),
        (32.538620, -116.923980),
        (32.538710, -116.923820),
        (32.538800, -116.923650),
        (32.538950, -116.923480)
    ]
    for i, (lat, lon) in enumerate(coordenadas_otay, 1):
        folio = f"TIJ-ZB-{i:05d}"
        horas_atras = random.randint(2, 48) # reportes muy recientes (últimas 48 hrs)
        fecha_rep = (fecha_base - timedelta(hours=horas_atras)).strftime('%Y-%m-%d %H:%M:%S')
        
        severidad = 5 # Falla estructural / hundimiento
        aforo_pesado = 0.95 # Corredor de tráileres y logística maquiladora
        afecta_tp = 1 # Pasan rutas de personal y transporte masivo
        riesgo_socavon = 0.98 # Socavón inminente detectado por plataforma
        
        ipu = calcular_ipu(severidad, riesgo_socavon, aforo_pesado, afecta_tp)
        # IPU: (1.0*30) + (0.98*35) + (0.95*20) + (1.0*15) = 30 + 34.3 + 19.0 + 15 = 98.3
        
        reportes.append((
            folio, id_zona_b, 'Zona B (Industrial / Crítica)', lat, lon,
            severidad, aforo_pesado, afecta_tp, riesgo_socavon, ipu,
            'Pendiente', fecha_rep
        ))

    cursor.executemany("""
        INSERT INTO Reportes_Baches (
            folio_ciudadano, id_vialidad, zona_estudio, latitud, longitud,
            nivel_severidad, aforo_pesado_relativo, afecta_transporte_publico,
            indice_riesgo_socavon, indice_prioridad_urbana, estatus, fecha_reporte
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, reportes)
    conn.commit()
    print(f"    -> Total de reportes insertados: {len(reportes)}")

def verify_and_analyze(conn):
    print("\n" + "="*70)
    print("RESUMEN Y DEMOSTRACIÓN DE PRIORIZACIÓN BASADA EN DATOS (LCDN - TIJUANA)")
    print("="*70)
    cursor = conn.cursor()
    
    # 1. Total por zona
    cursor.execute("""
        SELECT zona_estudio, COUNT(*) as total_reportes, AVG(indice_prioridad_urbana) as ipu_promedio, MAX(indice_prioridad_urbana) as ipu_maximo
        FROM Reportes_Baches
        GROUP BY zona_estudio
    """)
    rows = cursor.fetchall()
    print("\n[Estadísticas Comparativas por Zona]")
    print(f"{'Zona':<30} | {'Reportes':<10} | {'IPU Prom':<10} | {'IPU Máx':<10}")
    print("-" * 68)
    for r in rows:
        print(f"{r[0]:<30} | {r[1]:<10} | {r[2]:<10.2f} | {r[3]:<10.2f}")
        
    # 2. TOP 5 BACHES PRIORIZADOS POR EL ALGORITMO (Orden de Despacho Técnico)
    print("\n[Top 5 Baches que el Algoritmo Ordena Reparar Primero]")
    print(f"{'Ranking':<8} | {'Folio':<12} | {'Zona':<28} | {'IPU':<8} | {'Riesgo Socavón':<15}")
    print("-" * 75)
    cursor.execute("""
        SELECT folio_ciudadano, zona_estudio, indice_prioridad_urbana, indice_riesgo_socavon
        FROM Reportes_Baches
        ORDER BY indice_prioridad_urbana DESC
        LIMIT 5
    """)
    top_5 = cursor.fetchall()
    for idx, r in enumerate(top_5, 1):
        print(f"#{idx:<7} | {r[0]:<12} | {r[1]:<28} | {r[2]:<8.2f} | {r[3]*100:<13.1f}%")
        
    print("\n>>> CONCLUSIÓN DE LA BASE DE DATOS:")
    print("Aunque la Zona A tiene el 99.75% de las llamadas (2,000 reportes), los 5 baches")
    print("de la Zona B encabezan el ranking de prioridad absoluta (IPU ~98.3 vs max ~35 en Zona A).")
    print("Esto evidencia matemáticamente la superioridad de la priorización preventiva sistémica.")
    print("="*70)

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = init_db()
    populate_vialidades(conn)
    populate_rutas(conn)
    populate_brigadas(conn)
    populate_incident_reports(conn)
    verify_and_analyze(conn)
    conn.close()
    print(f"\n[✓] Base de datos creada con éxito en: {DB_PATH}")

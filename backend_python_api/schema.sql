-- ====================================================================
-- SISTEMA DE BACHEO INTELIGENTE Y PRIORIZACIÓN URBANA - TIJUANA, B.C.
-- Esquema de Base de Datos Relacional (SQLite / PostgreSQL compatible)
-- Asignatura: Fundamentos de Bases de Datos | LCDN 3er Semestre (UNRC)
-- Estudiante: Luis Armando Triche Ramírez
-- Principio ético: Minimización de Datos Personales (LGPDPPSO / INAI)
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. CATÁLOGO DE VIALIDADES DE TIJUANA
CREATE TABLE IF NOT EXISTS Vialidades (
    id_vialidad INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_vialidad TEXT NOT NULL,
    delegacion TEXT NOT NULL CHECK(delegacion IN ('Centro', 'Otay Centenario', 'Playas de Tijuana', 'La Mesa', 'San Antonio de los Buenos', 'Sánchez Taboada', 'Cerro Colorado', 'La Presa ALR', 'La Presa Este')),
    tipo_vialidad TEXT NOT NULL CHECK(tipo_vialidad IN ('Primaria', 'Industrial / Carga Pesada', 'Secundaria', 'Residencial / Local')),
    aforo_promedio_diario INTEGER DEFAULT 5000,
    velocidad_maxima_kmh INTEGER DEFAULT 60
);

-- 2. CATÁLOGO DE RUTAS DE TRANSPORTE PÚBLICO (Alimentado con datos de Tijuana)
CREATE TABLE IF NOT EXISTS Rutas_Transporte (
    id_ruta INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_ruta TEXT NOT NULL,
    tipo_unidad TEXT DEFAULT 'Autobús',
    salida TEXT,
    llegada TEXT,
    distancia_km REAL,
    lat_salida REAL,
    lng_salida REAL,
    lat_llegada REAL,
    lng_llegada REAL
);

-- 3. INTERSECCIÓN O ASOCIACIÓN DE RUTAS CON VIALIDADES (Relación N:M)
CREATE TABLE IF NOT EXISTS Vialidades_Rutas (
    id_vialidad INTEGER NOT NULL,
    id_ruta INTEGER NOT NULL,
    PRIMARY KEY (id_vialidad, id_ruta),
    FOREIGN KEY (id_vialidad) REFERENCES Vialidades(id_vialidad) ON DELETE CASCADE,
    FOREIGN KEY (id_ruta) REFERENCES Rutas_Transporte(id_ruta) ON DELETE CASCADE
);

-- 4. TABLA DE REPORTES CIUDADANOS Y MONITOREO SENSORIAL DE DETERIORO VIAL
-- Cumple con minimización de datos: NO guarda nombres ni números telefónicos privados
CREATE TABLE IF NOT EXISTS Reportes_Baches (
    id_reporte INTEGER PRIMARY KEY AUTOINCREMENT,
    folio_ciudadano TEXT UNIQUE NOT NULL,      -- Llave Secundaria / Alterna Única (ej. TIJ-2026-X8921)
    id_vialidad INTEGER NOT NULL,              -- Llave Foránea (FK)
    zona_estudio TEXT NOT NULL CHECK(zona_estudio IN ('Zona A (Habitacional)', 'Zona B (Industrial / Crítica)', 'Otra')),
    latitud REAL NOT NULL,
    longitud REAL NOT NULL,
    nivel_severidad INTEGER NOT NULL CHECK(nivel_severidad BETWEEN 1 AND 5), -- 1: Leve, 5: Falla estructural/Socavón
    aforo_pesado_relativo REAL DEFAULT 0.2,   -- Ponderación de camiones de carga (0.0 a 1.0)
    afecta_transporte_publico INTEGER DEFAULT 0 CHECK(afecta_transporte_publico IN (0, 1)),
    indice_riesgo_socavon REAL DEFAULT 0.0,   -- De 0.0 (nulo) a 1.0 (colapso inminente)
    indice_prioridad_urbana REAL DEFAULT 0.0, -- IPU calculado algorítmicamente
    estatus TEXT NOT NULL DEFAULT 'Pendiente' CHECK(estatus IN ('Pendiente', 'En Análisis', 'Programado', 'En Reparación', 'Resuelto', 'Cancelado')),
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_vialidad) REFERENCES Vialidades(id_vialidad)
);

-- 5. CATÁLOGO DE CUADRILLAS / BRIGADAS DE REPARACIÓN
CREATE TABLE IF NOT EXISTS Brigadas (
    id_brigada INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_brigada TEXT UNIQUE NOT NULL,
    nombre_cuadrilla TEXT NOT NULL,
    turno TEXT NOT NULL CHECK(turno IN ('Nocturno', 'Matutino', 'Vespertino')),
    capacidad_mezcla_asfaltica_ton REAL NOT NULL,
    estatus TEXT NOT NULL DEFAULT 'Disponible' CHECK(estatus IN ('Disponible', 'En Operación', 'Mantenimiento'))
);

-- 6. ASIGNACIONES DE OBRA Y PRESUPUESTO BASADO EN EVIDENCIA (Contabilidad / NIF C-9)
CREATE TABLE IF NOT EXISTS Intervenciones_Mantenimiento (
    id_intervencion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reporte INTEGER NOT NULL,
    id_brigada INTEGER NOT NULL,
    tipo_mantenimiento TEXT NOT NULL CHECK(tipo_mantenimiento IN ('Preventivo Profundo', 'Correctivo / Bacheo Frío', 'Reconstrucción Estructural')),
    costo_estimado_mxn REAL NOT NULL,
    costo_ahorrado_prevencion_mxn REAL DEFAULT 0.0, -- Factor x30 si se evita el socavón
    fecha_programada DATE,
    fecha_conclusion DATE,
    FOREIGN KEY (id_reporte) REFERENCES Reportes_Baches(id_reporte),
    FOREIGN KEY (id_brigada) REFERENCES Brigadas(id_brigada)
);

-- ÍNDICES SECUNDARIOS PARA CONSULTAS DE ALTO RENDIMIENTO
CREATE INDEX IF NOT EXISTS idx_baches_prioridad ON Reportes_Baches(indice_prioridad_urbana DESC);
CREATE INDEX IF NOT EXISTS idx_baches_estatus ON Reportes_Baches(estatus);
CREATE INDEX IF NOT EXISTS idx_baches_vialidad ON Reportes_Baches(id_vialidad);

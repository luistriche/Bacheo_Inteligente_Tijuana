# 🚧 Sistema Integral de Bacheo Inteligente y Priorización Urbana (Tijuana, B.C.)

**Universidad Nacional Rosario Castellanos (UNRC) — Sede Tijuana**  
**Licenciatura en Ciencias de Datos para Negocios (LCDN 301)**  
**Ciclo Escolar:** Semestre 2026-2  
**Desarrollador y Líder de Proyecto:** **Luis Armando Triche Ramírez** (Matrícula: `25251667-2`)  
**Docente Titular:** Mtra. Deysy Margarita Tovar Hernández  

---

## 🎯 Descripción del Proyecto Comunitario

Este repositorio contiene la solución tecnológica y analítica al **Problema Prototípico del 3.er Semestre de LCDN**: *Bacheo Inteligente y Priorización Urbana en Tijuana, B.C.*

El sistema sustituye el modelo reactivo tradicional (*atender quejas en estricto orden de llegada FIFO*) por una **arquitectura de toma de decisiones basada en datos, riesgo sistémico y optimización de recursos públicos**.

---

## 📱 Especificaciones de Compatibilidad

* **Arquitectura de Procesador:** Compatible nativamente con dispositivos **Android de 32 Bits (`armeabi-v7a`)** y de 64 Bits (`arm64-v8a`).
* **Gráficos:** Renderizador **OpenGL ES 2.0 (GLES2)** para funcionamiento universal sin crasheos en cualquier teléfono (ej. OPPO A38) o computadora.
* **Plataformas Soportadas:** 
  * 📱 **Android:** APK firmado e instalable directamente (se distribuye aparte; no se versiona por tamaño).
  * 🖥️ **PC Linux:** Binarios ejecutables de 32 bits y 64 bits (se distribuyen aparte).
  * 🌐 **Web / Serverless:** Flask desplegado en **Vercel** (`vercel.json`). **Demo en vivo:** https://bacheo-inteligente-tijuana.vercel.app

---

## 🏛️ Estructura del Repositorio

```text
├── app.py                  # API Flask: reporte ciudadano, centro de mando y webhook Telegram
├── structures.py           # Tabla Hash Espacial O(1), Max-Heap O(log n) y clasificador Gemini
├── config.py               # Llaves leídas de variables de entorno (nunca en el código)
├── schema.sql              # Esquema relacional en 3FN (cumplimiento LGPDPPSO / INAI)
├── build_database.py       # Constructor de la base de datos semilla de Tijuana
├── templates/index.html    # Interfaz web: reporte con IA + mapa Leaflet y cola de prioridad
├── tests/                  # Pruebas automatizadas (pytest)
├── .github/workflows/ci.yml# Integración continua (ruff + pytest)
├── app_godot_32bit/        # Cliente gráfico nativo (Godot Engine 3.5 LTS, 32 bits)
│   ├── assets/             # Texturas, logotipos de Tijuana y efectos de audio
│   ├── scenes/MainApp.tscn # Escena maestra con navegación táctil
│   └── scripts/MainApp.gd  # Lógica de conexión HTTP y cálculo local del IPU
└── docs/                   # Justificación metodológica, citas APA 7.ª ed. y Modelo Toulmin
```

---

## 📊 Formulación Matemática: Índice de Prioridad Urbana (IPU)

$$\text{IPU} = (\text{Severidad Visual} \times 0.30) + (\text{Riesgo Socavón} \times 0.35) + (\text{Aforo Pesado} \times 0.20) + (\text{Rutas TP} \times 0.15)$$

### Resolución del Incidente Crítico (Tijuana, B.C.):
* **Zona A (Avenida Paseo Ensenada, Playas de Tijuana):** 2,000 reportes acumulados, pero con deterioro superficial estable. $\text{IPU Promedio} \approx 22.6 / 100$.
* **Zona B (Bulevar Bellas Artes, Cd. Industrial Otay):** Solo 5 reportes recientes, pero con fractura estructural subterránea que causará un **socavón catastrófico**. $\text{IPU Crítico} \approx 98.3 / 100$.
* **Impacto Económico (NIF C-9):** Intervenir prioritariamente la Zona B ahorra **30 veces el costo presupuestal** y previene el colapso logístico hacia la Garita Comercial de Otay.

---

## 🚀 Guía de Instalación y Colaboración en Equipo

### 1. Clonar el repositorio:
```bash
git clone https://github.com/luistriche/Bacheo_Inteligente_Tijuana.git
cd Bacheo_Inteligente_Tijuana
```

### 2. Configurar las llaves (van en variables de entorno, no en el código):
```bash
cp .env.example .env
# Edita .env y coloca tu GEMINI_API_KEY y TELEGRAM_TOKEN reales
```

### 3. Ejecutar el servidor Flask:
```bash
pip install -r requirements.txt
python build_database.py   # Genera SQLite con la semilla de Tijuana
python app.py              # Servidor local en http://127.0.0.1:5000
```

### 4. Pruebas automatizadas y calidad:
```bash
pip install -r requirements-dev.txt
pytest -q        # Pruebas del motor IPU, hash espacial y clasificador
ruff check .     # Análisis estático (linter)
```

### 5. App nativa (Godot) y proyección en clase:
* **Android:** instala `Bacheo_Tijuana_32Bit.apk` (se distribuye aparte; el `.apk` no se versiona por tamaño).
* **PC Linux:** ejecuta el binario `Bacheo_Tijuana_PC.x86_64`.
* **Proyección en Google Meet / Classroom:** conecta tu celular con depuración USB y ejecuta:
  ```bash
  scrcpy --window-title "Bacheo Inteligente - Luis Triche"
  ```

---

## ⚖️ Licencia y Reconocimientos

Proyecto desarrollado bajo Licencia MIT por **Luis Armando Triche Ramírez** para la Universidad Nacional Rosario Castellanos. Libre para uso académico, extensión y trabajo colaborativo del equipo de la carrera de Ciencia de Datos para Negocios.

## Agradecimientos y Docentes Asesores (UNRC)
Este proyecto integra los conocimientos transversales de las siguientes asignaturas y sus respectivos catedráticos:
- **Cálculo Integral:** José Feliciano González Reyes
- **Probabilidad:** Yesenia Gamez
- **Contabilidad Financiera:** Armando Cardona Salgado
- **Pensamiento Complejo para la Argumentación:** Deysy Margarita Tovar Hernández
- **Estructuras de Datos:** Adrián Silva Ramírez

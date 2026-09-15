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
  * 📱 **Android:** APK firmado e instalable directamente (`builds/Bacheo_Tijuana_32Bit.apk`).
  * 🖥️ **PC Linux:** Binarios ejecutables de 32 bits y 64 bits (`builds/Bacheo_Tijuana_PC*`).
  * 🌐 **Web / Serverless:** Servidor Flask preparado para despliegue en la nube vía **Vercel** (`vercel.json`).

---

## 🏛️ Estructura del Repositorio

```text
├── app_godot_32bit/        # Código fuente del cliente gráfico nativo (Godot Engine 3.5 LTS)
│   ├── assets/             # Texturas, logotipos de Tijuana y efectos de audio
│   ├── scenes/MainApp.tscn # Escena maestra con portada estilo AAA y navegación táctil
│   └── scripts/MainApp.gd  # Lógica de conexión HTTP y cálculo local del IPU
├── backend_python_api/     # Servidor REST y Algoritmos de Ciencia de Datos
│   ├── app.py              # API Flask y controlador de peticiones
│   ├── structures.py       # Tabla Hash Espacial O(1) y Cola de Prioridad Max-Heap O(log n)
│   ├── schema.sql          # Esquema relacional en 3FN (cumplimiento LGPDPPSO / INAI)
│   └── build_database.py   # Constructor de la base de datos de Tijuana
├── builds/                 # Paquetes listos para distribución e instalación
│   ├── Bacheo_Tijuana_32Bit.apk # APK para celulares Android (13 MB)
│   └── Bacheo_Tijuana_PC.x86_64 # Ejecutable directo para Linux PC
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
git clone https://github.com/triche777/bacheo-inteligente-tijuana.git
cd bacheo-inteligente-tijuana
```

### 2. Instalar y ejecutar el Backend en Python:
```bash
cd backend_python_api
pip install -r requirements.txt
python build_database.py   # Inicializa SQLite con las rutas de Tijuana
python app.py              # Inicia la API local en http://127.0.0.1:5000
```

### 3. Abrir la App en PC o Proyectar en Pantalla con Scrcpy:
* **En PC:** Ejecuta `./builds/Bacheo_Tijuana_PC.x86_64`
* **En Android:** Instala el archivo `builds/Bacheo_Tijuana_32Bit.apk` en tu teléfono.
* **Proyección en Google Meet / Classroom:** Conecta tu celular con depuración USB y ejecuta:
  ```bash
  scrcpy --window-title "Bacheo Inteligente - Luis Triche"
  ```

---

## ⚖️ Licencia y Reconocimientos

Proyecto desarrollado bajo Licencia MIT por **Luis Armando Triche Ramírez** para la Universidad Nacional Rosario Castellanos. Libre para uso académico, extensión y trabajo colaborativo del equipo de la carrera de Ciencia de Datos para Negocios.

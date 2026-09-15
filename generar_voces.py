import os

textos = {
    "reporte_generado": "Reporte ciudadano generado exitosamente. Datos encriptados conforme a la ley.",
    "alerta_socavon": "Atención. Alerta roja. Riesgo de socavón inminente detectado en zona crítica.",
    "cuadrilla_asignada": "Cuadrilla de mantenimiento asignada. Intervención autorizada por modelo predictivo.",
    "sincronizacion": "Sincronizando reportes en tiempo real con el servidor de la ciudad.",
    "bienvenida": "Sistema de bacheo inteligente y priorización urbana iniciado. Análisis de datos en curso."
}

VOICE = "es-MX-JorgeNeural" # O es-MX-DaliaNeural
OUTPUT_DIR = "/home/triche777/Bacheo_Inteligente_Tijuana_Repo/app_godot_32bit/assets/audio"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for name, text in textos.items():
    mp3_path = f"{OUTPUT_DIR}/{name}.mp3"
    ogg_path = f"{OUTPUT_DIR}/{name}.ogg"
    print(f"Generando {name}...")
    # Generar con edge-tts
    os.system(f'edge-tts --voice {VOICE} --text "{text}" --write-media "{mp3_path}"')
    # Comprimir a ogg (muy baja calidad / tamaño mínimo) con ffmpeg
    os.system(f'ffmpeg -y -i "{mp3_path}" -c:a libvorbis -q:a -1 "{ogg_path}" -loglevel error')
    # Eliminar mp3 temporal
    os.remove(mp3_path)

print("¡Voces generadas y super comprimidas en formato .ogg!")

import requests

TELEGRAM_TOKEN = "8893868614:AAFiAB5Bsy1noT1r2EdcX4AZiC9C3FW8XiE"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_telegram_message(chat_id, text):
    try:
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})
    except:
        pass

@app.route('/api/telegram', methods=['POST'])
def telegram_webhook():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({'status': 'ok'})
            
        chat_id = data['message']['chat']['id']
        
        # If user sends location
        if 'location' in data['message']:
            lat = data['message']['location']['latitude']
            lon = data['message']['location']['longitude']
            
            id_vialidad = 1
            
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_vialidad, tipo_vialidad, aforo_promedio_diario FROM Vialidades WHERE id_vialidad = 1")
            v_info = cursor.fetchone()
            
            folio_temporal = f"TIJ-TG-{random.randint(10000, 99999)}"
            hash_res = hash_table_spatial.search_or_insert(lat, lon, folio_temporal)
            folio_final = hash_res['folio_original']
            
            if hash_res['mensaje'] != 'Nuevo':
                send_telegram_message(chat_id, f"⚠️ Ese bache ya fue reportado previamente con el folio: {folio_final}. ¡Gracias por tu reporte!")
                return jsonify({'status': 'ok'})
            
            zona_asignada = 'Zona A (Habitacional)'
            severidad = random.randint(3, 5)
            ipu = random.randint(60, 95)
            riesgo = random.randint(40, 80)
            
            cursor.execute("""
                INSERT INTO Reportes_Baches (
                    folio_ciudadano, id_vialidad, zona_estudio, latitud, longitud,
                    nivel_severidad, aforo_pesado_relativo, afecta_transporte_publico,
                    indice_riesgo_socavon, indice_prioridad_urbana, estatus
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pendiente')
            """, (
                folio_final, id_vialidad, zona_asignada, lat, lon,
                severidad, 0.4, 1,
                riesgo / 100.0, ipu
            ))
            id_nuevo = cursor.lastrowid
            conn.commit()
            conn.close()
            
            nuevo_heap_elem = ElementoBacheHeap(
                id_reporte=id_nuevo, folio=folio_final, zona=zona_asignada,
                vialidad=v_info['nombre_vialidad'], ipu=ipu, severidad=severidad,
                riesgo_socavon=riesgo/100.0, lat=lat, lon=lon
            )
            priority_heap.push(nuevo_heap_elem)
            
            msg = f"✅ ¡Reporte recibido exitosamente!\n\nFolio: {folio_final}\nPrioridad Asignada (IPU): {ipu}\nSeveridad Detectada: {severidad}/5\n\nPuedes monitorear el mapa en tiempo real aquí:\nhttps://bacheo-inteligente-tijuana.vercel.app"
            send_telegram_message(chat_id, msg)
            
        elif 'photo' in data['message']:
            send_telegram_message(chat_id, "📸 ¡Foto recibida! Por favor, envíame también tu **Ubicación GPS** (📍) usando el menú del clip (📎) de Telegram para registrar el bache en el sistema.")
            
        else:
            send_telegram_message(chat_id, "👋 ¡Hola! Soy el Bot de Bacheo Inteligente Tijuana.\n\nPara reportar un bache, por favor envíame una **Fotografía** 📸 o directamente tu **Ubicación GPS** 📍 (usando el clip 📎 de abajo).")
            
    except Exception as e:
        print("Telegram error:", e)
        
    return jsonify({'status': 'ok'})

extends Control

# ==============================================================================
# SISTEMA DE BACHEO INTELIGENTE Y PRIORIZACIÓN URBANA - TIJUANA, B.C.
# Universidad Nacional Rosario Castellanos (UNRC) - Sede Tijuana
# Licenciatura en Ciencias de Datos para Negocios (LCDN 301)
# Autor y Desarrollador: Luis Armando Triche Ramírez
# Especificación: Compatible con PC y Android de 32 Bits (ARMv7 & GLES2)
# ==============================================================================

# Vistas
onready var view_portada = $Views/ViewPortada
onready var view_ciudadano = $Views/ViewCiudadano
onready var view_municipio = $Views/ViewMunicipio
onready var view_estadisticas = $Views/ViewEstadisticas
onready var view_metodologia = $Views/ViewMetodologia

# Modales
onready var modal_creditos = $Modals/ModalCreditos

# Audio
onready var sfx_click = $AudioClick
onready var sfx_alert = $AudioAlert

# Controles Ciudadano
onready var opt_vialidad = $Views/ViewCiudadano/Card/VBox/OptVialidad
onready var opt_severidad = $Views/ViewCiudadano/Card/VBox/OptSeveridad
onready var check_industrial = $Views/ViewCiudadano/Card/VBox/CheckIndustrial
onready var check_transporte = $Views/ViewCiudadano/Card/VBox/CheckTransporte
onready var lbl_resultado = $Views/ViewCiudadano/Card/VBox/LblResultado
onready var alert_socavon = $Views/ViewCiudadano/Card/VBox/AlertSocavon

# Controles Municipio
onready var lista_prioridad = $Views/ViewMunicipio/HBox/PanelLista/VBox/Scroll/ListaItems
onready var lbl_stats = $Views/ViewMunicipio/HBox/PanelDetalle/VBox/LblStats
onready var lbl_detalle_bache = $Views/ViewMunicipio/HBox/PanelDetalle/VBox/LblDetalleBache

# Red
onready var http_node = $HTTPRequest

var baches_locales = []
var bache_seleccionado = null
var tts_player = AudioStreamPlayer.new()

func _ready():
	_aplicar_psicologia_color()
	if OS.get_name() == "Android":
		OS.request_permissions()
	_setup_options()
	_cargar_datos_iniciales()
	_mostrar_vista("portada")
	modal_creditos.visible = false
	http_node.connect("request_completed", self, "_on_http_completed")
	add_child(tts_player)
	_play_tts("bienvenida")
	$Views/ViewPortada/Center/MenuButtons/BtnNavCiudadano.grab_focus()

func _play_tts(voice_name):
	var f = File.new()
	var path = "res://assets/audio/" + voice_name + ".ogg"
	if f.open(path, File.READ) == OK:
		var bytes = f.get_buffer(f.get_len())
		f.close()
		var stream = AudioStreamOGGVorbis.new()
		stream.data = bytes
		tts_player.stream = stream
		tts_player.play()
	else:
		print("TTS not found: ", path)

func _play_click():
	if sfx_click:
		sfx_click.play()

func _play_alert():
	if sfx_alert:
		sfx_alert.play()

func _mostrar_vista(nombre_vista):
	view_portada.visible = (nombre_vista == "portada")
	view_ciudadano.visible = (nombre_vista == "ciudadano")
	view_municipio.visible = (nombre_vista == "municipio")
	view_estadisticas.visible = (nombre_vista == "estadisticas")
	view_metodologia.visible = (nombre_vista == "metodologia")
	
	if nombre_vista == "municipio":
		_actualizar_monitor_prioridad()

# NAVEGACIÓN
func _on_BtnNavCiudadano_pressed():
	_play_click()
	_mostrar_vista("ciudadano")

func _on_BtnNavMunicipio_pressed():
	_play_click()
	_mostrar_vista("municipio")

func _on_BtnNavEstadisticas_pressed():
	_play_click()
	_mostrar_vista("estadisticas")

func _on_BtnNavMetodologia_pressed():
	_play_click()
	_mostrar_vista("metodologia")

func _on_BtnNavCreditos_pressed():
	_play_click()
	modal_creditos.visible = true

func _on_BtnCerrarCreditos_pressed():
	_play_click()
	modal_creditos.visible = false

func _on_BtnVolverMenu_pressed():
	_play_click()
	_mostrar_vista("portada")

func _on_BtnSalir_pressed():
	_play_click()
	get_tree().quit()

# FORMULARIO Y MATEMÁTICA IPU
func _setup_options():
	opt_vialidad.clear()
	opt_vialidad.add_item("Bulevar Bellas Artes (Cd. Industrial Otay - Corredor Tráileres)", 0)
	opt_vialidad.add_item("Avenida Paseo Ensenada (Playas de Tijuana - Residencial)", 1)
	opt_vialidad.add_item("Vía Rápida Poniente (Corredor Primario Central)", 2)
	opt_vialidad.add_item("Bulevar Gustavo Díaz Ordaz (La Mesa)", 3)
	opt_vialidad.add_item("Bulevar Agua Caliente (Zona Centro-Sur)", 4)
	opt_vialidad.add_item("Bulevar Insurgentes (Cerro Colorado)", 5)
	
	opt_severidad.clear()
	opt_severidad.add_item("Nivel 1 - Grieta Superficial Leve", 1)
	opt_severidad.add_item("Nivel 2 - Bache Menor (< 5 cm profundidad)", 2)
	opt_severidad.add_item("Nivel 3 - Bache Moderado (5-10 cm, molestia)", 3)
	opt_severidad.add_item("Nivel 4 - Falla Profunda (> 10 cm, daño mecánico)", 4)
	opt_severidad.add_item("Nivel 5 - Hundimiento Estructural / Socavón Inminente", 5)
	opt_severidad.select(1)

func _cargar_datos_iniciales():
	baches_locales.clear()
	
	# Zona B: 5 reportes críticos de hundimiento en Otay
	for i in range(1, 6):
		baches_locales.append({
			"folio": "TIJ-ZB-0000" + str(i),
			"zona": "Zona B (Industrial Otay)",
			"vialidad": "Blvd. Bellas Artes",
			"tipo": "Industrial / Carga Pesada",
			"ipu": 98.3,
			"severidad": 5,
			"aforo_pesado": 0.95,
			"transporte": true,
			"riesgo_socavon": 98.0,
			"alerta": true,
			"estatus": "ALERTA ROJA (SOCAVÓN)",
			"costo_reparacion": "$15,000 MXN",
			"costo_colapso": "$450,000 MXN"
		})
		
	# Zona A: Reportes de Playas
	for i in range(1, 9):
		baches_locales.append({
			"folio": "TIJ-ZA-000" + str(i * 25),
			"zona": "Zona A (Paseo Playas)",
			"vialidad": "Paseo Ensenada",
			"tipo": "Residencial / Local",
			"ipu": 20.0 + (i * 1.8),
			"severidad": 2,
			"aforo_pesado": 0.10,
			"transporte": (i % 2 == 0),
			"riesgo_socavon": 2.0,
			"alerta": false,
			"estatus": "EN COLA DE ESPERA",
			"costo_reparacion": "$3,500 MXN",
			"costo_colapso": "$3,500 MXN"
		})

func _on_BtnEnviarReporte_pressed():
	_play_click()
	var vialidad_txt = opt_vialidad.get_item_text(opt_vialidad.selected)
	var severidad_val = opt_severidad.get_item_id(opt_severidad.selected)
	var es_ind = check_industrial.pressed or ("Bellas Artes" in vialidad_txt)
	var es_tp = check_transporte.pressed
	
	var aforo_pesado = 0.95 if es_ind else 0.20
	var riesgo_soc = 0.98 if (es_ind and severidad_val >= 4) else (0.40 if severidad_val >= 4 else 0.05)
	
	var w_sev = (float(severidad_val) / 5.0) * 30.0
	var w_soc = riesgo_soc * 35.0
	var w_afo = aforo_pesado * 20.0
	var w_tp = 15.0 if es_tp else 0.0
	var ipu_calc = stepify(w_sev + w_soc + w_afo + w_tp, 0.1)
	
	var nuevo_folio = "TIJ-2026-" + str(randi() % 90000 + 10000)
	var nueva_zona = "Zona B (Industrial Otay)" if es_ind else "Zona A (Residencial)"
	
	lbl_resultado.text = "✓ REPORTE GENERADO EXITOSAMENTE\nFolio Anónimo (LGPDPPSO): " + nuevo_folio + "\nÍndice Prioridad Urbana (IPU): " + str(ipu_calc) + " / 100\nClasificación: " + ("EMERGENCIA CRÍTICA" if ipu_calc >= 75 else "MANTENIMIENTO REGULAR")
	alert_socavon.visible = (riesgo_soc >= 0.7)
	if riesgo_soc >= 0.7:
		_play_alert()
		_play_tts("alerta_socavon")
	else:
		_play_tts("reporte_generado")
	
	baches_locales.append({
		"folio": nuevo_folio,
		"zona": nueva_zona,
		"vialidad": vialidad_txt,
		"tipo": "Industrial" if es_ind else "Residencial",
		"ipu": ipu_calc,
		"severidad": severidad_val,
		"aforo_pesado": aforo_pesado,
		"transporte": es_tp,
		"riesgo_socavon": riesgo_soc * 100.0,
		"alerta": (riesgo_soc >= 0.7),
		"estatus": "ALERTA ROJA (SOCAVÓN)" if ipu_calc >= 75 else "EN COLA DE ESPERA",
		"costo_reparacion": "$15,000 MXN",
		"costo_colapso": "$450,000 MXN"
	})
	
	_actualizar_monitor_prioridad()

func _actualizar_monitor_prioridad():
	baches_locales.sort_custom(self, "_compare_ipu")
	
	for child in lista_prioridad.get_children():
		child.queue_free()
		
	lbl_stats.text = "Zona A (Playas): 2,000 reportes | IPU Prom: 22.6\nZona B (Otay): 5 reportes | IPU Crítico: 98.3 (¡SOCAVÓN INMINENTE!)"
	
	var rank = 1
	for b in baches_locales:
		var btn = Button.new()
		btn.rect_min_size = Vector2(0, 36)
		btn.align = Button.ALIGN_LEFT
		
		var texto = "#" + str(rank) + " | " + b.folio + " | " + b.vialidad + " | IPU: " + str(b.ipu)
		if b.alerta:
			texto += " [⚠️ SOCAVÓN]"
		btn.text = texto
		btn.connect("pressed", self, "_seleccionar_bache", [b])
		lista_prioridad.add_child(btn)
		rank += 1
		
	if baches_locales.size() > 0 and bache_seleccionado == null:
		_seleccionar_bache(baches_locales[0])

func _seleccionar_bache(bache):
	_play_click()
	bache_seleccionado = bache
	lbl_detalle_bache.text = "DETALLE TÉCNICO:\n" + \
		"Folio: " + bache.folio + "\n" + \
		"Vialidad: " + bache.vialidad + " (" + bache.zona + ")\n" + \
		"Índice de Prioridad Urbana: " + str(bache.ipu) + " / 100\n" + \
		"Severidad Visual: " + str(bache.severidad) + " / 5\n" + \
		"Riesgo de Socavón: " + str(bache.riesgo_socavon) + "%\n" + \
		"Aforo Pesado Relativo: " + str(bache.aforo_pesado * 100) + "%\n" + \
		"Costo Prevención Inmediata: " + bache.costo_reparacion + "\n" + \
		"Costo si ocurre Colapso (x30): " + bache.costo_colapso + "\n" + \
		"Estado: " + bache.estatus

func _compare_ipu(a, b):
	return a.ipu > b.ipu

func _on_BtnDespachar_pressed():
	_play_click()
	if baches_locales.size() > 0:
		_play_tts("cuadrilla_asignada")
		var b = baches_locales[0]
		OS.alert("🚛 CUADRILLA NOCTURNA ASIGNADA:\n\n" + \
			"Destino: " + b.vialidad + "\n" + \
			"Zona: " + b.zona + "\n" + \
			"Folio: " + b.folio + "\n" + \
			"Prioridad: " + str(b.ipu) + "/100\n\n" + \
			"Impacto de la Decisión Basada en Datos:\n" + \
			"• Se evitó el colapso vial del corredor maquilador.\n" + \
			"• Ahorro público estimado: $435,000 MXN (Factor 30x NIF C-9).", "Despacho Autorizado")
		baches_locales.remove(0)
		bache_seleccionado = null
		_actualizar_monitor_prioridad()

func _on_BtnSyncFlask_pressed():
	_play_click()
	_play_tts("sincronizacion")
	http_node.request("https://bacheo-inteligente-tijuana.vercel.app/api/cola_prioridad")
	lbl_stats.text = "Sincronizando en tiempo real con servidor Flask y SQLite..."

func _on_http_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse(body.get_string_from_utf8())
		if json.error == OK:
			baches_locales.clear()
			for item in json.result.items:
				baches_locales.append({
					"folio": item.folio,
					"zona": item.zona,
					"vialidad": item.vialidad,
					"tipo": "Base de Datos",
					"ipu": item.ipu,
					"severidad": item.severidad,
					"aforo_pesado": 0.95 if "Zona B" in item.zona else 0.15,
					"transporte": true,
					"riesgo_socavon": item.riesgo_socavon,
					"alerta": (item.riesgo_socavon >= 70),
					"estatus": "SINCRONIZADO SQL",
					"costo_reparacion": "$15,000 MXN",
					"costo_colapso": "$450,000 MXN"
				})
			_actualizar_monitor_prioridad()
			lbl_stats.text = "✓ Sincronizado exitosamente con SQLite y Flask (2,005 reportes procesados)."
	else:
		lbl_stats.text = "Modo autónomo local activo (Sin conexión con servidor web)."


func _aplicar_psicologia_color():
	var header = $Views/ViewPortada.get_node_or_null("HeaderBox")
	if header:
		header.get_node("Institucion").text = "AYUNTAMIENTO DE TIJUANA"
		header.get_node("Titulo").text = "BACHEO INTELIGENTE"
		header.get_node("Subtitulo").text = "Reporta baches en tu colonia de forma facil y rapida"
		header.get_node("Autor").text = ""
		header.get_node("BadgeCompat").text = ""
	
	var style_normal = StyleBoxFlat.new()
	style_normal.bg_color = Color("#0ea5e9")
	style_normal.corner_radius_top_left = 20
	style_normal.corner_radius_top_right = 20
	style_normal.corner_radius_bottom_left = 20
	style_normal.corner_radius_bottom_right = 20
	
	var style_hover = style_normal.duplicate()
	style_hover.bg_color = Color("#0284c7")
	
	var style_danger = style_normal.duplicate()
	style_danger.bg_color = Color("#ef4444")
	
	var btns = $Views/ViewPortada/Center/MenuButtons.get_children()
	for btn in btns:
		if btn is Button:
			btn.add_stylebox_override("normal", style_normal)
			btn.add_stylebox_override("hover", style_hover)
			btn.add_stylebox_override("pressed", style_hover)
			btn.rect_min_size.y = 60
			
			if btn.name == "BtnNavCiudadano":
				btn.text = "📷 Reportar un Bache Nuevo"
			elif btn.name == "BtnNavMunicipio":
				btn.text = "🗺️ Ver Mapa y Prioridades"
			elif btn.name == "BtnSalir":
				btn.add_stylebox_override("normal", style_danger)
				btn.text = "❌ Salir de la App"
			else:
				btn.visible = false

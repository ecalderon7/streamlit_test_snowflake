import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def formatear_duracion(segundos: float) -> str:
    """Recibe segundos (float) y devuelve cadena en formato mm:ss"""
    minutos = int(segundos // 60)
    segundos_restantes = int(segundos % 60)
    return f"{minutos:02d}:{segundos_restantes:02d}"

def obtener_duracion_archivo(archivo):
    """
    Función alternativa para obtener duración sin mutagen.
    Retorna una duración por defecto basada en el tipo de archivo.
    """
    if archivo is None:
        return "00:00"
    
    # Obtener extensión del archivo
    import os
    extension = os.path.splitext(archivo.name)[1].lower()
    
    # Mapeo de duraciones por defecto según tipo de archivo
    duraciones_default = {
        '.mp3': "00:20",  # 20 segundos por defecto para spots
        '.wav': "00:20",  # 20 segundos por defecto para spots
        '.mp4': "00:30",  # 30 segundos por defecto para videos
        '.pdf': "N/A"     # No aplica para PDFs
    }
    
    return duraciones_default.get(extension, "00:20")

st.set_page_config(layout="wide")

# MENU LATERAL/PRINCIPAL
menu_options = ["Pautas de Transmisión", "Convenios", "➕ Nueva Pauta"]

if "opcion_menu" not in st.session_state:
    # Por defecto Pautas de Transmisión
    st.session_state.opcion_menu = menu_options[0]  

opcion_menu = st.sidebar.selectbox(
    "🏠 MENU PRINCIPAL",
    options=menu_options,
    index=menu_options.index(st.session_state.opcion_menu)
)

# Opcional: espacio antes de las métricas
st.sidebar.markdown("## ")  
st.sidebar.markdown("## ")  

# METRICAS
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size: 15px;'>
    <b>🔢 METRICAS</b><br><br>
    <div style='margin-bottom: 0.5em;'>TOTAL DE PAUTAS: <b style='float:right;'>140</b></div>
    <div style='margin-bottom: 0.5em;'>MIS BORRADORES: <b style='float:right;'>5</b></div>
    <div style='margin-bottom: 0.5em;'>VENTAS (4): <b style='float:right;'>20</b></div>
    <div style='margin-bottom: 0.5em;'>CONTACO COMERCIAL (5): <b style='float:right;'>5</b></div>
    <div style='margin-bottom: 0.5em;'>CAPTURA (3): <b style='float:right;'>10</b></div>
    <div style='margin-bottom: 0.5em;'>PROCESADO F1: <b style='float:right;'>100</b></div>
</div>
""", unsafe_allow_html=True)

# Opcional: espacio antes de Ayuda
st.sidebar.markdown("## ")  
st.sidebar.markdown("## ")  
st.sidebar.markdown("## ")  
st.sidebar.markdown("## ")  

with st.sidebar.expander("❓ AYUDA"):
    st.markdown("- ¿Cómo subir un archivo?")
    st.markdown("- ¿Cómo guardar una pauta?")
    st.markdown("- Descargar Formato Excel")
    st.markdown("- ¿A quién contactar?")

#===== OPCION + NUEVA PAUTA
if opcion_menu == "➕ Nueva Pauta":
    # Estilos personalizados para diseño compacto y títulos uniformes
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
        }

        input, select, textarea {
            padding-top: 3px !important;
            padding-bottom: 3px !important;
            height: 32px !important;
            font-size: 13px !important;
        }

        .stDateInput input {
            font-size: 13px !important;
            height: 32px !important;
        }

        label {
            font-size: 13px !important;
            margin-bottom: 1px !important;
            margin-top: -3px !important;
        }

        .stColumns {
            gap: 0.75rem !important;
        }

        .stTextInput > div, .stSelectbox > div {
            padding-bottom: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Título con bloque de usuario alineado al nivel
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0rem;">
            <h1 style="font-size: 28px; font-weight: 700; margin: 0.6em;">
                PRELLENADO ORDEN/PAUTA DE TRANSMISION RADIO
            </h1>
            <div style="display: flex; align-items: center;">
                <div style="text-align: right; margin-right: 10px;">
                    <p style="margin: 0.3em; font-size: 14px; font-weight: bold;">BIENVENIDO<br>VENTAS</p>
                </div>
                <div style="background-color: #000000; color: white; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold;">
                    VE
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Subida de archivo
    st.markdown("""
        <h2 style='font-size: 20px; font-weight: 600; margin-top: 0em;'>
            📥 Subir archivo de Pauta Excel/Pdf (opcional)
        </h2>
    """, unsafe_allow_html=True)

    archivo = st.file_uploader("Selecciona un archivo Excel con estructura compatible.", type=["xlsx"])
    df_base = pd.DataFrame()

    # Variables con valores por defecto
    datos_generales = {
        "CLIENTE": "",
        "AGENCIA": "",
        "MARCA": "",
        "TIPO CONVENIO": "",
        "NOMBRE DEL CONVENIO": "",
        "ANUNCIA": "",
        "CAMPAÑA": "",
        "INICIO CAMPAÑA": datetime.today(),
        "FIN CAMPAÑA": datetime.today() + timedelta(days=28),
        "NUMERO DE ORDEN": "",
        "EJECUTIVO / VENDEDOR": "",
        "NOMBRE EVENTO": "",
        "FACTURAR A": "",
        "FIRMA PAGARE (SI / NO)": "NO",
        "ES AGREGADO (SI / NO)": "NO"
    }

    if archivo:
        try:
            # Leer encabezados desde filas 0 a 13
            encabezado_df = pd.read_excel(archivo, nrows=13, header=None)

            def buscar_valor(nombre):
                for fila in encabezado_df.itertuples(index=False):
                    for i, celda in enumerate(fila):
                        if isinstance(celda, str) and nombre in celda.upper():
                            valor = fila[i+1] if i+1 < len(fila) else ""
                            return valor
                return ""

            # Asignar valores encontrados
            datos_generales["CLIENTE"] = buscar_valor("CLIENTE")
            datos_generales["AGENCIA"] = buscar_valor("AGENCIA")
            datos_generales["MARCA"] = buscar_valor("MARCA")
            datos_generales["TIPO CONVENIO"] = buscar_valor("TIPO CONVENIO")
            datos_generales["NOMBRE DEL CONVENIO"] = buscar_valor("NOMBRE DEL CONVENIO")
            datos_generales["ANUNCIA"] = buscar_valor("ANUNCIA")
            datos_generales["CAMPAÑA"] = buscar_valor("CAMPAÑA")
            datos_generales["NUMERO DE ORDEN"] = buscar_valor("NUMERO DE ORDEN")
            datos_generales["EJECUTIVO / VENDEDOR"] = buscar_valor("AGENTE / EJECUTIVO")
            datos_generales["NOMBRE EVENTO"] = buscar_valor("NOMBRE EVENTO")
            datos_generales["FACTURAR A"] = buscar_valor("FACTURAR A")
            datos_generales["FIRMA PAGARE (SI / NO)"] = buscar_valor("FIRMA PAGARE")
            datos_generales["ES AGREGADO (SI / NO)"] = buscar_valor("ES AGREGADO")

            # Leer fechas si están en formato válido
            try:
                datos_generales["INICIO CAMPAÑA"] = pd.to_datetime(buscar_valor("INICIO CAMPAÑA"), dayfirst=True)
            except: pass
            try:
                datos_generales["FIN CAMPAÑA"] = pd.to_datetime(buscar_valor("FIN CAMPAÑA"), dayfirst=True)
            except: pass         

        except Exception as e:
            st.warning(f"No se pudieron extraer datos generales: {e}")

    # === Captura de Fechas y Datos Generales ===
    with st.expander("🙍 Información del Cliente y Campaña", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            cliente = st.text_input("CLIENTE / RAZON SOCIAL*", datos_generales["CLIENTE"],
            help="Ingresa la razón social del cliente.")
            agencia = st.text_input("AGENCIA", datos_generales["AGENCIA"])
            marca = st.text_input("MARCA", datos_generales["MARCA"])
            opciones_convenio = [
                "EFECTIVO",
                "EFECTIVO NO REVOLVENTE",
                "FACTURACION ANTICIPADA",
                "FA DIRECTA",
                "FA INTERCAMBIO",
                "PROMOCIÓN INDUSTRIAL",
                "INTERCAMBIO",
                "INTERCAMBIO DE MEDIOS",
                "PINTERCAMBIO",
                "MOVIMIENTO ADMINISTRATIVO"
            ]
            tipo_convenio = st.selectbox(
                "TIPO CONVENIO*",
                opciones_convenio,
                index=opciones_convenio.index(str(datos_generales["TIPO CONVENIO"]).upper()) if str(datos_generales["TIPO CONVENIO"]).upper() in opciones_convenio else 0,
                help="Selecciona el Tipo de Convenio según el acuerdo comercial: Efectivo, Intercambio, FA, etc."
            )

            inicio_camp = st.date_input("INICIO CAMPAÑA*", value=datos_generales["INICIO CAMPAÑA"], format="DD/MM/YYYY")
        with col2:
            ejecutivo = st.text_input("EJECUTIVO / VENDEDOR*", datos_generales["EJECUTIVO / VENDEDOR"])
            anuncia = st.text_input("ANUNCIA", datos_generales["ANUNCIA"])
            campana = st.text_input("CAMPAÑA", datos_generales["CAMPAÑA"])
            nombre_convenio = st.text_input("NOMBRE DEL CONVENIO", datos_generales["NOMBRE DEL CONVENIO"])
            fin_camp = st.date_input("FIN CAMPAÑA*", value=datos_generales["FIN CAMPAÑA"], format="DD/MM/YYYY")
        with col3:
            numero_orden = st.text_input("NUMERO DE ORDEN", datos_generales["NUMERO DE ORDEN"])
            evento = st.text_input("NOMBRE EVENTO", datos_generales["NOMBRE EVENTO"])
            factura_a = st.text_input("FACTURAR A", datos_generales["FACTURAR A"])
            valores_sn = ["NO", "SI"]
            valor_cliente_nuevo = str(datos_generales.get("ES CLIENTE NUEVO (SI/NO)", "NO")).strip().upper()
            if valor_cliente_nuevo not in valores_sn:
                valor_cliente_nuevo = "NO"  # valor por defecto
            cliente_nuevo = st.selectbox("ES CLIENTE NUEVO (SI/NO)", valores_sn, index=valores_sn.index(valor_cliente_nuevo))
            es_agregado = st.selectbox("ES AGREGADO (SI / NO)", ["NO", "SI"], index=["NO", "SI"].index(str(datos_generales["ES AGREGADO (SI / NO)"]).upper()))
            
    # Calendario
    num_dias = 45
    calendario_fechas = [inicio_camp + timedelta(days=i) for i in range(num_dias)]
    dias_es = {"Monday": "L", "Tuesday": "M", "Wednesday": "M", "Thursday": "J", "Friday": "V", "Saturday": "S", "Sunday": "D"}
    calendario_columnas = [f"{f.day}/{dias_es[f.strftime('%A')]}" for f in calendario_fechas]
    fechas_legibles = [f.strftime('%d/%m/%Y') for f in calendario_fechas]

    columnas_iniciales = [
        "PLAZA TRANS", "TIPO MEDIO", "MEDIO", "PROGRAMA", "DURACION",
        "PRODUCTO", "VERSION", "TALENTO", "HORA INICIO", "HORA FIN",
        "TOTAL IMPACTOS", "TARIFA", "TOTAL INVERSION"
    ]
    all_columns = columnas_iniciales + calendario_columnas

    if archivo:
        try:
            # Leer desde fila 15
            df_archivo = pd.read_excel(archivo, header=14)

            # Cortar donde la columna 'PLAZA TRANS' esté vacía
            if "PLAZA TRANS" in df_archivo.columns:
                fila_corte = df_archivo[df_archivo["PLAZA TRANS"].isna()].index
                if not fila_corte.empty:
                    df_archivo = df_archivo.iloc[:fila_corte[0]]
                    st.info("Se ignoraron filas vacías o de totales al final del archivo.")

            # Validar columnas requeridas
            columnas_faltantes = [col for col in columnas_iniciales if col not in df_archivo.columns]
            if columnas_faltantes:
                st.error(f"El archivo no contiene las siguientes columnas obligatorias: {columnas_faltantes}")
            else:
                for col in calendario_columnas:
                    if col not in df_archivo.columns:
                        df_archivo[col] = 0
                df_base = df_archivo[all_columns]
                
                st.success("Archivo cargado correctamente. Puedes revisar y editar abajo.")

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    if df_base.empty:
        fila_ejemplo = [
            "MONTERREY", "RADIO", "XERT-AM", ".", "20''",
            "SPOT", "VERSION1", ".", "05:00", "10:00"
        ] + [0 for _ in calendario_columnas] + [0, 0, 0]
        df_base = pd.DataFrame([fila_ejemplo], columns=all_columns)

    # Título sección transmisiones
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; gap: 20px; margin-top: 0em;'>
            <h2 style='font-size: 20px; font-weight: 600; margin: 0;'>📡 Transmisiones por Día</h2>
            <span style='font-weight: bold;'>📅 Inicio: {inicio_camp.strftime('%d/%m/%Y')}</span>
            <span style='font-weight: bold;'>🗓️ Fin: {fin_camp.strftime('%d/%m/%Y')}</span>
        </div>
        """, unsafe_allow_html=True
    )

    # Editor con cálculos automáticos
    df_editado = st.data_editor(
        df_base,
        num_rows="dynamic",
        use_container_width=True,
        key="data_editor_impacts"
    )

    # Recalcular impactos e inversión por fila
    for idx in df_editado.index:
        impactos = 0
        for col in calendario_columnas:
            try:
                impactos += int(df_editado.at[idx, col])
            except:
                pass

        try:
            tarifa = float(df_editado.at[idx, "TARIFA"])
        except:
            tarifa = 0

        df_editado.at[idx, "TOTAL IMPACTOS"] = impactos
        df_editado.at[idx, "TOTAL INVERSION"] = round(impactos * tarifa, 2)

    # Resumen financiero
    st.markdown("""
        <h2 style='font-size: 20px; font-weight: 600; margin-top: 0em;'>
            📊 Resumen Transmisiones
        </h2>
    """, unsafe_allow_html=True)

    #===== OPCION +NUEVA PAUTA : Selección IVA y Moneda ===
    col1, col2 = st.columns(2)
    with col1:
        tipo_iva = st.selectbox("Selecciona IVA", ["16%", "8%", "0%", "Exento"], index=0)
    with col2:
        divisa = st.selectbox("Selecciona Moneda", ["MN", "USD", "EUR"], index=0)

    # Convertir tasa de IVA
    iva_map = {
        "16%": 0.16,
        "8%": 0.08,
        "0%": 0.0,
        "Exento": 0.0
    }
    iva_rate = iva_map[tipo_iva]

    # Calcular montos
    subtotal = df_editado["TOTAL INVERSION"].astype(float).sum()
    iva = round(subtotal * iva_rate, 2)
    total = round(subtotal + iva, 2)
    impactos_totales = df_editado["TOTAL IMPACTOS"].astype(int).sum()

    # Mostrar resumen
    resumen_df = pd.DataFrame([{
        "TOTAL IMPACTOS": impactos_totales,
        "SUBTOTAL": f"${subtotal:,.2f}",
        f"IVA ({tipo_iva})": f"${iva:,.2f}" if tipo_iva != "Exento" else "Exento",
        f"TOTAL ({divisa})": f"${total:,.2f}"
    }])
    st.dataframe(resumen_df, hide_index=True, use_container_width=True)

    # Secciones adicionales
    st.markdown("""
        <h2 style='font-size: 20px; font-weight: 600; margin-top: 0em;'>
            📦 ¿Materiales, indicaciones especiales?
        </h2>
    """, unsafe_allow_html=True)
    st.text_area("Indica materiales u observaciones especiales", placeholder="Ejemplo : Materiales pendientes por el cliente.")

    # ————— Sección: Materiales publicitarios —————
    st.header("Materiales Publicitarios")

    # Inicializar session_state si no existe
    if 'materiales' not in st.session_state:
        st.session_state['materiales'] = []

    with st.expander("Información de Materiales"):
        nombre = st.text_input("Nombre de Material", key="input_nombre")
        archivo_material = st.file_uploader("Subir Archivo (mp3, wav, mp4, pdf)", type=["mp3", "wav", "mp4", "pdf"], key="input_archivo")
        version = st.text_input("Versión", key="input_version")
        tipo = st.selectbox("Tipo de Material", ["Spot", "Jingle", "Cortinilla", "Otro"], key="input_tipo")

        # Botón para añadir el material a la lista
        if st.button("Añadir", key="btn_add_material"):
            if not nombre:
                st.warning("Debes indicar un nombre para el material.")
            elif archivo_material is None:
                st.warning("Debes subir un archivo antes de añadir.")
            else:
                # Usar función alternativa sin mutagen
                duracion_str = obtener_duracion_archivo(archivo_material)

                # Guardar en session_state
                st.session_state['materiales'].append({
                    "Nombre": nombre,
                    "Archivo": archivo_material.name,
                    "Versión": version,
                    "Tipo": tipo,
                    "Duración": duracion_str
                })
                st.success(f"Material '{nombre}' añadido correctamente!")

    # Mostrar la tabla sólo si hay al menos un material
    if st.session_state['materiales']:
        st.table(st.session_state['materiales'])

    st.markdown("""
        <h2 style='font-size: 20px; font-weight: 600; margin-top: 0em;'>
            🎙️ ¿Indicaciones Operativas / Conducción / Talentos?
        </h2>
    """, unsafe_allow_html=True)
    st.text_area("Honorarios / Talentos", placeholder="Ejemplo : Detallar el monto de honorarios y talentos.")

    st.markdown("""
        <h2 style='font-size: 20px; font-weight: 600; margin-top: 0em;'>
            💳 ¿Indicaciones Facturación y Cobranza?
        </h2>
    """, unsafe_allow_html=True)
    st.text_area("Cobranza", placeholder = "Ejemplo : Facturación al término de la campaña. El cliente no es moroso; y no está bloqueado.")
    # Nuevo campo para cargar el pagaré
    pagare_pdf = st.file_uploader("📎 Cargar pagaré (PDF)", type=["pdf"], key="carga_pagare")

    col_action1, col_action2, col_action3 = st.columns(3)

    with col_action1:
        if st.button("💾 Guardar como Borrador"):
            st.success("✅ Borrador Guardado Exitosamente.\n   📄 Folio Generado: FOLIO-100.\n    📥 Archivos Borrador Excel/PDF Descargados.")

    with col_action2:
        if st.button("❌ Descartar Cambios"):
            st.warning("❌ Cambios descartados por el usuario.")
            st.rerun()  # Cambiado de st.experimental_rerun() a st.rerun()

    with col_action3:
        if st.button("📤 Enviar Campaña OTC"):
            folio_num = 100
            folio = f"FOLIO-{folio_num:03}"
            output_filename = f"{folio}_Resumen_Pauta.xlsx"
            #---
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 30px;">
                <div style="border:1px solid #ccc; padding: 1.5em; border-radius: 10px; background-color: #eef6fb; width: 400px;">
                    <h4 style="color:green;">Se guardó el <b>{folio}</b> exitosamente</h4>
                    <p><b>CLIENTE:</b> {cliente}</p>
                    <p><b>CAMPAÑA:</b> {campana}</p>
                    <p><b>INICIO CAMPAÑA:</b> {inicio_camp.strftime("%d/%m/%Y")}</p>
                    <p><b>FIN CAMPAÑA:</b> {fin_camp.strftime("%d/%m/%Y")}</p>
                    <p><b>IMPACTOS:</b> {impactos_totales}</p>
                    <p><b>SUBTOTAL:</b> ${subtotal:,.2f}</p>
                    <p><b>IVA:  ({tipo_iva}):</b> {"Exento" if tipo_iva == "Exento" else f"${iva:,.2f}"}</p>
                    <p><b>TOTAL: ({divisa}):</b> ${total:,.2f}</p>
                    <p><b>MATERIALES:</b> {len(st.session_state.get('materiales', []))}</p>
                    <p><b>VENDEDOR:</b> {ejecutivo}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            #---
            st.success(f"✅ Campaña Enviada Correctamente.\n   📄 Folio Generado: {folio}.\n    📥 Archivos Orden/Pauta Excel/PDF Descargados.")        

#===== OPCION PAUTAS TRANSMISION : OPCION PAUTAS DE TRANSMISION
elif opcion_menu == "Pautas de Transmisión":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0rem;">
        <h2 style="font-size: 28px; font-weight: 700; margin: 0;">
            LISTADO DE ORDENES/PAUTAS DE TRANSMISION RADIO
        </h2>
        <div style="display: flex; align-items: center;">
            <div style="text-align: right; margin-right: 10px;">
                <p style="margin: 0; font-size: 14px; font-weight: bold;">BIENVENIDO<br>VENTAS</p>
            </div>
            <div style="background-color: #000000; color: white; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold;">
                VE
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

    # Estilos para armonizar botones con los campos ---
    st.markdown("""
        <style>
        .filtro-btn button {
            background-color: white;
            color: #31333F;
            border: 1px solid #D0D1D5;
            border-radius: 6px;
            height: 35px !important;
            padding: 0px 14px;
            font-size: 14px;
            font-weight: 500;
            margin-right: 6px;
        }
        .filtro-btn button:hover {
            background-color: #f0f0f5;
            border-color: #c0c0c5;
        }
        .stDateInput>div>input {
            height: 35px !important;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    #===== OPCION PAUTAS TRANSMISION : FILTROS PAUTAS DE TRANSMISION
    with st.expander("🔍 Filtros de búsqueda", expanded=True):

        # Fila 1: CLIENTE | AGENCIA | CAMPAÑA
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            cliente = st.text_input("CLIENTE / RAZON SOCIAL", 
            help="Ingresa la razón social del cliente.")
        with col2:
            agencia = st.text_input("AGENCIA")
        with col3:
            campana = st.text_input("CAMPAÑA")

        # Fila 2: FECHA1 | FECHA2 | FILTROS AVANZADOS | BOTONES
        col4, col5, col6, col7 = st.columns([1, 1, 1, 1.5])
        with col4:
            fecha1 = st.date_input("FECHA INICIO LLENADO", value=datetime.today().date() - timedelta(days=7), format="DD/MM/YYYY")
        with col5:
            fecha2 = st.date_input("FECHA FIN LLENADO", format="DD/MM/YYYY")
        with col6:
            filtro_estatus_otc = st.multiselect(
                "ESTATUS OTC",
                options=["BORRADOR", "VENTAS", "CONTACTO COMERCIAL", "CAPTURA", "PROCESADO F1"],
                default=[],
                placeholder="Selecciona una opción"
            )
        
        with col7:
            st.markdown("<div style='margin-top: 28px;' class='filtro-btn'>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
            with col_btn1:
                if st.button("🔄 Filtrar"):
                    pass
            with col_btn2:
                if st.button("➕ Nueva Pauta"):
                    st.session_state.opcion_menu = menu_options[2]
            with col_btn3:
                if st.button("⚙️ Avanzados"):
                    st.session_state["filtros_avanzados"] = True

    st.markdown("---")               
    # DATOS DE EJEMPLO
    data = {
        "ARCHIVO" :"📄",
        "FOLIO INTERNO": ["FOLIO-001", "FOLIO-002", "FOLIO-003"],
        "FOLIO F1": ["MTY0525277066", "",""],
        "CLIENTE": ["POLLO LOCO", "POLLOS ASADOS OCHOA","POLLO LOCO"],
        "AGENCIA": ["", "",""],
        "TIPO CONVENIO": ["EFECTIVO", "FACTURACION ANTICIPADA","EFECTIVO"],
        "CAMPAÑA": ["VERANO 2025", "BUEN FIN 2025","NAVIDAD 2025"],
        "INICIO CAMPAÑA": ["01-07-2025", "15-10-2025","01-12-2025"],
        "FIN CAMPAÑA": ["31-07-2025", "31-10-2025", "31-12-2025"],
        "TOTAL": ["$12,000", "$100,000","$90,000"],
        "MONEDA": ["MN", "MN","MN"],
        "ESTATUS CAMPAÑA": ["EN PROCESO","PROGRAMADA", "PROGRAMADA"],
        "ESTATUS OTC": ["PROCESADO F1", "CAPTURA", "CONTACTO COMERCIAL"],
        "FECHA CAPTURA": ["27-06-2025", "16-07-2025","24-07-2025"],
        "PLAZA VENTA": ["MONTERREY", "MONTERREY","MONTERREY"],
        "EJECUTIVO": ["CRISTA REYNA", "CRISTA REYNA","CRISTA REYNA"]
    }

    df = pd.DataFrame(data)

    # Copiar el DataFrame original
    df_con_checkbox = df.copy()

    # Insertar la columna de selección al principio
    df_con_checkbox.insert(0, "✅ SELECCIONAR", [False] * len(df_con_checkbox))

    #===== OPCION PAUTAS TRANSMISION : BOTONES DE ACCION DEL GRID
    # Usa proporciones más estrechas para reducir espacio entre los botones
    col1, col2, col3, col4, col5 = st.columns([0.8, 0.8, 0.8, 0.8, 0.8])  
    with col1:
        if st.button("👁️ Ver", key="btn_ver"):
            st.session_state["accion"] = "ver"

    with col2:
        if st.button("✏️ Editar", key="btn_editar"):
            st.session_state["accion"] = "editar"

    with col3:
        if st.button("📋 Duplicar", key="btn_duplicar"):
            st.session_state["accion"] = "duplicar"

    with col4:
        if st.button("🗑️ Eliminar", key="btn_eliminar"):
            st.session_state["accion"] = "eliminar"

    with col5:
        if st.button("📥 Descargar", key="btn_descargar"):
            st.session_state["accion"] = "eliminar"

    # Mostrar el grid con checkbox por fila
    selected_df = st.data_editor(
        df_con_checkbox,
        use_container_width=True,
        hide_index=True,
        column_config={
            "✅ SELECCIONAR": st.column_config.CheckboxColumn(
                label="✅", help="Seleccionar"
            )
        },
        key="grid_pautas_con_checkbox"
    )

    st.markdown("---")  

    #===== OPCION PAUTAS TRANSMISION : TABS EDICIONES DE LA PAUTA
    if "folio_edicion" not in st.session_state:
        st.session_state["folio_edicion"] = None
    
    if st.button("✏️ Editar FOLIO-003"):
        st.session_state["folio_edicion"] = "FOLIO-003"

    if st.session_state["folio_edicion"]:
        folio = st.session_state["folio_edicion"]       

        # === Inicialización de df_base y calendario para edición ===
        inicio_campaña = st.session_state.get("edit_inicio_campaña", "01/12/2025")
        fin_campaña    = st.session_state.get("edit_fin_campaña", "31/12/2025") 

        try:
            fecha_inicio = datetime.strptime(inicio_campaña, "%d/%m/%Y")
            fecha_fin = datetime.strptime(fin_campaña, "%d/%m/%Y")
        except:
            fecha_inicio = datetime.today()
            fecha_fin = datetime.today() + timedelta(days=28)

        num_dias = (fecha_fin - fecha_inicio).days + 1
        calendario_fechas = [fecha_inicio + timedelta(days=i) for i in range(num_dias)]
        dias_es = {"Monday": "L", "Tuesday": "M", "Wednesday": "M", "Thursday": "J", "Friday": "V", "Saturday": "S", "Sunday": "D"}
        calendario_columnas = [f"{f.day}/{dias_es[f.strftime('%A')]}" for f in calendario_fechas]

        columnas_iniciales = [
            "PLAZA TRANS", "TIPO MEDIO", "MEDIO", "PROGRAMA", "DURACION",
            "PRODUCTO", "VERSION", "TALENTO", "HORA INICIO", "HORA FIN",
            "TOTAL IMPACTOS", "TARIFA", "TOTAL INVERSION"
        ]
        all_columns = columnas_iniciales + calendario_columnas

        fila_ejemplo = [
            "MONTERREY", "RADIO", "XERT-AM", ".", "20''",
            "SPOT", "VERSION1", ".", "05:00", "10:00"
        ] + [0 for _ in calendario_columnas] + [0, 0, 0]

        df_base = pd.DataFrame([fila_ejemplo], columns=all_columns)

        st.markdown(f"<h1 style='font-size:26px; font-weight:700;'>✏️ EDITANDO ORDEN/PAUTA DE TRANSMISION RADIO : {folio}</h1>", unsafe_allow_html=True)
        
        tabs = st.tabs(["🙍 CLIENTE   ", "🎯 CAMPAÑA", "📡 TRANSMISIONES", "📦 MATERIALES", "📝 INDICACIONES", "➡️ VISTA PREVIA Y ENVIO"])
        
        with tabs[0]:
            with st.expander("🙍  Información del Cliente y Campaña", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    cliente = st.text_input("CLIENTE / RAZON SOCIAL*", "POLLO LOCO", key="edit_cliente")
                    facturar_a = st.text_input("FACTURAR A", "POLLO LOCO", key="edit_facturar_a")
                    direccion = st.text_input("DIRECCION FACTURACION", "", key="edit_direccion")
                    agencia = st.text_input("AGENCIA", "", key="edit_agencia")

                with col2:
                    ejecutivo = st.text_input("EJECUTIVO / VENDEDOR*", "CRISTA REYNA", key="edit_ejecutivo")
                    plaza = st.text_input("PLAZA DE VENTA", "MONTERREY", key="edit_plaza")
                    tipo_convenio = st.selectbox("TIPO DE CONVENIO", [
                        "EFECTIVO",
                        "FACTURACION ANTICIPADA",
                        "INTERCAMBIO",
                        "MOVIMIENTO ADMINISTRATIVO",
                        "FA DIRECTA",
                        "FA INTERCAMBIO",
                        "PROMOCIÓN INDUSTRIAL"
                    ], key="edit_tipo_convenio")
                    nombre_convenio = st.text_input("NOMBRE DEL CONVENIO", "", key="edit_nombre_convenio")

                with col3:
                    fecha_captura = st.text_input("FECHA CAPTURA", "24/07/2025", key="edit_fecha_captura")
                    total_pauta =  st.text_input("TOTAL PAUTA ($)", "$90,000", key="edit_total_pauta")
                    cliente_nuevo = st.selectbox("FIRMA PAGARE (SI/NO)", ["NO", "SI"], index=0, key="edit_firma_pagare")
                    es_agregado = st.selectbox("ES AGREGADO (SI/NO)", ["NO", "SI"], index=0, key="edit_es_agregado")

        with tabs[1]:
            with st.expander("🎯  Información de la Campaña", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    inicio_campaña = st.text_input("INICIO CAMPAÑA", "01/12/2025", key="edit_inicio_campaña")
                    campana = st.text_input("CAMPAÑA", "NAVIDAD 2025", key="edit_campana")
                with col2:
                    fin_campaña = st.text_input("FIN CAMPAÑA", "31/12/2025", key="edit_fin_campaña")
                    marca = st.text_input("MARCA", "", key="edit_marca")
                with col3:
                    numero_orden = st.text_input("NUMERO DE ORDEN", "", key="edit_numero_orden")
                    total_pauta2 = st.text_input("TOTAL PAUTA ($)2", "$90,000", key="edit_total_pauta2")
                
                # Segunda línea opcional para campos adicionales
                col4, col5, col6 = st.columns(3)
                with col4:
                    anuncia = st.text_input("ANUNCIA", "", key="edit_anuncia")
                with col5:
                    nombre_evento = st.text_input("NOMBRE EVENTO", "", key="edit_nombre_evento")
                with col6:
                    pass  # espacio vacío si no se requiere más campos

        with tabs[2]:
            # === BLOQUE DE TRANSMISIONES POR DÍA ===
            st.markdown(
                f"""
                <div style='display: flex; align-items: center; gap: 20px; margin-top: 0em;'>
                    <h2 style='font-size: 20px; font-weight: 600; margin: 0;'>📡 Transmisiones por Día</h2>
                    <span style='font-weight: bold;'>📅 Inicio: {inicio_campaña}</span>
                    <span style='font-weight: bold;'>🗓️ Fin: {fin_campaña}</span>
                </div>
                """, unsafe_allow_html=True
            )

            df_editado = st.data_editor(
                df_base,
                num_rows="dynamic",
                use_container_width=True,
                key="data_editor_impacts_edit"
            )

            # Recalcular impactos e inversión por fila
            for idx in df_editado.index:
                impactos = 0
                for col in calendario_columnas:
                    try:
                        impactos += int(df_editado.at[idx, col])
                    except:
                        pass

                try:
                    tarifa = float(df_editado.at[idx, "TARIFA"])
                except:
                    tarifa = 0

                df_editado.at[idx, "TOTAL IMPACTOS"] = impactos
                df_editado.at[idx, "TOTAL INVERSION"] = round(impactos * tarifa, 2)

            st.markdown("""
                <h2 style='font-size: 20px; font-weight: 600; margin-top: 0em;'>
                    📊 Resumen Transmisiones
                </h2>
            """, unsafe_allow_html=True)
            
            # === SECCIÓN: Selección IVA y Moneda en modo EDICIÓN ===
            col1, col2 = st.columns(2)
            with col1:
                tipo_iva_edit = st.selectbox("Selecciona IVA", ["16%", "8%", "0%", "Exento"], index=0, key="edit_iva")
            with col2:
                divisa_edit = st.selectbox("Selecciona Moneda", ["MN", "USD", "EUR"], index=0, key="edit_divisa")

            iva_map_edit = {
                "16%": 0.16,
                "8%": 0.08,
                "0%": 0.0,
                "Exento": 0.0
            }
            iva_rate_edit = iva_map_edit[tipo_iva_edit]

            # Calcular resumen
            subtotal_edit = df_editado["TOTAL INVERSION"].astype(float).sum()
            iva_edit = round(subtotal_edit * iva_rate_edit, 2)
            total_edit = round(subtotal_edit + iva_edit, 2)
            impactos_totales_edit = df_editado["TOTAL IMPACTOS"].astype(int).sum()

            # Mostrar resumen en tabla
            resumen_df_edit = pd.DataFrame([{
                "TOTAL IMPACTOS": impactos_totales_edit,
                "SUBTOTAL": f"${subtotal_edit:,.2f}",
                f"IVA ({tipo_iva_edit})": f"${iva_edit:,.2f}" if tipo_iva_edit != "Exento" else "Exento",
                f"TOTAL ({divisa_edit})": f"${total_edit:,.2f}"
            }])
            st.dataframe(resumen_df_edit, hide_index=True, use_container_width=True)

        with tabs[3]:
            if 'materiales_edit' not in st.session_state:
                st.session_state['materiales_edit'] = []

            with st.expander("📦 Información de Materiales", expanded=True):
                nombre = st.text_input("Nombre de Material", key="edit_input_nombre")
                archivo_material_edit = st.file_uploader("Subir Archivo (mp3, wav, mp4, pdf)", type=["mp3", "wav", "mp4", "pdf"], key="edit_input_archivo")
                version = st.text_input("Versión", key="edit_input_version")
                tipo = st.selectbox("Tipo de Material", ["Spot", "Jingle", "Cortinilla", "Otro"], key="edit_input_tipo")

                if st.button("Añadir", key="edit_btn_add_material"):
                    if not nombre:
                        st.warning("Debes indicar un nombre para el material.")
                    elif archivo_material_edit is None:
                        st.warning("Debes subir un archivo antes de añadir.")
                    else:
                        # Usar función alternativa sin mutagen
                        duracion_str = obtener_duracion_archivo(archivo_material_edit)

                        st.session_state['materiales_edit'].append({
                            "Nombre": nombre,
                            "Archivo": archivo_material_edit.name,
                            "Versión": version,
                            "Tipo": tipo,
                            "Duración": duracion_str
                        })
                        st.success(f"Material '{nombre}' añadido correctamente!")

            if st.session_state['materiales_edit']:
                st.table(st.session_state['materiales_edit'])

        with tabs[4]:
            st.markdown("""
                <h2 style='font-size: 20px; font-weight: 600; margin-top: 0em;'>🎙️ ¿Indicaciones Operativas / Conducción / Talentos?</h2>
            """, unsafe_allow_html=True)
            st.text_area("Honorarios / Talentos", placeholder="Ejemplo : Detallar el monto de honorarios y talentos.", key="edit_talentos")

            st.markdown("""
                <h2 style='font-size: 20px; font-weight: 600; margin-top: 1em;'>💳 ¿Indicaciones Facturación y Cobranza?</h2>
            """, unsafe_allow_html=True)
            st.text_area("Cobranza", placeholder="Ejemplo : Facturación al término de la campaña. El cliente no es moroso; y no está bloqueado.", key="edit_cobranza")

            st.markdown("📎 **Cargar pagaré (PDF)**")
            st.file_uploader(" ", type=["pdf"], key="edit_pagare")
            
        with tabs[5]:
            st.button("📤 Enviar Campaña OTC")

        col1, col2, col3 = st.columns(3)
        if col1.button("💾 Guardar Cambios"):
            st.success("Cambios guardados correctamente.")
            st.session_state["folio_edicion"] = None
        if col2.button("❌ Descartar Cambios"):
            st.warning("Edición cancelada.")
            st.session_state["folio_edicion"] = None
        if col3.button("⬅️ Regresar Rechazar"):
            st.warning("Edición cancelada.")
            st.session_state["folio_edicion"] = None

#===== OPCION CONVENIOS
elif opcion_menu == "Convenios":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0rem;">
        <h2 style="font-size: 28px; font-weight: 700; margin: 0;">
            LISTADO DE CONVENIOS
        </h2>
        <div style="display: flex; align-items: center;">
            <div style="text-align: right; margin-right: 10px;">
                <p style="margin: 0; font-size: 14px; font-weight: bold;">BIENVENIDO<br>VENTAS</p>
            </div>
            <div style="background-color: #000000; color: white; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold;">
                VE
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
    st.info("Aquí se mostraría un tabla con los convenios existentes. (Funcionalidad pendiente)")

# FIN
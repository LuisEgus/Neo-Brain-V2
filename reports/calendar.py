import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

import streamlit.components.v1 as components

st.set_page_config(page_title="Neo Brain - Autocalendar", layout="wide")

st.title("Autocalendar")
st.markdown("""
Esta página permite la gestión de reuniones y la asignación de códigos a las mismas.  
Se disponen de dos métodos de asignación:
- **Autorellenado Automático:** Se sugieren códigos para cada reunión; el usuario puede confirmar la propuesta o indicar que no es correcta y asignar otra.
- **Rellenado Manual (por Lotes):** Permite seleccionar varias reuniones y, de forma simultánea, asignar un mismo código.
""")

# -----------------------
# Datos y funciones auxiliares
# -----------------------

def obtener_reuniones():
    # Simula 20 reuniones con fechas, horas y detalles
    data = [
        {
            "id": i,
            "fecha": (datetime.today() - timedelta(days=i % 10)).date(),
            "hora": f"{8 + (i % 9):02d}:00",
            "duracion": f"{30 + 15 * (i % 4)}m",
            "titulo": f"Reunión {i} de equipo",
            "codigo": "" if i % 3 != 0 else f"#1741208{i}",
            "detalles": "Revisión de avances y planificación."
        }
        for i in range(1, 21)
    ]
    return pd.DataFrame(data)

df_reuniones = obtener_reuniones()

# -----------------------
# Filtros generales
# -----------------------
st.subheader("Filtros Generales")

col1, col2, col3 = st.columns(3)
with col1:
    fecha_inicio = st.date_input("Fecha inicio", value=df_reuniones["fecha"].min())
with col2:
    fecha_fin = st.date_input("Fecha fin", value=df_reuniones["fecha"].max())
with col3:
    filtro_codigo = st.radio("Filtrar por código", ("Todos", "Con código", "Sin código"), index=0)
filtro_texto = st.text_input("Buscar en título o detalles")

df_filtrado = df_reuniones.copy()
df_filtrado = df_filtrado[(df_filtrado["fecha"] >= fecha_inicio) & (df_filtrado["fecha"] <= fecha_fin)]
if filtro_codigo == "Con código":
    df_filtrado = df_filtrado[df_filtrado["codigo"] != ""]
elif filtro_codigo == "Sin código":
    df_filtrado = df_filtrado[df_filtrado["codigo"] == ""]
if filtro_texto:
    df_filtrado = df_filtrado[
        df_filtrado["titulo"].str.lower().str.contains(filtro_texto.lower()) | 
        df_filtrado["detalles"].str.lower().str.contains(filtro_texto.lower())
    ]

# -----------------------
# Tabs internas para asignación de códigos
# -----------------------
tabs = st.tabs(["Autorellenado Automático", "Rellenado Manual (por Lotes)"])

# ------------------------------------------
# Autorellenado Automático
# ------------------------------------------
with tabs[0]:
    st.subheader("Autorellenado Automático")
    st.markdown("Para cada reunión se sugiere un código. Confirma la sugerencia o ingresa otro código si no es correcto.")
    
    # Trabajo sobre el DataFrame filtrado para el auto-relleno
    df_auto = df_filtrado.copy()
    
    for idx, row in df_auto.iterrows():
        st.markdown(f"### {row['titulo']} (ID: {row['id']})")
        st.write(f"**Fecha:** {row['fecha']}  |  **Hora:** {row['hora']}  |  **Duración:** {row['duracion']}")
        st.write(f"**Detalles:** {row['detalles']}")
        codigo_recomendado = f"#1741{row['id']:04d}"
        if row['codigo']:
            st.write(f"**Código asignado:** {row['codigo']}")
        else:
            st.warning("Esta reunión no tiene código asignado.")
            st.info(f"Código recomendado: {codigo_recomendado}")
            opcion = st.radio(f"Para la reunión '{row['titulo']}'", 
                               ["Confirmar recomendado", "No es correcto"], key=f"auto_{row['id']}")
            if opcion == "Confirmar recomendado":
                df_auto.at[idx, "codigo"] = codigo_recomendado
                st.success(f"Código actualizado a: {codigo_recomendado}")
            else:
                nuevo_codigo = st.text_input(f"Ingrese otro código para '{row['titulo']}'", key=f"nuevo_auto_{row['id']}")
                if nuevo_codigo:
                    df_auto.at[idx, "codigo"] = nuevo_codigo
                    st.success(f"Código actualizado a: {nuevo_codigo}")
    if st.button("Confirmar cambios en Autorellenado Automático"):
        st.success("Se actualizaron los datos (simulación).")
    st.dataframe(df_auto)

# ------------------------------------------
# Rellenado Manual (por Lotes)
# ------------------------------------------
with tabs[1]:
    st.subheader("Rellenado Manual (por Lotes)")
    st.markdown("Selecciona una o varias reuniones y asigna un código en bloque para actualizarlas simultáneamente.")
    
    df_manual = df_filtrado.copy()
    
    # Agregar columna de selección
    seleccionados = []
    st.markdown("### Selección de Reuniones")
    # Se crea una lista de IDs para las reuniones seleccionadas
    for idx, row in df_manual.iterrows():
        col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.3, 0.2])
        with col1:
            seleccion = st.checkbox("", key=f"check_{row['id']}")
            if seleccion:
                seleccionados.append(row['id'])
        with col2:
            st.write(f"**{row['titulo']}**")
        with col3:
            st.write(f"{row['fecha']} - {row['hora']}")
        with col4:
            st.write("Código:", row['codigo'] if row['codigo'] else "N/A")
    st.markdown("---")
    st.write(f"Reuniones seleccionadas: {len(seleccionados)}")
    codigo_lote = st.text_input("Ingrese código para aplicar a las reuniones seleccionadas (ej. '#17412081')", key="codigo_lote")
    if st.button("Asignar código por lotes"):
        if codigo_lote and seleccionados:
            for idx, row in df_manual.iterrows():
                if row['id'] in seleccionados:
                    df_manual.at[idx, "codigo"] = codigo_lote
            st.success(f"Se asignó el código {codigo_lote} a {len(seleccionados)} reunión(es).")
        elif not codigo_lote:
            st.error("Ingrese un código para asignar.")
        else:
            st.error("No se ha seleccionado ninguna reunión.")
    if st.button("Confirmar cambios en Rellenado Manual"):
        st.success("Se actualizaron los datos (simulación).")
    st.dataframe(df_manual)

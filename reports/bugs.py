import streamlit as st
from send_email import send

to = "contacto@tonidev.es"
sender = "Tool"
subject = "Reporte de errores Gestoria VilaFant"

st.title("Reportar errores 🐞")

st.markdown("Si has encontrado un error en la aplicación, por favor, rellena el siguiente formulario para que podamos solucionarlo lo antes posible.")

# Formulario para reportar errores
with st.form(key="error_report"):
    descripcion = st.text_area("Descripción del error")
    pasos = st.text_area("Pasos para reproducir el error")
    comentarios  = st.text_area("Comentarios adicionales (opcional)")
    file = st.file_uploader("Adjuntar captura de pantalla (opcional)", type=["png", "jpg", "jpeg"])
    # Enviar formulario
    if st.form_submit_button("Enviar reporte"):
        st.spinner("Enviando reporte...")
        # Lógica de envío de correo
        send(descripcion,pasos,descripcion,to,file,)
        st.success("¡Gracias por tu reporte! El error ha sido enviado correctamente.")
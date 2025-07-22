import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría ISO 27001", layout="wide")
st.title("🛡️ Evaluación de Auditoría de Sistemas - ISO 27001")

# Diccionario de preguntas por dominio
cuestionario = {
    "Gestión de Accesos": [
        "¿Se aplica el principio de mínimo privilegio en los sistemas críticos?",
        "¿Se implementa autenticación multifactor para accesos remotos?",
        "¿Se revisan periódicamente los accesos otorgados a los usuarios?"
    ],
    "Gestión de Incidentes": [
        "¿Existe un procedimiento formal para responder ante incidentes?",
        "¿Se registran y documentan todos los incidentes ocurridos en los sistemas?",
        "¿Se analizan las causas raíz de los incidentes para evitar recurrencias?"
    ],
    "Seguridad Física": [
        "¿Se controla el acceso físico a las áreas de servidores y centros de datos?",
        "¿Se cuenta con vigilancia y monitoreo en las instalaciones críticas?",
        "¿Se llevan registros de ingreso y salida de personal autorizado?"
    ],
    "Seguridad en BD": [
        "¿Las bases de datos cuentan con cifrado para proteger la información?",
        "¿Se realizan respaldos periódicos de las bases de datos críticas?",
        "¿Se controlan los accesos a las bases de datos mediante roles definidos?"
    ]
}

respuestas = []
st.subheader("📝 Cuestionario ISO 27001")

# Mostrar preguntas con subtítulos por dominio
for dominio, preguntas in cuestionario.items():
    st.markdown(f"### 🔹 {dominio}")  # Subtema como título
    for pregunta in preguntas:
        valor = st.slider(pregunta, 1, 5, 3)
        respuestas.append({"Dominio": dominio, "Pregunta": pregunta, "Respuesta": valor})

# Botón para generar informe
if st.button("✅ Generar Informe"):
    df = pd.DataFrame(respuestas)
    resumen = df.groupby("Dominio")["Respuesta"].mean().reset_index()

    st.subheader("📊 Promedios por Dominio")
    st.dataframe(resumen)

    fig = px.bar(resumen, x="Dominio", y="Respuesta", color="Dominio", range_y=[0, 5])
    st.plotly_chart(fig)

    st.subheader("🚦 Semáforo de Evaluación")
    for _, row in resumen.iterrows():
        dominio = row["Dominio"]
        promedio = row["Respuesta"]

        if promedio < 2.1:
            st.error(f"🔴 {dominio}: Riesgo Alto ({promedio:.2f}) – Se requiere intervención inmediata.")
        elif promedio < 3.6:
            st.warning(f"🟡 {dominio}: Riesgo Medio ({promedio:.2f}) – Oportunidad de mejora.")
        else:
            st.success(f"🟢 {dominio}: Cumplimiento Bueno ({promedio:.2f}) – Controles adecuados.")

        # Recomendaciones por dominio
        if dominio == "Gestión de Accesos":
            st.info("🔧 Recomendación: Aplica mínimo privilegio, revisiones periódicas y autenticación multifactor.")
        elif dominio == "Gestión de Incidentes":
            st.info("🔧 Recomendación: Formaliza los procedimientos de respuesta, registra y analiza los incidentes.")
        elif dominio == "Seguridad Física":
            st.info("🔧 Recomendación: Controla accesos físicos, aplica vigilancia y registra accesos a zonas críticas.")
        elif dominio == "Seguridad en BD":
            st.info("🔧 Recomendación: Protege las bases con cifrado, respaldos automáticos y control por roles.")

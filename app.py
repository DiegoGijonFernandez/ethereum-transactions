import streamlit as st
st.set_page_config(layout="wide")
from base64 import b64encode

def set_background(image_file_path):
    with open(image_file_path, "rb") as f:
        encoded = b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 12px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("data/1984-de-george-orwell-9.jpeg")


import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("data/Transacciones_Simuladas_Ethereum.csv", parse_dates=['timestamp'])

    # Mapear tipo de transacción a su descripción
    df['tx_type_desc'] = df['tx_type'].map({
        '0x0': 'Legacy (pre-EIP)',
        '0x1': 'Access List (EIP-2930)',
        '0x2': 'Dynamic Fees (EIP-1559)',
        '0x3': 'Blob (EIP-4844)',
        '0x4': 'SetCode (EIP-7702)'
    })

    # Una transacción se considera de riesgo si cumple con una o más de las siguientes condiciones:
    # mueve una cantidad significativa de valor (más de 5 ETH), utiliza una cantidad inusualmente alta de gas (más de 250,000 unidades, lo cual puede indicar operaciones complejas o costosas), 
    # despliega un contrato inteligente (que podría contener lógica maliciosa), 
    # o utiliza tipos de transacción avanzados como blob (`0x3`, EIP-4844) o setcode (`0x4`, EIP-7702), que son menos comunes y potencialmente más peligrosos si se abusan. 
    # Cuantas más de estas condiciones se cumplan, mayor será el nivel de riesgo asignado a la transacción

    def evaluar_riesgo(tx):
        explicaciones = []
        puntos = 0

        if tx['value'] > 5:
            puntos += 1
            explicaciones.append(f"Valor enviado = {tx['value']} ETH > 5 ETH")
        if tx['gasUsed'] > 250000:
            puntos += 1
            explicaciones.append(f"Gas usado = {tx['gasUsed']} > 250000")
        if tx['contract_deploy'] == 1:
            puntos += 1
            explicaciones.append("Es despliegue de contrato")
        if tx['tx_type'] in ['0x3', '0x4']:
            puntos += 1
            explicaciones.append(f"Tipo avanzado: {tx['tx_type']}")

        if puntos >= 3:
            return pd.Series(["Alto", "; ".join(explicaciones)])
        elif puntos == 2:
            return pd.Series(["Medio", "; ".join(explicaciones)])
        elif puntos == 1:
            return pd.Series(["Bajo", "; ".join(explicaciones)])
        else:
            return pd.Series(["Ninguno", "Sin señales claras de riesgo"])

    df[['Riesgo', 'Explicacion']] = df.apply(evaluar_riesgo, axis=1)

    return df

df = load_data()

st.title("Explorador y Análisis de Transacciones Ethereum")

tab1, tab2 = st.tabs(["📁 Explorador de Bloques", "⚠️ Análisis de Riesgo"])


with tab1:
    st.header("🔎 Explora transacciones por bloque, tipo o emisor")

    col1, col2, col3 = st.columns(3)
    with col1:
        bloque = st.selectbox("Selecciona bloque", options=["Todos"] + sorted(df['blockNumber'].unique().tolist()))
    with col2:
        tipo = st.selectbox("Tipo de transacción", options=["Todos"] + df['tx_type'].unique().tolist())
    with col3:
        emisor = st.text_input("Buscar dirección del emisor")

    filtrado = df.copy()
    if bloque != "Todos":
        filtrado = filtrado[filtrado['blockNumber'] == int(bloque)]
    if tipo != "Todos":
        filtrado = filtrado[filtrado['tx_type'] == tipo]
    if emisor:
        filtrado = filtrado[filtrado['from'].str.contains(emisor, case=False)]

    st.write(f"Transacciones encontradas: {len(filtrado)}")
    st.dataframe(filtrado[[
        'blockNumber', 'timestamp', 'from', 'to', 'value',
        'gasUsed', 'tx_type', 'tx_type_desc', 'contract_deploy', 'hash'
    ]].rename(columns={
        'blockNumber': 'Bloque',
        'timestamp': 'Fecha',
        'from': 'Emisor',
        'to': 'Receptor',
        'value': 'Valor (ETH)',
        'gasUsed': 'Gas Usado',
        'tx_type': 'Tipo',
        'tx_type_desc': 'Descripción Tipo',
        'contract_deploy': '¿Contrato?',
        'hash': 'Hash'
    }), height=400)

with tab2:
    st.header("⚠️ Análisis detallado de riesgo")

    col1, col2, col3 = st.columns(3)
    with col1:
        riesgo = st.selectbox("Filtrar por riesgo", options=["Todos", "Alto", "Medio", "Bajo", "Ninguno"])
    with col2:
        tipo2 = st.selectbox("Tipo de transacción", options=["Todos"] + df['tx_type'].unique().tolist(), key='tipo2')
    with col3:
        bloque2 = st.selectbox("Bloque", options=["Todos"] + sorted(df['blockNumber'].unique().tolist()), key='bloque2')

    sospechosas = df.copy()
    if riesgo != "Todos":
        sospechosas = sospechosas[sospechosas['Riesgo'] == riesgo]
    if tipo2 != "Todos":
        sospechosas = sospechosas[sospechosas['tx_type'] == tipo2]
    if bloque2 != "Todos":
        sospechosas = sospechosas[sospechosas['blockNumber'] == int(bloque2)]

    st.subheader("📋 Transacciones con riesgo")
    st.dataframe(sospechosas[[
        'timestamp', 'from', 'to', 'value', 'gasUsed',
        'tx_type', 'tx_type_desc', 'contract_deploy', 'Riesgo', 'Explicacion'
    ]].rename(columns={
        'timestamp': 'Fecha',
        'from': 'Emisor',
        'to': 'Receptor',
        'value': 'Valor (ETH)',
        'gasUsed': 'Gas Usado',
        'tx_type': 'Tipo',
        'tx_type_desc': 'Descripción Tipo',
        'contract_deploy': '¿Contrato?',
        'Riesgo': 'Nivel de Riesgo',
        'Explicacion': 'Justificación'
    }), height=400)

    st.subheader("📊 Visualización")
    col4, col5 = st.columns(2)

    with col4:
        fig1, ax1 = plt.subplots()
        df['Riesgo'].value_counts().plot(kind='bar', ax=ax1, color='gray')
        ax1.set_title("Niveles de riesgo")
        ax1.set_ylabel("Número de transacciones")
        st.pyplot(fig1)

    with col5:
        fig2, ax2 = plt.subplots()
        df['tx_type_desc'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
        ax2.set_ylabel("")
        ax2.set_title("Distribución por tipo de transacción")
        st.pyplot(fig2)
        
st.markdown("""
    <style>
    /* Color de texto general */
    html, body, .stApp {
        color: black !important;
    }

    /* Cuadro de texto */
    .stTextInput input {
        background-color: black !important;
        color: white !important;
        border: 1px solid #888 !important;
        border-radius: 8px;
    }

    /* Cuadros de selección */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        color: black !important;
        border-radius: 6px;
    }

    .stSelectbox [role="option"] {
        background-color: white !important;
        color: black !important;
    }

    /* Encabezados y etiquetas */
    h1, h2, h3, h4, h5, h6, label {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

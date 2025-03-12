import streamlit as st
import pandas as pd

def formato_moneda(valor):
    """Formatea un valor numérico como moneda en pesos argentinos."""
    try:
        return f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return f"${valor}"

def validar_numero_positivo(valor):
    """Valida que un valor sea un número positivo."""
    try:
        numero = float(valor)
        return numero >= 0
    except ValueError:
        return False

def exportar_datos(df):
    """Exporta los datos a un archivo CSV."""
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="datos_financieros.csv",
        mime="text/csv"
    )
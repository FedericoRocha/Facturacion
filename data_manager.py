import pandas as pd
import numpy as np

def agregar_registro(df, fecha, datos):
    """Agrega un nuevo registro financiero al DataFrame."""
    datos['fecha'] = fecha
    datos['iva_debito'] = datos['facturacion_a'] * 0.21 + datos['facturacion_b'] * 0.21
    datos['iva_credito'] = datos['gastos_operativos'] * 0.21
    datos['iva_total'] = datos['iva_debito'] - datos['iva_credito']

    datos['ingresos_brutos'] = (datos['facturacion_a'] + datos['facturacion_b'] + datos['facturacion_c']) * 0.035

    datos['utilidad'] = (
        datos['facturacion_a'] + datos['facturacion_b'] + datos['facturacion_c']
        - datos['gastos_operativos']
        - datos['otros_gastos']
        - datos['iva_total']
        - datos['ingresos_brutos']
        - datos['retenciones']
    )

    nuevo_registro = pd.DataFrame([datos])
    return pd.concat([df, nuevo_registro], ignore_index=True)

def agrupar_por_periodo(df, periodo):
    """Agrupa los datos según el período seleccionado."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'])

    if periodo == "Mensual":
        return df.set_index('fecha').resample('ME').sum()
    elif periodo == "Bimestral":
        return df.set_index('fecha').resample('2ME').sum()
    elif periodo == "Trimestral":
        return df.set_index('fecha').resample('QE').sum()
    else:  # Anual
        return df.set_index('fecha').resample('YE').sum()

def analisis_mensual(df):
    """Realiza un análisis detallado mensual."""
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'])
    df_mensual = df.set_index('fecha').resample('ME').agg({
        'facturacion_a': 'sum',
        'facturacion_b': 'sum',
        'facturacion_c': 'sum',
        'gastos_operativos': 'sum',
        'otros_gastos': 'sum',
        'retenciones': 'sum',
        'iva_total': 'sum',
        'ingresos_brutos': 'sum',
        'utilidad': 'sum'
    })

    # Calcular totales y promedios mensuales
    df_mensual['facturacion_total'] = df_mensual['facturacion_a'] + df_mensual['facturacion_b'] + df_mensual['facturacion_c']
    df_mensual['gastos_totales'] = df_mensual['gastos_operativos'] + df_mensual['otros_gastos']
    df_mensual['impuestos_totales'] = df_mensual['iva_total'] + df_mensual['ingresos_brutos'] + df_mensual['retenciones']

    return df_mensual

def calcular_estadisticas(df):
    """Calcula estadísticas básicas de los datos financieros."""
    return {
        'facturacion_total': df[['facturacion_a', 'facturacion_b', 'facturacion_c']].sum().sum(),
        'gastos_totales': df['gastos_operativos'].sum() + df['otros_gastos'].sum(),
        'impuestos_totales': df['iva_total'].sum() + df['ingresos_brutos'].sum() + df['retenciones'].sum(),
        'utilidad_total': df['utilidad'].sum(),
        'promedio_facturacion': df[['facturacion_a', 'facturacion_b', 'facturacion_c']].sum(axis=1).mean(),
        'promedio_gastos': (df['gastos_operativos'] + df['otros_gastos']).mean()
    }
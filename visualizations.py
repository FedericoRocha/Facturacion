import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def grafico_lineas_temporales(df):
    """Crea un gráfico de líneas para la evolución temporal."""
    fig = go.Figure()

    # Facturación total
    facturacion_total = df['facturacion_a'] + df['facturacion_b'] + df['facturacion_c']
    fig.add_trace(go.Scatter(
        x=df.index,
        y=facturacion_total,
        name='Facturación Total',
        line=dict(color='#2ecc71')
    ))

    # Gastos totales
    gastos_totales = df['gastos_operativos'] + df['otros_gastos']
    fig.add_trace(go.Scatter(
        x=df.index,
        y=gastos_totales,
        name='Gastos Totales',
        line=dict(color='#e74c3c')
    ))

    # Utilidad
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['utilidad'],
        name='Utilidad',
        line=dict(color='#3498db')
    ))

    fig.update_layout(
        title='Evolución Temporal',
        xaxis_title='Fecha',
        yaxis_title='Monto ($)',
        hovermode='x unified',
        xaxis=dict(
            tickformat="%B %Y",
            tickangle=45
        )
    )

    return fig

def grafico_barras_comparativo(df):
    """Crea un gráfico de barras comparativo de facturación por tipo."""
    fig = go.Figure(data=[
        go.Bar(
            name='Facturación A',
            x=df.index,
            y=df['facturacion_a'],
            marker_color='#2ecc71'
        ),
        go.Bar(
            name='Facturación B',
            x=df.index,
            y=df['facturacion_b'],
            marker_color='#3498db'
        ),
        go.Bar(
            name='Facturación C',
            x=df.index,
            y=df['facturacion_c'],
            marker_color='#9b59b6'
        )
    ])

    fig.update_layout(
        title='Comparativo de Facturación por Tipo',
        barmode='stack',
        xaxis_title='Fecha',
        yaxis_title='Monto ($)',
        xaxis=dict(
            tickformat="%B %Y",
            tickangle=45
        )
    )

    return fig

def grafico_barras_gastos(df):
    """Crea un gráfico de barras para los gastos."""
    fig = go.Figure(data=[
        go.Bar(
            name='Gastos Operativos',
            x=df.index,
            y=df['gastos_operativos'],
            marker_color='#e74c3c'
        ),
        go.Bar(
            name='Otros Gastos',
            x=df.index,
            y=df['otros_gastos'],
            marker_color='#f39c12'
        )
    ])

    fig.update_layout(
        title='Análisis de Gastos',
        barmode='stack',
        xaxis_title='Fecha',
        yaxis_title='Monto ($)',
        xaxis=dict(
            tickformat="%B %Y",
            tickangle=45
        )
    )

    return fig

def grafico_impuestos(df):
    """Crea un gráfico de área para los impuestos."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['iva_total'],
        name='IVA',
        fill='tonexty',
        line=dict(color='#3498db')
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['ingresos_brutos'],
        name='Ingresos Brutos',
        fill='tonexty',
        line=dict(color='#2ecc71')
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['retenciones'],
        name='Retenciones',
        fill='tonexty',
        line=dict(color='#e74c3c')
    ))

    fig.update_layout(
        title='Evolución de Impuestos',
        xaxis_title='Fecha',
        yaxis_title='Monto ($)',
        hovermode='x unified',
        xaxis=dict(
            tickformat="%B %Y",
            tickangle=45
        )
    )

    return fig
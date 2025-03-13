import streamlit as st
import pandas as pd
from datetime import datetime
import data_manager as dm
import visualizations as viz
import utils
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la página
try:
    st.set_page_config(
        page_title="Gestión Financiera",
        page_icon="💰",
        layout="wide"
    )
    logger.info("Configuración de página completada")
except Exception as e:
    logger.error(f"Error en la configuración de página: {str(e)}")
    st.error("Error al configurar la página")

# Inicialización del estado de la sesión
try:
    if 'datos_financieros' not in st.session_state:
        st.session_state.datos_financieros = pd.DataFrame(columns=[
            'fecha', 'facturacion_a', 'facturacion_b', 'facturacion_c',
            'gastos_operativos', 'otros_gastos', 'retenciones',
            'iva_debito', 'iva_credito', 'iva_total',
            'ingresos_brutos', 'utilidad'
        ])
        logger.info("Estado de sesión inicializado correctamente")
except Exception as e:
    logger.error(f"Error al inicializar el estado de sesión: {str(e)}")
    st.error("Error al inicializar los datos")

def main():
    try:
        st.title("📊 Sistema de Gestión Financiera")
        logger.info("Aplicación iniciada correctamente")

        # Sidebar para navegación
        menu = st.sidebar.selectbox(
            "Menú Principal",
            ["Ingreso de Datos", "Análisis Mensual", "Análisis Temporal", "Estadísticas"]
        )

        if menu == "Ingreso de Datos":
            mostrar_ingreso_datos()
        elif menu == "Análisis Mensual":
            mostrar_analisis_mensual()
        elif menu == "Análisis Temporal":
            mostrar_analisis_temporal()
        else:
            mostrar_estadisticas()

    except Exception as e:
        logger.error(f"Error en la función principal: {str(e)}")
        st.error("Se produjo un error en la aplicación")

def mostrar_ingreso_datos():
    st.header("📝 Ingreso de Datos Financieros")

    with st.form("formulario_datos"):
        col1, col2, col3 = st.columns([1, 1, 1])

        # Primera fila: Mes, Año y Gastos operativos
        with col1:
            # Selector de mes
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            mes = st.selectbox(
                "Mes",
                meses,
                index=datetime.now().month - 1,  # Mes actual por defecto
                help="Seleccione el mes"
            )

        with col2:
            # Selector de año
            año_actual = datetime.now().year
            año = st.selectbox(
                "Año",
                range(año_actual - 5, año_actual + 1),
                index=5,  # Seleccionar año actual por defecto
                help="Seleccione el año"
            )

        with col3:
            gastos_operativos = st.number_input(
                "Gastos Operativos ($)",
                min_value=0.0,
                format="%f",
                help="Ingrese el total de gastos operativos"
            )

        # Segunda fila: Facturaciones
        st.markdown("### Facturación")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            facturacion_a = st.number_input(
                "Facturación A ($)",
                min_value=0.0,
                format="%f",
                help="Ingrese el monto de facturación tipo A"
            )

        with col2:
            facturacion_b = st.number_input(
                "Facturación B ($)",
                min_value=0.0,
                format="%f",
                help="Ingrese el monto de facturación tipo B"
            )

        with col3:
            facturacion_c = st.number_input(
                "Facturación C ($)",
                min_value=0.0,
                format="%f",
                help="Ingrese el monto de facturación tipo C"
            )

        # Tercera fila: Otros gastos y retenciones
        st.markdown("### Otros Conceptos")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            otros_gastos = st.number_input(
                "Otros Gastos ($)",
                min_value=0.0,
                format="%f",
                help="Ingrese otros gastos no operativos"
            )

        with col2:
            retenciones = st.number_input(
                "Retenciones ($)",
                min_value=0.0,
                format="%f",
                help="Ingrese el monto total de retenciones"
            )

        submitted = st.form_submit_button("Guardar Datos")

        if submitted:
            # Crear fecha para el primer día del mes seleccionado
            mes_num = meses.index(mes) + 1
            fecha = pd.Timestamp(año, mes_num, 1)

            datos = {
                'facturacion_a': facturacion_a,
                'facturacion_b': facturacion_b,
                'facturacion_c': facturacion_c,
                'gastos_operativos': gastos_operativos,
                'otros_gastos': otros_gastos,
                'retenciones': retenciones
            }

            try:
                nuevo_registro = dm.agregar_registro(
                    st.session_state.datos_financieros,
                    fecha,
                    datos
                )
                st.session_state.datos_financieros = nuevo_registro
                st.success("✅ Datos guardados exitosamente!")
                logger.info("Datos guardados correctamente")
            except Exception as e:
                logger.error(f"Error al guardar los datos: {str(e)}")
                st.error("Error al guardar los datos")


def mostrar_analisis_mensual():
    st.header("📅 Análisis Mensual")

    if st.session_state.datos_financieros.empty:
        st.warning("⚠️ No hay datos disponibles para analizar")
        return

    # Obtener análisis mensual
    try:
        df_mensual = dm.analisis_mensual(st.session_state.datos_financieros)
    except Exception as e:
        logger.error(f"Error al generar el análisis mensual: {str(e)}")
        st.error("Error al generar el análisis mensual")
        return

    # Selector de mes
    meses = df_mensual.index.strftime('%B %Y').tolist()
    mes_seleccionado = st.selectbox("Seleccione el mes", meses)
    df_mes = df_mensual.loc[df_mensual.index.strftime('%B %Y') == mes_seleccionado]

    # Mostrar resumen del mes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Facturación Total del Mes",
            utils.formato_moneda(df_mes['facturacion_total'].iloc[0])
        )

    with col2:
        st.metric(
            "Gastos Totales del Mes",
            utils.formato_moneda(df_mes['gastos_totales'].iloc[0])
        )

    with col3:
        st.metric(
            "Utilidad del Mes",
            utils.formato_moneda(df_mes['utilidad'].iloc[0])
        )

    # Gráficos mensuales
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            viz.grafico_barras_comparativo(df_mensual),
            use_container_width=True
        )
        st.plotly_chart(
            viz.grafico_impuestos(df_mensual),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            viz.grafico_barras_gastos(df_mensual),
            use_container_width=True
        )
        st.plotly_chart(
            viz.grafico_lineas_temporales(df_mensual),
            use_container_width=True
        )

def mostrar_analisis_temporal():
    st.header("📈 Análisis Temporal")

    if st.session_state.datos_financieros.empty:
        st.warning("⚠️ No hay datos disponibles para analizar")
        return

    periodo = st.selectbox(
        "Seleccione el período de análisis",
        ["Mensual", "Bimestral", "Trimestral", "Anual"]
    )

    try:
        df_analisis = dm.agrupar_por_periodo(
            st.session_state.datos_financieros,
            periodo
        )
    except Exception as e:
        logger.error(f"Error al generar el análisis temporal: {str(e)}")
        st.error("Error al generar el análisis temporal")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            viz.grafico_lineas_temporales(df_analisis),
            use_container_width=True
        )
        st.plotly_chart(
            viz.grafico_impuestos(df_analisis),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            viz.grafico_barras_comparativo(df_analisis),
            use_container_width=True
        )
        st.plotly_chart(
            viz.grafico_barras_gastos(df_analisis),
            use_container_width=True
        )

def mostrar_estadisticas():
    st.header("📊 Estadísticas Financieras")

    if st.session_state.datos_financieros.empty:
        st.warning("⚠️ No hay datos disponibles para analizar")
        return

    try:
        stats = dm.calcular_estadisticas(st.session_state.datos_financieros)
    except Exception as e:
        logger.error(f"Error al calcular las estadísticas: {str(e)}")
        st.error("Error al calcular las estadísticas")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resumen General")
        st.metric(
            "Facturación Total",
            utils.formato_moneda(stats['facturacion_total'])
        )
        st.metric(
            "Gastos Totales",
            utils.formato_moneda(stats['gastos_totales'])
        )
        st.metric(
            "Impuestos Totales",
            utils.formato_moneda(stats['impuestos_totales'])
        )
        st.metric(
            "Utilidad Total",
            utils.formato_moneda(stats['utilidad_total'])
        )

    with col2:
        st.plotly_chart(
            viz.grafico_lineas_temporales(st.session_state.datos_financieros),
            use_container_width=True
        )

    if st.button("Exportar Datos"):
        try:
            utils.exportar_datos(st.session_state.datos_financieros)
            logger.info("Datos exportados correctamente")
        except Exception as e:
            logger.error(f"Error al exportar los datos: {str(e)}")
            st.error("Error al exportar los datos")

if __name__ == "__main__":
    try:
        main()
        logger.info("Aplicación ejecutada exitosamente")
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {str(e)}")
        st.error("Error crítico en la aplicación")
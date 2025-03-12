from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
import data_manager as dm

api = FastAPI(title="API Financiera para Power BI")

# Variable global para almacenar datos
datos_financieros = pd.DataFrame(columns=[
    'fecha', 'facturacion_a', 'facturacion_b', 'facturacion_c',
    'gastos_operativos', 'otros_gastos', 'retenciones',
    'iva_debito', 'iva_credito', 'iva_total',
    'ingresos_brutos', 'utilidad'
])

# Configurar CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/")
async def root():
    """Endpoint de prueba."""
    return {"message": "API Financiera funcionando correctamente"}

@api.post("/actualizar_datos")
async def actualizar_datos(data: dict):
    """Endpoint para actualizar datos desde Streamlit."""
    global datos_financieros
    try:
        datos_financieros = pd.DataFrame(data['datos'])
        return {"message": "Datos actualizados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/datos/mensuales")
async def obtener_datos_mensuales():
    """Endpoint para obtener datos mensuales."""
    try:
        if datos_financieros.empty:
            return []

        df_mensual = dm.analisis_mensual(datos_financieros)
        datos_power_bi = df_mensual.reset_index().to_dict(orient='records')

        # Formatear fechas para Power BI
        for registro in datos_power_bi:
            registro['fecha'] = registro['fecha'].strftime('%Y-%m-%d')

        return datos_power_bi
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/datos/estadisticas")
async def obtener_estadisticas():
    """Endpoint para obtener estadísticas generales."""
    try:
        if datos_financieros.empty:
            return {}
        return dm.calcular_estadisticas(datos_financieros)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/datos/categorias")
async def obtener_datos_por_categoria():
    """Endpoint para obtener datos agrupados por categoría."""
    try:
        if datos_financieros.empty:
            return {}

        # Agrupar datos por categorías relevantes
        categorias = {
            'facturacion': {
                'A': float(datos_financieros['facturacion_a'].sum()),
                'B': float(datos_financieros['facturacion_b'].sum()),
                'C': float(datos_financieros['facturacion_c'].sum())
            },
            'gastos': {
                'operativos': float(datos_financieros['gastos_operativos'].sum()),
                'otros': float(datos_financieros['otros_gastos'].sum())
            },
            'impuestos': {
                'iva': float(datos_financieros['iva_total'].sum()),
                'ingresos_brutos': float(datos_financieros['ingresos_brutos'].sum()),
                'retenciones': float(datos_financieros['retenciones'].sum())
            }
        }

        return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
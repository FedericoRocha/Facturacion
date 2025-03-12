# Sistema de Gestión Financiera

Aplicación de gestión financiera desarrollada con Streamlit para análisis temporal y visualizaciones.

## Requisitos previos

1. Python 3.10 o superior
2. pip (gestor de paquetes de Python)
3. Power BI Desktop (para la integración con Power BI)

## Instalación

1. Clona o descarga este repositorio en tu equipo local

2. Instala las dependencias necesarias ejecutando:
```bash
pip install streamlit pandas plotly numpy fastapi uvicorn
```

## Ejecución Local

Para ejecutar la aplicación completa necesitas iniciar dos componentes en terminales separadas:

1. La aplicación Streamlit (interfaz de usuario):
```bash
streamlit run main.py
```
La interfaz estará disponible en: http://localhost:8501

2. La API para Power BI (en una terminal separada):
```bash
python run_api.py
```
La API estará disponible en: http://localhost:8000

## Estructura del Proyecto

- `main.py`: Aplicación principal (Streamlit)
- `run_api.py`: Servidor de la API
- `api.py`: Definición de endpoints de la API
- `data_manager.py`: Gestión y procesamiento de datos
- `visualizations.py`: Funciones para crear gráficos
- `utils.py`: Utilidades y funciones auxiliares

## Integración con Power BI

1. Asegúrate de que ambos servidores estén ejecutándose:
   - Aplicación Streamlit en http://localhost:8501
   - API en http://localhost:8000

2. En Power BI Desktop:
   - Selecciona "Obtener datos" > "Web"
   - Ingresa una de las siguientes URLs:
     * Datos mensuales: `http://localhost:8000/datos/mensuales`
     * Estadísticas generales: `http://localhost:8000/datos/estadisticas`
     * Datos por categoría: `http://localhost:8000/datos/categorias`
   - Selecciona "JSON" como formato de origen de datos
   - Haz clic en "Aceptar"

3. Creación de visualizaciones en Power BI:
   - Usa el campo 'fecha' para el eje temporal
   - Arrastra campos como 'facturacion_total', 'gastos_totales' o 'utilidad' a la zona de valores
   - Crea gráficos según tus necesidades:
     * Gráfico de líneas para tendencias temporales
     * Gráfico de barras para comparaciones mensuales
     * Tarjetas para mostrar totales y promedios

4. Los datos se actualizarán automáticamente cada vez que refresques Power BI


## Solución de Problemas Comunes

1. **La aplicación no se inicia**
   - Verifica que Python esté instalado: `python --version`
   - Asegúrate de tener todas las dependencias: `pip list`
   - Revisa que estés en el directorio correcto

2. **No puedes ver la aplicación en el navegador**
   - Verifica que los puertos 8501 y 8000 estén disponibles
   - Intenta acceder directamente a http://localhost:8501
   - Asegúrate de que no hay otros servicios usando estos puertos

3. **Power BI no puede conectarse a la API**
   - Verifica que el servidor API esté ejecutándose (python run_api.py)
   - Prueba acceder a http://localhost:8000/datos/estadisticas en tu navegador
   - Asegúrate de usar 'localhost' en lugar de '0.0.0.0' en Power BI

4. **Los datos no persisten**
   - Usa la función "Exportar Datos" en la sección de Estadísticas
   - Guarda regularmente tus datos en CSV

## Funcionalidades

1. **Ingreso de Datos**
   - Registro de facturación (A, B, C)
   - Gastos operativos y otros gastos
   - Retenciones e impuestos

2. **Análisis Mensual**
   - Visualización detallada por mes
   - Gráficos comparativos
   - Métricas clave

3. **Análisis Temporal**
   - Evolución de indicadores en el tiempo
   - Comparativas por períodos
   - Tendencias y patrones

4. **Estadísticas**
   - Resumen general
   - Indicadores clave
   - Exportación de datos

## Datos

Los datos se almacenan en memoria durante la sesión. Si necesitas persistencia, puedes exportar los datos a CSV usando la opción "Exportar Datos" en la sección de Estadísticas.

## Respaldo de Datos

Para mantener un registro de tus datos:
1. Usa regularmente la función "Exportar Datos" en la sección de Estadísticas
2. Guarda los archivos CSV exportados en una ubicación segura
3. Puedes usar estos archivos para análisis externos o como respaldo
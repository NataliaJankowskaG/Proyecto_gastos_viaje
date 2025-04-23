# Proyecto_gastos_viaje

Objetivo del proyecto:
Automatización Inteligente de Gastos de Viaje con API de ChatGPT, usando Python y visualizando en Power BI.

Por aquí os comparto un proyecto en el que he trabajado junto a [@Nombre1], [@Nombre2], [@Nombre3] y [@Nombre4], donde combinamos el poder de la automatización con inteligencia artificial (API de ChatGPT) para transformar la gestión de gastos de viaje en más automatizado, eficiente y visual.

¿Cuál era el reto?
Procesar tickets y facturas de viaje de forma manual es lento, propenso a errores y limita el control financiero en tiempo real.

Resumen: diseñamos un sistema que automatiza el ciclo (el usuario tiene que sacar o escanear fotos de facturas y meterlos en carpeta), después a usando la API de chatGPT el código lee de forma automatizada texto de las imágenes (facturas - tickets) y pasa la información a formato de base de datos (.db) en sqlite. Después preparamos en PowerBI análisis y visualización con dashboard interactivo.

En equipo creamos una solución que:
Utiliza la API de ChatGPT (GPT-4o-mini) para leer imágenes de tickets y extraer información estructurada automáticamente (fecha, importe, tipo de gasto, lugar, etc.).
Procesa los datos con Python, clasificando automáticamente los tipos de gasto gracias al análisis de lenguaje natural.
Guarda los datos de forma segura en una base de datos SQLite, lista para ser consultada, auditada o integrada con otros sistemas.
Visualiza todo en Power BI, con dashboards dinámicos.

Beneficios para el negocio:
Reducción del tiempo de procesamiento de tickets.
Eliminación de errores humanos gracias a la clasificación automática por IA (API).
Visualización clara del presupuesto en tiempo real.
Optimización de gastos personales o corporativos con base en datos históricos y categorización inteligente.


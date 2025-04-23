# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 13:56:27 2025

@author: LANER
"""

from funciones import procesamiento_prompt, procesar_respuesta_JSON, rellenar_tabla_desde_json, procesar_imagenes_en_carpeta


# Ruta a la imagen del ticket
ruta_imagen = r"C:\Users\iblan\Desktop\Proyecto IA+Python+Power BI\Tickets"

# Prompt para el análisis (puedes personalizarlo)
prompt = """
Por favor, extrae toda la información relevante de la siguiente factura en formato estructurado. Los detalles que necesitas extraer incluyen:

1. Fecha de la factura: La fecha en la que fue emitida la factura. Ejemplo: "2025-04-05". Formato: "YYYY-MM-DD" (ISO 8601).
2. Coste total de la factura: El valor total de la factura, incluyendo impuestos, si corresponde. Asegúrate de que el coste esté en euros (€). Ejemplo: "3,60 €". Formato: Número con dos decimales seguido de un espacio y símbolo de euro.
3. Tipo de gasto: El tipo de gasto asociado a la factura, como por ejemplo: "Comida", "Transporte", "Alojamiento", "Otros gastos". Ejemplo: "Transporte". Formato: Primera letra en mayúscula, el resto en minúsculas.
4. Nombre de la empresa: El nombre de la empresa que emitió la factura. Ejemplo: "ABC Servicios S.A.". Formato: Cada palabra con la primera letra en mayúscula.
5. Ciudad, provincia y país: La ciudad, la provincia y el país donde se realizó el gasto. Ejemplo: "Bilbao, Vizcaya, España". Formato: Primera letra en mayúscula, el resto en minúsculas.
6. Número de factura: El número único de la factura. Ejemplo: "FAC-123456". Se conserva exactamente como aparece (no se altera mayúsculas o formato).
7. Método de pago: El método de pago utilizado, si está disponible. Ejemplo: "Tarjeta de crédito", "Efectivo", etc.

**Instrucciones adicionales:**
- Devuelve la información extraída en formato JSON, con los campos exactamente como se describen a continuación.
- Si un campo no está disponible o no se encuentra en la factura, debe devolver el valor como ‘No disponible’.
- Asegúrate de que la respuesta esté perfectamente estructurada como un JSON válido, sin texto adicional.
- Los valores monetarios deben estar siempre en **euros (€)**.
-
Formato del JSON:
{
  "fecha_factura": "2025-04-05",
  "coste_total": "3,60 €",
  "tipo_gasto": "Comida",
  "nombre_empresa": "ABC Servicios S.A.",
  "ciudad": "Bilbao",
  "provincia": "Vizcaya",
  "pais": "España",
  "numero_factura": "FAC-123456",
  "metodo_pago": "Tarjeta de crédito"
}
"""

ruta_db = "tickets.db"
nombre_tabla = "gastos"

procesar_imagenes_en_carpeta(ruta_imagen, prompt, ruta_db, nombre_tabla)

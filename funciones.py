# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 13:56:29 2025

@author: LANER
"""

import os
import openai
from openai import OpenAI
import json
import logging
import sqlite3
import base64
from dotenv import load_dotenv
import shutil


# Esta función se encarga de enviar el texto + imagen (si hay) a OpenAI y obtener una respuesta.
def procesamiento_prompt(prompt, image_file=None):
    # Cargar archivo .env desde la ruta absoluta (más seguro)
    load_dotenv(dotenv_path=".env")
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if image_file:
        # Convertir la imagen a base64
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1500,
        )
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
        )

    return response.choices[0].message.content


def procesar_respuesta_JSON(respuesta):
    """
    Procesa la respuesta devuelta por OpenAI y extrae el contenido JSON.
    
    Args:
        respuesta (str): La respuesta de OpenAI en formato de texto.
        
    Returns:
        dict o list: Un diccionario o lista con los datos extraídos.
        None: Si no se puede procesar la respuesta como JSON.
    """
    try:
        # Detectar si hay un objeto o una lista JSON en la respuesta
        json_inicio_obj = respuesta.find('{')
        json_inicio_list = respuesta.find('[')

        # Determinar qué tipo de estructura aparece primero
        if (json_inicio_list != -1 and (json_inicio_obj == -1 or json_inicio_list < json_inicio_obj)):
            json_inicio = json_inicio_list
            json_final = respuesta.rfind(']') + 1
        elif json_inicio_obj != -1:
            json_inicio = json_inicio_obj
            json_final = respuesta.rfind('}') + 1
        else:
            print("❌ No se encontró un JSON válido en la respuesta.")
            logging.error(f"No se encontró JSON válido en la respuesta: {respuesta}")
            return None

        json_str = respuesta[json_inicio:json_final]

        # Intentamos parsear el JSON
        datos = json.loads(json_str)
        return datos

    except json.JSONDecodeError as e:
        print("❌ Error al leer JSON de respuesta.")
        print(f"Respuesta recibida:\n{respuesta}")
        logging.error(f"JSON inválido: {e}")
        return None


def rellenar_tabla_desde_json(json_data: dict, ruta_db: str, nombre_tabla: str):
    with sqlite3.connect(ruta_db) as conn:
        cursor = conn.cursor()

        # Crear la tabla solo con los campos que vas a usar
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {nombre_tabla} (
                fecha_factura TEXT,
                coste_total TEXT,  -- Usamos TEXT por si viene con símbolos como "€"
                tipo_gasto TEXT,
                nombre_empresa TEXT,
                ciudad TEXT,
                provincia TEXT,
                pais TEXT,
                numero_factura TEXT,
                metodo_pago TEXT
            )
        """)

        # Insertar directamente el diccionario
        cursor.execute(f"""
            INSERT INTO {nombre_tabla} (
                fecha_factura,
                coste_total,
                tipo_gasto,
                nombre_empresa,
                ciudad,
                provincia,
                pais,
                numero_factura,
                metodo_pago
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            json_data.get("fecha_factura"),
            json_data.get("coste_total"),
            json_data.get("tipo_gasto"),
            json_data.get("nombre_empresa"),
            json_data.get("ciudad"),
            json_data.get("provincia"),
            json_data.get("pais"),
            json_data.get("numero_factura"),
            json_data.get("metodo_pago")
        ))

        conn.commit()

# Función para recorrer todas las imágenes de una carpeta y procesarlas
def procesar_imagenes_en_carpeta(carpeta, prompt, ruta_db, nombre_tabla):
    imagenes = [archivo for archivo in os.listdir(carpeta) if archivo.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Ruta a la carpeta 'tickets procesados' al mismo nivel que 'tickets'
    carpeta_base = os.path.dirname(carpeta)
    carpeta_procesados = os.path.join(carpeta_base, "Tickets procesados")
    os.makedirs(carpeta_procesados, exist_ok=True)

    for imagen in imagenes:
        ruta_imagen = os.path.join(carpeta, imagen)
        
        try:
            with open(ruta_imagen, "rb") as image_file:
                respuesta = procesamiento_prompt(prompt, image_file=image_file)


            json_extraido = procesar_respuesta_JSON(respuesta)
            
            if json_extraido:
                rellenar_tabla_desde_json(json_extraido, ruta_db, nombre_tabla)
                print(f"✅ {imagen} procesada y guardada en la base de datos.")
            else:
                print(f"⚠️ No se pudo extraer JSON de {imagen}.")

            # Mover la imagen a 'tickets procesados'
            shutil.move(ruta_imagen, os.path.join(carpeta_procesados, imagen))
        
        except Exception as e:
            print(f"❌ Error procesando {imagen}: {e}")





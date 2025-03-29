import datetime
import os
import shutil
import pymysql
from reportlab.lib.pagesizes import letter, portrait, legal
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from conexion import ConexionDB

class OperacionesDB:
    def __init__(self):
        self.conexion_db = ConexionDB()
        
    def obtener_estadisticas_animales_por_especie(self):
        """
        Retorna una lista de diccionarios con la cantidad de animales por especie.
        Ejemplo de resultado:
        [{"especie": "Bovino", "cantidad": 150}, {"especie": "Porcino", "cantidad": 80}]
        """
        query = """
            SELECT especie, COUNT(id) AS cantidad
            FROM animales
            GROUP BY especie
            ORDER BY cantidad DESC
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()
                return [{"especie": row[0], "cantidad": row[1]} for row in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener estadísticas de animales por especie: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()


    def obtener_decomisos_totales_por_especie(self):
        """
        Retorna una lista de diccionarios con la cantidad total de decomisos por especie.
        Ejemplo de resultado:
        [{"especie": "Bovino", "cantidad_decomisos": 20}, {"especie": "Porcino", "cantidad_decomisos": 5}]
        """
        query = """
            SELECT a.especie, COUNT(d.id) AS cantidad_decomisos
            FROM decomisos d
            JOIN animales a ON d.id_animal = a.id
            GROUP BY a.especie
            ORDER BY cantidad_decomisos DESC
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()
                return [{"especie": row[0], "cantidad_decomisos": row[1]} for row in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener decomisos totales por especie: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()
            
    
    def obtener_estadisticas_animales_por_especie_establecimiento(self, establecimiento_id):
        """
        Retorna una lista de diccionarios con la cantidad de animales por especie
        para el establecimiento especificado.
        Ejemplo de resultado:
        [{"especie": "Bovino", "cantidad": 25}, {"especie": "Porcino", "cantidad": 15}]
        """
        query = """
            SELECT especie, COUNT(id) AS cantidad
            FROM animales
            WHERE id_establecimiento = %s
            GROUP BY especie
            ORDER BY cantidad DESC
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (establecimiento_id,))
                resultados = cursor.fetchall()
                return [{"especie": row[0], "cantidad": row[1]} for row in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener estadísticas de animales por especie para establecimiento: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()


    def obtener_distribucion_sexo_por_especie_establecimiento(self, establecimiento_id):
        """
        Retorna una lista de diccionarios con la distribución de animales por sexo
        para cada especie en el establecimiento especificado.
        Ejemplo de resultado:
        [{"especie": "Bovino", "Macho": 10, "Hembra": 15},
        {"especie": "Porcino", "Macho": 5, "Hembra": 8}]
        """
        query = """
            SELECT especie,
                SUM(CASE WHEN sexo = 'Macho' THEN 1 ELSE 0 END) AS Macho,
                SUM(CASE WHEN sexo = 'Hembra' THEN 1 ELSE 0 END) AS Hembra
            FROM animales
            WHERE id_establecimiento = %s
            GROUP BY especie
            ORDER BY especie
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (establecimiento_id,))
                resultados = cursor.fetchall()
                return [{"especie": row[0], "Macho": row[1], "Hembra": row[2]} for row in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener distribución de sexo por especie: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_peso_promedio_por_especie_establecimiento(self, establecimiento_id):
        """
        Retorna una lista de diccionarios con el peso promedio de animales por especie
        para el establecimiento especificado.
        Ejemplo de resultado:
        [{"especie": "Bovino", "peso_promedio": 450.0}, {"especie": "Porcino", "peso_promedio": 120.0}]
        """
        query = """
            SELECT especie, AVG(peso) AS peso_promedio
            FROM animales
            WHERE id_establecimiento = %s
            GROUP BY especie
            ORDER BY peso_promedio DESC
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (establecimiento_id,))
                resultados = cursor.fetchall()
                # Convertir el peso promedio a float para mayor claridad
                return [{"especie": row[0], "peso_promedio": float(row[1])} for row in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener peso promedio por especie para establecimiento: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()


    def obtener_evolucion_ingresos_establecimiento(self, establecimiento_id):
        """
        Retorna una lista de diccionarios con la evolución temporal de ingresos para
        el establecimiento especificado, agrupando por la fecha de ingreso.
        Ejemplo de resultado:
        [{"fecha": "2024-01-01", "cantidad": 3}, {"fecha": "2024-01-02", "cantidad": 5}]
        """
        query = """
            SELECT DATE(fecha_ingreso) AS fecha, COUNT(id) AS cantidad
            FROM animales
            WHERE id_establecimiento = %s
            GROUP BY DATE(fecha_ingreso)
            ORDER BY fecha ASC
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (establecimiento_id,))
                resultados = cursor.fetchall()
                return [{"fecha": row[0].strftime("%Y-%m-%d") if hasattr(row[0], "strftime") else row[0],
                        "cantidad": row[1]} for row in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener evolución de ingresos para establecimiento: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_guias_por_establecimiento(self, establecimiento_id):
        """
        Retorna una lista de diccionarios con las guías de transporte asociadas al establecimiento.
        Se utiliza la relación a través de la tabla 'animales'.
        Ejemplo de resultado: [{"id": 1, "fecha": "2024-02-22"}, ...]
        """
        query = """
            SELECT DISTINCT gt.id, gt.fecha
            FROM guia_transporte gt
            JOIN guia_transporte_detalle gtd ON gt.id = gtd.id_guia_transporte
            JOIN ingresos_detalles idet ON gtd.id_ingreso_detalle = idet.id
            JOIN animales a ON idet.id_animales = a.id
            WHERE a.id_establecimiento = %s
            ORDER BY gt.fecha DESC
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (establecimiento_id,))
                resultados = cursor.fetchall()
                return [{"id": row[0], "fecha": row[1]} for row in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener guías por establecimiento: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()
            
    def obtener_animales_por_guia(self, guia_id):
        """
        Retorna una lista de diccionarios con la información de los animales asociados a una guía de transporte.
        Ejemplo de resultado:
        [{
            "id": 10,
            "numero_animal": 12345,
            "numero_tiquete": 67890,
            "guia_movilizacion": "XYZ",
            "especie": "Bovino",
            "peso": 450,
            "fecha_ingreso": "2024-02-22",
            "nombre_establecimiento": "Establecimiento A"
        }, ...]
        """
        query = """
            SELECT a.id, a.numero_animal, a.numero_tiquete, a.guia_movilizacion,
                a.especie, a.peso, a.fecha_ingreso, e.nombre_establecimiento
            FROM guia_transporte_detalle gtd
            JOIN ingresos_detalles idet ON gtd.id_ingreso_detalle = idet.id
            JOIN animales a ON idet.id_animales = a.id
            JOIN establecimiento e ON a.id_establecimiento = e.id
            WHERE gtd.id_guia_transporte = %s
        """
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (guia_id,))
                resultados = cursor.fetchall()
                return [
                    {
                        "id": row[0],
                        "numero_animal": row[1],
                        "numero_tiquete": row[2],
                        "guia_movilizacion": row[3],
                        "especie": row[4],
                        "peso": row[5],
                        "fecha_ingreso": row[6],
                        "nombre_establecimiento": row[7]
                    }
                    for row in resultados
                ]
        except pymysql.MySQLError as e:
            print(f"Error al obtener animales por guía: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()



    def obtener_destinos(self):
        destinos_sql = "SELECT id, marca_diferencial FROM establecimiento"
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(destinos_sql)
                resultados = cursor.fetchall()
                return [(destino[1], destino[0]) for destino in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener destinos: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_plantas(self):
        planta_sql = "SELECT nombre FROM planta"

        connection = self.conexion_db.conectar()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute(planta_sql)
                resultados = cursor.fetchall()
                return [planta[0] for planta in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener plantas: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_vehiculos(self):
        vehiculo_sql = "SELECT placa FROM vehiculo"

        connection = self.conexion_db.conectar()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute(vehiculo_sql)
                resultados = cursor.fetchall()
                return [vehiculo[0] for vehiculo in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener vehiculos: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_conductores(self):
        conductores_sql = "select nombre from conductores"

        connection = self.conexion_db.conectar()
        if not connection:
            return
        try:
            with connection.cursor() as cursor:
                cursor.execute(conductores_sql)
                resultados = cursor.fetchall()
                return [conductor[0] for conductor in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener conductores: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_animales(self, destino, fecha):
        animales_sql = """
        SELECT a.numero_animal, idet.id, a.id AS id_animales
        FROM ingresos i
        INNER JOIN ingresos_detalles idet ON i.id = idet.id_ingresos
        INNER JOIN animales a ON idet.id_animales = a.id
        WHERE a.id_establecimiento = (
            SELECT id FROM establecimiento WHERE marca_diferencial = %s
        )
        AND i.fecha = %s
        AND a.estado = 'NO_DESPACHADO'
        """

        connection = self.conexion_db.conectar()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute(animales_sql, (destino, fecha))
                resultados = cursor.fetchall()
                # Devolver una lista de tuplas con (numero_animal, id_ingreso_detalle, id_animales)
                return [(animal[0], animal[1], animal[2]) for animal in resultados]
        except pymysql.MySQLError as e:
            print(f"Error al obtener animales: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_establecimientos(self):
        establecimientos_sql = "SELECT id, marca_diferencial FROM establecimiento"

        connection = self.conexion_db.conectar()

        if not connection:
            return  []

        try:
            with connection.cursor() as cursor:
                cursor.execute(establecimientos_sql)
                resultados = cursor.fetchall()
                return  resultados
        except pymysql.MySQLError as e:
            print(f"Error al obtener los establecimientos: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def guardar_ingreso(self, id_user, id_planta, fecha, animales):
        insert_ingreso_sql = """
            INSERT INTO ingresos (id_user, id_planta, fecha, created_at, updated_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        check_ingreso_sql = """
            SELECT id FROM ingresos WHERE id_user = %s AND fecha = %s
        """
        insert_animal_sql = """
            INSERT INTO animales (numero_animal, peso, numero_tiquete, sexo, guia_movilizacion, fecha_guia_ica, fecha_ingreso, especie, id_establecimiento, numero_corral, estado, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'NO_DESPACHADO', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        insert_detalles_sql = """
            INSERT INTO ingresos_detalles (id_ingresos, id_animales, created_at, updated_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """

        connection = self.conexion_db.conectar()
        if not connection:
            print("No se pudo establecer conexión con la base de datos.")
            return False

        try:
            with connection.cursor() as cursor:
                # Verificar si ya existe un ingreso para hoy
                cursor.execute(check_ingreso_sql, (id_user, fecha))
                ingreso_resultado = cursor.fetchone()

                if ingreso_resultado:
                    id_ingreso = ingreso_resultado[0]
                    print(f"Ingreso existente encontrado con ID: {id_ingreso}")
                else:
                    # Crear un nuevo ingreso
                    cursor.execute(insert_ingreso_sql, (id_user, id_planta, fecha))
                    id_ingreso = cursor.lastrowid
                    print(f"Nuevo ingreso creado con ID: {id_ingreso}")

                # Insertar los animales y vincularlos al ingreso
                for animal in animales:
                    try:
                        # Insertar animal
                        cursor.execute(insert_animal_sql, (
                            animal["numero_animal"],
                            animal["peso"],
                            animal["numero_tiquete"],
                            animal["sexo"],
                            animal["guia_movilizacion"],
                            animal["fecha_ica"],
                            animal["fecha_ingreso"],
                            animal["especie"],
                            animal["destino"],
                            animal["numero_corral"]
                        ))
                        id_animal = cursor.lastrowid
                        print(f"Animal creado con ID: {id_animal}")

                        # Vincular animal con el ingreso
                        cursor.execute(insert_detalles_sql, (id_ingreso, id_animal))
                        print(f"Detalle creado para el ingreso {id_ingreso} con el animal {id_animal}")
                    except pymysql.MySQLError as e:
                        print(f"Error al insertar animal: {animal['numero_animal']} - {e}")
                        continue

                print(animales)

            connection.commit()
            print("Ingreso y detalles guardados correctamente.")
            return True

        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error al guardar los datos: {e}")
            return False

        finally:
            self.conexion_db.cerrar_conexion()


    def guardar_datos_backend(self, datos):
        """
        Recibe los datos desde el front-end y los guarda en la base de datos.
        """

        print("Datos Recibidos: ", datos)
        
        print(f"id del destino {datos['id_destino']}")
        
        try:
            connection = self.conexion_db.conectar()

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # Usar DictCursor para obtener resultados como diccionarios
                # Buscar o crear el registro vehiculo_conductor
                sql_vehiculo_conductor = """
                INSERT INTO vehiculo_conductor (id_vehiculo, id_conductores, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE updated_at = NOW()
                """
                cursor.execute(sql_vehiculo_conductor, (
                    datos['id_vehiculo'], datos['id_conductores']
                ))

                # Obtener el id_vehiculo_conductor generado o actualizado
                id_vehiculo_conductor = cursor.lastrowid

                # Insertar encabezado de la guía de transporte
                sql_guia = """
                INSERT INTO guia_transporte (fecha, id_planta, id_vehiculo_conductor)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql_guia, (datos['fecha'], datos['id_planta'], id_vehiculo_conductor))
                id_guia = cursor.lastrowid

                # Insertar detalles de la guía de transporte
                for detalle in datos['guia_transporte']:
                    # Insertar el detalle de la guía
                    sql_detalle = """
                    INSERT INTO guia_transporte_detalle (id_guia_transporte, id_ingreso_detalle, carne_octavos, viseras_blancas, viseras_rojas, cabezas, temperatura_promedio, dictamen)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_detalle, (
                        id_guia, detalle['id_ingreso_detalle'], detalle['carne_octavos'], detalle['viseras_blancas'],
                        detalle['viseras_rojas'], detalle['cabezas'], detalle['temperatura_promedio'], detalle['dictamen']
                    ))
                    id_detalle = cursor.lastrowid

                    # Procesar decomisos si están presentes
                    if 'decomisos' in detalle:
                        for decomiso in detalle['decomisos']:
                            # Validar que el id_animal esté en los datos
                            if 'id_animal' not in decomiso:
                                raise Exception(f"El decomiso no contiene un id_animal válido: {decomiso}")

                            # Usar el id_animal directamente de los datos
                            id_animal = decomiso['id_animal']

                            # Insertar el decomiso
                            sql_decomiso = """
                            INSERT INTO decomisos (id_animal, producto, cantidad, motivo, fecha)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(sql_decomiso, (id_animal, decomiso['producto'], decomiso['cantidad'], decomiso['motivo'], decomiso['fecha']))


            # Confirmar cambios y cerrar conexión
            connection.commit()
            self.conexion_db.cerrar_conexion()

            # Mostrar mensaje de éxito
            print("Éxito", "La guía de transporte y los decomisos se guardaron correctamente.")

            self.generar_pdf(id_guia_transporte=id_guia, id_destino=datos['id_destino'])

        except Exception as e:
            raise Exception(f"Error al guardar los datos: {str(e)}")
        
        
    def generar_pdf(self, id_guia_transporte,id_destino):
        try:
            # Conexión a la base de datos para obtener la información relacionada con la guía de transporte
            connection = self.conexion_db.conectar()
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Obtener los datos principales de la guía de transporte
                sql_guia = """
                SELECT g.fecha, p.nombre AS nombre_planta, p.telefono, p.direccion,
                    v.tipo_vehiculo, v.tipo_refrigeracion, v.placa , c.nombre AS nombre_conductor,
                    c.numero_cedula, c.telefono
                FROM guia_transporte g
                JOIN planta p ON g.id_planta = p.id
                JOIN vehiculo_conductor vc ON g.id_vehiculo_conductor = vc.id
                JOIN vehiculo v ON vc.id_vehiculo = v.id
                JOIN conductores c ON vc.id_conductores = c.id
                WHERE g.id = %s
                """
                cursor.execute(sql_guia, (id_guia_transporte,))
                guia = cursor.fetchone()

                # Obtener los detalles de la guía, incluyendo el ID del animal
                sql_detalle = """
                SELECT d.carne_octavos, d.viseras_blancas, d.viseras_rojas, d.cabezas, 
                    d.temperatura_promedio, d.dictamen, a.numero_animal, a.especie, a.guia_movilizacion
                FROM guia_transporte_detalle d
                JOIN ingresos_detalles i ON d.id_ingreso_detalle = i.id
                JOIN animales a ON i.id_animales = a.id
                WHERE d.id_guia_transporte = %s
                """
                cursor.execute(sql_detalle, (id_guia_transporte,))
                detalles = cursor.fetchall()

                # Obtener los decomisos relacionados
                sql_decomiso = """
                SELECT de.producto, de.cantidad, de.motivo, a.numero_animal
                FROM decomisos de
                JOIN animales a ON de.id_animal = a.id
                JOIN ingresos_detalles i ON a.id = i.id_animales
                JOIN guia_transporte_detalle gd ON gd.id_ingreso_detalle = i.id
                JOIN guia_transporte g ON gd.id_guia_transporte = g.id
                WHERE gd.id_guia_transporte = %s AND g.fecha = %s
                """
                cursor.execute(sql_decomiso, (id_guia_transporte, guia.get('fecha')))
                decomisos = cursor.fetchall()
                
                sql_destino = """
                SELECT es.nombre_dueno, es.nombre_establecimiento, es.direccion, 
                    es.marca_diferencial ,m.nombre_municipios, d.nombre_departamento
                FROM establecimiento es
                JOIN municipio m ON es.id_municipio = m.id
                JOIN departamento d ON m.id_departamento = d.id
                WHERE es.id = %s
                """
                cursor.execute(sql_destino, (id_destino))
                destino = cursor.fetchone()
                
            
            print(f"informacion del destino{destino}")
            
            # Cerrar la conexión a la base de datos
            self.conexion_db.cerrar_conexion()

            # Crear el PDF con tamaño oficio
            pdf_filename = f"guia_transporte_{id_guia_transporte}.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=legal)  # Cambiar a tamaño oficio
            c.setFont("Helvetica", 10)

            fecha = guia.get('fecha', 'N/A')
            fecha_obj = str(fecha.year)[-2:]
            print(f"año de dos digitos {fecha_obj}")

            # Posición inicial de los títulos
            y_position = 950  # Ajustar la posición inicial para el tamaño oficio

            codigo_invima = "N/A"
            if detalles:
                especies = set(detalle.get('especie', '').lower() for detalle in detalles)
                if len(especies) == 1:
                    especie = especies.pop()
                    if especie in ['bovino', 'bovinos','Bovino', 'Bovinos']:
                        codigo_invima = "567 B"
                    elif especie in ['porcino', 'porcinos','Porcino', 'Porcinos']:
                        codigo_invima = "150 P"

            # Definir los textos y sus colores
            texto1 = str(id_guia_transporte)  # Convertir a string
            color1 = colors.green  # Color para id_guia_transporte
            texto2 = codigo_invima  # Código INVIMA
            texto3 = fecha_obj  # Fecha (ajusta esto según tu variable real)
            color2 = colors.red  # Color para codigo_invima
            color3 = colors.red  # Color para fecha_obj (puedes cambiarlo)

            # Definir el margen más estrecho
            margen_izquierdo = 15  # Margen izquierdo
            separacion = 5  # Espacio entre los textos

            # Cambiar el tamaño de la fuente para los textos
            tamanio_fuente = 16  # Tamaño de fuente más grande
            c.setFont("Helvetica-Bold", tamanio_fuente)

            # Calcular el ancho de los textos
            ancho_texto1 = c.stringWidth(texto1, "Helvetica-Bold", tamanio_fuente)
            ancho_texto2 = c.stringWidth(texto2, "Helvetica-Bold", tamanio_fuente)
            ancho_texto3 = c.stringWidth(texto3, "Helvetica-Bold", tamanio_fuente)
            ancho_guion = c.stringWidth("-", "Helvetica-Bold", tamanio_fuente)

            # Dibujar texto1 (id_guia_transporte) en verde
            c.setFillColor(color1)
            c.drawString(margen_izquierdo, y_position, texto1)

            # Dibujar el primer guion
            c.setFillColor(colors.black)  # Color del guion
            c.drawString(margen_izquierdo + ancho_texto1 + separacion, y_position, "-")

            # Dibujar texto2 (codigo_invima) en rojo
            c.setFillColor(color2)
            c.drawString(margen_izquierdo + ancho_texto1 + separacion + ancho_guion + separacion, y_position, texto2)

            # Dibujar el segundo guion
            c.setFillColor(colors.black)  # Color del guion
            c.drawString(margen_izquierdo + ancho_texto1 + separacion + ancho_guion + separacion + ancho_texto2 + separacion, y_position, "-")

            # Dibujar texto3 (fecha_obj) en azul
            c.setFillColor(color3)
            c.drawString(margen_izquierdo + ancho_texto1 + separacion + ancho_guion + separacion + ancho_texto2 + separacion + ancho_guion + separacion, y_position, texto3)

            # --- Agregar recuadro con texto en la parte derecha ---
            # Texto que irá dentro del recuadro
            texto_recuadro = str(destino.get("marca_diferencial", "N/A"))  # Texto como cadena
            tamanio_fuente_recuadro = 12
            color_texto_recuadro = colors.black
            color_fondo_recuadro = colors.yellow

            # Ancho fijo del recuadro
            ancho_recuadro = 50  # Ancho fijo en puntos
            alto_recuadro = 50  # Altura del recuadro

            # Definir el margen derecho
            margen_derecho = 30  # Margen derecho
            ancho_pagina = legal[0]  # Ancho de la página (612 puntos para tamaño oficio)

            # Calcular la posición del recuadro
            x_recuadro = ancho_pagina - margen_derecho - ancho_recuadro  # Alinear a la derecha
            y_recuadro = 980  # Posición vertical del recuadro (ajustada para tamaño oficio)

            # Dibujar el recuadro amarillo con borde negro
            c.setFillColor(color_fondo_recuadro)
            c.setStrokeColor(colors.black)  # Color del borde
            c.setLineWidth(1)  # Grosor del borde (1px)
            c.rect(x_recuadro, y_recuadro - alto_recuadro, ancho_recuadro, alto_recuadro, fill=1, stroke=1)

            # Dibujar el texto dentro del recuadro
            c.setFillColor(color_texto_recuadro)
            c.setFont("Helvetica-Bold", tamanio_fuente_recuadro)

            # Centrar el texto horizontalmente dentro del recuadro
            ancho_linea = c.stringWidth(texto_recuadro, "Helvetica-Bold", tamanio_fuente_recuadro)
            x_texto = x_recuadro + (ancho_recuadro - ancho_linea) / 2  # Centrar horizontalmente

            # Centrar el texto verticalmente dentro del recuadro
            y_texto = y_recuadro - alto_recuadro + (alto_recuadro / 2) - (tamanio_fuente_recuadro / 2)  # Centrar verticalmente

            # Dibujar el texto centrado
            c.drawString(x_texto, y_texto, texto_recuadro)

            # Ajustar la posición vertical para el siguiente contenido
            y_position -= 15  # Espacio después del recuadro

            # TITULOS Y DATOS
            c.setFillColor(colors.red)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y_position, f"1. IDENTIFICACION DE LA PLANTA DE BENEFICIO DE PROCEDENCIA")
            y_position -= 15
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(30, y_position, f"emp.varias@caicedonia-valle.gov.co")
            y_position -= 15

            # Informacion General De La Planta
            info = [
                ["Planta", guia.get('nombre_planta','N/A')],
                ["Departamento", destino.get('nombre_departamento', 'N/A')],
                ["Municipio o Ciudad", destino.get('nombre_municipios', 'N/A')],
                ["Codigo INVIMA", codigo_invima],
                ["Direccion", guia.get('direccion', 'N/A')],
                ["Sacrificio y Despacho", guia.get('fecha', 'N/A')],
            ]

            table_info = Table(info)
            table_info.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            # Calcula el tamaño de la tabla y dibújala en la posición correcta
            table_width, table_height = table_info.wrapOn(c, 500, y_position)
            table_info.drawOn(c, 30, y_position - table_height)

            # Actualiza la posición para la tabla de decomisos
            y_position -= (table_height + 20)

            # Informacion Del Destino
            info_destino = [
                ["Nombre Dueño", destino.get('nombre_dueno', 'N/A')],
                ["Nombre Establecimiento", destino.get('nombre_establecimiento', 'N/A')],
                ["Direccion", destino.get('direccion', 'N/A')],
            ]

            c.setFillColor(colors.red)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y_position, f"2.DESTINO")
            y_position -= 15

            table_destino = Table(info_destino)
            table_destino.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            # Calcula el tamaño de la tabla y dibújala en la posición correcta
            table_width, table_height = table_destino.wrapOn(c, 500, y_position)
            table_destino.drawOn(c, 30, y_position - table_height)

            # Actualiza la posición para la tabla de Destino
            y_position -= (table_height + 20)

            # Detalles de la guía
            data_detalles = [["ID Animal", "Especie", "Carne en Octavos", "Viseras Blancas", "Viseras Rojas", "Cabezas", "Temperatura Promedio", "Dictamen"]]
            for detalle in detalles:
                row = [
                    detalle.get('numero_animal', 'N/A'),
                    detalle.get('especie', 'N/A'),
                    detalle.get('carne_octavos', 'N/A'),
                    detalle.get('viseras_blancas', 'N/A'),
                    detalle.get('viseras_rojas', 'N/A'),
                    detalle.get('cabezas', 'N/A'),
                    detalle.get('temperatura_promedio', 'N/A'),
                    detalle.get('dictamen', 'N/A')
                ]
                data_detalles.append(row)

            c.setFillColor(colors.red)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y_position, f"3. DESCRIPCION DEL PRODUCTO")
            y_position -= 15

            table_detalles = Table(data_detalles)
            table_detalles.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            # Calcula el tamaño de la tabla y dibújala en la posición correcta
            table_width, table_height = table_detalles.wrapOn(c, 500, y_position)
            table_detalles.drawOn(c, 30, y_position - table_height)

            # Actualiza la posición para la tabla de decomisos
            y_position -= (table_height + 20)
            
            c.setFillColor(colors.red)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y_position, f"4. VEHICULO TRANSPORTADOR")
            y_position -= 15
            
            transporte = [
                ["Tipo Vehiculo ", guia.get('tipo_vehiculo','N/A')],
                ["Placa", guia.get('placa', 'N/A')],
                ["Nombre del Coductor", guia.get('nombre_conductor', 'N/A')],
                ["N° Cedula", guia.get('numero_cedula', 'N/A')],
                ["Tipo Refrigeracion", guia.get('tipo_refrigeracion', 'N/A')],

            ]
            
            table_transporte = Table(transporte)
            table_transporte.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            # Calcula el tamaño de la tabla y dibújala en la posición correcta
            table_width, table_height = table_transporte.wrapOn(c, 500, y_position)
            table_transporte.drawOn(c, 30, y_position - table_height)
            
            # Actualiza la posición para la tabla de decomisos
            y_position -= (table_height + 20)
            
            c.setFillColor(colors.red)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y_position, f"5. DECOMISOS")
            y_position -= 15
            
            margen_inferior = 50
            
            # Datos de decomisos
            headers = ["Producto", "ID Animal", "Cantidad", "Motivo"]  # Encabezados
            data_decomisos = [headers]  # Incluir los encabezados en la lista de datos
            for decomiso in decomisos:
                row = [
                    decomiso.get('producto', 'N/A'),
                    decomiso.get('numero_animal', 'N/A'),
                    decomiso.get('cantidad', 'N/A'),
                    decomiso.get('motivo', 'N/A'),
                ]
                data_decomisos.append(row)

            # Calcular el alto de una fila de la tabla de decomisos
            alto_fila = 12  # Ajusta este valor según el tamaño de la fuente y el padding de la tabla
            # Definir el ancho fijo de las columnas
            ancho_columnas = [50, 50, 50, 50]  # Ancho fijo de 100 puntos para cada columna

            # Dibujar la tabla de decomisos fila por fila
            for i, fila in enumerate(data_decomisos):
                # Crear una tabla con una sola fila y ancho fijo
                tabla_fila = Table([fila], colWidths=ancho_columnas)
                tabla_fila.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey if i == 0 else colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke if i == 0 else colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))

                # Calcular el alto de la fila
                _, alto_fila_actual = tabla_fila.wrapOn(c, 500, y_position)

                # Verificar si la fila cabe en la página actual
                if y_position - alto_fila_actual < margen_inferior:
                    c.showPage()  # Crear una nueva página
                    y_position = 950  # Reiniciar la posición vertical en la nueva página

                # Dibujar la fila
                tabla_fila.drawOn(c, 30, y_position - alto_fila_actual)
                y_position -= alto_fila_actual

            # Guardar el PDF
            c.save()

            # Ruta de la carpeta de destino
            directorio_destino = "reportes_pdf/"

            # Crear la carpeta si no existe
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)

            destino_final = os.path.join(directorio_destino, pdf_filename)
            shutil.move(pdf_filename, destino_final)

            print(f"PDF generado correctamente: {pdf_filename}")

        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")


    def buscar_animal(self, numero):
        """
        Busca coincidencias en la tabla animales con base en el número proporcionado.
        """
        consulta_sql = """
        SELECT id, numero_animal, numero_tiquete, guia_movilizacion, especie, peso, fecha_guia_ica, fecha_ingreso
        FROM animales
        WHERE id LIKE %s OR numero_animal LIKE %s OR numero_tiquete LIKE %s OR guia_movilizacion LIKE %s
        """
        connection = self.conexion_db.conectar()
        if not connection:
            print("No se pudo establecer conexión con la base de datos.")
            return []

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Busca coincidencias parciales usando LIKE
                parametro_busqueda = f"%{numero}%"  # Permite buscar coincidencias parciales
                cursor.execute(consulta_sql, (parametro_busqueda, parametro_busqueda, parametro_busqueda, parametro_busqueda))
                resultados = cursor.fetchall()
                return resultados  # Devuelve una lista de diccionarios con las coincidencias
        except pymysql.MySQLError as e:
            print(f"Error al buscar animal: {e}")
            return []
        finally:
            self.conexion_db.cerrar_conexion()

    def obtener_ingreso_por_fecha(self, fecha):
        """
        Obtiene la información de un ingreso existente en la base de datos para la fecha especificada.
        """
        consulta_ingreso = """
        SELECT i.id, i.id_user, i.id_planta, i.fecha, idet.id AS id_ingreso_detalle, 
                a.numero_animal, a.peso, a.numero_tiquete, a.sexo, a.guia_movilizacion,
                a.fecha_guia_ica, a.fecha_ingreso, a.especie, a.numero_corral, e.nombre_establecimiento
        FROM ingresos i
        INNER JOIN ingresos_detalles idet ON i.id = idet.id_ingresos
        INNER JOIN animales a ON idet.id_animales = a.id
        INNER JOIN establecimiento e ON a.id_establecimiento = e.id
        WHERE i.fecha = %s
        """

        connection = self.conexion_db.conectar()
        if not connection:
            print("No se pudo establecer conexión con la base de datos.")
            return None

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Ejecutar la consulta para obtener la información del ingreso
                cursor.execute(consulta_ingreso, (fecha,))
                resultados = cursor.fetchall()

                if not resultados:
                    print("No se encontró ningún ingreso para la fecha proporcionada.")
                    return None

                # Organizar la información para facilitar su uso
                ingreso_data = {
                    "id_ingreso": resultados[0]["id"],
                    "id_user": resultados[0]["id_user"],
                    "id_planta": resultados[0]["id_planta"],
                    "fecha": resultados[0]["fecha"],
                    "detalles": []
                }

                for resultado in resultados:
                    detalle = {
                        "id_ingreso_detalle": resultado["id_ingreso_detalle"],
                        "numero_animal": resultado["numero_animal"],
                        "peso": resultado["peso"],
                        "numero_tiquete": resultado["numero_tiquete"],
                        "sexo": resultado["sexo"],
                        "guia_movilizacion": resultado["guia_movilizacion"],
                        "fecha_guia_ica" : resultado["fecha_guia_ica"],
                        "fecha_ingreso" : resultado["fecha_ingreso"],
                        "especie": resultado["especie"],
                        "numero_corral" : resultado["numero_corral"],
                        "nombre_establecimiento" : resultado["nombre_establecimiento"]
                    }
                    ingreso_data["detalles"].append(detalle)

                return ingreso_data

        except pymysql.MySQLError as e:
            print(f"Error al obtener ingreso por fecha: {e}")
            return None
        finally:
            self.conexion_db.cerrar_conexion()

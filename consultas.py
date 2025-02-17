import pymysql
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from conexion import ConexionDB

class OperacionesDB:
    def __init__(self):
        self.conexion_db = ConexionDB()


    def obtener_destinos(self):
        destinos_sql = "SELECT nombre_establecimiento FROM establecimiento"
        connection = self.conexion_db.conectar()
        if not connection:
            return []
        try:
            with connection.cursor() as cursor:
                cursor.execute(destinos_sql)
                resultados = cursor.fetchall()
                return [destino[0] for destino in resultados]
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
            SELECT id FROM establecimiento WHERE nombre_establecimiento = %s
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
        establecimientos_sql = "SELECT id, nombre_establecimiento FROM establecimiento"

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
                            INSERT INTO decomisos (id_animal, producto, cantidad, motivo)
                            VALUES (%s, %s, %s, %s)
                            """
                            cursor.execute(sql_decomiso, (id_animal, decomiso['producto'], decomiso['cantidad'], decomiso['motivo']))


            # Confirmar cambios y cerrar conexión
            connection.commit()
            self.conexion_db.cerrar_conexion()

            # Mostrar mensaje de éxito
            print("Éxito", "La guía de transporte y los decomisos se guardaron correctamente.")

            self.generar_pdf(id_guia_transporte=id_guia)

        except Exception as e:
            raise Exception(f"Error al guardar los datos: {str(e)}")


    def generar_pdf(self, id_guia_transporte):
        try:
            # Conexión a la base de datos para obtener la información relacionada con la guía de transporte
            connection = self.conexion_db.conectar()
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Obtener los datos principales de la guía de transporte
                sql_guia = """
                SELECT g.fecha, p.nombre AS nombre_planta, p.telefono, v.tipo_vehiculo, c.nombre AS nombre_conductor
                FROM guia_transporte g
                JOIN planta p ON g.id_planta = p.id
                JOIN vehiculo_conductor vc ON g.id_vehiculo_conductor = vc.id
                JOIN vehiculo v ON vc.id_vehiculo = v.id
                JOIN conductores c ON vc.id_conductores = c.id
                WHERE g.id = %s
                """
                cursor.execute(sql_guia, (id_guia_transporte,))
                guia = cursor.fetchone()

                # Obtener los detalles de la guía
                sql_detalle = """
                SELECT d.carne_octavos, d.viseras_blancas, d.viseras_rojas, d.cabezas, d.temperatura_promedio, d.dictamen
                FROM guia_transporte_detalle d
                WHERE d.id_guia_transporte = %s
                """
                cursor.execute(sql_detalle, (id_guia_transporte,))
                detalles = cursor.fetchall()

                # Obtener los decomisos relacionados
                sql_decomiso = """
                SELECT de.producto, de.cantidad, de.motivo, a.numero_animal
                FROM decomisos de
                JOIN animales a ON de.id_animal = a.id
                WHERE de.id_animal IN (SELECT id_animal FROM guia_transporte_detalle WHERE id_guia_transporte = %s)
                """
                cursor.execute(sql_decomiso, (id_guia_transporte,))
                decomisos = cursor.fetchall()

            # Cerrar la conexión a la base de datos
            self.conexion_db.cerrar_conexion()

            # Crear el PDF
            pdf_filename = f"guia_transporte_{id_guia_transporte}.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setFont("Helvetica", 10)

            # Títulos y contenido
            c.drawString(30, 750, f"Guía de Transporte: {id_guia_transporte}")
            c.drawString(30, 735, f"Fecha: {guia['fecha']}")
            c.drawString(30, 720, f"Planta: {guia['nombre_planta']}")
            c.drawString(30, 705, f"Teléfono: {guia['telefono']}")
            c.drawString(30, 690, f"Vehículo: {guia['tipo_vehiculo']}")
            c.drawString(30, 675, f"Conductor: {guia['nombre_conductor']}")

            y_position = 650
            c.drawString(30, y_position, "Detalles de la Guía de Transporte:")
            y_position -= 15
            for detalle in detalles:
                c.drawString(30, y_position, f"Carne en octavos: {detalle['carne_octavos']}, Visceras Blancas: {detalle['viseras_blancas']}, Cabezas: {detalle['cabezas']}")
                y_position -= 15

            if decomisos:
                c.drawString(30, y_position, "Decomisos:")
                y_position -= 15
                for decomiso in decomisos:
                    c.drawString(30, y_position, f"Producto: {decomiso['producto']}, Animal: {decomiso['numero_animal']}, Cantidad: {decomiso['cantidad']}, Motivo: {decomiso['motivo']}")
                    y_position -= 15

            c.save()

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
        WHERE numero_animal LIKE %s OR numero_tiquete LIKE %s OR guia_movilizacion LIKE %s
        """
        connection = self.conexion_db.conectar()
        if not connection:
            print("No se pudo establecer conexión con la base de datos.")
            return []

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Busca coincidencias parciales usando LIKE
                parametro_busqueda = f"%{numero}%"  # Permite buscar coincidencias parciales
                cursor.execute(consulta_sql, (parametro_busqueda, parametro_busqueda, parametro_busqueda))
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

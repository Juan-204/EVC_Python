import pymysql

class ConexionDB:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = ""
        self.database = "proyectoevc"
        self.connection = None

    def conectar(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión exitosa a la base de datos.")
            return self.connection
        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def cerrar_conexion(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada correctamente.")

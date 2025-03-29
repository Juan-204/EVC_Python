import os
import subprocess
import pymysql
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QProgressBar

class InstallGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Instalación del Sistema")
        self.setGeometry(200, 200, 500, 400)
        
        self.layout = QVBoxLayout()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.progress = QProgressBar()
        self.start_button = QPushButton("Iniciar Instalación")
        self.start_button.clicked.connect(self.start_installation)
        
        self.layout.addWidget(self.log)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)
    
    def log_message(self, message):
        self.log.append(message)
        QApplication.processEvents()
    
    def start_installation(self):
        self.start_button.setEnabled(False)
        steps = 5
        self.progress.setMaximum(steps)

        self.log_message("Clonando el repositorio desde GitHub...")
        self.clonar_repositorio()
        self.progress.setValue(1)

        self.log_message("Iniciando XAMPP...")
        self.iniciar_xampp()
        self.progress.setValue(2)
        
        self.log_message("Instalando dependencias...")
        self.instalar_dependencias()
        self.progress.setValue(3)
        
        self.log_message("Configurando base de datos...")
        self.configurar_base_datos()
        self.progress.setValue(4)
        
        self.log_message("Ejecutando aplicación...")
        self.ejecutar_aplicacion()
        self.progress.setValue(5)
        
        self.log_message("Instalación completa.")
    
    def clonar_repositorio(self):
        if not os.path.exists("EVC_Python"):
            try:
                subprocess.run(["git", "clone", "https://github.com/Juan-204/EVC_Python.git"])
                self.log_message("Repositorio clonado correctamente.\n")
                os.chdir("EVC_Python")  # Cambiar al directorio del proyecto
            except Exception as e:
                self.log_message(f"Error al clonar el repositorio: {e}\n")
        else:
            self.log_message("El repositorio ya existe, omitiendo clonación.\n")
            os.chdir("EVC_Python")  # Cambiar al directorio del proyecto si ya está clonado
    
    def iniciar_xampp(self):
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["C:\\xampp\\xampp_start.exe"], shell=True)
            else:  # Linux
                subprocess.run(["sudo", "/opt/lampp/lampp", "start"])
            time.sleep(5)
            self.log_message("XAMPP iniciado correctamente.\n")
        except Exception as e:
            self.log_message(f"Error al iniciar XAMPP: {e}\n")
    
    def instalar_dependencias(self):
        paquetes = ["PyQt5", "pymysql", "reportlab", "matplotlib"]
        for paquete in paquetes:
            subprocess.run(["pip", "install", paquete])
        self.log_message("Dependencias instaladas correctamente.\n")
    
    def configurar_base_datos(self):
        try:
            conexion = pymysql.connect(host="localhost", user="root", password="")
            cursor = conexion.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS proyectoevc;")
            conexion.close()
            self.log_message("Base de datos configurada exitosamente.\n")
        except Exception as e:
            self.log_message(f"Error al configurar la base de datos: {e}\n")
    
    def ejecutar_aplicacion(self):
        try:
            subprocess.run(["python", "main.py"])
        except Exception as e:
            self.log_message(f"Error al ejecutar la aplicación: {e}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = InstallGUI()
    gui.show()
    sys.exit(app.exec_())

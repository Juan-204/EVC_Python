import sys
import os
import subprocess
import psutil  
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QHBoxLayout

from entradaproducto import AnimalForm
from estadisticas import Estadisticas
from guiatransporte import GuiaTransporteApp
from tabs_buscador import ConsultaWidget

def iniciar_xampp():
    """Verifica si XAMPP ya está corriendo, si no, lo inicia."""
    if os.name == "nt":  # Windows
        apache_running = any("httpd.exe" in p.name() for p in psutil.process_iter())
        mysql_running = any("mysqld.exe" in p.name() for p in psutil.process_iter())
        
        if not apache_running or not mysql_running:
            try:
                subprocess.run(["C:\\xampp\\xampp_start.exe"], shell=True)
            except Exception as e:
                print(f"Error al iniciar XAMPP: {e}")
        else:
            print("XAMPP ya está en ejecución.")
    else:  # Linux
        try:
            subprocess.run(["sudo", "/opt/lampp/lampp", "start"])
        except Exception as e:
            print(f"Error al iniciar XAMPP: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PBA")
        self.setGeometry(100, 100, 800, 600)

        # Iniciar XAMPP antes de cargar la aplicación
        iniciar_xampp()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(2,2,2,2)

        btn_animal_form = QPushButton("Agregar Animal")
        btn_animal_form.clicked.connect(lambda: self.cambiar_pantalla(0))

        btn_guia_form = QPushButton("Guia de Transporte")
        btn_guia_form.clicked.connect(lambda: self.cambiar_pantalla(1))

        btn_pantalla3 = QPushButton("Consulta")
        btn_pantalla3.clicked.connect(lambda: self.cambiar_pantalla(2))
        
        btn_pantalla4 = QPushButton("Estadisticas")
        btn_pantalla4.clicked.connect(lambda: self.cambiar_pantalla(3))

        sidebar_layout.addWidget(btn_animal_form)
        sidebar_layout.addWidget(btn_guia_form)
        sidebar_layout.addWidget(btn_pantalla3)
        sidebar_layout.addWidget(btn_pantalla4)
        sidebar_layout.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;
                color: white;
                border: 2px solid #1B4F72;
                margin: 0px;
            }
            QPushButton {
                background-color: #5DADE2;
                color: white;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
            QPushButton:pressed {
                background-color: #2874A6;
            }
        """)
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(150)
        main_layout.addWidget(sidebar_widget, 1)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(AnimalForm())
        self.stacked_widget.addWidget(GuiaTransporteApp())
        self.stacked_widget.addWidget(ConsultaWidget())
        self.stacked_widget.addWidget(Estadisticas())
        main_layout.addWidget(self.stacked_widget, 4)

    def cambiar_pantalla(self, index):
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
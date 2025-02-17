import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QHBoxLayout

from buscador import Buscador
from entradaproducto import AnimalForm  # Importar la clase desde entradaproducto.py
from guiatransporte import GuiaTransporteApp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PBA")
        self.setGeometry(100, 100, 800, 600)

        # Crear el widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout principal
        main_layout = QHBoxLayout(main_widget)

        # Barra lateral
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(2,2,2,2)

        btn_animal_form = QPushButton("Agregar Animal")
        btn_animal_form.clicked.connect(lambda: self.cambiar_pantalla(0))

        btn_guia_form = QPushButton("Guia de Transporte")
        btn_guia_form.clicked.connect(lambda: self.cambiar_pantalla(1))


        btn_pantalla3 = QPushButton("Consulta")
        btn_pantalla3.clicked.connect(lambda: self.cambiar_pantalla(2))

        sidebar_layout.addWidget(btn_animal_form)
        sidebar_layout.addWidget(btn_guia_form)
        sidebar_layout.addWidget(btn_pantalla3)
        sidebar_layout.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #2E86C1;  /* Color de fondo del sidebar */
                color: white;               /* Color del texto en el sidebar */
                border: 2px solid #1B4F72;  /* Opcional: Borde derecho */
                margin: 0px;
            }
            QPushButton {
                background-color: #5DADE2;  /* Color de fondo de los botones */
                color: white;               /* Color del texto en los botones */
                border: none;               /* Sin bordes */
                padding: 10px;              /* Espaciado interno */
            }
            QPushButton:hover {
                background-color: #3498DB;  /* Color de los botones al pasar el mouse */
            }
            QPushButton:pressed {
                background-color: #2874A6;  /* Color de los botones al hacer clic */
            }
        """)
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(150)
        main_layout.addWidget(sidebar_widget, 1)

        # Contenedor de pantallas
        self.stacked_widget = QStackedWidget()

        # Agregar pantallas al QStackedWidget
        self.stacked_widget.addWidget(AnimalForm())
        self.stacked_widget.addWidget(GuiaTransporteApp())  # Pantalla 2: AnimalForm
        self.stacked_widget.addWidget(Buscador())
        main_layout.addWidget(self.stacked_widget, 3)

    def crear_pantalla(self, titulo):
        pantalla = QWidget()
        layout = QVBoxLayout(pantalla)
        label = QPushButton(titulo)
        layout.addWidget(label)
        return pantalla

    def cambiar_pantalla(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

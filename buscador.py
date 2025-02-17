from PyQt5.QtWidgets import QPushButton, QTableWidget, QGridLayout, QHeaderView, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt

from consultas import OperacionesDB

class Buscador(QWidget):
    def __init__(self):
        super().__init__()
        self.db = OperacionesDB()

        #Configuracion de la Ventana
        self.setWindowTitle("Buscador")
        self.setGeometry(100, 100, 1100, 500)

        layout = QGridLayout()

        self.search_label = QLabel("Ingrese un Numero para Buscar:")
        self.search_label.setStyleSheet("padding: 10px ;font-size: 24px; font-weight: bold; color: #3f51b5;")
        self.search_input = QLineEdit()
        self.search_input.setFixedSize(600, 40)
        self.search_input.setPlaceholderText("Numero de animal, tiquete o guia...")

        self.search_button = QPushButton("Buscar")
        self.search_button.setFixedSize(150,40)
        self.search_button.clicked.connect(self.buscar_animal)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(8)
        self.results_table.setStyleSheet("font-size: 18px")
        self.results_table.setHorizontalHeaderLabels(["ID","# ANIMAL","# TIQUETE","GUIA MOVILIZACION","ESPECIE","PESO","FECHA GUIA ICA","FECHA INGRESO"])
        self.results_table.resizeColumnsToContents()
        self.results_table.resizeRowsToContents()
        self.results_table.setSortingEnabled(True)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setWordWrap(True)

        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.search_label, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.search_input, 2, 1, Qt.AlignCenter)
        layout.addWidget(self.search_button, 2, 1, Qt.AlignRight)
        layout.addWidget(self.results_table, 4, 1)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 20px;
            }
        """)

    def buscar_animal(self):
        numero = self.search_input.text()
        print(type(numero))
        if not numero:
            QMessageBox.warning(self, "Advertencia", "Por Favor, Ingrese un Numero para Buscar.")
            return

        resultados = self.db.buscar_animal(numero)
        if resultados:
            self.mostrar_resultados(resultados)
        else:
            self.results_table.setRowCount(0)
            QMessageBox.information(self, "Sin Resultados", "No se encontraron coincidencias")

    def mostrar_resultados(self, resultados):
        self.results_table.setRowCount(len(resultados))  # Configura el número de filas

        for fila, resultado in enumerate(resultados):
            self.results_table.setItem(fila, 0, QTableWidgetItem(str(resultado.get('id', ''))))
            self.results_table.setItem(fila, 1, QTableWidgetItem(str(resultado.get('numero_animal', ''))))
            self.results_table.setItem(fila, 2, QTableWidgetItem(str(resultado.get('numero_tiquete', ''))))
            self.results_table.setItem(fila, 3, QTableWidgetItem(str(resultado.get('guia_movilizacion', ''))))
            self.results_table.setItem(fila, 4, QTableWidgetItem(str(resultado.get('especie', ''))))
            self.results_table.setItem(fila, 5, QTableWidgetItem(str(resultado.get('peso', ''))))
            self.results_table.setItem(fila, 6, QTableWidgetItem(str(resultado.get('fecha_guia_ica', ''))))
            self.results_table.setItem(fila, 7, QTableWidgetItem(str(resultado.get('fecha_ingreso', ''))))


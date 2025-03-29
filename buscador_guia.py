from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from consultas import OperacionesDB

class GuiasTransporteBuscador(QWidget):
    def __init__(self):
        super().__init__()
        self.db = OperacionesDB()
        self.setWindowTitle("Guías de Transporte y Animales Asociados")
        self.setGeometry(100, 100, 1100, 600)
        
        layout = QVBoxLayout()

        # Sección para seleccionar el establecimiento
        est_layout = QHBoxLayout()
        lbl_est = QLabel("Establecimiento:")
        self.combo_establecimientos = QComboBox()
        self.combo_establecimientos.setFixedWidth(300)
        self.combo_establecimientos.currentIndexChanged.connect(self.cargar_guias)
        est_layout.addWidget(lbl_est)
        est_layout.addWidget(self.combo_establecimientos)
        est_layout.addStretch()
        layout.addLayout(est_layout)
        
        # Tabla para mostrar las guías de transporte
        self.table_guias = QTableWidget()
        self.table_guias.setColumnCount(2)
        self.table_guias.setHorizontalHeaderLabels(["ID", "Fecha"])
        self.table_guias.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_guias.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_guias.cellClicked.connect(self.cargar_animales)
        layout.addWidget(QLabel("Guías de Transporte:"))
        layout.addWidget(self.table_guias)
        
        # Tabla para mostrar los animales asociados a la guía seleccionada
        # Ahora se muestran 8 columnas con los campos adicionales.
        self.table_animales = QTableWidget()
        self.table_animales.setColumnCount(8)
        self.table_animales.setHorizontalHeaderLabels([
            "ID", "# Animal", "# Tiquete", "Guía Movilización",
            "Especie", "Peso", "Fecha Ingreso", "Establecimiento"
        ])
        self.table_animales.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_animales.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(QLabel("Animales Asociados a la Guía:"))
        layout.addWidget(self.table_animales)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 18px;
            }
        """)
        
        # Cargar los establecimientos al iniciar el widget
        self.cargar_establecimientos()
    
    def cargar_establecimientos(self):
        """
        Se espera que 'obtener_establecimientos()' retorne una lista de tuplas:
        [(id, nombre), (id, nombre), ...]
        """
        establecimientos = self.db.obtener_establecimientos()
        self.combo_establecimientos.clear()
        if not establecimientos:
            QMessageBox.warning(self, "Advertencia", "No hay establecimientos registrados.")
            return
        for est in establecimientos:
            # Se asume que cada tupla es (id, nombre)
            self.combo_establecimientos.addItem(est[1], est[0])
        # Cargar las guías del primer establecimiento por defecto
        self.cargar_guias()
    
    def cargar_guias(self):
        """
        Carga las guías de transporte asociadas al establecimiento seleccionado y
        las muestra en la tabla de guías.
        """
        establecimiento_id = self.combo_establecimientos.currentData()
        if not establecimiento_id:
            self.table_guias.setRowCount(0)
            return
        
        guias = self.db.obtener_guias_por_establecimiento(establecimiento_id)
        if not guias:
            self.table_guias.setRowCount(0)
            QMessageBox.information(self, "Sin Resultados", "No se encontraron guías para este establecimiento.")
            return
        
        self.table_guias.setRowCount(len(guias))
        for fila, guia in enumerate(guias):
            self.table_guias.setItem(fila, 0, QTableWidgetItem(str(guia.get('id', ''))))
            self.table_guias.setItem(fila, 1, QTableWidgetItem(str(guia.get('fecha', ''))))
        # Al actualizar las guías, se limpia la tabla de animales
        self.table_animales.setRowCount(0)
    
    def cargar_animales(self, row, column):
        """
        Al seleccionar una guía en la tabla, carga y muestra los animales asociados.
        """
        guia_id_item = self.table_guias.item(row, 0)
        if not guia_id_item:
            return
        guia_id = guia_id_item.text()
        animales = self.db.obtener_animales_por_guia(guia_id)
        if not animales:
            self.table_animales.setRowCount(0)
            QMessageBox.information(self, "Sin Resultados", "No se encontraron animales asociados a esta guía.")
            return
        
        self.table_animales.setRowCount(len(animales))
        for fila, animal in enumerate(animales):
            self.table_animales.setItem(fila, 0, QTableWidgetItem(str(animal.get("id", ""))))
            self.table_animales.setItem(fila, 1, QTableWidgetItem(str(animal.get("numero_animal", ""))))
            self.table_animales.setItem(fila, 2, QTableWidgetItem(str(animal.get("numero_tiquete", ""))))
            self.table_animales.setItem(fila, 3, QTableWidgetItem(str(animal.get("guia_movilizacion", ""))))
            self.table_animales.setItem(fila, 4, QTableWidgetItem(animal.get("especie", "")))
            self.table_animales.setItem(fila, 5, QTableWidgetItem(str(animal.get("peso", ""))))
            self.table_animales.setItem(fila, 6, QTableWidgetItem(str(animal.get("fecha_ingreso", ""))))
            self.table_animales.setItem(fila, 7, QTableWidgetItem(animal.get("nombre_establecimiento", "")))

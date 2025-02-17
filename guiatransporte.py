from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QDateEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QDialog, QHeaderView, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtCore import  QDate, Qt


from consultas import OperacionesDB  # Asegúrate de importar la clase de operaciones DB

class GuiaTransporteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Transporte y Decomisos")
        self.resize(1000, 700)

        self.db_ops = OperacionesDB()  # Instanciamos la clase para usar sus métodos
        self.setup_ui()

        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 20px;
            }
            QLabel, QLineEdit, QComboBox, QSpinBox, QDateEdit, QPushButton {
                font-size: 16px;
                padding: 10px;  # Aumenta el padding (espacio interno) de los widgets
            }
            QLineEdit, QComboBox, QSpinBox, QDateEdit {
                height: 40px;  # Aumenta la altura de los campos de entrada
            }
            QPushButton {
                height: 40px;  # Aumenta la altura del botón
            }
        """)

    def setup_ui(self):
        layout = QVBoxLayout()

        # Grid Layout para los formularios
        self.grid_layout = QGridLayout()

        title_label = QLabel('Agregar Animal')
        title_label.setStyleSheet("padding: 10px ;font-size: 24px; font-weight: bold; color: #3f51b5;")
        self.grid_layout.addWidget(title_label, 0, 3)  # Título en la primera fila, ocupa 2 columnas

        # Campos del formulario principal
        self.grid_layout.addWidget(QLabel("Fecha:"), 1, 0)
        self.fecha_input = QDateEdit()
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setCalendarPopup(True)
        self.grid_layout.addWidget(self.fecha_input, 1, 1)

        self.grid_layout.addWidget(QLabel("Destino:"), 1, 2)
        self.destino_combo = QComboBox()
        self.destino_combo.addItem("Seleccione el Destino", -1)
        self.grid_layout.addWidget(self.destino_combo, 1, 3)

        self.grid_layout.addWidget(QLabel("Planta:"), 1, 4)
        self.planta_combo = QComboBox()
        self.grid_layout.addWidget(self.planta_combo, 1, 5)

        self.grid_layout.addWidget(QLabel("Vehículo:"), 2, 0)
        self.vehiculo_combo = QComboBox()
        self.grid_layout.addWidget(self.vehiculo_combo, 2, 1)

        self.grid_layout.addWidget(QLabel("Conductor:"), 2, 2)
        self.conductor_combo = QComboBox()
        self.grid_layout.addWidget(self.conductor_combo, 2, 3)

        title_label = QLabel('Descripcion del Producto')
        title_label.setStyleSheet("padding: 10px ;font-size: 24px; font-weight: bold; color: #3f51b5;")
        self.grid_layout.addWidget(title_label, 3, 3, 1, 2)

        self.grid_layout.addWidget(QLabel("Animal Disponible:"), 4, 0)
        self.animal_combo = QComboBox()
        self.animal_combo.addItem("Seleccione")
        self.animal_combo.currentIndexChanged.connect(self.print_selected_animal)
        self.grid_layout.addWidget(self.animal_combo, 4, 1)

        # Campos de datos manuales
        self.grid_layout.addWidget(QLabel("Carne en Octavos:"), 5, 0)
        self.carne_input = QSpinBox()
        self.grid_layout.addWidget(self.carne_input, 5, 1)

        self.grid_layout.addWidget(QLabel("Viseras Blancas:"), 5, 2)
        self.viseras_blancas_input = QSpinBox()
        self.grid_layout.addWidget(self.viseras_blancas_input, 5, 3)

        self.grid_layout.addWidget(QLabel("Viseras Rojas:"), 5, 4)
        self.viseras_rojas_input = QSpinBox()
        self.grid_layout.addWidget(self.viseras_rojas_input, 5, 5)

        self.grid_layout.addWidget(QLabel("Cabezas:"), 6, 0)
        self.cabezas_input = QSpinBox()
        self.grid_layout.addWidget(self.cabezas_input, 6, 1)

        self.grid_layout.addWidget(QLabel("Temperatura Promedio:"), 6, 2)
        self.temperatura_input = QLineEdit()
        self.grid_layout.addWidget(self.temperatura_input, 6, 3)

        self.grid_layout.addWidget(QLabel("Dictamen:"), 6, 4)
        self.dictamen_combo = QComboBox()
        self.dictamen_combo.addItems(["A", "AC"])
        #self.dictamen_combo.currentTextChanged.connect(self.toggle_decomiso_form)
        self.grid_layout.addWidget(self.dictamen_combo, 6, 5)

        # Botón para agregar los datos manuales a la tabla
        self.add_data_button = QPushButton("Agregar Datos")
        self.add_data_button.clicked.connect(self.add_manual_data_to_table)
        self.grid_layout.addWidget(self.add_data_button, 7, 3, 1, 1)

        self.limpiar_button = QPushButton("Limpiar")
        self.limpiar_button.clicked.connect(self.limpiar)
        self.grid_layout.addWidget(self.limpiar_button, 7, 6, Qt.AlignLeft)

        layout.addLayout(self.grid_layout)


        # Formulario de decomisos
        self.decomiso_form = QDialog()
        self.decomiso_form.setWindowTitle("Formulario de Decomisos")
        self.decomiso_layout = QGridLayout()

        self.decomiso_layout.addWidget(QLabel("Producto:"), 0, 0)
        self.producto_input = QLineEdit()
        self.decomiso_layout.addWidget(self.producto_input, 0, 1)

        self.decomiso_layout.addWidget(QLabel("# Animal:"), 1, 0)
        self.animal_decomiso_input = QLineEdit()
        self.animal_decomiso_input.setReadOnly(True)
        self.decomiso_layout.addWidget(self.animal_decomiso_input, 1, 1)

        self.decomiso_layout.addWidget(QLabel("Cantidad:"), 2, 0)
        self.cantidad_input = QSpinBox()
        self.decomiso_layout.addWidget(self.cantidad_input, 2, 1)

        self.decomiso_layout.addWidget(QLabel("Motivo:"), 3, 0)
        self.motivo_input = QLineEdit()
        self.decomiso_layout.addWidget(self.motivo_input, 3, 1)

        self.add_decomiso_button = QPushButton("Agregar Decomiso")
        self.add_decomiso_button.clicked.connect(self.add_decomiso_to_table)
        self.decomiso_layout.addWidget(self.add_decomiso_button, 4, 0, 1, 2)

        self.decomiso_form.setLayout(self.decomiso_layout)

        # Crear un QHBoxLayout para las tablas
        hbox_layout = QHBoxLayout()

        # Tabla para datos manuales
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(7)
        self.data_table.setHorizontalHeaderLabels(["Animal", "Carne Octavos", "Viseras Blancas", "Viseras Rojas", "Cabezas", "Temperatura", "Dictamen"])
        self.data_table.resizeColumnsToContents()
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Tabla para decomisos
        self.decomiso_table = QTableWidget()
        self.decomiso_table.setColumnCount(4)
        self.decomiso_table.setFixedWidth(400)
        self.decomiso_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.decomiso_table.setHorizontalHeaderLabels(["Producto", "# Animal", "Cantidad", "Motivo"])

        # Añadir las tablas al layout horizontal
        hbox_layout.addWidget(self.data_table)
        hbox_layout.addWidget(self.decomiso_table)

        # Añadir el layout horizontal al layout principal
        layout.addLayout(hbox_layout)


        # Botón para guardar todo
        self.save_button = QPushButton("Guardar Todo")
        self.save_button.clicked.connect(self.guardar_todo)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Cargar los comboboxes
        self.load_destinos()
        self.load_plantas()
        self.load_vehiculos()
        self.load_conductores()

        # Conectar las señales para cargar animales cuando se cambien destino o fecha
        self.destino_combo.currentTextChanged.connect(self.on_destino_fecha_change)
        self.fecha_input.dateChanged.connect(self.on_destino_fecha_change)

    """
    def toggle_decomiso_form(self, value):
        if value == "AC":
            self.animal_decomiso_input.setText(self.animal_combo.currentText())
            self.decomiso_form.show()
        else:
            self.decomiso_form.hide()
    """

    def add_manual_data_to_table(self):
        establecimiento = self.destino_combo.currentText()
        animales = self.animal_combo.currentText()

        # Verificar si el número de animal ya está en la tabla
        for row in range(self.data_table.rowCount()):
            if self.data_table.item(row, 0).text() == animales:
                QMessageBox.warning(self, "Error", f"El número de animal {animales} ya existe en la tabla.")
                return  # No agregar la fila si el animal ya está en la tabla

        if establecimiento == "Seleccione el Destino":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Seleccione el Destino")
            msg.setStyleSheet("font-family: Arial;font-size: 20px;")
            msg.exec_()
            return
        elif animales == "Seleccione un Animal":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Seleccione un Animal")
            msg.setStyleSheet("font-family: Arial;font-size: 20px;")
            msg.exec_()
            return
        elif animales == "No hay Animales Disponibles":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Seleccione un Animal")
            msg.setStyleSheet("font-family: Arial;font-size: 20px;")
            msg.exec_()
            return

        campos = [
            (self.animal_combo.currentText(), "Animal"),
            (self.carne_input.value(), "Carne"),
            (self.viseras_blancas_input.value(), "Viseras Blancas"),
            (self.viseras_rojas_input.value(), "Viseras Rojas"),
            (self.cabezas_input.value(), "Cabezas"),
            (self.temperatura_input.text(), "Temperatura"),
            (self.dictamen_combo.currentText(), "Dictamen")
        ]

        # Validar campos
        for valor, nombre in campos:
            if not valor or (isinstance(valor, (int, float)) and valor <= 0):
                QMessageBox.warning(self, "Error de Validación", f"El campo {nombre} no puede estar vacío ni ser 0.")
                return

        row_position = self.data_table.rowCount()
        self.data_table.insertRow(row_position)

        # Insertar los datos en la tabla
        self.data_table.setItem(row_position, 0, QTableWidgetItem(self.animal_combo.currentText()))
        self.data_table.setItem(row_position, 1, QTableWidgetItem(str(self.carne_input.value())))
        self.data_table.setItem(row_position, 2, QTableWidgetItem(str(self.viseras_blancas_input.value())))
        self.data_table.setItem(row_position, 3, QTableWidgetItem(str(self.viseras_rojas_input.value())))
        self.data_table.setItem(row_position, 4, QTableWidgetItem(str(self.cabezas_input.value())))
        self.data_table.setItem(row_position, 5, QTableWidgetItem(self.temperatura_input.text()))
        self.data_table.setItem(row_position, 6, QTableWidgetItem(self.dictamen_combo.currentText()))

        # Imprimir los datos añadidos
        for row in range(self.data_table.rowCount()):
            row_data = [self.data_table.item(row, col).text() for col in range(self.data_table.columnCount())]
            print(f"Datos en fila {row}: {row_data}")

        dictamen = self.data_table.item(row_position, 6).text()
        if dictamen == "AC":
            self.animal_decomiso_input.setText(self.animal_combo.currentText())
            self.decomiso_form.show()


    def add_decomiso_to_table(self):
        row_position = self.decomiso_table.rowCount()
        self.decomiso_table.insertRow(row_position)

        # Insertar los datos en la tabla
        self.decomiso_table.setItem(row_position, 0, QTableWidgetItem(self.producto_input.text()))
        self.decomiso_table.setItem(row_position, 1, QTableWidgetItem(self.animal_decomiso_input.text()))
        self.decomiso_table.setItem(row_position, 2, QTableWidgetItem(str(self.cantidad_input.value())))
        self.decomiso_table.setItem(row_position, 3, QTableWidgetItem(self.motivo_input.text()))

        # Imprimir los datos añadidos
        for row in range(self.decomiso_table.rowCount()):
            row_data = [self.decomiso_table.item(row, col).text() for col in range(self.decomiso_table.columnCount())]
            print(f"Datos en fila {row}: {row_data}")


    def mostrar_mensaje(self, titulo, mensaje):
        from PyQt5.QtWidgets import QMessageBox
        print(mensaje)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(QMessageBox.Information if titulo == "Datos guardados" else QMessageBox.Critical)
        msg_box.exec_()

    def print_selected_animal(self):

        # Para obtener y mostrar el texto de la opción seleccionada
        print("El texto de la seleccion", self.animal_combo.currentText())

        # Para obtener y mostrar los datos asociados (si es necesario)
        print("Los datos de la seleccion", self.animal_combo.currentData())


    def load_destinos(self):
        destinos = self.db_ops.obtener_destinos()  # Llamamos al método para obtener destinos
        self.destino_combo.addItems(destinos)

    def load_plantas(self):
        plantas = self.db_ops.obtener_plantas()  # Llamamos al método para obtener plantas
        self.planta_combo.addItems(plantas)

    def load_vehiculos(self):
        vehiculos = self.db_ops.obtener_vehiculos()  # Llamamos al método para obtener vehículos
        self.vehiculo_combo.addItems(vehiculos)

    def load_conductores(self):
        conductores = self.db_ops.obtener_conductores()  # Llamamos al método para obtener conductores
        self.conductor_combo.addItems(conductores)

    def load_animales(self):
        # Obtener el destino y la fecha seleccionados
        destino = self.destino_combo.currentText()
        fecha = self.fecha_input.date().toString("yyyy-MM-dd")

        # Obtener los animales y su correspondiente id_ingreso_detalle desde la base de datos
        animales = self.db_ops.obtener_animales(destino, fecha)

        # Limpiar el combo box de animales
        self.animal_combo.clear()

        if animales:
            self.animal_combo.addItem("Seleccione un Animal", -1)
            # Añadir los animales al combo box. El formato será algo como "Animal - ID Ingreso"
            for numero_animal, id_ingreso_detalle, id_animales in animales:
                # Usar el id_ingreso_detalle como el dato asociado al item
                self.animal_combo.addItem(f"{numero_animal}", (id_ingreso_detalle, id_animales))
        else:
            self.animal_combo.addItem("No hay Animales Disponibles", -1)

    def on_destino_fecha_change(self):
        # Actualizar los animales disponibles cuando el destino o fecha cambian
        self.load_animales()

    def limpiar(self):
        self.data_table.setRowCount(0)
        self.decomiso_table.setRowCount(0)


    def guardar_todo(self):
        """
        Recolecta todos los datos desde la interfaz (campos, combos, tablas) y los envía al back-end para ser guardados.
        """
        try:
            # Recolectar datos generales del formulario
            fecha = self.fecha_input.date().toString("yyyy-MM-dd")
            id_planta = self.planta_combo.currentIndex() + 1  # Asume que los índices coinciden con los ID
            id_vehiculo = self.vehiculo_combo.currentIndex() + 1
            id_conductores = self.conductor_combo.currentIndex() + 1


            # Preparar detalles de la guía de transporte
            guia_transporte_detalle = []

            for row in range(self.data_table.rowCount()):
                # Obtén los datos del combo para el animal seleccionado en esta fila
                id_ingreso_detalle, id_animal = self.animal_combo.itemData(row)
                data_table_n_animal = self.data_table.item(row, 0).text()
                print("este es el numero del animal", data_table_n_animal)

                detalle = {
                    'id_ingreso_detalle': id_ingreso_detalle,
                    'id_animal': id_animal,
                    'carne_octavos': int(self.data_table.item(row, 1).text()),
                    'viseras_blancas': int(self.data_table.item(row, 2).text()),
                    'viseras_rojas': int(self.data_table.item(row, 3).text()),
                    'cabezas': int(self.data_table.item(row, 4).text()),
                    'temperatura_promedio': self.data_table.item(row, 5).text(),
                    'dictamen': self.data_table.item(row, 6).text(),
                    'decomisos': []  # Inicializa la lista de decomisos
                }

                # Si el dictamen es "AC", buscar decomisos correspondientes
                if detalle['dictamen'] == 'AC':
                    for decomiso_row in range(self.decomiso_table.rowCount()):
                        # Obtener datos de cada decomiso
                        producto = self.decomiso_table.item(decomiso_row, 0).text().strip()
                        numero_animal_decomiso = self.decomiso_table.item(decomiso_row, 1).text().strip()
                        cantidad = int(self.decomiso_table.item(decomiso_row, 2).text().strip())
                        motivo = self.decomiso_table.item(decomiso_row, 3).text().strip()

                        print("este es el numero del animal en el decomiso", numero_animal_decomiso)
                        # Verificar si el número de animal del decomiso coincide con el animal actual
                        if numero_animal_decomiso == data_table_n_animal:  # Comparar con el ID correcto
                            decomiso = {
                                'id_animal': detalle['id_animal'],  # Asociar al animal correcto
                                'producto': producto,
                                'cantidad': cantidad,
                                'motivo': motivo
                            }
                            print(f"Decomisos para animal {detalle['id_animal']}: {detalle['decomisos']}")
                            detalle['decomisos'].append(decomiso)

                guia_transporte_detalle.append(detalle)

            # Preparar los datos para enviar al backend
            datos_para_guardar = {
                'fecha': fecha,
                'id_planta': id_planta,
                'id_vehiculo': id_vehiculo,
                'id_conductores': id_conductores,
                'guia_transporte': guia_transporte_detalle
            }

            print(datos_para_guardar)

            if not guia_transporte_detalle:
                print("La Lista Esta Vacia")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Advertencia")
                msg.setText("""
                La Tabla Esta Vacia,
                Ingrese Detalles Antes De Guardar""")
                msg.setStyleSheet("font-family: Arial;font-size: 20px;")
                msg.exec_()
            else:
                print("La Lista Tiene Datos")
                # Llamar al back-end para almacenar los datos
                self.db_ops.guardar_datos_backend(datos_para_guardar)
                self.limpiar()


        except Exception as e:
            self.mostrar_mensaje("Error", f"Ocurrió un error al recolectar los datos: {str(e)}")


#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    window = GuiaTransporteApp()
#    window.show()
#    sys.exit(app.exec_())

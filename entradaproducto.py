
from PyQt5.QtCore import QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QGridLayout, QLabel, QLineEdit, \
    QComboBox, \
    QPushButton, QDateEdit, QTableWidget, QHeaderView, QMessageBox

from consultas import OperacionesDB


class AnimalForm(QWidget):
    def __init__(self):
        super().__init__()
        self.is_nuevo = True
        
        # Configuración de la ventana
        self.setWindowTitle('Agregar Animal')
        self.setGeometry(100, 100, 1100, 500)

        # Layout Grid
        grid_layout = QGridLayout()

        # Título
        title_label = QLabel('Agregar Animal')
        title_label.setStyleSheet("padding: 10px ;font-size: 24px; font-weight: bold; color: #3f51b5;")
        grid_layout.addWidget(title_label, 0, 3)  # Título en la primera fila, ocupa 2 columnas

        # Fecha
        self.fecha_input = QDateEdit(self)
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setCalendarPopup(True)
        grid_layout.addWidget(QLabel('Fecha'), 1, 0)
        grid_layout.addWidget(self.fecha_input, 1, 1)
        self.fecha_input.dateChanged.connect(self.on_destino_fecha_change)

        # Destino (ComboBox)
        self.destino_input = QComboBox(self)
        grid_layout.addWidget(QLabel('Destino:'), 1, 2)
        grid_layout.addWidget(self.destino_input, 1, 3)

        self.cargar_destinos()

        # Fecha Ingreso Planta
        self.fecha_ingreso_input = QDateEdit(self)
        self.fecha_ingreso_input.setDate(QDate.currentDate())
        self.fecha_ingreso_input.setCalendarPopup(True)
        grid_layout.addWidget(QLabel('Fecha Ingreso Planta:'), 1, 4)
        grid_layout.addWidget(self.fecha_ingreso_input, 1, 5)

        # Número de Animal
        self.numero_animal_input = QLineEdit(self)
        self.numero_animal_input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        grid_layout.addWidget(QLabel('Número de Animal:'), 2, 0)
        grid_layout.addWidget(self.numero_animal_input, 2, 1)

        # Sexo (ComboBox)
        self.sexo_input = QComboBox(self)
        self.sexo_input.addItem("Seleccione El Genero")
        self.sexo_input.addItem("Macho")
        self.sexo_input.addItem("Hembra")
        grid_layout.addWidget(QLabel('Sexo:'), 2, 2)
        grid_layout.addWidget(self.sexo_input, 2, 3)

        # Peso
        self.peso_input = QLineEdit(self)
        self.peso_input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        grid_layout.addWidget(QLabel('Peso:'), 2, 4)
        grid_layout.addWidget(self.peso_input, 2, 5)

        # Número de Tiquete
        self.numero_tiquete_input = QLineEdit(self)
        self.numero_tiquete_input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        grid_layout.addWidget(QLabel('Número de Tiquete:'), 3, 0)
        grid_layout.addWidget(self.numero_tiquete_input, 3, 1)

        # Guía de Movilización
        self.guia_movilizacion_input = QLineEdit(self)
        self.guia_movilizacion_input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        grid_layout.addWidget(QLabel('Guía de Movilización:'), 3, 2)
        grid_layout.addWidget(self.guia_movilizacion_input, 3, 3)

        # Fecha Guía ICA
        self.fecha_ica_input = QDateEdit(self)
        self.fecha_ica_input.setDate(QDate.currentDate())
        self.fecha_ica_input.setCalendarPopup(True)
        grid_layout.addWidget(QLabel('Fecha Guía ICA:'), 3, 4)
        grid_layout.addWidget(self.fecha_ica_input, 3, 5)

        # Número de Corral
        self.numero_corral_input = QLineEdit(self)
        self.numero_corral_input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        grid_layout.addWidget(QLabel('Número de Corral:'), 4, 0)
        grid_layout.addWidget(self.numero_corral_input, 4, 1)

        # Especie (ComboBox)
        self.especie_input = QComboBox(self)
        self.especie_input.addItem("Seleccione la Especie")
        self.especie_input.addItem("Bovino")
        self.especie_input.addItem("Porcino")
        grid_layout.addWidget(QLabel('Especie:'), 4, 2)
        grid_layout.addWidget(self.especie_input, 4, 3)

        # Botón de Enviar
        submit_button = QPushButton('Agregar Animal a La Tabla', self)
        submit_button.clicked.connect(self.on_submit)
        grid_layout.addWidget(submit_button, 5, 0, 2, 2)  # El botón ocupa 2 columnas

        # Botón de Enviar
        saved_button = QPushButton('Guardar', self)
        saved_button.clicked.connect(self.guardar_en_db)
        grid_layout.addWidget(saved_button, 12, 0, 1, 2)  # El botón ocupa 2 columnas

        # Tabla para mostrar los animales ingresados
        self.table = QTableWidget(self)
        self.table.setColumnCount(11)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(['Destino', '# Animal', 'Sexo', 'Kilos', '#.Tiquete', 'Fecha Ingreso', 'Guia Movilizacion', 'Fecha Guia ICA', '# De Corral', 'Especie', 'is_nuevo' ])
        self.table.setColumnHidden(10, True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        grid_layout.addWidget(self.table, 7, 0, 1, 10)  # La tabla ocupa 6 columnas

        self.setLayout(grid_layout)

        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 20px;
            }
            QLabel, QLineEdit, QComboBox, QSpinBox, QDateEdit, QPushButton {
                font-size: 16px;
                padding: 12px;  # Aumenta el padding (espacio interno) de los widgets
            }
            QLineEdit, QComboBox, QSpinBox, QDateEdit {
                height: 40px;  # Aumenta la altura de los campos de entrada
            }
            QPushButton {
                height: 40px;  # Aumenta la altura del botón
            }
        """)

    def on_submit(self):
        # Obtener los datos del formulario
        id_establecimiento = self.destino_input.currentData()
        if id_establecimiento == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Seleccione un Establecimiento Primero Antes De Guardar")
            msg.exec_()
            print("Seleccione un Establecimiento")
            return

        sexo = self.sexo_input.currentText()
        if sexo == "Seleccione El Genero":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Seleccione el Genero Primero Antes De Guardar")
            msg.exec_()
            return

        especie = self.especie_input.currentText()
        if especie == "Seleccione la Especie":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Seleccione la Especie Primero Antes De Guardar")
            msg.exec_()

        numero_animal = self.numero_animal_input.text().strip()
        print("numero de animal en el input",numero_animal)

        if not numero_animal:
            QMessageBox.warning(self, "Error de Validacion", "El numero del animal no puede estar vacio")
            return

        for row in range(self.table.rowCount()):
            if self.table.item(row, 1).text() == numero_animal:
                QMessageBox.warning(self, "Error", f"el numero de animal {numero_animal} ya existe en la tabla")
                return

        data = {
            "destino" : self.destino_input.currentText(),
            "numero_animal" : self.numero_animal_input.text(),
            "sexo" : self.sexo_input.currentText(),
            "peso" : self.peso_input.text(),
            "numero_tiquete" : self.numero_tiquete_input.text(),
            "fecha_ingreso" : self.fecha_ingreso_input.date().toString("yyyy-MM-dd"),
            "guia_movilizacion" : self.guia_movilizacion_input.text(),
            "fecha_ica" : self.fecha_ica_input.date().toString("yyyy-MM-dd"),
            "numero_corral" : self.numero_corral_input.text(),
            "especie": self.especie_input.currentText(),
            "is_nuevo": self.is_nuevo,
        }

        validacion = True

        for field, value in data.items():
            input_widget = getattr(self, f"{field}_input", None)

            if not value or value in ["Seleccione un Seleccione un Destino", "Seleccione El Genero", "Seleccione la Especie"]:
                validacion = False
                if input_widget:
                    input_widget.setStyleSheet("border: 1px solid red;")
            elif input_widget:
                input_widget.setStyleSheet("background-color: white;")

        if validacion:

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            for idx, (field, value) in enumerate(data.items()):
                self.table.setItem(row_position, idx, QTableWidgetItem(str(value)))

            self.table.setItem(row_position, 10, QTableWidgetItem("True"))

        else:

            self.clear_form()

    def clear_form(self):
        # Limpiar los campos del formulario después de agregar el animal
        self.fecha_input.setDate(QDate.currentDate())
        self.destino_input.setCurrentIndex(0)
        self.fecha_ingreso_input.setDate(QDate.currentDate())
        self.numero_animal_input.clear()
        self.sexo_input.setCurrentIndex(0)
        self.peso_input.clear()  # Cambiado a clear()
        self.numero_tiquete_input.clear()
        self.guia_movilizacion_input.clear()
        self.fecha_ica_input.setDate(QDate.currentDate())
        self.numero_corral_input.clear()
        self.especie_input.setCurrentIndex(0)

    def on_destino_fecha_change(self):
        self.animales_por_fecha()

    def animales_por_fecha(self):
        fecha = self.fecha_input.date().toString("yyyy-MM-dd")

        db = OperacionesDB()
        animales = db.obtener_ingreso_por_fecha(fecha)

        if not animales or not animales.get('detalles'):
            return  # Detiene la ejecución si no hay resultados

        # Limpia la tabla antes de agregar nuevos datos
        self.table.setRowCount(0)

        for row, detalle in enumerate(animales['detalles']):
            detalle["is_nuevo"] = False

            values = [
                detalle["nombre_establecimiento"],
                detalle["numero_animal"],
                detalle["sexo"],
                detalle["peso"],
                detalle["numero_tiquete"],
                detalle["fecha_ingreso"].strftime("%d/%m/%Y"),
                detalle["guia_movilizacion"],
                detalle["fecha_guia_ica"].strftime("%d/%m/%Y"),
                detalle["numero_corral"],
                detalle["especie"],
                detalle["is_nuevo"],
            ]

            # Insertar una nueva fila
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_position, col, item)


    def cargar_destinos(self):

        db = OperacionesDB()
        destinos = db.obtener_establecimientos()


        if destinos:
            self.destino_input.addItem("Seleccione un destino", -1)
            for id, nombre_establecimiento in destinos:
                self.destino_input.addItem(nombre_establecimiento, id)
        else:
            self.destino_input.addItem("No hay destinos disponibles", -1)


    def limpia(self):
        self.table.setRowCount(0)

    def guardar_en_db(self):
        animales = []

        id_establecimiento = self.destino_input.currentData()
        if id_establecimiento == -1:
            print("Seleccione un Establecimiento")
            return

        for row in range(self.table.rowCount()):
            is_nuevo_item = self.table.item(row, 10)
            if is_nuevo_item and is_nuevo_item.text() != "True":
                print(f"El registro en la fila {row + 1} no es nuevo, se omite.")
                continue  # Saltar filas que no son nuevas

            animal = {
                "destino" : id_establecimiento,
                "numero_animal" : self.table.item(row, 1).text(),
                "sexo" : self.table.item(row, 2).text(),
                "peso" : self.table.item(row, 3).text(),
                "numero_tiquete" : self.table.item(row, 4).text(),
                "fecha_ingreso" : self.table.item(row, 5).text(),
                "guia_movilizacion" : self.table.item(row, 6).text(),
                "fecha_ica" : self.table.item(row, 7).text(),
                "numero_corral" : self.table.item(row, 8).text(),
                "especie" : self.table.item(row, 9).text(),
            }

            try:
                QDate.fromString(animal["fecha_ingreso"], "yyyy-MM-dd")
                QDate.fromString(animal["fecha_ica"], "yyyy-MM-dd")
            except ValueError:
                print(f"Error en el formato para el animal: {animal['numero_animal']}")
                continue

            animales.append(animal)


        if not animales:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("""
            La Tabla Esta Vacia,
            Ingrese Animales Antes De Guardar""")
            msg.exec_()
            return


        id_user = 1
        id_planta = 1
        fecha = self.fecha_input.date().toString("yyyy-MM-dd")

        db = OperacionesDB()
        if db.guardar_ingreso(id_user, id_planta, fecha, animales):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Exito")
            msg.setText("""
            La Informacion Se Ingreso en la Base de Datos Correctamente
            """)
            msg.exec_()

            self.limpia()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("""
            La Informacion No Se Pudo Ingresar En La Base De Datos
            """)
            msg.exec_()




#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    window = AnimalForm()
#    window.show()
#    sys.exit(app.exec_())

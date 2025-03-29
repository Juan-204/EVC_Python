import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from consultas import OperacionesDB  # Asegúrate de que esta clase tenga implementados los métodos necesarios
import numpy as np

def make_autopct(values):
    """Función para mostrar el valor absoluto en lugar del porcentaje en un gráfico de pastel."""
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{val}'
    return my_autopct

class Estadisticas(QWidget):
    def __init__(self):
        super().__init__()
        self.db = OperacionesDB()
        self.setWindowTitle("Estadísticas Globales y Adicionales")
        self.setGeometry(100, 100, 1000, 800)
        
        main_layout = QVBoxLayout()
        
        # ---------------------------
        # Área superior: Estadísticas Globales
        # ---------------------------
        self.top_widget = QWidget()
        top_layout = QHBoxLayout(self.top_widget)
        self.top_figure, (self.ax_global_animales, self.ax_global_decomisos) = plt.subplots(1, 2, figsize=(8, 4))
        self.top_canvas = FigureCanvas(self.top_figure)
        top_layout.addWidget(self.top_canvas)
        self.top_widget.setFixedHeight(300)
        main_layout.addWidget(self.top_widget)
        
        # ---------------------------
        # Área inferior: Estadísticas Adicionales
        # ---------------------------
        self.lower_widget = QWidget()
        lower_layout = QVBoxLayout(self.lower_widget)
        
        # Combobox de establecimientos para filtrar estadísticas adicionales
        self.combo_establecimientos = QComboBox()
        self.cargar_establecimientos()
        self.combo_establecimientos.currentIndexChanged.connect(self.actualizar_estadisticas_adicionales)
        lower_layout.addWidget(self.combo_establecimientos)
        
        # Crear una figura para los gráficos adicionales usando GridSpec
        self.lower_figure = plt.figure(figsize=(10, 6))
        gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
        self.ax_animales_est = self.lower_figure.add_subplot(gs[0, 0])
        self.ax_sexo_especie = self.lower_figure.add_subplot(gs[0, 1])
        self.ax_evolucion = self.lower_figure.add_subplot(gs[1, :])
        self.lower_canvas = FigureCanvas(self.lower_figure)
        lower_layout.addWidget(self.lower_canvas)
        
        main_layout.addWidget(self.lower_widget)
        self.setLayout(main_layout)
        
        # Cargar datos globales y actualizar el panel adicional según la selección
        self.cargar_estadisticas_globales()
        self.actualizar_estadisticas_adicionales()
    
    def cargar_estadisticas_globales(self):
        """Carga y muestra los gráficos globales de animales y decomisos por especie."""
        self.ax_global_animales.clear()
        self.ax_global_decomisos.clear()

        # Global: Animales por especie (gráfico de pastel)
        datos_animales = self.db.obtener_estadisticas_animales_por_especie()
        if datos_animales:
            especies = [d['especie'] for d in datos_animales]
            cantidades = [d['cantidad'] for d in datos_animales]
            self.ax_global_animales.pie(cantidades, labels=especies, autopct=make_autopct(cantidades),
                                        startangle=140, textprops={'fontsize': 12})
            self.ax_global_animales.set_title("Animales por Especie (Global)", fontsize=14)
        else:
            self.ax_global_animales.text(0.5, 0.5, "Sin datos de animales", ha='center', va='center', fontsize=12)

        # Global: Decomisos por especie (gráfico de pastel)
        datos_decomisos = self.db.obtener_decomisos_totales_por_especie()
        if datos_decomisos:
            especies_dec = [d['especie'] for d in datos_decomisos]
            cantidades_dec = [d['cantidad_decomisos'] for d in datos_decomisos]
            self.ax_global_decomisos.pie(cantidades_dec, labels=especies_dec, autopct=make_autopct(cantidades_dec),
                                         startangle=140, textprops={'fontsize': 12})
            self.ax_global_decomisos.set_title("Decomisos por Especie (Global)", fontsize=14)
        else:
            self.ax_global_decomisos.text(0.5, 0.5, "Sin datos de decomisos", ha='center', va='center', fontsize=12)

        self.top_canvas.draw()
    
    def cargar_establecimientos(self):
        """Carga los establecimientos en el combobox."""
        establecimientos = self.db.obtener_establecimientos()
        self.combo_establecimientos.clear()
        self.combo_establecimientos.addItem("Seleccione un establecimiento", None)
        for est in establecimientos:
            self.combo_establecimientos.addItem(est[1], est[0])
    
    def actualizar_estadisticas_adicionales(self):
        """Actualiza los gráficos adicionales según el establecimiento seleccionado."""
        est_id = self.combo_establecimientos.currentData()
        for ax in [self.ax_animales_est, self.ax_sexo_especie, self.ax_evolucion]:
            ax.clear()

        if not est_id:
            for ax in [self.ax_animales_est, self.ax_sexo_especie, self.ax_evolucion]:
                ax.text(0.5, 0.5, "Seleccione un establecimiento", ha='center', va='center', fontsize=12)
            self.lower_canvas.draw()
            return
        
        # Animales por especie
        datos_animales_est = self.db.obtener_estadisticas_animales_por_especie_establecimiento(est_id)
        if datos_animales_est:
            especies = [d['especie'] for d in datos_animales_est]
            cantidades = [d['cantidad'] for d in datos_animales_est]
            bars = self.ax_animales_est.bar(especies, cantidades, color='#3f51b5')
            self.ax_animales_est.set_title("Animales por Especie", fontsize=14)
            self.ax_animales_est.set_xlabel("Especie", fontsize=12)
            self.ax_animales_est.set_ylabel("Cantidad", fontsize=12)
            self.ax_animales_est.tick_params(axis='x', labelsize=10, rotation=0)
            
            for bar in bars:
                height = bar.get_height()
                self.ax_animales_est.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}',
                                          ha='center', va='bottom', fontsize=12, color='black')

        # Distribución de sexo
        datos_sexo_especie = self.db.obtener_distribucion_sexo_por_especie_establecimiento(est_id)
        if datos_sexo_especie:
            especies = [d['especie'] for d in datos_sexo_especie]
            macho = [d['Macho'] for d in datos_sexo_especie]
            hembra = [d['Hembra'] for d in datos_sexo_especie]
            x = np.arange(len(especies))
            width = 0.35
            self.ax_sexo_especie.bar(x - width/2, macho, width, label='Macho', color='#2196f3')
            self.ax_sexo_especie.bar(x + width/2, hembra, width, label='Hembra', color='#f44336')
            self.ax_sexo_especie.set_xticks(x)
            self.ax_sexo_especie.set_xticklabels(especies, rotation=0, fontsize=10)
            self.ax_sexo_especie.set_title("Distribución de Sexo por Especie", fontsize=14)
            self.ax_sexo_especie.legend(fontsize=12)

        # Evolución temporal de ingresos
        datos_evolucion = self.db.obtener_evolucion_ingresos_establecimiento(est_id)
        if datos_evolucion:
            fechas = [d['fecha'] for d in datos_evolucion]
            cantidades_ing = [d['cantidad'] for d in datos_evolucion]
            self.ax_evolucion.plot(fechas, cantidades_ing, marker='o', linestyle='-', color='#ff9800', markersize=8)
            self.ax_evolucion.set_title("Evolución Temporal de Ingresos", fontsize=14)
            self.ax_evolucion.grid(True, linestyle='--', alpha=0.5)

        self.lower_canvas.draw()

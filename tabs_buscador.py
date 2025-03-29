from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from buscador import Buscador
from buscador_guia import GuiasTransporteBuscador
#from guiatransporte import GuiasTransporteWidget

class ConsultaWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Creamos el QTabWidget para las pestañas internas
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                font-size: 12px;
                min-width: 0px;
                min-height: 0px;
            }
            QTabBar::tab:selected {
                background-color: #5DADE2;
                color: white;
            }
        """)


        # Pestaña 1: Buscador individual
        tab_widget.addTab(Buscador(), "Busqueda Individual")
        # Pestaña 2: Guías de Transporte
        tab_widget.addTab(GuiasTransporteBuscador(), "Busqueda por Establecimiento")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)

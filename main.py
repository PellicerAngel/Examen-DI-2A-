from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHeaderView
from database import Database
import sys
import os
import sqlite3
from PySide6.QtWidgets import (
    QMessageBox,QAbstractItemView, QDialog, QFormLayout, QMenu,QDialogButtonBox
)
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtGui import QAction, QKeySequence

from PySide6.QtCore import QTranslator, QLibraryInfo

class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestió de Productes")
        self.setGeometry(100, 100, 600, 500)
        self.db = Database()



        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)

        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Menu")


        accion = QAction("&Afegir i Modificar", self)
        accion.triggered.connect(self.add_product)
        menu.addAction(accion)



        # Formulari (tot amb QLineEdit)
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()  
        self.category_input = QLineEdit()  


        self.edit_button = QPushButton("Eliminar Producte")
        self.edit_button.clicked.connect(self.mostrar_dialogo_delete)
        self.layout.addWidget(self.edit_button)

        

        # Taula de productes
        self.table = self.create_table()
        self.layout.addWidget(self.table)

        self.load_products()



    class ProductForm(QDialog):
        def __init__(self, parent=None, product=None):
            super().__init__(parent)
            self.setWindowTitle("Gestió de Producte")
            self.layout = QVBoxLayout()

            form_layout = QFormLayout()
            self.nom_input = QLineEdit()
            self.preu_input = QLineEdit()
            self.quantitat_input = QLineEdit()
            form_layout.addRow("Nom:", self.nom_input)
            form_layout.addRow("Preu:", self.preu_input)
            form_layout.addRow("Quantitat:", self.quantitat_input)
            
            self.accept_button = QPushButton("Guardar")
            self.modificar_button = QPushButton("Modificar")
            self.cancel_button = QPushButton("Cancel·lar")
            
            self.layout.addLayout(form_layout)
            self.layout.addWidget(self.accept_button)
            self.layout.addWidget(self.modificar_button)
            self.layout.addWidget(self.cancel_button)
            self.setLayout(self.layout)
            
            self.accept_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self.modificar_button.clicked.connect(self.mostrar_dialogo_edit)
            
            self.product = product
            if product:
                self.nom_input.setText(product[1])
                self.preu_input.setText(str(product[2]))
                self.quantitat_input.setText(str(product[3]))

        def get_product_data(self):
            return self.nom_input.text(), self.preu_input.text(), self.quantitat_input.text()
        
        def edit_product(self):
            print("holi caracoli")
            selected_row = self.table.currentRow()
            if selected_row == -1:
                return

            product_id = self.db.get_products()[selected_row][0]
            
            new_name = self.name_input.text()
            new_price = self.price_input.text()
            new_category = self.category_input.text()

            if new_name and new_price and new_category:
                self.db.update_product(product_id, new_name, new_price, new_category)
                self.load_products()

        def mostrar_dialogo_edit(self):
            ventana_dialogo = self.DialogoPersonalizado()
            ventana_dialogo.setWindowTitle("Ventana de dialogo personalizado")
            resultado = ventana_dialogo.exec()
            if resultado:
                self.edit_product()
            else:
                print("Cancelada")

        def DialogoPersonalizado(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)

                self.setWindowTitle("Dialogo personalizado")

                botones = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

                self.caja_botones = QDialogButtonBox(botones)
                self.caja_botones.accepted.connect(self.accept)
                self.caja_botones.rejected.connect(self.reject)

                self.layout_dialogo = QVBoxLayout()
                self.layout_dialogo.addWidget(
                    QLabel("¿Estás seguro de querer realizar esta acción?"))
                self.layout_dialogo.addWidget(self.caja_botones)
                self.setLayout(self.layout_dialogo)

        
    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nom", "Preu", "Categoria"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        return table

    def load_products(self):
        self.table.setRowCount(0)
        products = self.db.get_products()
        for row_index, (product_id, name, price, category) in enumerate(products):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(price))
            self.table.setItem(row_index, 2, QTableWidgetItem(category))


    def add_product(self):
        dialog = self.ProductForm(self)
        if dialog.exec():
            nom, preu, quantitat = dialog.get_product_data()
            if nom and preu and quantitat:
                self.db.add_product(nom, float(preu),quantitat)
                self.load_products()
            else:
                QMessageBox.warning(self, "Error", "Tots els camps són obligatoris")







    def delete_product(self):
        print("holi")
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        product_id = self.db.get_products()[selected_row][0]
        self.db.delete_product(product_id)
        self.load_products()


    def mostrar_dialogo_delete(self):
        ventana_dialogo = self.DialogoPersonalizado(self)
        ventana_dialogo.setWindowTitle("Ventana de dialogo personalizado")
        resultado = ventana_dialogo.exec()
        if resultado:
        
            self.delete_product()
        else:
            print("Cancelada")











if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec())

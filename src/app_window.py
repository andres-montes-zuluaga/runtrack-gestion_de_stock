from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QFileDialog, QInputDialog, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from .stock_class import Stock
import csv

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de Stock")
        self.setGeometry(100, 100, 800, 600)
        try:
            print("Connecting to database...")
            self.stock_manager = Stock(host="localhost", user="root", password="123456789", database="store")
            print("Connected to database successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Database Connection Error", f"Failed to connect to the database: {e}")
            print(f"Database connection error: {e}")
            return
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        # First row of buttons
        self.button_layout1 = QHBoxLayout()
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        self.button_layout1.addWidget(self.add_button)
        
        self.delete_button = QPushButton("Delete Product")
        self.delete_button.clicked.connect(self.delete_product)
        self.button_layout1.addWidget(self.delete_button)
        
        self.modify_button = QPushButton("Modify Product")
        self.modify_button.clicked.connect(self.modify_product)
        self.button_layout1.addWidget(self.modify_button)
        
        self.layout.addLayout(self.button_layout1)
        
        # Second row of buttons
        self.button_layout2 = QHBoxLayout()
        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.button_layout2.addWidget(self.export_button)
        
        self.filter_button = QPushButton("Filter by Category")
        self.filter_button.clicked.connect(self.filter_by_category)
        self.button_layout2.addWidget(self.filter_button)
        
        self.chart_button = QPushButton("Show Product Quantities Chart")
        self.chart_button.clicked.connect(self.show_chart)
        self.button_layout2.addWidget(self.chart_button)
        
        self.layout.addLayout(self.button_layout2)
        
        # Third row of buttons
        self.button_layout3 = QHBoxLayout()
        self.total_stock_value_button = QPushButton("Show Total Stock Value")
        self.total_stock_value_button.clicked.connect(self.show_total_stock_value)
        self.button_layout3.addWidget(self.total_stock_value_button)
        
        self.layout.addLayout(self.button_layout3)
        
        self.load_products()
    
    def load_products(self, products=None):
        try:
            print("Loading products...")
            self.table.clear()
            if products is None:
                products = self.stock_manager.show_products()
            self.table.setRowCount(len(products))
            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Description", "Price", "Quantity", "Image", "Category ID"])
            
            for row_idx, product in enumerate(products):
                for col_idx, item in enumerate(product):
                    if col_idx == 5:  # Image column
                        label = QLabel()
                        pixmap = QPixmap(item)
                        label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                        self.table.setCellWidget(row_idx, col_idx, label)
                    else:
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
            print("Products loaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")
            print(f"Failed to load products: {e}")
    
    def add_product(self):
        try:
            print("Adding product...")
            name, ok = QInputDialog.getText(self, 'Add Product', 'Enter product name:')
            if ok:
                description, ok = QInputDialog.getText(self, 'Add Product', 'Enter product description:')
                if ok:
                    price, ok = QInputDialog.getDouble(self, 'Add Product', 'Enter product price:')
                    if ok:
                        quantity, ok = QInputDialog.getInt(self, 'Add Product', 'Enter product quantity:')
                        if ok:
                            image_url, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.jpg *.jpeg)')
                            if image_url:
                                id_category, ok = QInputDialog.getInt(self, 'Add Product', 'Enter category ID:')
                                if ok:
                                    self.stock_manager.add_product(name, description, price, quantity, image_url, id_category)
                                    self.load_products()
                                    print("Product added successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add product: {e}")
            print(f"Failed to add product: {e}")

    def delete_product(self):
        try:
            print("Deleting product...")
            product_id, ok = QInputDialog.getInt(self, 'Delete Product', 'Enter product ID to delete:')
            if ok:
                self.stock_manager.delete_product(product_id)
                self.load_products()
                print("Product deleted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete product: {e}")
            print(f"Failed to delete product: {e}")

    def modify_product(self):
        try:
            print("Modifying product...")
            product_id, ok = QInputDialog.getInt(self, 'Modify Product', 'Enter product ID to modify:')
            if ok:
                name, ok = QInputDialog.getText(self, 'Modify Product', 'Enter new product name (leave blank to keep current):')
                if ok:
                    description, ok = QInputDialog.getText(self, 'Modify Product', 'Enter new product description (leave blank to keep current):')
                    if ok:
                        price, ok = QInputDialog.getDouble(self, 'Modify Product', 'Enter new product price (leave blank to keep current):', decimals=2)
                        if ok:
                            quantity, ok = QInputDialog.getInt(self, 'Modify Product', 'Enter new product quantity (leave blank to keep current):')
                            if ok:
                                image_url, _ = QFileDialog.getOpenFileName(self, 'Select New Image (leave blank to keep current)', '', 'Images (*.png *.jpg *.jpeg)')
                                id_category, ok = QInputDialog.getInt(self, 'Modify Product', 'Enter new category ID (leave blank to keep current):')
                                if ok:
                                    self.stock_manager.modify_product(product_id, name or None, description or None, price or None, quantity or None, image_url or None, id_category or None)
                                    self.load_products()
                                    print("Product modified successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to modify product: {e}")
            print(f"Failed to modify product: {e}")

    def export_to_csv(self):
        try:
            print("Exporting to CSV...")
            file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
            if file_path:
                products = self.stock_manager.show_products()
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Name", "Description", "Price", "Quantity", "Image", "Category ID"])
                    for product in products:
                        writer.writerow(product)
                print("Exported to CSV successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export to CSV: {e}")
            print(f"Failed to export to CSV: {e}")

    def filter_by_category(self):
        try:
            print("Filtering by category...")
            categories = self.stock_manager.show_categories()
            category_names = ["All categories"] + [category[1] for category in categories]
            category_name, ok = QInputDialog.getItem(self, "Filter by Category", "Select category:", category_names, 0, False)
            if ok and category_name:
                if category_name == "All categories":
                    products = self.stock_manager.show_products()
                else:
                    category_id = next(category[0] for category in categories if category[1] == category_name)
                    products = self.stock_manager.show_products_by_category(category_id)
                self.load_products(products)
                print(f"Filtered by category: {category_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to filter by category: {e}")
            print(f"Failed to filter by category: {e}")

    def show_chart(self):
        try:
            print("Showing chart...")
            products = self.stock_manager.show_products()
            series = QPieSeries()
            for product in products:
                slice = series.append(product[1], product[4])
                slice.setColor(Qt.GlobalColor(product[0] % 19 + 2))  # Set different colors for each slice
            
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Product Quantities")
            
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)
            
            chart_window = QMainWindow(self)
            chart_window.setCentralWidget(chart_view)
            chart_window.resize(800, 600)
            chart_window.show()
            print("Chart shown successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to show chart: {e}")
            print(f"Failed to show chart: {e}")

    def show_total_stock_value(self):
        try:
            print("Showing total stock value...")
            total_value = self.stock_manager.stock_total_price()
            QMessageBox.information(self, "Total Stock Value", f"Total stock value: ${total_value}")
            print(f"Total stock value: ${total_value}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to show total stock value: {e}")
            print(f"Failed to show total stock value: {e}")

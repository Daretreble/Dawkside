import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Alert Example")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.alert_button = QPushButton("Show Alert")
        layout.addWidget(self.alert_button)

        self.alert_button.clicked.connect(self.show_alert)
        
        # Connect the focus event to show_alert_on_focus
        self.input_field.installEventFilter(self)

    def show_alert(self):
        input_text = self.input_field.text()
        alert_text = f"Field Text: {input_text}"
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Alert")
        msg_box.setText(alert_text)
        msg_box.exec()

    def eventFilter(self, obj, event):
        if obj == self.input_field and event.type() == 9:  # 9 corresponds to the FocusIn event
            self.show_alert_on_focus()
        return super().eventFilter(obj, event)

    def show_alert_on_focus(self):
        alert_text = "Field is Focused!"
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Alert")
        msg_box.setText(alert_text)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
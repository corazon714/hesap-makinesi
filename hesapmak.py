import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False  # Flag to indicate if dark mode is enabled
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # Create the input field with larger font
        self.input_field = QLineEdit()
        font = self.input_field.font()
        font.setPointSize(24)
        self.input_field.setFont(font)
        self.input_field.setReadOnly(True)
        layout.addWidget(self.input_field)

        # Create the buttons with larger font using a grid layout
        buttons_grid = QGridLayout()

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '(', ')'],
            ['+', '='],
        ]

        for i, row in enumerate(buttons):
            for j, label in enumerate(row):
                button = QPushButton(label)
                font = button.font()
                font.setPointSize(20)
                button.setFont(font)
                button.clicked.connect(self.on_button_click)
                buttons_grid.addWidget(button, i, j)

        # Add the reset button with larger font
        reset_button = QPushButton('Reset')
        font = reset_button.font()
        font.setPointSize(16)
        reset_button.setFont(font)
        reset_button.clicked.connect(self.reset_calculator)
        buttons_grid.addWidget(reset_button, 4, 2, 1, 2)  # Make reset button span two columns

        # Add the scientific function buttons with larger font
        scientific_buttons = ['√', 'x^2', 'sin', 'cos', 'tan']
        for i, label in enumerate(scientific_buttons):
            button = QPushButton(label)
            font = button.font()
            font.setPointSize(16)
            button.setFont(font)
            button.clicked.connect(self.on_button_click)
            buttons_grid.addWidget(button, 5, i)

        scientific_buttons_2 = ['π', 'e', 'abs', 'exp', 'log']
        for i, label in enumerate(scientific_buttons_2):
            button = QPushButton(label)
            font = button.font()
            font.setPointSize(16)
            button.setFont(font)
            button.clicked.connect(self.on_button_click)
            buttons_grid.addWidget(button, 6, i)

        layout.addLayout(buttons_grid)
        self.central_widget.setLayout(layout)
        self.setWindowTitle('Calculator')
        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:  # Close the calculator when Escape is pressed
            self.close()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:  # Calculate when Enter is pressed
            self.calculate_result()
        elif key == Qt.Key_Backspace:  # Clear the last character when Backspace is pressed
            self.input_field.backspace()
        elif key == Qt.Key_Delete:  # Clear the entire input when Delete is pressed
            self.reset_calculator()
        else:  # For other keys, append their text to the input field
            text = event.text()
            if text:
                self.input_field.insert(text)

    def on_button_click(self):
        sender = self.sender()
        clicked_text = sender.text()

        if clicked_text == '=':
            self.calculate_result()
        elif clicked_text == '√':
            self.calculate_unary_operation(math.sqrt)
        elif clicked_text == 'x^2':
            self.calculate_unary_operation(lambda x: x ** 2)
        elif clicked_text == 'sin':
            self.calculate_unary_operation(math.sin, math.radians)
        elif clicked_text == 'cos':
            self.calculate_unary_operation(math.cos, math.radians)
        elif clicked_text == 'tan':
            self.calculate_unary_operation(math.tan, math.radians)
        elif clicked_text == 'log':
            self.calculate_unary_operation(math.log10)
        elif clicked_text == 'π':
            self.input_field.setText(str(math.pi))
        elif clicked_text == 'e':
            self.input_field.setText(str(math.e))
        elif clicked_text == 'abs':
            self.calculate_unary_operation(abs)
        elif clicked_text == 'exp':
            self.calculate_unary_operation(math.exp)
        else:
            self.input_field.setText(self.input_field.text() + clicked_text)

    def calculate_result(self):
        try:
            result = eval(self.input_field.text())
            if result == 31:
                result = "31 xD"
            else:
                result = str(result)
            self.input_field.setText(result)
        except Exception as e:
            self.input_field.setText("Error " + e.__class__.__name__ + ": " + str(e) + ". Press Del to reset.")

    def calculate_unary_operation(self, operation, converter=None):
        try:
            value = float(self.input_field.text())
            if converter:
                value = converter(value)
            result = str(operation(value))
            self.input_field.setText(result)
        except ValueError:
            self.input_field.setText("Error")

    def reset_calculator(self):
        self.input_field.clear()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #333;
                    color: #FFF;
                }
                QPushButton {
                    background-color: #444;
                    color: #FFF;
                }
                QLineEdit {
                    background-color: #222;
                    color: #FFF;
                }
            """)
        else:
            self.setStyleSheet("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()

    # Add the dark mode toggle button
    dark_mode_button = QPushButton('Toggle Dark Mode')
    dark_mode_button.clicked.connect(calc.toggle_dark_mode)
    calc.centralWidget().layout().addWidget(dark_mode_button)

    sys.exit(app.exec_())

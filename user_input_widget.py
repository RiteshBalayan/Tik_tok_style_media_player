# user_input_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QRadioButton, QPushButton, QLabel
from PyQt5.QtGui import QFont

class UserInputWidget(QWidget):
    def __init__(self, callback):
        super().__init__()

        self.callback = callback  # Callback function to call when user has entered their data

        self.setGeometry(100, 100, 600, 800)  # Set the geometry to match WidgetManager
        self.setFixedSize(600, 800)  # Set the size to be fixed

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel('Enter your name:')
        self.name_input = QLineEdit()

        self.student_radio = QRadioButton('Student')
        self.teacher_radio = QRadioButton('Teacher')

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.student_radio)
        self.layout.addWidget(self.teacher_radio)
        self.layout.addWidget(self.submit_button)

        # Set font
        font = QFont('Arial', 20)  # Set bigger font size
        self.setFont(font)

    def submit(self):
        name = self.name_input.text()
        role = 'Student' if self.student_radio.isChecked() else 'Teacher'

        self.callback(name, role)  # Call the callback function with the entered data

        self.close()  # Close the widget after the data has been submitted



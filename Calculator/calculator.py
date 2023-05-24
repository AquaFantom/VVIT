import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5 import QtGui


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("Calculator")
        self.op = None
        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_0 = QHBoxLayout()
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_0)
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addLayout(self.hbox_3)
        self.vbox.addLayout(self.hbox_4)
        self.vbox.addLayout(self.hbox_result)

        self.input = QLabel(self)
        # self.input.setDisabled(True)

        self.hbox_input.addWidget(self.input)

        self.b_clear = QPushButton("C", self)
        self.hbox_0.addWidget(self.b_clear)

        self.b_1 = QPushButton("1", self)
        self.hbox_1.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_1.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_1.addWidget(self.b_3)

        self.b_plus = QPushButton("+", self)
        self.hbox_1.addWidget(self.b_plus)

        self.b_4 = QPushButton("4", self)
        self.hbox_2.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_2.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_2.addWidget(self.b_6)

        self.b_minus = QPushButton("-", self)
        self.hbox_2.addWidget(self.b_minus)

        self.b_7 = QPushButton("7", self)
        self.hbox_3.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_3.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_3.addWidget(self.b_9)

        self.b_multiply = QPushButton("*", self)
        self.hbox_3.addWidget(self.b_multiply)

        self.b_point = QPushButton(".", self)
        self.hbox_4.addWidget(self.b_point)

        self.b_0 = QPushButton("0", self)
        self.hbox_4.addWidget(self.b_0)

        self.b_divide = QPushButton("/", self)
        self.hbox_4.addWidget(self.b_divide)

        self.b_mod = QPushButton("%", self)
        self.hbox_4.addWidget(self.b_mod)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_multiply.clicked.connect(lambda: self._operation("*"))
        self.b_divide.clicked.connect(lambda: self._operation("/"))
        self.b_mod.clicked.connect(lambda: self._operation("%"))
        self.b_clear.clicked.connect(lambda: self._operation("0"))
        self.b_result.clicked.connect(self._result)

        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_point.clicked.connect(lambda: self._button("."))

    def _button(self, param):
        line = self.input.text()
        self.input.setText(line + param)

    def _operation(self, op):
        if self.input.text():
            self.num_1 = float(self.input.text())
            self.op = op
            self.input.setText("")

    def _result(self):
        if self.input.text():

            if self.op:
                self.num_2 = float(self.input.text())
                if self.op == "+":
                    if (self.num_1 + self.num_2).is_integer():
                        self.input.setText(str(int(self.num_1 + self.num_2)))
                    else:
                        self.input.setText(str(self.num_1 + self.num_2))
                elif self.op == "-":
                    if (self.num_1 - self.num_2).is_integer():
                        self.input.setText(str(int(self.num_1 - self.num_2)))
                    else:
                        self.input.setText(str(self.num_1 - self.num_2))
                elif self.op == "*":
                    if (self.num_1 * self.num_2).is_integer():
                        self.input.setText(str(int(self.num_1 * self.num_2)))
                    else:
                        self.input.setText(str(self.num_1 * self.num_2))
                elif self.op == "/":
                    try:
                        if (self.num_1 / self.num_2).is_integer():
                            self.input.setText(str(int(self.num_1 / self.num_2)))
                        else:
                            self.input.setText(str(self.num_1 / self.num_2))
                    except ZeroDivisionError:
                        self.input.setText('inf')
                elif self.op == "%":
                    try:
                        if (self.num_1 % self.num_2).is_integer():
                            self.input.setText(str(int(self.num_1 % self.num_2)))
                        else:
                            self.input.setText(str(self.num_1 % self.num_2))
                    except ZeroDivisionError:
                        self.input.setText('inf')
                elif self.op == "0":
                    self.input.setText(str(''))
                    self.num_1 = self.num_2 = 0


app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())

import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox, QGridLayout, QMainWindow)


class ConnectToDb():
    def __init__(self):
        self.conn = psycopg2.connect(database="mtuci_table",
                                     user="postgres",
                                     password="1234",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def connect(self):
        return self.conn


class Timetable(QTableWidget):
    def __init__(self, day, parent=None):
        super(QTableWidget, self).__init__(parent=parent)
        self.connect = ConnectToDb().connect()
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["id", "Неделя", "Предмет", "Кабинет", "Время", "", ""])
        self.day = day

    def get_rows(self) -> list:
        cursor = self.connect.cursor()
        cursor.execute("""SELECT
                                  timetable.id,
                                  timetable.week,
                                  subject.name AS subject_name,  
                                  timetable.room_numb, 
                                  timetable.start_time
                                FROM 
                                  timetable 
                                  INNER JOIN subject ON timetable.subject = subject.id 
                                  INNER JOIN teacher ON timetable.subject = teacher.subject
                                WHERE day=%s
                                ORDER BY timetable.start_time""", (self.day,))
        result = list(cursor.fetchall())
        return result

    def update_rows(self):
        rows = self.get_rows()
        if not rows:
            return

        self.setColumnCount(len(rows[0]))
        self.setRowCount(0)

        for row in rows:
            self.setRowCount(self.rowCount() + 1)
            rowPosition = self.rowCount()
            self.insertRow(rowPosition)
            for num_column in range(len(row)):
                self.setItem(rowPosition, num_column, QTableWidgetItem(str(row[num_column])))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_schedule_tab()

    def _create_schedule_tab(self):
        self.day_tables = {}
        group_box = QGroupBox("Расписание")
        tabs_widget = QTabWidget(group_box)

        layout = QGridLayout(group_box)
        layout.addWidget(tabs_widget)

        for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']:

            day_table = Timetable(day, tabs_widget)
            tabs_widget.addTab(day_table, day)
            self.tabs.setCurrentIndex(self.tabs.count() - 2)

            self.setCentralWidget(group_box)

            day_table.update_rows()

            layout = QGridLayout(group_box)
            layout.addWidget(tabs_widget)

            self.setCentralWidget(group_box)

            self.update_schedule_button = QPushButton("Update")
            # self.update_schedule_button.clicked.connect(self._update_schedule)

            self.add_row_button = QPushButton("Add")
            # self.shbox3.addWidget(self.add_row_button)
            # self.add_row_button.clicked.connect(self._add_row)


        self.tabs.setCurrentIndex(0)


    def _create_day_table(self):

        return self.day_table

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="mtuci_table",
                                     user="postgres",
                                     password="1234",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "subject")

        self.subject_gbox = QGroupBox("Table")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subject_gbox)

        self._create_subject_table()

        self.update_subject_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)



app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())

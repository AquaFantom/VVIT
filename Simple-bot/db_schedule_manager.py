import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_schedule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="mtuci_table",
                                     user="postgres",
                                     password="1234",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_schedule_tab(self):
        self.day_tables = {}
        for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']:
            self.schedule_tab = QWidget()
            self.tabs.addTab(self.schedule_tab, day)
            self.tabs.setCurrentIndex(self.tabs.count() - 2)
            self.day_gbox = QGroupBox("Расписание")

            self.svbox = QVBoxLayout()
            self.shbox1 = QHBoxLayout()
            self.shbox2 = QHBoxLayout()
            self.shbox3 = QHBoxLayout()

            self.svbox.addLayout(self.shbox1)
            self.svbox.addLayout(self.shbox2)
            self.svbox.addLayout(self.shbox3)

            self.shbox1.addWidget(self.day_gbox)

            self.day_tables[day] = self._create_day_table()

            self.update_schedule_button = QPushButton("Update")
            self.shbox2.addWidget(self.update_schedule_button)
            self.update_schedule_button.clicked.connect(self._update_schedule)

            self.add_row_button = QPushButton("Add")
            self.shbox3.addWidget(self.add_row_button)
            self.add_row_button.clicked.connect(self._add_row)

            self.schedule_tab.setLayout(self.svbox)
        self.tabs.setCurrentIndex(0)

    def _create_day_table(self):
        self.day_table = QTableWidget()
        self.day_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.day_table.setColumnCount(7)
        self.day_table.setHorizontalHeaderLabels(["id", "Неделя", "Предмет", "Кабинет", "Время", "", ""])

        self._update_day_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.day_table)
        self.day_gbox.setLayout(self.mvbox)
        return self.day_table

    def _update_day_table(self):

        day = self.tabs.tabText(self.tabs.currentIndex())
        self.cursor.execute("""SELECT
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
                                    ORDER BY timetable.start_time""", (day,))
        records = list(self.cursor.fetchall())
        if self.tabs.tabText(self.tabs.currentIndex()) in self.day_tables:
            self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setRowCount(0)
            self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setRowCount(len(records))

            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                deleteButton = QPushButton("Delete")
                for j in range(5):
                    self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setItem(i, j,
                                                                                         QTableWidgetItem(str(r[j])))
                self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setCellWidget(i, 5, joinButton)
                self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setCellWidget(i, 6, deleteButton)

                joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
                deleteButton.clicked.connect(lambda ch, num=i: self._delete_row(num))

            self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].resizeRowsToContents()
        else:
            self.day_table.setRowCount(len(records))

            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                deleteButton = QPushButton("Delete")

                for j in range(5):
                    self.day_table.setItem(i, j,
                                           QTableWidgetItem(str(r[j])))
                self.day_table.setCellWidget(i, 5, joinButton)
                self.day_table.setCellWidget(i, 6, deleteButton)

                joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
                deleteButton.clicked.connect(lambda ch, num=i: self._delete_row(num))

            self.day_table.resizeRowsToContents()

    def _change_day_from_table(self, rowNum):
        row = list()
        for i in range(self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].columnCount() - 1):
            try:
                row.append(self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].item(rowNum, i).text())
            except:
                row.append(None)
        try:
            if row[0] is None:
                self.cursor.execute(
                    "INSERT INTO timetable (week, day, subject, room_numb, start_time) VALUES (%s, %s, (SELECT id FROM subject WHERE name = %s), %s, %s)",
                    (row[1], self.tabs.tabText(self.tabs.currentIndex()), row[2], row[3], row[4]))
            else:
                self.cursor.execute(
                    "UPDATE timetable SET week = %s, subject = (SELECT id FROM subject WHERE name = %s), room_numb = %s,"
                    " start_time = %s WHERE id = %s",
                    (row[1], row[2], row[3], row[4], row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_row(self, rowNum):
        try:
            self.cursor.execute("DELETE FROM timetable WHERE id = %s",
                                (self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].item(rowNum, 0).text(),))
            self.conn.commit()
            self._update_day_table()
        except:
            QMessageBox.about(self, "Error", "Unable to delete")

    def _add_row(self):
        row_len = self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].rowCount()
        self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setRowCount(row_len + 1)
        joinButton = QPushButton("Join")
        deleteButton = QPushButton("Delete")
        self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setCellWidget(row_len, 5, joinButton)
        self.day_tables[self.tabs.tabText(self.tabs.currentIndex())].setCellWidget(row_len, 6, deleteButton)
        joinButton.clicked.connect(lambda ch, num=row_len: self._change_day_from_table(num))
        deleteButton.clicked.connect(lambda ch, num=row_len: self._delete_row(num))

    def _update_schedule(self):
        self._update_day_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())

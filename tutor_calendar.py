import calendar
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore

# The list of tutors and their availability
tutors = [
    {
        "name": "Alice",
        "availability": [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 29, 30, 31]
    },
    {
        "name": "Bob",
        "availability": [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30, 31]
    },
    {
        "name": "Charlie",
        "availability": [4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29]
    }
]

class CalendarWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.setWindowTitle("Tutor Calendar")
        self.setGeometry(100, 100, 500, 500)

        # Create the calendar widget
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendar.currentPageChanged.connect(self.update_display)
        self.calendar.setStyleSheet("font-size: 20px;")

        # Create the tutor list widget
        self.tutor_list = QtWidgets.QListWidget(self)
        self.tutor_list.setFixedWidth(200)
        self.tutor_list.itemClicked.connect(self.update_display)
        for tutor in tutors:
            self.tutor_list.addItem(tutor["name"])
        self.tutor_list.setCurrentRow(0)

        # Create the text area
        self.text_area = QtWidgets.QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("font-size: 20px;")

        # Add the widgets to the layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(self.tutor_list)
        layout.addWidget(self.text_area)

        # Update the display
        self.update_display()

    def update_display(self):
        # Get the selected month and year
        month = self.calendar.monthShown()
        year = self.calendar.yearShown()

        # Get the selected tutor
        tutor_name = self.tutor_list.currentItem().text()
        tutor = next(tutor for tutor in tutors if tutor["name"] == tutor_name)

        # Get the calendar for the selected month
        cal = calendar.monthcalendar(year, month)

        # Build the calendar display
        display = f"Calendar for {calendar.month_name[month]} {year}\n"
        display += "-----------------------------\n"
        display += "  Mo Tu We Th Fr Sa Su\n"
        now = datetime.now()
        for week in cal:
            line = ""
            for day in week:
                if day == 0:
                    # If the day is 0, it means it's a blank space in the calendar
                    line += "   "
                else:
                    # If the day is not 0, it means it's a real day
                    # Check if the day is in the past or the present
                    if datetime(year, month, day) < now:
                        # If the day is in the past, gray it out
                        line += f"\033[90m{day:2d}\033[0m "
                    elif now.day == day and now.month == month and now.year == year:
                        # If the day is today, highlight it in red
                        line += f"\033[91m{day:2d}\033[0m "
                    else:
                        # If the day is in the future, leave it as normal
                        line += f"{day:2d} "
            # Print the line with the dates for the week
            display += line + "\n"

        # Build the availability display
        display += "\nAvailability:\n"
        for week in cal:
            line = ""
            for day in week:
                if day == 0:
                    # If the day is 0, it means it's a blank space in the calendar
                    line += "  "
                else:
                    # If the day is not 0, it means it's a real day
                    if day in tutor["availability"]:
                        # If the tutor is available on this day, print an "X"
                        line += "X "
                    else:
                        # If the tutor is not available on this day, print a blank space
                        line += "  "
            # Print the line with the availability for the week
            display += line + "\n"

        # Update the text area
        self.text_area.setText(display)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    calendar = CalendarWidget()
    calendar.show()
    app.exec_()

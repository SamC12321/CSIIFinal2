import csv

from PyQt6.QtCore import Qt

from gui import *
from PyQt6.QtWidgets import *
from patients import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Initializes Logic Class. Initializes window and gui.
        """
        super().__init__()
        self.setupUi(self)
        self.frame_dropdownConfirm.hide()
        self.setUpDropDowns()
        self.hideBookedSlots()
        self.frame_appointmentInfo.hide()

        self.__calendar = self.setUpCalendarDict()
        self.setUpCalendarUI(self.__calendar)

        self.pushButton_addPatient.clicked.connect(lambda : self.addPatient())
        self.pushButton_ADDBack.clicked.connect(lambda : self.goToHome())
        self.pushButton_newBooking.clicked.connect(lambda : self.newBooking())
        self.pushButton_confirm.clicked.connect(lambda : self.confirm())
        self.pushButton_ADDAddPatient.clicked.connect(lambda : self.ADDaddPatient())
        self.pushButton_ok.clicked.connect(lambda : self.okButtonClicked())
        self.pushButton_cancelAppointment.clicked.connect(lambda: self.cancelAppointment())
        self.connectPatientButtons()



    def addPatient(self) -> None:
        """
        Called when Add Patient button is clicked. Changes Stacked Widget to Add Patient Page.
        :return: None
        """
        self.stackedWidget.setCurrentIndex(0)
        self.lineEdit_ADDFirstName.clear()
        self.lineEdit_ADDFirstName.setFocus()
        self.lineEdit_ADDLastName.clear()
        self.lineEdit_ADDAge.clear()
        self.textEdit_ADDNotes.clear()
        self.label_firstNameError.hide()
        self.label_lastNameError.hide()
        self.label_ageError.hide()


    def goToHome(self) -> None:
        """
        Changes Stacked Widget to Home Page.
        :return: None
        """
        self.stackedWidget.setCurrentIndex(1)
        self.pushButton_addPatient.clearFocus()


    def newBooking(self) -> None:
        """
        Opens new booking widget.
        :return: None
        """
        self.frame_dropdownConfirm.show()
        self.label_timeSlotFull.hide()


    def confirm(self) -> None:
        """
        Called when confirm button is clicked. Creates a new appointment booking. Updates Calendar.
        :return: None
        """
        id = str(self.comboBox_patients.currentData())
        time = self.comboBox_times.currentText()
        time = time.split(":")[0]
        if len(self.__calendar[time]) < 7 or id in self.__calendar[time]:
            patient = self.createPatientObject(id)
            try:
                patient.setAppointment(time)
            except AttributeError:
                pass
            self.updateCSV(id, patient)
            self.updateCalendarGUI()
            self.label_timeSlotFull.hide()
        else:
            self.label_timeSlotFull.show()
            self.label_timeSlotFull.setText(f'{time}:00 is Full')



    def ADDaddPatient(self) -> None:
        """
        Creates a new patient.
        :return: None
        """
        first_name, last_name, age, id, time_booked, notes = self.checkInputs()
        if first_name != False and last_name != False and age != False:
            new_patient = Patient(first_name, last_name, age, id, time_booked, notes)
            self.addPatientToCSV(new_patient)
            self.updatePatientDropDown(first_name, last_name, id)
            self.stackedWidget.setCurrentIndex(1)


    def updatePatientDropDown(self, first_name: str, last_name: str, id: str) -> None:
        """
        Updates patient drop down after adding a new patient.
        :param first_name:Patient's first name
        :param last_name: Patient's last name
        :param id: Patient's ID
        :return: None
        """
        name = first_name + " " + last_name
        self.comboBox_patients.addItem(name, id)


    def setUpDropDowns(self) -> None:
        """
        Sets up the patient drop down.
        :return: None
        """
        self.comboBox_times.addItems(
            ["9:00", "10:00", "11:00", "12:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00"])
        with open('patients.csv') as file:
            row_count = 0
            for row in csv.reader(file):
                if row_count == 0:
                    row_count += 1
                    continue
                else:
                    try:
                        self.comboBox_patients.addItem(f'{row[0]} {row[1]}', f'{row[3]}')
                    except IndexError:
                        break


    def generateID(self) -> int:
        """
        Generates a new patient ID.
        :return: Patient ID
        """
        with open('patients.csv') as file:
            reader = csv.reader(file)
            num_rows = -1
            for row in reader:
                num_rows += 1
        return num_rows


    def setUpCalendarDict(self) -> dict:
        """
        Sets up the calendar dictionary.
        :return: The calendar dictionary.
        """
        calendarDict = {'9': [], '10': [], '11': [], '12': [], '1': [], '2': [], '3': [],
                        '4': [], '5': [], '6': []}
        with open('patients.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    if row[4] != None and row[4] != "time_booked" and row[4] != "":
                        calendarDict[f'{row[4]}'].append(f'{row[3]}')
                except IndexError:
                    pass
        return calendarDict


    def hideBookedSlots(self) -> None:
        """
        Hides booked slots.
        :return: None
        """
        row_num = 8
        for row in range(0, 10):
            if row_num < 12:
                row_num += 1
            elif row_num == 12:
                row_num = 1
            for column in range(0,7):
                frame = getattr(self, f"frame_{row_num}_{column}")
                frame.hide()


    def setUpCalendarUI(self, dict: dict) -> None:
        """
        Sets up the calendar UI.
        :param dict: Calendar dictionary.
        :return: None
        """
        for key in dict:
            if len(dict[key]) > 0:
                len_index = 0
                for value in range(len(dict[key])):
                    frame = getattr(self, f"frame_{key}_{len_index}")
                    frame.show()
                    patient = self.createPatientObject(dict[key][len_index])
                    button = getattr(self, f"pushButton_{key}_{len_index}")
                    button.setText(f"{patient.getFirstName()} {patient.getLastName()}")
                    button.setProperty('patient_id', f'{patient.getID()}')
                    len_index += 1


    def createPatientObject(self, patient_id: str) -> Patient | None:
        """
        Creates a patient object.
        :param patient_id: Patient ID
        :return: Patient object
        """
        with open('patients.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[3] == patient_id:
                    patient = Patient(row[0], row[1], row[2], row[3], row[4], row[5])
                    return patient


    def patientInfo(self, patient_id: str) -> None:
        """
        Open's booked appointment information widget.
        :param patient_id: Patient ID
        :return: None
        """
        patient = self.createPatientObject(patient_id)
        self.frame_dropdownConfirm.hide()
        self.frame_appointmentInfo.show()
        self.frame_appointmentInfo.setProperty('patient_id', patient_id)
        self.label_patientNameAutoUpdate.setText(f'{patient.getFirstName()} {patient.getLastName()}')
        self.label_patientAgeAutoUpdate.setText(f'{patient.getAge()}')
        self.label_patientAppointmentTimeAutoUpdate.setText(f'{patient.getTimeBooked()}:00')
        self.textEdit_notes.setPlainText(f'{patient.getNotes()}')



    def connectPatientButtons(self) -> None:
        """
        Sets up event driven connect to the appointment widgets.
        :return: None
        """
        row_num = 8
        for row in range(0, 10):
            if row_num < 12:
                row_num += 1
            elif row_num == 12:
                row_num = 1
            for column in range(0, 7):
                button = getattr(self, f"pushButton_{row_num}_{column}", None)
                if button is not None:
                    button.clicked.connect(lambda: self.patientButtonClicked())


    def patientButtonClicked(self) -> None:
        """
        Called when an appointment button is clicked. Calls patientInfo function to open appointment info widget.
        :return: None
        """
        button = self.sender()
        id = button.property("patient_id")
        self.patientInfo(id)


    def okButtonClicked(self) -> None:
        """
        Called when ok button is clicked. Updates notes and hides appointment info widget.
        :return: None
        """
        self.updateNotes()
        self.frame_appointmentInfo.hide()


    def cancelAppointment(self) -> None:
        """
        Cancels appointment associated with a patient.
        :return: None
        """
        id = self.frame_appointmentInfo.property('patient_id')
        patient = self.createPatientObject(id)
        patient.setAppointment(None)
        self.updateCSV(id, patient)
        self.updateCalendarGUI()
        self.frame_appointmentInfo.hide()
        self.__calendar = self.setUpCalendarDict()

    def updateCSV(self, id: str, patient: Patient) -> None:
        """
        Updates the CSV file.
        :param id: Patient ID
        :param patient: Patient object
        :return: None
        """
        rows = []

        with open('patients.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[3] == id:
                    row[0] = patient.getFirstName()
                    row[1] = patient.getLastName()
                    row[2] = patient.getAge()
                    row[4] = patient.getTimeBooked()
                    row[5] = patient.getNotes()

                rows.append(row)

        with open('patients.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def updateNotes(self) -> None:
        """
        Updates the notes associated with a patient.
        :return: None
        """
        id = self.frame_appointmentInfo.property('patient_id')
        patient = self.createPatientObject(id)
        patient.setNotes(self.textEdit_notes.toPlainText())
        self.updateCSV(id, patient)


    def updateCalendarGUI(self) -> None:
        """
        Updates the calendar gui.
        :return: None
        """
        self.hideBookedSlots()
        self.__calendar = self.setUpCalendarDict()
        self.setUpCalendarUI(self.__calendar)


    def addPatientToCSV(self, patient: Patient) -> None:
        """
        Adds a patient to the CSV file.
        :param patient: Patient object
        :return: None
        """
        with open('patients.csv', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([patient.getFirstName(), patient.getLastName(), patient.getAge(), patient.getID(), patient.getTimeBooked(), patient.getNotes()])


    def checkInputs(self) -> tuple:
        """
        Checks that input info for new patient is valid.
        :return: Tuple of Person Object Properties
        """
        if self.lineEdit_ADDFirstName.text().isalpha():
            first_name = self.lineEdit_ADDFirstName.text().strip()
            self.label_firstNameError.hide()
        else:
            first_name = False
            self.label_firstNameError.show()
        if self.lineEdit_ADDLastName.text().isalpha():
            last_name = self.lineEdit_ADDLastName.text().strip()
            self.label_lastNameError.hide()
        else:
            last_name = False
            self.label_lastNameError.show()
        try:
            age = int(self.lineEdit_ADDAge.text().strip())
            self.label_ageError.hide()
            if age < 0 or age > 125:
                raise ValueError
        except ValueError:
            age = False
            self.label_ageError.show()


        id = self.generateID()
        time_booked = None
        notes = self.textEdit_ADDNotes.toPlainText()

        return first_name, last_name, age, id, time_booked, notes
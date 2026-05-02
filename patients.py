class Patient:
    def __init__(self, first_name: str, last_name: str, age: str, id:str, time_booked: str | None = None, notes: str = "") -> None:
        """
        Initialize a patient object
        :param first_name: Patient first name
        :param last_name: Patient last name
        :param age: Patient age
        :param id: Patient ID
        :param time_booked: Appointment booked time
        :param notes: Patient notes
        """
        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = age
        self.__id = id
        self.__time_booked = time_booked
        self.__notes = notes

    def getFirstName(self) -> str:
        """
        Returns the patient's first name
        """
        return self.__first_name


    def getLastName(self) -> str:
        """
        Returns the patient's last name
        """
        return self.__last_name


    def getAge(self) -> str:
        """
        Returns the patient's age
        """
        return self.__age


    def getID(self) -> str:
        """
        Returns the patient's ID
        """
        return self.__id


    def getNotes(self) -> str:
        """
        Returns the notes associated with the patient
        """
        return self.__notes


    def getTimeBooked(self) -> str | None:
        """
        Returns the patient's booked appointment time
        """
        return self.__time_booked

    def setAppointment(self, time: str | None) -> None:
        """
        Sets the patient's booked appointment time
        :param time: Appointment time
        """
        self.__time_booked = time



    def setNotes(self, new_notes: str) -> None:
        """
        Sets the notes associated with a patient
        """
        self.__notes = new_notes


    def __str__(self) -> str:
        return f'{self.getFirstName()}'
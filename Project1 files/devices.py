class Device:
    def __init__(self, name, propagate=None, alert=None, cancel=None, coming_alert=None, coming_cancel=None):
        """
        Class for device objects, with each object representing different device.
        name = its ID
        propagate = Dictionary containing ID to propagate as keys, delay as values. Default = None
        alert = Dictionary containing description of alert as keys, time as values. Default = None
        cancel = Dictionary containing description of cancel as keys, time as values. Default = None
        coming_alert = List containing description of coming alert. Default = None
        coming_cancel = List containing description of coming cancel. Default = None
        """
        self.name = name
        self.propagate = propagate
        self.alert = alert
        self.cancel = cancel
        self.coming_alert = coming_alert
        self.coming_cancel = coming_cancel

    def __eq__(self, another) -> bool:
        """
        Define a method to check if two Device objects are equal to each other.
        If "another" is Device object and has all attributes equal to self, return True.
        Otherwise, return False.
        """
        if type(another) == Device:
            if (self.name == another.name) and (self.propagate == another.propagate) and (self.alert == another.alert) and (self.cancel == another.cancel) and (self.coming_alert == another.coming_alert) and (self.coming_cancel == another.coming_cancel):
                return True
        return False

    def add_prop(self, ID, delay):
        """
        Take in two parameters: ID of Device to propagate, delay it takes to propagate.
        Store the info in dictionary: ID as key, delay as value.
        """
        if type(self.propagate) != dict:
            self.propagate = {}

        self.propagate[ID] = int(delay)

    def add_alert(self, desc, time):
        """
        Take in two parameters: description of alert, when the alert will go off.
        Store the info in dictionary: description as key, time as value.
        """
        if type(self.alert) != dict:
            self.alert = {}

        self.alert[desc] = int(time)

    def add_cancel(self, desc, time):
        """
        Take in two parameters: description of cancel, when the cancel will go off.
        Store the info in dictionary: description as key, time as value.
        """
        if type(self.cancel) != dict:
            self.cancel = {}

        self.cancel[desc] = int(time)

    def add_coming_alert(self, sender, desc, time):
        """
        Take in three parameters: ID of Device that sent the alert, description of alert,
            when the alert will arrive.
        Store as list, with each element being list of [ID, Desc, time]
        """
        if type(self.coming_alert) != list:
            self.coming_alert = []

        self.coming_alert.append([sender, desc, int(time)])

    def add_coming_cancel(self, sender, desc, time):
        """
        Take in three parameters: ID of Device that sent the cancel, description of cancel,
            when the cancel will arrive.
        Store as list, with each element being list of [ID, Desc, time]
        """
        if type(self.coming_cancel) != list:
            self.coming_cancel = []

        self.coming_cancel.append([sender, desc, int(time)])

    def is_canceled(self, desc) -> bool:
        """
        Check if the description is canceled already.
        Parameter: description of alert or cancel to check if it's already canceled.
        Return True if there exists a cancel with same key as description, False if not.
        """
        if (type(self.cancel) == dict) and (desc in self.cancel.keys()):
            return True
        else:
            return False

    def get_schedule(self) -> list:
        """
        Return list of times the device will act.
        """
        schedule = []
        if self.coming_alert is not None:
            for alerts in self.coming_alert:
                schedule.append(alerts[2])
        if self.coming_cancel is not None:
            for cancels in self.coming_cancel:
                schedule.append(cancels[2])
        return schedule
from devices import Device

class Simulation:
    def __init__(self, length: int, devices=None, schedule=None):
        """
        Class for Simulation objects.
        Length = Nanoseconds the simulation will run.
        Devices = List of Device objects. Default = None
        Schedule = List of times when events should occur. Default = None
        """
        self.length = length
        self.devices = devices
        self.schedule = schedule

    def __eq__(self, other):
        """
        Define a method to check if two Simulation objects are equal to each other.
        If "other" is Simulation object and has all attributes equal to self, return True.
        Otherwise, return False.
        """
        if type(other) == Simulation:
            if (self.length == other.length) and (self.devices == other.devices) and (self.schedule == other.schedule):
                return True
        return False

    def add_device(self, device: Device):
        """
        Adds Device object to list of devices.
        """
        if type(self.devices) != list:
            self.devices = []

        self.devices.append(device)

    def add_schedule(self, time: int):
        """
        If the input time is not in schedule, add the time to it.
        After a time is added, the list is sorted.
        """
        if type(self.schedule) != list:
            self.schedule = []

        if time not in self.schedule:
            self.schedule.append(time)

        self.schedule.sort()
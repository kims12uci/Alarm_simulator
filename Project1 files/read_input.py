from devices import Device
from simulObject import Simulation

def readContent(inputFile) -> list:
    """
    Read the input file and return relevant info.
    Takes in file object as input, return a list with each element being a list of
        the relevant line's info, split by spaces.
    The returned list's each element's o index specifies what the line is about.
    Relevant info = lines that start with LENGTH, DEVICE, PROPAGATE, ALERT or CANCEL.
    """
    lines = inputFile.readlines()
    content = []
    for line in lines:
        if len(line) >= 5:
            cut = line.split()
            if (cut[0] == 'DEVICE') or (cut[0] == 'LENGTH') or (cut[0] == 'PROPAGATE') or (cut[0] == 'ALERT') or (cut[0] == 'CANCEL'):
                single_line_content = []
                for elem in cut:
                    single_line_content.append(elem)
                content.append(single_line_content)

    return content

def interpret_content(content) -> Simulation:
    """
    Take in the relevant info processed by readContent function.
    First, create simulation object looking for LENGTH specification.
    Second, create device objects looking for DEVICE instruction, adding them to
        the simulation object.
    Then, according to other three instruction, edit each device object's info.
    Return the created simulation object.
    """
    simul = None
    for line in content:
        if line[0] == 'LENGTH':
            simul = Simulation(int(line[1]))

    for line in content:
        if line[0] == 'DEVICE':
            simul.add_device(Device(int(line[1])))

    for line in content:
        if line[0] == 'PROPAGATE':
            for devices in simul.devices:
                if int(line[1]) == devices.name:
                    devices.add_prop(int(line[2]), int(line[3]))
        if line[0] == 'ALERT':
            for devices in simul.devices:
                if int(line[1]) == devices.name:
                    devices.add_coming_alert(None, line[2], int(line[3]))
        if line[0] == 'CANCEL':
            for devices in simul.devices:
                if int(line[1]) == devices.name:
                    devices.add_coming_cancel(None, line[2], int(line[3]))
    return simul
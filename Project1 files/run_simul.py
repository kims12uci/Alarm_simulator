from simulObject import Simulation
from devices import Device

def start(sim: Simulation):
    """
    Initialize schedule of Simulation object.
    Calls on run function to run the simulation.
    """
    sim.add_schedule(sim.length)
    for dev in sim.devices:
        for times in dev.get_schedule():
            sim.add_schedule(times)
    run(sim)

def run(sim: Simulation):
    """
    Take in the Simulation object and run simulation.
    Main purpose: keep track of current time, change time,
        and calls other functions that should be triggered according to current time.
    """
    current_time = 0
    running = True

    while running:
        if current_time == sim.length:
            print(f'@{current_time}: END')
            running = False
        if running:
            for dev in sim.devices:
                receive_alert(dev, current_time)
                send_alert(sim, dev, current_time)

            for dev in sim.devices:
                receive_cancel(dev, current_time)
                send_cancel(sim, dev, current_time)

            if current_time == sim.schedule[0]:
                sim.schedule.remove(current_time)

            current_time = sim.schedule[0]
            sim.schedule.remove(current_time)

def receive_alert(dev: Device, current_time: int):
    """
    For each coming alerts of the input Device object, if it's time to receive the alert,
        receive it and add the alert to Device object's alerts.
    Also remove coming alerts after dealing with them.
    """
    if dev.coming_alert is not None:
        for comings in dev.coming_alert[:]:
            if comings[2] == current_time:
                if comings[0] is not None:
                    print(f'@{current_time}: #{dev.name} RECEIVED ALERT FROM #{comings[0]}: {comings[1]}')
                dev.add_alert(comings[1], current_time)
                dev.coming_alert.remove(comings)

def send_alert(sim: Simulation, dev: Device, current_time: int):
    """
    For each alert in the input Device object, if it's time for the alert to go off,
        check if the alert is canceled, send not canceled alerts to other Devices designated,
        and update schedule of the Simulation object.
    """
    if dev.propagate is not None:
        if dev.alert is not None:
            for device in sim.devices:
                if device.name in list(dev.propagate.keys()):
                    for alerts in list(dev.alert.items()):
                        if alerts[1] == current_time:
                            alert_desc = alerts[0]
                            alert_time = alerts[1] + dev.propagate[device.name]
                            if not dev.is_canceled(alert_desc):
                                device.add_coming_alert(dev.name, alert_desc, alert_time)
                                print(f'@{current_time}: #{dev.name} SENT ALERT TO #{device.name}: {alert_desc}')
                                sim.add_schedule(alert_time)

def receive_cancel(dev: Device, current_time: int):
    """
    For each coming cancels of the input Device object, if it's time to receive the cancel,
        receive it and add the cancel to Device object's cancels if the Device object has not
        received the same cancel.
    Also remove coming cancels after dealing with them.
    """
    if dev.coming_cancel is not None:
        for comings in dev.coming_cancel[:]:
            if comings[2] == current_time:
                if comings[0] is not None:
                    print(f'@{current_time}: #{dev.name} RECEIVED CANCELLATION FROM #{comings[0]}: {comings[1]}')
                if not dev.is_canceled(comings[1]):
                    dev.add_cancel(comings[1], current_time)
                dev.coming_cancel.remove(comings)

def send_cancel(sim: Simulation, dev: Device, current_time: int):
    """
    For each cancel in the input Device object, if it's time for the cancel to go off,
        send not cancels to other Devices designated,
        and update schedule of the Simulation object.
    """
    if dev.propagate is not None:
        if dev.cancel is not None:
            for device in sim.devices:
                if device.name in list(dev.propagate.keys()):
                    for cancels in list(dev.cancel.items()):
                        if cancels[1] == current_time:
                            cancel_desc = cancels[0]
                            cancel_time = cancels[1] + dev.propagate[device.name]
                            print(f'@{current_time}: #{dev.name} SENT CANCELLATION TO #{device.name}: {cancel_desc}')
                            device.add_coming_cancel(dev.name, cancel_desc, cancel_time)
                            sim.add_schedule(cancel_time)
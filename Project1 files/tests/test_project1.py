import unittest
from project1 import main
from devices import Device
from simulObject import Simulation
from read_input import readContent, interpret_content
from run_simul import start, run, receive_alert, receive_cancel, send_alert, send_cancel
import contextlib
import io
from pathlib import Path

class TestProject1Main(unittest.TestCase):
    def test_main_no_file_found(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            main(testPath='someRandomPath')
            self.assertEqual(output.getvalue(), 'FILE NOT FOUND\n')

    def test_main_input_file_case(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            main(testPath = Path('C:\\Users\\qkzmf\\Downloads\\UCI Courses\\ICS33\\Project1 files\\samples\\sample_input.txt'))
            self.assertEqual(output.getvalue(), '@0: #1 SENT ALERT TO #2: Trouble\n@750: #2 RECEIVED ALERT FROM #1: Trouble\n@750: #2 SENT ALERT TO #3: Trouble\n@2000: #3 RECEIVED ALERT FROM #2: Trouble\n@2000: #3 SENT ALERT TO #4: Trouble\n@2200: #1 SENT CANCELLATION TO #2: Trouble\n@2500: #4 RECEIVED ALERT FROM #3: Trouble\n@2500: #4 SENT ALERT TO #1: Trouble\n@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble\n@2950: #2 SENT CANCELLATION TO #3: Trouble\n@3500: #1 RECEIVED ALERT FROM #4: Trouble\n@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble\n@4200: #3 SENT CANCELLATION TO #4: Trouble\n@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble\n@4700: #4 SENT CANCELLATION TO #1: Trouble\n@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble\n@9999: END\n')

class testDevices(unittest.TestCase):
    def test_equality_equal_case(self):
        d1 = Device(1, {2: 5000}, {'Nyo': 200}, {'Nyo': 500})
        d2 = Device(1, {2: 5000}, {'Nyo': 200}, {'Nyo': 500})
        self.assertEqual(d1, d2)

    def test_equality_different_case(self):
        d1 = Device(1, {2: 5000}, {'Nyo': 200}, {'Nyo': 500})
        d2 = Device(2, {2: 5000}, {'Nyo': 200}, {'Nyo': 500})
        self.assertNotEqual(d1, d2)

    def test_equality_different_case_not_Device(self):
        d1 = Device(1, {2: 5000}, {'Nyo': 200}, {'Nyo': 500})
        d2 = 10
        self.assertNotEqual(d1, d2)

    def test_addProp_normal(self):
        device = Device(1)
        device.add_prop(2, 1000)
        device2 = Device(1, {2: 1000})
        self.assertEqual(device.propagate, device2.propagate)

    def test_addProp_normal_multiple_calls(self):
        device = Device(1)
        device.add_prop(2, 1000)
        device.add_prop(3, 2000)
        device.add_prop(4, 1000)
        device2 = Device(1, {2: 1000, 3: 2000, 4: 1000})
        self.assertEqual(device.propagate, device2.propagate)

    def test_add_alert_normal(self):
        device = Device(1)
        device.add_alert('Ohno', 5000)
        device2 = Device(1, alert={'Ohno':5000})
        self.assertEqual(device.alert, device2.alert)

    def test_add_alert_normal_multiple_calls(self):
        device = Device(1)
        device.add_alert('Ohno', 5000)
        device.add_alert('Nono', 3000)
        device.add_alert('No?', 600)
        device2 = Device(1, alert = {'Ohno': 5000, 'Nono': 3000, 'No?':600})
        self.assertEqual(device.alert, device2.alert)

    def test_add_cancel_normal(self):
        device = Device(1)
        device.add_cancel('Ohno', 5000)
        device2 = Device(1, cancel = {'Ohno': 5000})
        self.assertEqual(device.cancel, device2.cancel)

    def test_add_cancel_normal_multiple_calls(self):
        device = Device(1)
        device.add_cancel('Ohno', 5000)
        device.add_cancel('Nono', 3000)
        device.add_cancel('No?', 600)
        device2 = Device(1, cancel = {'Ohno': 5000, 'Nono': 3000, 'No?':600})
        self.assertEqual(device.cancel, device2.cancel)

    def test_add_coming_alert_normal(self):
        d = Device(1)
        d.add_coming_alert(2, 'Nyo', 3000)
        d2 = Device(1, coming_alert = [[2, 'Nyo', 3000]])
        self.assertEqual(d.coming_alert, d2.coming_alert)

    def test_add_coming_alert_normal_multiple_calls(self):
        d = Device(1)
        d.add_coming_alert(2, 'Nyo', 3000)
        d.add_coming_alert(3, 'Hi', 2000)
        d.add_coming_alert(4, 'Yeah', 2000)
        d2 = Device(1, coming_alert = [[2, 'Nyo', 3000], [3, 'Hi', 2000], [4, 'Yeah', 2000]])
        self.assertEqual(d.coming_alert, d2.coming_alert)

    def test_add_coming_cancel_normal(self):
        d = Device(1)
        d.add_coming_cancel(2, 'Nyo', 3000)
        d2 = Device(1, coming_cancel = [[2, 'Nyo', 3000]])
        self.assertEqual(d.coming_cancel, d2.coming_cancel)

    def test_add_coming_cancel_normal_multiple_calls(self):
        d = Device(1)
        d.add_coming_cancel(2, 'Nyo', 3000)
        d.add_coming_cancel(3, 'Hi', 2000)
        d.add_coming_cancel(4, 'Yeah', 2000)
        d2 = Device(1, coming_cancel = [[2, 'Nyo', 3000], [3, 'Hi', 2000], [4, 'Yeah', 2000]])
        self.assertEqual(d.coming_cancel, d2.coming_cancel)

    def test_is_canceled_True_case(self):
        device = Device(1, cancel = {'Ohno':5000})
        self.assertEqual(device.is_canceled('Ohno'), True)

    def test_is_canceled_False_case(self):
        device = Device(1)
        self.assertEqual(device.is_canceled('Ohno'), False)

    def test_get_schedule_all_None_case(self):
        d = Device(1)
        self.assertEqual(d.get_schedule(), [])

    def test_get_schedule_alert_only_case(self):
        d = Device(1, coming_alert=[[None, 'Nyo', 2000], [1, 'Nope', 1300], [2, 'No', 2400]])
        self.assertEqual(d.get_schedule(), [2000, 1300, 2400])

    def test_get_schedule_cancel_only_case(self):
        d = Device(1, coming_cancel=[[None, 'Nyo', 2000], [1, 'Nope', 1300], [2, 'No', 2400]])
        self.assertEqual(d.get_schedule(), [2000, 1300, 2400])

    def test_get_schedule_alert_and_cancel_case(self):
        d = Device(1, coming_alert=[[None, 'Nyo', 2000], [1, 'Nope', 1300]], coming_cancel=[[1, 'Nope', 1300], [2, 'No', 2400]])
        self.assertEqual(d.get_schedule(), [2000, 1300, 1300, 2400])

class testSimulclass(unittest.TestCase):
    def test_equality_True(self):
        s = Simulation(3000, [Device(1), Device(2), Device(3)], [2000, 3000])
        s2 = Simulation(3000, [Device(1), Device(2), Device(3)], [2000, 3000])
        self.assertEqual(s, s2)

    def test_equality_False(self):
        s = Simulation(3000, [Device(1), Device(2), Device(3)], [2000, 3000])
        s2 = Simulation(3000, [Device(1), Device(2), Device(4)], [2000, 3000])
        self.assertNotEqual(s, s2)

    def test_quality_False_not_Simulation(self):
        s = Simulation(3000, [Device(1), Device(2), Device(3)], [2000, 3000])
        s2 = 1
        self.assertNotEqual(s, s2)

    def test_add_device_normal(self):
        s = Simulation(3000)
        device = Device(1)
        s.add_device(device)
        s2 = Simulation(3000, [device])
        self.assertEqual(s.devices, s2.devices)

    def test_add_device_normal_multiple_calls(self):
        s = Simulation(3000)
        device = Device(1)
        device2 = Device(2)
        s.add_device(device)
        s.add_device(device2)
        s2 = Simulation(3000, [device, device2])
        self.assertEqual(s.devices, s2.devices)

    def test_add_schedule_normal(self):
        s = Simulation(3000)
        s.add_schedule(2000)
        s2 = Simulation(3000, schedule=[2000])
        self.assertEqual(s.schedule, s2.schedule)

    def test_add_schedule_normal_multiple_call(self):
        s = Simulation(3000)
        s.add_schedule(2000)
        s.add_schedule(2500)
        s.add_schedule(2700)
        s2 = Simulation(3000, schedule = [2000, 2500, 2700])
        self.assertEqual(s.schedule, s2.schedule)

    def test_add_schedule_mixed_order(self):
        s = Simulation(3000)
        s.add_schedule(2700)
        s.add_schedule(2000)
        s.add_schedule(2500)
        s2 = Simulation(3000, schedule = [2000, 2500, 2700])
        self.assertEqual(s.schedule, s2.schedule)

    def test_add_schedule_multiple_same_time(self):
        s = Simulation(3000)
        s.add_schedule(2700)
        s.add_schedule(2700)
        s.add_schedule(2500)
        s2 = Simulation(3000, schedule = [2500, 2700])
        self.assertEqual(s.schedule, s2.schedule)

class testReadInput(unittest.TestCase):
    def test_readContent_sample_file(self):
        path = Path('C:\\Users\\qkzmf\\Downloads\\UCI Courses\\ICS33\\Project1 files\\samples\\sample_input.txt')
        with open(path, 'r') as file:
            content = readContent(file)
        self.assertEqual(content, [['LENGTH', '9999'], ['DEVICE', '1'], ['DEVICE', '2'], ['DEVICE', '3'], ['DEVICE', '4'], ['PROPAGATE', '1', '2', '750'], ['PROPAGATE', '2', '3', '1250'], ['PROPAGATE', '3', '4', '500'], ['PROPAGATE', '4', '1', '1000'], ['ALERT', '1', 'Trouble', '0'], ['CANCEL', '1', 'Trouble', '2200']])

    def test_interpret_content_LENGTH_only(self):
        content = [['LENGTH', '9999']]
        s = interpret_content(content)
        s2 = Simulation(9999)
        self.assertEqual(s.length, s2.length)

    def test_interpret_content_LENGTH_and_DEVICE(self):
        content = [['LENGTH', '9999'], ['DEVICE', '1'], ['DEVICE', '2'], ['DEVICE', '3'], ['DEVICE', '4']]
        s = interpret_content(content)
        s2 = Simulation(9999, [Device(1), Device(2), Device(3), Device(4)])
        self.assertEqual(s, s2)

    def test_interpret_content_LENGTH_DEVICE_and_PROPAGATE(self):
        content = [['LENGTH', '9999'], ['DEVICE', '1'], ['DEVICE', '2'], ['DEVICE', '3'], ['DEVICE', '4'], ['PROPAGATE', '1', '2', '750'], ['PROPAGATE', '2', '3', '1250'], ['PROPAGATE', '3', '4', '500'], ['PROPAGATE', '4', '1', '1000']]
        s = interpret_content(content)
        s2 = Simulation(9999, [Device(1, {2:750}), Device(2, {3:1250}), Device(3, {4:500}), Device(4, {1:1000})])
        self.assertEqual(s, s2)

    def test_interpret_content_LENGTH_DEVICE_PROPAGATE_and_ALERT(self):
        content = [['LENGTH', '9999'], ['DEVICE', '1'], ['DEVICE', '2'], ['DEVICE', '3'], ['DEVICE', '4'], ['PROPAGATE', '1', '2', '750'], ['PROPAGATE', '2', '3', '1250'], ['PROPAGATE', '3', '4', '500'], ['PROPAGATE', '4', '1', '1000'], ['ALERT', '1', 'Trouble', '0']]
        s = interpret_content(content)
        s2 = Simulation(9999, [Device(1, {2:750}, coming_alert = [[None, 'Trouble', 0]]), Device(2, {3:1250}), Device(3, {4:500}), Device(4, {1:1000})])
        self.assertEqual(s, s2)

    def test_interpret_content_all_five(self):
        content = [['LENGTH', '9999'], ['DEVICE', '1'], ['DEVICE', '2'], ['DEVICE', '3'], ['DEVICE', '4'], ['PROPAGATE', '1', '2', '750'], ['PROPAGATE', '2', '3', '1250'], ['PROPAGATE', '3', '4', '500'], ['PROPAGATE', '4', '1', '1000'], ['ALERT', '1', 'Trouble', '0'], ['CANCEL', '1', 'Trouble', '2200']]
        s = interpret_content(content)
        s2 = Simulation(9999, [Device(1, {2:750}, coming_alert = [[None, 'Trouble', 0]], coming_cancel = [[None, 'Trouble', 2200]]), Device(2, {3:1250}), Device(3, {4:500}), Device(4, {1:1000})])
        self.assertEqual(s, s2)

class testRunSimul(unittest.TestCase):
    def test_receive_alert_coming_alert_is_None(self):
        d = Device(1)
        d2 = Device(1)
        receive_alert(d, 0)
        self.assertEqual(d, d2)

    def test_receive_alert_not_right_time(self):
        d = Device(1, coming_alert = [[None, 'Trouble', 0]])
        d2 = Device(1, coming_alert = [[None, 'Trouble', 0]])
        receive_alert(d, 100)
        self.assertEqual(d, d2)

    def test_receive_alert_right_time_sender_is_None(self):
        d = Device(1, coming_alert = [[None, 'Trouble', 0]])
        receive_alert(d, 0)
        self.assertEqual(d, Device(1, alert = {'Trouble':0}, coming_alert = []))

    def test_receive_alert_right_time_sender_is_not_None(self):
        d = Device(1, coming_alert = [[2, 'Trouble', 0]])
        d2 = Device(1, alert = {'Trouble':0}, coming_alert = [])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            receive_alert(d, 0)
            self.assertTrue((output.getvalue() == '@0: #1 RECEIVED ALERT FROM #2: Trouble\n') and (d == d2))

    def test_receive_cancel_coming_cancel_is_None(self):
        d = Device(1)
        d2 = Device(1)
        receive_cancel(d, 0)
        self.assertEqual(d, d2)

    def test_receive_cancel_not_right_time(self):
        d = Device(1, coming_cancel = [[None, 'Trouble', 0]])
        d2 = Device(1, coming_cancel = [[None, 'Trouble', 0]])
        receive_cancel(d, 100)
        self.assertEqual(d, d2)

    def test_receive_cancel_right_time_sender_is_None(self):
        d = Device(1, coming_cancel = [[None, 'Trouble', 0]])
        receive_cancel(d, 0)
        self.assertEqual(d, Device(1, cancel = {'Trouble':0}, coming_cancel = []))

    def test_receive_cancel_right_time_sender_is_None_and_knew_cancellation(self):
        d = Device(1, cancel = {'Trouble': 0}, coming_cancel = [[None, 'Trouble', 0]])
        receive_cancel(d, 0)
        self.assertEqual(d, Device(1, cancel = {'Trouble': 0}, coming_cancel = []))

    def test_receive_cancel_right_time_sender_is_not_None(self):
        d = Device(1, coming_cancel = [[2, 'Trouble', 0]])
        d2 = Device(1, cancel = {'Trouble':0}, coming_cancel = [])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            receive_cancel(d, 0)
            self.assertTrue((output.getvalue() == '@0: #1 RECEIVED CANCELLATION FROM #2: Trouble\n') and (d == d2))

    def test_send_alert_propagate_is_None(self):
        d = Device(1)
        d_copy = Device(1)
        s = Simulation(1000, [d])
        s_copy = Simulation(1000, [d_copy])
        send_alert(s, d, 0)
        self.assertTrue((d == d_copy) and (s == s_copy))

    def test_send_alert_no_alert(self):
        d = Device(1, {2:200})
        d_copy = Device(1, {2:200})
        s = Simulation(1000, [d])
        s_copy = Simulation(1000, [d_copy])
        send_alert(s, d, 0)
        self.assertTrue((d == d_copy) and (s == s_copy))

    def test_send_alert_no_target_device(self):
        d = Device(1, {2: 200}, {'Nyo': 1000})
        d_copy = Device(1, {2: 200}, {'Nyo': 1000})
        s = Simulation(1000, [d, Device(3)])
        s_copy = Simulation(1000, [d_copy, Device(3)])
        send_alert(s, d, 0)
        self.assertTrue((d == d_copy) and (s == s_copy))

    def test_send_alert_not_right_time(self):
        d = Device(1, {2: 200}, {'Nyo': 1000})
        d2 = Device(2)
        s = Simulation(1000, [d, d2])
        send_alert(s, d, 0)
        self.assertEqual(d2, Device(2))

    def test_send_alert_canceled_alert(self):
        d = Device(1, {2: 200}, {'Nyo': 1000}, {'Nyo':500})
        d2 = Device(2)
        s = Simulation(2000, [d, d2])
        send_alert(s, d, 1000)
        self.assertEqual(d2, Device(2))

    def test_send_alert_sending_case(self):
        d = Device(1, {2: 200}, {'Nyo': 1000})
        d2 = Device(2)
        s = Simulation(2000, [d, d2])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            send_alert(s, d, 1000)
            self.assertTrue((output.getvalue() == '@1000: #1 SENT ALERT TO #2: Nyo\n') and (d2 == Device(2, coming_alert = [[1, 'Nyo', 1200]])))

    def test_send_cancel_propagate_is_None(self):
        d = Device(1)
        d_copy = Device(1)
        s = Simulation(1000, [d])
        s_copy = Simulation(1000, [d_copy])
        send_cancel(s, d, 0)
        self.assertTrue((d == d_copy) and (s == s_copy))

    def test_send_cancel_no_cancel(self):
        d = Device(1, {2:200})
        d_copy = Device(1, {2:200})
        s = Simulation(1000, [d])
        s_copy = Simulation(1000, [d_copy])
        send_cancel(s, d, 0)
        self.assertTrue((d == d_copy) and (s == s_copy))

    def test_send_cancel_no_target_device(self):
        d = Device(1, {2: 200}, cancel = {'Nyo': 1000})
        d_copy = Device(1, {2: 200}, cancel = {'Nyo': 1000})
        s = Simulation(1000, [d, Device(3)])
        s_copy = Simulation(1000, [d_copy, Device(3)])
        send_cancel(s, d, 0)
        self.assertTrue((d == d_copy) and (s == s_copy))

    def test_send_cancel_not_right_time(self):
        d = Device(1, {2: 200}, cancel = {'Nyo': 1000})
        d2 = Device(2)
        s = Simulation(1000, [d, d2])
        send_cancel(s, d, 0)
        self.assertEqual(d2, Device(2))

    def test_send_cancel_sending_case(self):
        d = Device(1, {2: 200}, cancel = {'Nyo': 1000})
        d2 = Device(2)
        s = Simulation(1000, [d, d2])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            send_cancel(s, d, 1000)
            self.assertTrue((output.getvalue() == '@1000: #1 SENT CANCELLATION TO #2: Nyo\n') and (d2 == Device(2, coming_cancel = [[1, 'Nyo', 1200]])))

    def test_run_Length_0_case(self):
        s = Simulation(0)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            run(s)
            self.assertEqual(output.getvalue(), '@0: END\n')

    def test_run_no_Device_update_time_init_time_not_in_schedule(self):
        s = Simulation(1000, devices = [], schedule = [10, 20, 50, 1000])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            run(s)
            self.assertEqual(output.getvalue(), '@1000: END\n')

    def test_run_no_Device_update_time_init_time_in_schedule(self):
        s = Simulation(1000, devices = [], schedule = [0, 20, 50, 1000])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            run(s)
            self.assertEqual(output.getvalue(), '@1000: END\n')

    def test_start_input_file_case(self):
        s2 = Simulation(9999, [Device(1, {2:750}, coming_alert = [[None, 'Trouble', 0]], coming_cancel = [[None, 'Trouble', 2200]]), Device(2, {3:1250}), Device(3, {4:500}), Device(4, {1:1000})])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            start(s2)
            self.assertEqual(output.getvalue(), '@0: #1 SENT ALERT TO #2: Trouble\n@750: #2 RECEIVED ALERT FROM #1: Trouble\n@750: #2 SENT ALERT TO #3: Trouble\n@2000: #3 RECEIVED ALERT FROM #2: Trouble\n@2000: #3 SENT ALERT TO #4: Trouble\n@2200: #1 SENT CANCELLATION TO #2: Trouble\n@2500: #4 RECEIVED ALERT FROM #3: Trouble\n@2500: #4 SENT ALERT TO #1: Trouble\n@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble\n@2950: #2 SENT CANCELLATION TO #3: Trouble\n@3500: #1 RECEIVED ALERT FROM #4: Trouble\n@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble\n@4200: #3 SENT CANCELLATION TO #4: Trouble\n@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble\n@4700: #4 SENT CANCELLATION TO #1: Trouble\n@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble\n@9999: END\n')

if __name__ == '__main__':
    unittest.main()
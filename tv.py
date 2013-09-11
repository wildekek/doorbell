from subprocess import Popen, PIPE, STDOUT

cecDeviceId = 0

def cec_command(deviceId, command):
    p = Popen(['cec-client', '-s', '-d', '1'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input = command + ' ' + str(deviceId))[0]
    print stdout_data


cec_command(cecDeviceId, 'pow')

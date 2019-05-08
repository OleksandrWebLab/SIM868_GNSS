import time

import serial

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

ser = serial.Serial(
    '/dev/ttyUSB0',
    115200,
    bytesize=EIGHTBITS,
    parity=PARITY_NONE,
    stopbits=STOPBITS_ONE,
    timeout=None,
    xonxoff=False,
    rtscts=False,
    write_timeout=None,
    dsrdtr=False,
    inter_byte_timeout=None,
    exclusive=None
)

commands = [
    'AT+CGNSPWR=1',
    'AT+CGNSSEQ="GGA"',
    'AT+CGNSINF'
]

okResponse = b'OK\r\n'
errorResponse = b'ERROR\r\n'

commandIndex = 0
timeSleep = 1
lastResponse = ''
data = []

try:
    while True:
        command = 'b' + commands[commandIndex] + '\r\n'

        ser.write(command.encode())

        while lastResponse != okResponse and lastResponse != errorResponse:
            lastResponse = ser.read_until()
            data.append(lastResponse.decode())

            print(lastResponse)

        if lastResponse == errorResponse:
            break

        print('')

        if commandIndex < len(commands) - 1:
            commandIndex = commandIndex + 1

        lastResponse = ''
        data = []

        time.sleep(timeSleep)
except KeyboardInterrupt:
    if ser is not None:
        ser.close()

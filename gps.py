import time
import serial

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

ser = serial.Serial(
    '/dev/ttyUSB0',
    115200
)

commands = [
    'AT+CGNSPWR=1',
    'AT+CGNSSEQ="GGA"',
    'AT+CGNSINF'
]

dataFormat = [
    'GPS run status',
    'Fix status',
    'UTC date & Time',
    'Latitude',
    'Longitude',
    'MSL Altitude',
    'Speed Over Ground',
    'Course Over Ground',
    'Fix Mode',
    'Reserved1',
    'HDOP',
    'PDOP',
    'VDOP',
    'Reserved2',
    'GPS Satellites in View',
    'GNSS Satellites Used',
    'GLONASS Satellites in View',
    'Reserved3',
    'C/N0 max',
    'HPA',
    'VPA',
]

okResponse = 'OK'
errorResponse = 'ERROR'

commandIndex = 0
timeSleep = 1
lastResponse = ''
data = []

try:
    while True:
        command = commands[commandIndex]
        preparedCommand = command + '\r\n'

        ser.write(preparedCommand.encode())

        while lastResponse != okResponse and lastResponse != errorResponse:
            lastResponse = ser.read_until().decode()
            lastResponse = lastResponse.replace('\r', '')
            lastResponse = lastResponse.replace('\n', '')

            if lastResponse != "":
                # print(lastResponse)
                data.append(lastResponse)

        if lastResponse == errorResponse:
            break

        # print(data)

        if command == 'AT+CGNSINF':
            data = data[1].split(':')
            data = data[1].strip(' ').split(',')
            data = dict(zip(dataFormat, data))
            print(data)

        if commandIndex < len(commands) - 1:
            commandIndex = commandIndex + 1

        lastResponse = ''
        data = []

        time.sleep(timeSleep)
except KeyboardInterrupt:
    if ser is not None:
        ser.close()

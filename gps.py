import serial
import time

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

ser = serial.Serial(
    '/dev/ttyS0',
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
    'AT+CLTS=1'
]

try:
    while True:
        command = 'b' + commands[0] + '\r\n'

        ser.write(command.encode())
        ser.flushInput()

        data = ser.read_until()

        print(data)

        # print(ser.inWaiting())

        # print ser.inWaiting()
        # while ser.inWaiting() > 0:
        #     data += ser.read(ser.inWaiting()).decode()
        # if data != "":
        #     print(data)
except KeyboardInterrupt:
    if ser != None:
        ser.close()

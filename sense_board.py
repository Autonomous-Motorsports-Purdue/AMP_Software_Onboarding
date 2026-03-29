import serial
import io
import os


with serial.Serial() as ser:
    ser.baudrate = 115200
    ser.port = "COM7" # will be different on linux/macos
    ser.open()
    ser_text = io.TextIOWrapper(ser, newline='\r')
    ser_text.readline()

    # order is gx, gy, gz, ax, ay, az, mx, my, mz

    while True:
        x = ser_text.readline()
        raw = x.strip().split(",")
        # remove first 3 chars from each elem in raw
        raw = [elem[3:] for elem in raw]
        gx, gy, gz, ax, ay, az, mx, my, mz = raw
        print(f"g_vec: ({gx}, {gy}, {gz})")
        print(f"a_vec: ({ax}, {ay}, {az})")
        print(f"m_vec: ({mx}, {my}, {mz})")
        os.system("cls") # "clear", if you are on linux/macos
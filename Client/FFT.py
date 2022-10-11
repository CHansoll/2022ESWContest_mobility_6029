import sys
import smbus
from time import sleep
import numpy as np
import math

PWR_MGMT_1 = 0x6B
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C

ACCEL_X_OUT_H = 0x3B
ACCEL_Y_OUT_H = 0x3D
ACCEL_Z_OUT_H = 0x3F
GYRO_X_OUT_H = 0x43
GYRO_Y_OUT_H = 0x45
GYRO_Z_OUT_H = 0x47

bus = smbus.SMBus(1)
device_address = 0x68  # This is the I2C address [0110 1000]

freq = 1000
guarda = 500

frequency = 0
po = 0
i = 0
Peak = 0
position = []

axyz = []
kal_x=[]
kal_y=[]
kal_z=[]

measure_variance_x = 0.05
measure_variance_y = 0.05
measure_variance_z = 0.05
process_variance_x = 0.125
process_variance_y = 0.125
process_variance_z = 0.125

X = np.matrix([[0], [0], [9.81]])
P = np.matrix([
               [process_variance_x**2, 0, 0],
               [0, process_variance_y**2, 0],
               [0, 0, process_variance_z**2],
              ])
A = np.identity(3)
A_T = np.transpose(A)
B = np.identity(3)
u = np.matrix([[0], [0], [0]])
w = np.matrix([[0], [0], [0]])
Q = np.matrix([[0.001, 0, 0], [0, 0.001, 0], [0, 0, 0.001]])
H = np.identity(3)
H_T = np.transpose(H)
R = np.matrix([
               [measure_variance_x**2, 0, 0],
               [0, measure_variance_y**2, 0],
               [0, 0, measure_variance_z**2],
              ])
I = np.identity(3)
r = range(0, int(freq / 2 + 1), int(freq / guarda))

def mpu_init(bus, device_address):
    bus.write_byte_data(device_address, PWR_MGMT_1, 0)  # [0000 0000]

    bus.write_byte_data(device_address, GYRO_CONFIG, 0)  # [0000 0000]

    bus.write_byte_data(device_address, ACCEL_CONFIG, 0)  # [0000 0000]

    sleep(0.5)


def read_raw_data(bus, device_address, sensor_address):
    high = bus.read_byte_data(device_address, sensor_address)
    low = bus.read_byte_data(device_address, sensor_address + 1)
    value = ((high << 8) | low)

    if value > (65535 / 2):
        value = value - 65535

    return value


def convert_accel_to_g(raw_data):
    return raw_data / 16384.0


def get_accelerometer_data(bus, device_address):
    acc_x = read_raw_data(bus, device_address, ACCEL_X_OUT_H)
    acc_y = read_raw_data(bus, device_address, ACCEL_Y_OUT_H)
    acc_z = read_raw_data(bus, device_address, ACCEL_Z_OUT_H)

    acc_x_g = convert_accel_to_g(acc_x)
    acc_y_g = convert_accel_to_g(acc_y)
    acc_z_g = convert_accel_to_g(acc_z)

    return acc_x_g, acc_y_g, acc_z_g


def print_data(bus, device_address):
    print(get_accelerometer_data(bus, device_address))
    print('\n')


def kalman(Y):
    # predict state and process matrix for current iteration
    X_predict = A * X + B * u + w
    P_predict = A * P * A_T + Q

    # find kalman gain
    K = P_predict * H_T * (np.linalg.inv(H * P_predict * H_T + R))

    # estimate new state and process matricies
    X_estimate = X_predict + K * (Y - H * X_predict)
    P_estimate = (I - K * H) * P
    return X_estimate, P_estimate


# find the Peak
def peak(arr):
    peak = largest = -float('inf')
    for n in arr:
        if n > largest:
            peak = largest
            largest = n
        elif peak < n < largest:
            peak = n
    return peak


# calculate the fft and return Peak, frequency
def fft():
    global i, Peak, po, position, frequency
    frequencia = np.fft.fftfreq(guarda, d=1 / freq)
    try:
        accel_x, accel_y, accel_z = get_accelerometer_data(bus, device_address)
        Y = np.matrix([[accel_x], [accel_y], [accel_z]])
        X, P = kalman(Y)
        kal_x = X[0, 0]
        kal_y = X[1, 0]
        kal_z = X[2, 0]
        xyz = math.sqrt(kal_x * kal_x + kal_y * kal_y + kal_z * kal_z)
        axyz.append(xyz)

        if i > guarda:
            data3 = np.fft.fft(axyz[-guarda:])
            amplitude = abs(np.real(data3[:int(guarda / 2)]))
            Peak = peak(amplitude)
            position = np.where(amplitude == Peak)
            po = position[0]
            frequency = frequencia[po]

        i += 1
        if i > guarda:
            del axyz[0:1]

        return Peak, frequency


    except ValueError:
        pass

import pymysql
import FFT
import Read_temperature
import Socket_client as client

storage = [0] * 8  # Declare and initialize an array that stores type-specific shock accumulation

count_uphill = count_downhill = count_bump = count_winter = count_overcharge = count_overdischarge = count_overcurrent = 0
conn = None
cur = None
data0 = data1 = data2 = data3 = data4 = data5 = data6 = data7 = data8 = ""
sql = ""

conn = pymysql.connect(host='192.168.137.206', user='root', passwd='erica',
                       db='pythonDB')  # Connection Information , host : mariaDB server IP
cur = conn.cursor()  # Create Cursor


# send the data to DB
def send():  # cumulative count values in array storage

    data1 = storage[0]  # total
    data2 = storage[1]  # uphill
    data3 = storage[2]  # downhill
    data4 = storage[3]  # bump
    data5 = storage[4]  # winter
    data6 = storage[5]  # overcharge
    data7 = storage[6]  # overdischarge
    data8 = storage[7]  # overcurrent

    # Enter INSERT SQL statement in sql variable
    sql = "INSERT INTO storage VALUES('" + str(data1) + "','" + str(data2) + "','" + str(data3) + "','" + str(
        data4) + "','" + str(data5) + "','" + str(data6) + "','" + str(data7) + "'," + str(data8) + ")"
    cur.execute(sql)  # Run sql with cursor
    conn.commit()  # Final Save


# Analyze driving habits and situations with frequency, amplitude, and temperature values
if __name__ == "__main__":
    # Instead of skip-networking the default is now to listen only on
    # localhost which is more compatible and is not less secure.
    # bind-address            = 127.0.0.1

    while True:
        frequency = FFT.fft()[1]
        amplitude = FFT.fft()[0]
        temperature = Read_temperature.read_temp()
        # Instead of skip-networking the default is now to listen only on
        # localhost which is more compatible and is not less secure.
        # bind-address            = 127.0.0.1

        if (4 <= amplitude and 200 < frequency < 350):  # uphill
            count_uphill += 1
            if count_uphill == 30:
                client.cmd(1)

        elif (4 <= amplitude and 50 < frequency < 200):  # downhill
            count_downhill += 1
            if count_downhill == 30:
                client.cmd(2)

        elif (6 <= amplitude and 0 < frequency < 50) or (6 < amplitude and 350 < frequency < 450):  # bump
            count_bump += 1
            if count_bump == 30:
                client.cmd(3)

        else:
            continue

        if temperature <= -7:
            if (6 < amplitude and 0 <= frequency <= 50) or (6 < amplitude and 230 <= frequency <= 270) or (
                    6 < amplitude and 450 <= frequency):  # winter
                count_winter += 1
                if count_winter == 30:
                    client.cmd(4)

        elif temperature >= 60:
            if (6 <= amplitude and 0 < frequency < 50) or (6 < amplitude and 350 < frequency < 450):  # overcharge
                count_overcharge += 1
                if count_overcharge == 30:
                    client.cmd(5)

            elif 4 <= amplitude and 50 < frequency < 200:  # overdischarge
                count_overdischarge += 1
                if count_overdischarge == 30:
                    client.cmd(6)

            elif 4 <= amplitude and 200 < frequency < 350:  # overcurrent
                count_overcurrent += 1
                if count_overcurrent == 30:
                    client.cmd(7)
            else:
                continue

        total = count_uphill + count_downhill + count_bump + count_winter + count_overcharge + count_overdischarge + count_overcurrent

        # Store contextual cumulative count values in array storage
        storage[0] = total
        storage[1] = count_uphill
        storage[2] = count_downhill
        storage[3] = count_bump
        storage[4] = count_winter
        storage[5] = count_overcharge
        storage[6] = count_overdischarge
        storage[7] = count_overcurrent

        if total == 100:  # level1 warning
            client.senddata(count_uphill, count_downhill, count_bump, count_winter, count_overcharge,
                            count_overdischarge, count_overcurrent)
            send()

        elif total == 150:  # level2 warning
            client.senddata(count_uphill, count_downhill, count_bump, count_winter, count_overcharge,
                            count_overdischarge, count_overcurrent)
            send()

        elif total == 170:  # level3 warning
            client.senddata(count_uphill, count_downhill, count_bump, count_winter, count_overcharge,
                            count_overdischarge, count_overcurrent)
            send()
            conn.close()  # End of connection
            total = count_uphill = count_downhill = count_bump = count_winter = count_overcharge = count_overdischarge = count_overcurrent = 0  # Initialize variables
            break

        else:
            continue
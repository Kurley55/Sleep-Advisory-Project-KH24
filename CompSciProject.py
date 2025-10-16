import serial
import datetime
import pandas
import matplotlib.pyplot as plt


connection = serial.Serial('COM3', 115200)

age = []
recsleep = []
time_slept = []
while True:
    print('Sleep Assistant')
    data = connection.readline().decode().strip()
    data1 = connection.readline().decode().strip()
    data2 = connection.readline().decode().strip()
    if len(age) == 0:
        age.append(int(data))
        print("You are", age, "years old.")
    if len(recsleep) == 0:
        recsleep.append(int(data1))
        print("You require up to ",recsleep, "hours of sleep")
    if len(time_slept) == 0:
        time_slept.append(round(float(data2) / 3600, 2))
        print("And you slept", time_slept, "hours")
        
    enoughSleep = recsleep >= time_slept
    if enoughSleep == False:
        enoughSleep = ["TRUE"]
    else:
        enoughSleep = ["FALSE"]
    if len(age) == 1 and len(time_slept) == 1:
        with open('sleep_data.csv', 'a') as file:
            file.write(f'{age[0]}, {recsleep[0]},{time_slept[0]},')
        
    if enoughSleep == False:
        print("Keep up the Z's!")
    else:
        print("Sleep more!!!")

    repeat = input("Do you want to track more sleep data? (yes/no): ").lower()
    if repeat != 'yes':
        break
csventered = int(input("Access the microbit and download your data as CSV and enter it in the project folder and type 1 when you've done that"))
time_column = 'Time (seconds)'
sound_lvl = 'Sound'

if csventered == 1:
    with open('microbit.csv', 'r') as file:
        microbit_data = pandas.read_csv(file)
        microbit_data['Time (seconds)'] = pandas.to_datetime(microbit_data['Time (seconds)'], unit='s')
        avg_sound_lvl = microbit_data.groupby(microbit_data['Time (seconds)'].dt.hour)['Sound'].mean()
rounded_avg_sound_lvl = round(avg_sound_lvl.iloc[0], 2)
rounded_avg_sound_lvl_str = str(rounded_avg_sound_lvl)
with open('sleep_data.csv', 'a') as file:
    file.write(f'{rounded_avg_sound_lvl_str}, {enoughSleep[0]}\n')

data = pandas.read_csv('sleep_data.csv')
plt.subplot(1, 2, 1)
plt.bar(data.index - 0.2, data['Hours Slept'], color='blue', width=0.4, label='Hours Slept')
plt.bar(data.index + 0.2, data['Recommended Sleep'], color='green', width=0.4, label='Recommended Sleep')
plt.title('Hours Slept vs Recommended Sleep by Age')
plt.xlabel('Age')
plt.ylabel('Hours')
plt.xticks(data.index, data['Age']) 
plt.subplot(1, 2, 2)
plt.scatter(data['Avg Sound Levels'], data['Hours Slept'], color='blue', alpha=0.7)
plt.title('Effect of Sound Levels on Hours Slept')
plt.xlabel('Average Sound Levels (Decibels)')
plt.ylabel('Hours Slept')
plt.grid(True)
plt.show()  
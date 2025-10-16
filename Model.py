import pandas
import matplotlib.pyplot as plt

print("\nIf sound levels (validated parameters) are over 30 decibels, do you sleep (validated parameters) less than enough time (validated parameter)")
data = pandas.read_csv("sleep_data.csv")
eSleep = round((data['enoughSleep'].sum() / len(data)) * 100, 2)
highSound = round((data['Avg Sound Levels'] > 30).sum() / len(data) * 100, 2)
print("Percentage of people that get enough sleep:", eSleep)
print("Percentage of people that had sound levels above 30:", highSound)

print("\nIf you’re 18 or over (validated parameters), do you sleep (validated parameters) less than the enough time (validated parameter)")
over_18 = data[data['Age'] >= 18]
enough_false_over_18 = over_18[over_18['enoughSleep'] == False]
enough_false_over_18_perc = (len(enough_false_over_18) / len(over_18)) * 100 if len(over_18) > 0 else 0

teen = data[(data['Age'] >= 12) & (data['Age'] <= 17)]
enough_false_teen = teen[teen['enoughSleep'] == False]
enough_false_teen_perc = (len(enough_false_teen) / len(teen)) * 100 if len(teen) > 0 else 0

if enough_false_over_18_perc == 0 and enough_false_teen_perc == 0:
    high_perc_group = "neither group (no individuals with 'False' enoughSleep)"
else:
    high_perc_group = "neither group" if enough_false_over_18_perc == 0 and enough_false_teen_perc == 0 else ("people over the age of 18" if enough_false_over_18_perc > enough_false_teen_perc else "people aged 12-17")

print("Percentage of people over the age of 18 with not enough sleep:", enough_false_over_18_perc)
print("Percentage of people aged 12-17 with not enough sleep:", enough_false_teen_perc)
print("The group with a higher chance of not getting enough sleep:", high_perc_group)


def create_bar_plot(data, title):
    plt.bar(data.keys(), data.values(), color='red')
    plt.ylabel('Percentage')
    plt.title(title)
    plt.ylim(0, 100)
    for label, perc in data.items():
        plt.text(label, perc + 2, f'{perc:.2f}%', ha='center')
    plt.show()

data = pandas.read_csv("sleep_data.csv")

model1_data = {'Enough Sleep': (data['enoughSleep'].sum() / len(data)) * 100,
               'High Sound': (data['Avg Sound Levels'] > 30).sum() / len(data) * 100}
create_bar_plot(model1_data, 'Percentage of Various Sleep Metrics (Model 1)')

over_18 = data[data['Age'] >= 18]
teen = data[(data['Age'] >= 12) & (data['Age'] <= 17)]
model2_data = {'Over 18': (over_18['enoughSleep'] == False).mean() * 100,
               'Aged 12-17': (teen['enoughSleep'] == False).mean() * 100}
create_bar_plot(model2_data, 'Percentage of Individuals with Not Enough Sleep by Age Group (Model 2)')
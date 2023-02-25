#8
import pandas, time

df = pandas.read_csv('train.csv')

n = len(df['PassengerId'])

fareSum, count = 0, 0

s_time = time.time()

for i in range(n) :
    if df['Embarked'][i] == 'Q' :
        count += 1
        fareSum += df['Fare'][i]

print(f'average_fare = {fareSum / count}')
print(f'The time spent using for loop = {time.time() - s_time}')


s_time = time.time()

average_fare = df[(df['Embarked'] == 'Q')]['Fare'].mean()
print(f'average_fare = {average_fare}')

print(f'The time spent using vectorization = {time.time() - s_time}')
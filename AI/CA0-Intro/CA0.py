import pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from scipy.stats import norm
from sklearn import model_selection
import statistics

#1
df = pandas.read_csv('train.csv')
print(f'df.describe() output is : \n {df.describe()}')
print(f'df.tail() output is : \n {df.tail()}')
print(f'df.head() output is : \n {df.head()}')
print(df.info())

#2-1
print('Data types are :')
print(df.dtypes)

#2-2
le = LabelEncoder()
df['Sex'] = le.fit_transform(df['Sex'])
df['Embarked'] = le.fit_transform(df['Embarked'])
#C -> 0, Q -> 1, S -> 2

#3-1
print('Number of blank rows for each column :')
print(df.isnull().sum(axis = 0))

#3-2
#I removed the column 'Cabin'. Because most of its rows were empty
# and I replaced NaN rows of column 'Age' with average of the column
del df['Cabin']
age_mean = int(df['Age'].mean())
df['Age'] = df['Age'].fillna(age_mean)

#4
del df['PassengerId']
del df['Ticket']
del df['Name']

#5-1
men_count = df[(df['Sex'] == 1)]['Sex'].count()
women_count = df[(df['Sex'] == 0)]['Sex'].count()
print(f'Men count = {men_count}')
print(f'Women count = {women_count}')
#5-2
southhampton_count = df[(df['Sex'] == 1) & (df['Embarked'] == 2)]['Sex'].count()
print(f'Men count that embarked at Southhampton = {southhampton_count}')

#6
no_compeer_count = df[(df['Age'] > 35) & (df['Pclass'] == 3) & (df['SibSp'] == 0) & (df['Parch'] == 0)]['Sex'].count()
print(f'Number of passengers whoe are older than 35 and have no compeer and their ticket type is 3 = {no_compeer_count}')

#7
average_fare = df[(df['Embarked'] == 1)]['Fare'].mean()
print(f'Average fare for travelers who embarked at Queenstown = {average_fare}')

#9
df.hist()
plt.show()

#10
n_df = df.apply(lambda column : (column - column.mean()) / (column.std()))
n_df.hist()
plt.show()

#11
mean_for_deads = dict(df[(df['Survived'] == 0)].mean())
std_for_deads = dict(df[(df['Survived'] == 0)].std())
mean_for_surviveds = dict(df[(df['Survived'] == 1)].mean())
std_for_surviveds = dict(df[(df['Survived'] == 1)].std())

figure, axis = plt.subplots(1, 7)


def draw_plots(col_name, s, e, col) :
    r = np.arange(s, e, 0.01)
    axis[col].plot(r, norm.pdf(r, mean_for_deads[col_name], std_for_deads[col_name]), 'r')
    axis[col].plot(r, norm.pdf(r, mean_for_surviveds[col_name], std_for_surviveds[col_name]), 'b')
    axis[col].set_title(col_name)


draw_plots('Pclass', 1, 3, 0)
draw_plots('Sex', 0, 1, 1)
draw_plots('Age', 0, 80, 2)
draw_plots('SibSp', 0, 8, 3)
draw_plots('Parch', 0, 6, 4)
draw_plots('Fare', 0, 500, 5)
draw_plots('Embarked', 0, 3, 6)

plt.show()

#12
info = pandas.read_csv('test.csv')
tmp_info = info.copy()

info['Embarked'] = le.fit_transform(info['Embarked'])
info['Sex'] = le.fit_transform(info['Sex'])

def apply_norm(col_name, for_who) :
    if for_who == 's' :
        m, s = mean_for_surviveds[col_name], std_for_surviveds[col_name]
    else :
        m, s = mean_for_deads[col_name], std_for_deads[col_name]
    return info[col_name].apply(lambda x : norm(m, s).pdf(x))

pclass_s = apply_norm('Pclass', 's')
pclass_d = apply_norm('Pclass', 'd')
sex_s = apply_norm('Sex', 's')
sex_d = apply_norm('Sex', 'd')
embarked_s = apply_norm('Embarked', 's')
embarked_d = apply_norm('Embarked', 'd')

s_probability = pclass_s * sex_s * embarked_s
d_probability = pclass_d * sex_d * embarked_d

info['Survived'] = np.where(s_probability > d_probability, 1, 0)
tmp_info['Survivied'] = info['Survived']
tmp_info.to_csv('~/My Folders/University/5th Term/AI/CAs/CA0/result.csv', mode = 'w', index = False)

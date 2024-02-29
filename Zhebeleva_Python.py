# -*- coding: utf-8 -*-
"""Жебелева Мария, PYDA-49 - итоговый проект по курсу "Python для анализа данных".ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13p-lKvZWki8Zm1t7FLBd6_oLcJN1xGLT

Файл HR.csv с данными по опросу уровня удовлетворенности сотрудниками работой.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv('HR.csv')
df

"""## Описание датасета

**Признаки:**
1. satisfaction_level - Уровень удовлетворенности работой
2. Last_evaluation - Время с момента последней оценки в годах
3. number_projects - Количество проектов, выполненных за время работы
4. average_monthly_hours - Среднее количество часов на рабочем месте в месяц
5. time_spend_company - Стаж работы в компании в годах
6. work_accident - Происходили ли несчастные случаи на рабочем месте с сотрудником
7. left - уволился ли сотрудник
8. promotion_last_5years - повышался ли сотрудник за последние пять лет
9. department - отдел в котором работает сотрудник
10. salary - относительный уровень зарплаты

## 2. Основные статистики
"""

df.describe()

"""- В целом уровень удовлетворенности работой чуть выше среднего (по среднему значению датасета).
- Последняя оценка в среднем была примерно 8 месяцев назад (0,7 года).
- Сотрудники работали на 2 до 7 проектов, в среднем около 4.
- Рабочая нагрузка в месяц составляет от 96 до 310 часов, в среднем около 50 часов в неделю.
- Длительность работы в компании - от 2 до 10, но больше относительно новых сотрудников, которые работают 3 года.
- Несчастных случаев довольно малый процент, как и доля уволенных сотрудников в датасете.
- В течение последних 5 лет крайне малое число сотрудников получило повышение (около 2%).
"""

df.isna().mean() * 100

# типы данных
df.dtypes

"""**Числовые столбцы в числовом формате + два категориальных. Пропусков нет. Выбросы только по столбцу "Длительность работы в компании"**"""

#  получение списка числовых стобцов из DataFrame - "ящик с усами", исключая определенные столбцы
numeric_variables = df.select_dtypes(include=['float64', 'int64']).columns.difference(['Work_accident', 'left', 'promotion_last_5years'])

for variable in numeric_variables:
    fig = px.box(data_frame=df, y=variable, title=f'Распределение по {variable}')
    fig.show()

def calculate_mean(df): # среднее арифметическое для числовых столбцов
    mean_result = df.mean()
    print(f"Среднее арифметическое:")
    print(mean_result)

calculate_mean(df)

def calculate_median(df): # медиана для числовых столбцов
    median_result = df.median()
    print(f"Медиана:")
    print(median_result)

calculate_median(df)

def calculate_mode(df): # мода
    mode_result = df.mode().iloc[0]
    # без .iloc[0] выводится строка с модами по всем столбцам, а с .iloc[0] - мода для каждого столбца по-отдельности
    print(f"Мода:")
    print(mode_result)

mode_values = calculate_mode(df)

def calculate_max(df): # максимальное значение
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    max_result = numeric_columns.max()
    print("Максимальные значения по числовым столбцам:")
    print(max_result)

max_values = calculate_max(df)

def calculate_min(df): # минимальное значение
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    min_result = numeric_columns.min()
    print("Максимальные значения по числовым столбцам:")
    print(min_result)

min_values = calculate_min(df)

def calculate_std(df): # стандартное отклонение
    std_result = df.std()
    print(f"Стандартное отклонение:")
    print(std_result)

calculate_std(df)

"""## Корреляционная матрица для количественных переменных

Чтобы выбрать, какой коэффициент корреляции использовать, проверим нормальность распределения признаков и сравним дисперсии.
"""

import scipy.stats as stats

def test_normality(df):
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    for column in numeric_columns.columns:
        statistic, p_value = stats.kstest(df[column], 'norm', args=(df[column].mean(), df[column].std()))  # тест Колмогорова-Смирнова
        print(f"Столбец {column}:")
        print(f"Статистика теста: {round(statistic, 2)}, p-значение: {round(p_value, 2)}")

        if p_value > 0.05:
            print("Распределение нормальное")
        else:
            print("Распределение отличается от нормального")
        print()  # Пустая строка между результатами для каждого столбца

test_normality(df)

# данные распределены НЕ нормально

import itertools

def compare_variances(df):
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    compared_pairs = set() # для исключения повтора результатов сравнения
    for col1, col2 in itertools.combinations(numeric_columns, 2): # только числовые столбцы
        if (col1, col2) not in compared_pairs and (col2, col1) not in compared_pairs:
            statistic, p_value = stats.levene(df[col1], df[col2])
            print(f"Сравнение дисперсий между столбцами {col1} и {col2}:")
            print("Статистика критерия Левена:", round(statistic, 2), "p-value:", round(p_value, 2))
            alpha = 0.05
            if p_value < alpha:
                print("Отклоняем нулевую гипотезу: Дисперсии различаются")
            else:
                print("Не отклоняем нулевую гипотезу: Дисперсии не различаются")
            print()  # Пустая строка для разделения
            compared_pairs.add((col1, col2))

compare_variances(df)

# дисперсии различаются

"""Поскольку распределение не нормальное, дисперсии различаются, а данные у нас в основном числовые, выборка большая, использовать будем **коэффициент Спирмена**."""

# Спирмен
df.corr(method='spearman')

import matplotlib.pyplot as plt
import seaborn as sns

correlation_matrix_spearman = df.corr(method='spearman')

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix_spearman, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Тепловая карта корреляции (Спирмен)')
plt.show()

"""**2 самые скоррелированные переменные** - average_montly_hours и number_project (количество проектов, в которых задействован сотрудник, положительно связано с количеством рабочих часов в месяц). Еще сильная отрицательная связь между left и satisfaction_level, что логично (чем ниже удовлетворенность работой, тем выше вероятность увольнения).

**2 наименее скоррелированные переменные** - left и last_evaluation - нулевая связь между увольнением и проведением последней оценки; также корреляция равна 0 для work_accident и num_projects (количество проектов не связано с несчастными случаями на работе).

## Сколько сотрудников работает в каждом департаменте

Предполагая, что каждая строка датасета характеризует одного уникального сотрудника, то количество сотрудников по департаментам можно вычислить через подсчет значений.

В этом случае самым многочисленным является отдел продаж - 27,6% от всего штата сотрудников (4140 человек), на втором и третьем местах - технический департамент и отдел поддержки - 18,13% (2720 человек) и 14,86% (2229 человек) соответственно. Меньше всего сотрудников в отделе менеджмента - 4,2% (630 человек).
"""

value_counts = df['department'].value_counts()
percentages = (value_counts / len(df)) * 100
print(f"Количество сотрудников разных отделов:")
print(value_counts)
print()
print(f"Доля сотрудников разных отделов:")
print(round(percentages, 2))

"""## Распределение сотрудников по зарплатам"""

fig = px.pie(
    data_frame=df,
    names='salary',
    title='Распределение служащих по зарплате',
    hole=0.2
)
fig.show()

# почти половина (48,8%) получает сравнительно низкую ЗП, чуть меньше половины (43%) - средний заработок, высокая ЗП - меньшинство (8,25%)

"""## Распределение сотрудников по зарплатам в разных департаментах"""

import plotly.express as px

# группируем по столбцам 'department' и 'salary' и считаем количество значений
grouped_data = df.groupby(['department', 'salary']).size().reset_index(name='count')

fig = px.bar(grouped_data,
             x='department',
             y='count',
             color='salary',
             barmode='group',  # для разделения по столбцам 'salary'
             title='Распределение уровней зарплат по департаментам',
             labels={'count': 'Число сотрудников', 'salary': 'Уровень зарплаты', 'department': 'Департамент'},
             text='count',  # значения, которые будут отображаться на столбцах
             )
fig.show()

"""1. Равное количество сотрудников с высокой ЗП и со средней ЗП только в отделе менеджмента - по 225 человек (180 - низкая ЗП)
2. Число сотрудников со средней ЗП больше сотрудников с низкой ЗП только в 3 отделах:
* менеджмент (225 против 180)
* отдел кадров (359 против 335)
* RandD (372 против 364)
3. Во всех остальных отделах большинство сотрудников получает сравнительно низкую плату.

## Проверка гипотезы:

Сотрудники с высоким окладом проводят на работе больше времени, чем сотрудники с низким окладом.
"""

# рассчитаем среднее значение по столбцу average_montly_hours для категорий salary
df.groupby('salary')['average_montly_hours'].mean()

"""Гипотеза не подтвердилась. Различия по рабочим часам для категорий зарплат несущественные.

## Показатели среди уволившихся и не уволившихся сотрудников
"""

# доля сотрудников с повышением за последние 5 лет
df.groupby('left')['promotion_last_5years'].value_counts(normalize=True)

# среди оставшихся - 2,6%
# среди уволившихся - 0,5% - практически не получали повышения

# cредняя степень удовлетворенности
df.groupby('left')['satisfaction_level'].mean()

# среди оставшихся - 66%
# среди уволившихся - 44% - были менее удовлетворены работой

# cреднее количество проектов
df.groupby('left')['number_project'].mean()

# среди оставшихся - 3,7
# среди уволившихся - 3,8 - значимых различий нет

"""## Линейный дискриминантный анализ LDA

Модель LDA на основе имеющихся факторов (кроме department и
salary) должна предсказывать, уволился ли
сотрудник.
"""

# разделим данные на признаки (матрица X) и целевую переменную (y)
X = df.drop(['left', 'department', 'salary'], axis=1) # все остальные столбцы
y = df['left'] # целевая переменная

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=13) # делим на выборку для обучения 80% и тестирования 20%
# y - целевая переменная, stratify=y гарантирует, что распределение классов в обучающем и тестовом наборах будет как в исходных данных

from sklearn.preprocessing import StandardScaler # игнорирует категориальные столбцы department и salary
scaler = StandardScaler() # cоздаем экземпляр класса StandardScaler для масштабирования признаков

X_train_st = scaler.fit_transform(X_train)
"""
Метод fit_transform вычисляет среднее и стандартное отклонение каждого признака из обучающего набора X_train,
а затем так масштабирует признаки, чтобы среднее значение каждого признака = 0, а стандартное отклонение = 1.
Эти значения используются для масштабирования обучающих данных, приводя их к N распределению.
"""

X_test_st = scaler.transform(X_test)
"""
Метод transform масштабирует тестовый набор X_test с использованием тех же средних и стандартных отклонений,
которые были вычислены для обучающего набора данных X_train.
"""

X_train_st[:2]

# определим функцию, которая будет выводить нужные нам метрики

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

def print_all_metrics(y_true, y_pred, title = 'Метрики классификации'):
    print(title)
    print('\tAccuracy: {:.2f}'.format(accuracy_score(y_true, y_pred)))
    print('\tPrecision: {:.2f}'.format(precision_score(y_true, y_pred)))
    print('\tRecall: {:.2f}'.format(recall_score(y_true, y_pred)))
    print('\tF1: {:.2f}'.format(f1_score(y_true, y_pred)))

"""**Ограничение:** LDA предполагает, что данные распределены нормально, а матрицы ковариации для всех классов равны - у нас это требование не соблюдается."""

# модель LDA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis() # создаем экземпляр класса

lda.fit(X_train, y_train) # обучаем данные
lda.predict(X_test) # прогноз на тестовой выборке

# смотрим разницу факта и прогноза
result = pd.DataFrame({'Pop': y_test, 'Predicted': lda.predict(X_test)})
result

"""## Оценка качества модели на тестовой выборке"""

# рассчитаем точность модели на тестовой выборке - отношение верных прогнозов к общему количеству позиций
# хорошая метрика для сбалансированных классов (когда наблюдений в категориях примерно одинаковое количество)
from sklearn.metrics import accuracy_score

accuracy_score(y_test, lda.predict(X_test)) # y_test - правильные ответы, lda.predict(X_test) - предсказанные ответы

"""Точность - 75,3% - неплохая."""

# коэффициенты дискриминатных линий - которые обучались
lda.coef_

# satisfaction_level, last_evaluation, number_project, average_montly_hours, time_spend_company, Work_accident, promotion_last_5years

"""Видим, что больший вклад в признак, уволился человек или нет, вносит уровень удовлетворенности работой - связь отрицательная. На втором месте по значимости - повышение в течение последних 5 лет, затем - несчастный случай на работе.

Самое слабое влияние оказывает среднее количество рабочих часов в месяц.

## Загрузка решения на github
"""

# ссылка на github
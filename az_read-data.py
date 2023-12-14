import sqlite3
import pandas as pd

#connect to/create database
conn = sqlite3.connect('amztracker.db')

df = pd.read_sql_query('''SELECT * FROM prices''', conn)

print(df)


#save df to csv fiel and excel file
df.to_csv('azscraptable.csv')
df.to_excel('azscraptable.xlsx')

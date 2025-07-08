import pandas as pd


df = pd.read_csv('Lebrija_Espana.csv', skiprows=2)

print(df.info())
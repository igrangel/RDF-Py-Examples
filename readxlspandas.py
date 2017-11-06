import pandas as pd

# Reads a sheet by name[Tabelle1] of an excel file[st.xls] with a given number[0:3] of columns without Nan values
file = 'st.xls'
df = pd.read_excel(file, sheet_name='Tabelle1')
df1 = df[df.columns[0:3]]
df1.dropna(how='any', inplace=True)

for index, row in df.iterrows():
   print(row['Benennung'],
         row['Definition '],
         row['Quelle (IEC-Norm)'])


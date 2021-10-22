import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as plta
import prettytable


def load_file(filename):
    wb = xlrd.open_workbook(filename)
    sh = wb.sheet_by_index(0)

    columns_names = sh.row_values(0, start_colx=0, end_colx=None)
    rows = []
    for i in range(1,14):
        rows.append(sh.row_values(i, start_colx=0, end_colx=None))

    df = pd.DataFrame(rows,columns=columns_names)

    locations = np.unique(df['Office'].values).astype(str)
    service_year = np.unique(df['Service Years'].values).astype(str)

    #Display options
    print('Available locations')
    print(locations)

    print('Service years')
    print(service_year)

    Nloc = len(locations)
    Nsy = len(service_year)

    return df

filename = 'Data Sample.xlsx'
df = load_file(filename)

#### INPUTS
myloc = ['Dorval, QC', 'Edmonton, AB']
mysy = ['1-2 years', '3-5 years','Over 5 years']

res = pd.DataFrame(data=np.zeros([7,len(df.columns[19:-1])]), \
    columns=columns_names[19:-1], \
    index = ['','N/A','Very Dissatisfied','Neither Satisfied nor Dissatisfied','Somewhat Dissatisfied','Somewhat Satisfied','Very Satisfied'])

for col in columns_names[19:-1]:
    for loc in myloc:
        for sy in mysy:
            try:
                serie = df[(df['Office']==loc) & (df['Service Years']==sy)][col]
                lab,N = np.unique(serie,return_counts=True)
                res[col][lab] = res[col][lab] + N
            except:
                0
    res[col] = res[col] / np.sum(res[col])
res = res.rename(index = {'':'No Ans'})
display(res)

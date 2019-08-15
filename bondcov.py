import pandas as pd
import numpy as np
import sys
import csv

def remove_braces(s) :
    s = s.replace('Ltd', '').strip()
    s = s.replace('Plc', '').strip()
    s = s.replace('Inc', '').strip()

    start = s.find( '(' )
    end = s.find( ')' )
    if start != -1 and end != -1:
        s = s[:start]

    start = s.find( '[' )
    end = s.find( ']' )
    if start != -1 and end != -1:
        s = s[:start]
    return s.strip()

def match_syns(s) :
    for slist in syns :
        if str(s) in  str(slist):
            return slist[0]

    return s

def match(s) :
    ret = xlon.loc[xlon['Description'].str.contains(s.upper(),
        regex=False), 'ISIN Code']

    if len(ret) > 0: 
        return str(ret.iloc[0])

__syns = pd.read_csv('synonims.csv')
with open('synonims.csv', 'r') as f:
  reader = csv.reader(f)
  __syns = list(reader)

syns = []
for s in __syns :
    syns.append(list(filter(None, s)))

data = pd.read_excel('Dealscan- all loans for UK borrowers.xlsx')
xlon = pd.read_csv('20190813_TRQX_Instrument.csv', delimiter=';')

# df = data
df = data[data['Deal Purpose'] == 'General Purpose']
df.rename(columns={'Lead Arranger':'Name1'}, inplace=True)

r = (df.set_index(df.columns.drop('Name1',1).tolist())
   .Name1.str.split(',', expand=True)
   .stack()
   .reset_index()
   .rename(columns={0:'Name1'})
   .loc[:, df.columns]
)

r['LA'], r['Percent'] = (r['Name1']
        .loc[r['Name1']
        .str[-1] == '%']
        .str.rsplit(' ', 1).str)

r['LA'].loc[r['LA'].isna()] = r['Name1']
r['LA'] = r['LA'].str.strip()


#rr = r.iloc[0:1000]
rr = r
rr['LAA'] = rr['LA'].apply(match_syns)
rr['LAA'] = rr['LA'].apply(remove_braces)

rr.loc[r['LAA'].str.contains('Bank of Scotland'), 'LAA'] = 'ROYAL BANK OF SCOTLAND GROUP'
rr.loc[r['LAA'].str.contains('HSBC'), 'LAA'] = 'HSBC HOLDINGS PLC'
rr.loc[r['LAA'].str.contains('BNP Paribas'), 'LAA'] = 'BNP PARIBAS'
rr.loc[r['LAA'].str.contains('Goldman Sachs'), 'LAA'] = 'GOLDMAN SACHS GROUP INC'
rr.loc[r['LAA'].str.contains('Barclays'), 'LAA'] = 'BARCLAYS'
rr.loc[r['LAA'].str.contains('Agricole'), 'LAA'] = 'AGRICOLE'
rr.loc[r['LAA'].str.contains('SG Corporate'), 'LAA'] = 'SOCIETE GENERALE SA'
rr.loc[r['LAA'].str.contains('Lloyds'), 'LAA'] = 'Lloyds'
rr.loc[r['LAA'].str.contains('Merrill'), 'LAA'] = 'BANK OF AMERICA'
rr.loc[r['LAA'].str.contains('JP Morgan'), 'LAA'] = 'JPMORGAN'
rr.loc[r['LAA'].str.contains('ING'), 'LAA'] = 'ING'
rr.loc[r['LAA'].str.contains('Standard Chartered'), 'LAA'] = 'STANDARD CHARTERED'
rr.loc[r['LAA'].str.contains('Natixis'), 'LAA'] = 'NATIXIS'
rr.loc[r['LAA'].str.contains('Abbey'), 'LAA'] = 'ABBEY'
rr.loc[r['LAA'].str.contains('Bank of Ireland'), 'LAA'] = 'BANK OF IRELAND'
rr.loc[r['LAA'].str.contains('AIB'), 'LAA'] = 'AIB'
rr.loc[r['LAA'].str.contains('ABN AMRO'), 'LAA'] = 'ABN AMRO'
rr.loc[r['LAA'].str.contains('ABN AMRO'), 'LAA'] = 'ABN AMRO'
rr.loc[r['LAA'].str.contains('Citibank'), 'LAA'] = 'CITIGROUP'
rr.loc[r['LAA'].str.contains('Wells Fargo'), 'LAA'] = 'WELLS FARGO'
rr.loc[r['LAA'].str.contains('Svenska Handelsbanken'), 'LAA'] = 'SVENSKA HANDELSBANKEN'
rr.loc[r['LAA'].str.contains('Bilbao'), 'LAA'] = 'BILBAO'
rr.loc[r['LAA'].str.contains('UBS'), 'LAA'] = 'UBS'
rr.loc[r['LAA'].str.contains('Morgan Stanley'), 'LAA'] = 'MORGANSTANLEY'


rr['XLON'] = rr['LAA'].apply(match)

unk = rr['LAA'].loc[rr['XLON'].isnull()]

print(unk.value_counts())
print(rr.shape)
print(len(unk))
print('Total loans:       ' + str(len(rr['XLON'])))
print('Unknown loans:     ' + str(len(unk)))
print('Unknown companies: ' + str(len(unk.unique())))
print('Unique companies:  ' + str(len(rr['XLON'].unique())))

#print(sorted(unk.unique()))
#print(rr[['LA', 'LAA']])
#print(len(rr['LAA'].unique()))


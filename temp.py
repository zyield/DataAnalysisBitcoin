
import pandas as pd

test = pd.read_csv('btc_transactions.csv')
#test = test.iloc[0:200, :]
test2=[]
test2.extend(list(test['from_address']))
test2.extend(list(test['to_address']))
test2 = list(set(test2))

for i in test2:
    if len(i) > 34:
        test2.remove(i)

for i in test2:
    if len(i) > 34:
        test2.remove(i)
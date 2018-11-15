#from blockchain import statistics
import blockchain
from collections import Counter, OrderedDict
from datetime import datetime
#print(statistics.get().blocks_size)

#print(blockchain.statistics.get().blocks_size)
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_received)
#print(blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840'))
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_sent)
#est = blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt')
#tt = test.transactions

addr = '3Admys6487vaTxm3BRhFe62sD5NUoJVn9L'
#tt = blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840')

main_address = blockchain.blockexplorer.get_address(addr)

balance = main_address.final_balance

output_addrs={}
input_addrs={}
tran_id = []
time = []
amt_spent = []
amt_got = []

sum_in = 0
sum_out = 0
imp_trans = []

for i in main_address.transactions:
    tran_id.append(i.hash)
    time.append(datetime.utcfromtimestamp(int(i.time)).strftime('%Y-%m-%d %H:%M:%S'))
#    for j in i.outputs:
#        if (j.address == addr):
#            amt_got.append(j.value)
#            print(j.value)
#        output_addrs.append(j.address)
    for j in i.inputs:
        try:
            if (j.address == addr):
                amt_spent.append(j.value)
                for x in i.outputs:
                    if x.address not in output_addrs.keys():
                        output_addrs[x.address] = []
                    output_addrs[x.address].append(x.value)
                    #output_addrs.append(x.address)
                print('+++++++++++++++++++++', j.value)
            #input_addrs.append(j.address)
            if j.address not in input_addrs.keys():
                input_addrs[j.address] = []
            input_addrs[j.address].append(j.value)
        except:
            input_addrs.append('[]')
             
#freq_addrs_out = Counter(output_addrs)
#freq_addrs_out = freq_addrs_out.most_common
#freq_addrs_in = Counter(input_addrs)
#freq_addrs_in = freq_addrs_in.most_common
freq_addrs_in = sorted(input_addrs, key=lambda k: len(input_addrs[k]), reverse=True)
freq_addrs_out = sorted(output_addrs, key=lambda k: len(output_addrs[k]), reverse=True)

amt_addrs_in = {key: sum(input_addrs[key]) for key in input_addrs}
amt_addrs_in = sorted(amt_addrs_in, key=lambda x: amt_addrs_in[x], reverse=True)
amt_addrs_out = {key: sum(output_addrs[key]) for key in output_addrs}
amt_addrs_out = sorted(amt_addrs_out, key=lambda x: amt_addrs_out[x], reverse=True)

try:
    freq_addrs_in.remove(addr)
    amt_addrs_in.remove(addr)
    freq_addrs_out.remove(addr)
    amt_addrs_out.remove(addr)
except:
    1
final_list = []
for i in freq_addrs_out, amt_addrs_out, freq_addrs_in, amt_addrs_in:
    try:
        for j in i[0:10]:
            final_list.append(j)
    except:
        for j in i:
            final_list.append(j)

final_list = (Counter(final_list)).most_common








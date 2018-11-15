#from blockchain import statistics
import blockchain
from collections import Counter
from datetime import datetime
#print(statistics.get().blocks_size)

#print(blockchain.statistics.get().blocks_size)
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_received)
#print(blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840'))
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_sent)
#est = blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt')
#tt = test.transactions

addr = '3Nxwenay9Z8Lc9JBiywExpnEFiLp6Afp8v'
#tt = blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840')

main_address = blockchain.blockexplorer.get_address(addr)

balance = main_address.final_balance

output_addrs=[]
input_addrs=[]
tran_id = []
time = []
amt_spent = []
amt_got = []

sum_in = 0
sum_out = 0
for i in main_address.transactions:
    tran_id.append(i.hash)
    time.append(datetime.utcfromtimestamp(int(i.time)).strftime('%Y-%m-%d %H:%M:%S'))
    for j in i.outputs:
        if (j.address == addr):
            amt_got.append(j.value)
            print(j.value)
        output_addrs.append(j.address)
    for j in i.inputs:
        try:
            if (j.address == '1AK4LYE6PYwBmSYHQX3v2UsXXHTvCAsJeK'):
                amt_spent.append(j.value)
                print('+++++++++++++++++++++', j.value)
            input_addrs.append(j.address)                
        except:
            input_addrs.append('[]')
             
freq_addrs_out = Counter(output_addrs)
freq_addrs_out = freq_addrs_out.most_common
freq_addrs_in = Counter(input_addrs)
freq_addrs_in = freq_addrs_in.most_common
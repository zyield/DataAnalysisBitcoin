import psycopg2


try:
    conn = psycopg2.connect(dbname='chainspark_data', user='chaispark_admin', host='db-nddw4l3bc3tfwslpm46rcbae5e.coegqtcbi3dz.us-west-2.rds.amazonaws.com', password='jYjFkgRqpGhNQoKpWF3KgDNw')
except Exception as e:
    print ("I am unable to connect to the database", str(e))
    
cur = conn.cursor()

def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS label_wallets(wallet_name TEXT NOT NULL, address TEXT PRIMARY KEY NOT NULL,
                                                          type TEXT NOT NULL)''')
    conn.commit()

def read_from_db():
    cur.execute("SELECT address FROM label_wallets WHERE wallet_name='bitfinex'")                 #getting the data all at once
    l = []
    for data in cur.fetchall():
        print(data[0])
        l.append(data)
    print(len(l))
  
read_from_db()
      
if(conn):
    cur.close()
    conn.close()
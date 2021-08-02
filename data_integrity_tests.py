import sqlite3
import pandas as pd

path = './'
dbfilename = 'test01'

con = sqlite3.connect(path+dbfilename+'.db')

def is_relocation_nagative(conn):
    
    df = pd.read_sql_query("SELECT * from relocation", conn)
    
    df['dquantity'] = df['quantity']*df['direction']

    for date in pd.unique(df['date']):
        slicedf = df[df['date']<= date].copy()

        if (int(slicedf.groupby(['q_id','site_name','equip_type_name']).sum()[['dquantity']].min())<0):
            print ('error'+str(date))
            return date
    return 0

is_relocation_nagative(con)

def reconcile_bf_account_vs_externalparties(conn):

    conn.execute(
    'DROP VIEW IF EXISTS ReconcileEPBF ;'
    )

    conn.execute("""
    CREATE VIEW ReconcileEPBF AS

    SELECT ma_account_id, bf_amount - EPSUM AS BFDIFF FROM (SELECT ma_account_id AS MID, SUM(amount) AS EPSUM FROM ep_bf GROUP BY ma_account_id)
    LEFT JOIN (SELECT bf_amount, ma_account_id FROM account_bf) on MID = ma_account_id
    """)
    return pd.read_sql_query("SELECT * FROM ReconcileEPBF" %(table), conn)

reconcile_bf_account_vs_externalparties(con)

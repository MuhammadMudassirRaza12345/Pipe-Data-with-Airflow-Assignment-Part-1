import mysql.connector as sql
import pandas as pd


def transform(**kwargs):
    db_connection = sql.connect(host='127.0.0.1', database='complaindb', user='root', password='root')
    db_cursor = db_connection.cursor()
     # uesd 4000 because max limit is 4166 in googlesheet
    db_cursor.execute('SELECT * FROM  complaints LIMIT 4000')
    table_rows = db_cursor.fetchall()
    df1 = pd.DataFrame(table_rows,columns=['product','complaint_what_happened','date_sent_to_company','issue','sub_product','zip_code','tags','has_narrative','complaint_id','timely','consumer_consent_provided','company_response','submitted_via','company','date_received','state','consumer_disputed','company_public_response','sub_issue'])
    df2=df1.drop(columns =['complaint_what_happened', 'date_sent_to_company','zip_code','tags','has_narrative','consumer_consent_provided','consumer_disputed','company_public_response'])
    df2['Month Year'] = pd.to_datetime(df2['date_received']).dt.strftime('%d/%m/%Y')
    df3 = df2.groupby(['product','issue','sub_product','timely','company_response','submitted_via','company', 'date_received','state','sub_issue','Month Year'],as_index= False)['complaint_id'].nunique()
    df3.rename(columns = {'complaint_id':'Count of Complaints_id'}, inplace = True)
    kwargs['ti'].xcom_push(key="transform_data",values=df3) 

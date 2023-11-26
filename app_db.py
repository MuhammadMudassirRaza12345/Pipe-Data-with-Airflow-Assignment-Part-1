import pymysql
from pymysql import cursors
 

def dumb_db(**kwargs):
    # result = kwargs['ti'].xcom_pull(key='extracted_data')

    def create_connection():
        connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='root',
                                database='complaindb',
                                cursorclass=pymysql.cursors.DictCursor)
        return connection    

    def query_table_create():
        connection = create_connection()
        query='''CREATE TABLE IF NOT EXISTS complaints
                (product text, 
                complaint_what_happened text, 
                date_sent_to_company text, 
                issue text, 
                sub_product text, 
                zip_code text, 
                tags text, 
                has_narrative text,
                complaint_id integer, 
                timely text, 
                consumer_consent_provided text, 
                company_response text, 
                submitted_via text, 
                company text, 
                date_received text, 
                state text, 
                consumer_disputed text, 
                company_public_response text, 
                sub_issue text)'''

        with connection:
            connection.ping(reconnect=True)
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()

    def insert(result):
        connection = create_connection()
        table=query_table_create()
               
        with connection:
            with connection.cursor() as cursor:
                # query = "INSERT INTO `daraz_tables` (`id`,`name`,`product_image_url`,`product_original_price`, `discount`,`product_current_price`, `productUrl`) VALUES  (%s, %s, %s,%s, %s, %s, %s) "
                query="INSERT INTO `complaints` (`product`, `complaint_what_happened`, `date_sent_to_company`, `issue`, `sub_product`, `zip_code`, `tags`, `has_narrative`,`complaint_id`, `timely`, `consumer_consent_provided`, `company_response`, `submitted_via`, `company`, `date_received`, `state`, `consumer_disputed`, `company_public_response`, `sub_issue`)  VALUES  (%s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s)"
                cursor.executemany(query, result)
                connection.commit()
           
    result = kwargs['ti'].xcom_pull(task_ids="extract_data", key="extract_data_all ")
    insert(result)
    print("data sent successfully to database")
     

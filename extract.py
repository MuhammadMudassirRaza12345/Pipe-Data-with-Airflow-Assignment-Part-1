import requests
import json
from datetime import date, timedelta
 
 
  
 
result=[]
 

def extract(**kwargs):
           
    def get_state(city):
        # i will used 100 because of space issue in my local machine
        size = 500
        time_delta = 365
        max_date = (date.today()).strftime("%Y-%m-%d")
        min_date = (date.today() - timedelta(days=time_delta)).strftime("%Y-%m-%d") 
        city =  city
        url = f'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?field=complaint_what_happened&size={size}&date_received_max={max_date}&date_received_min={min_date}&state={city}'
        print(url)
        response = requests.get(url, timeout=1000)
        data = json.loads(response.text)
        return data

    def get_data(city):
        city = city
        data = get_state(city)
        for j in range(len(data['hits']['hits'])):
            data1=(
                data['hits']['hits'][j]['_source']['product'] ,
                data['hits']['hits'][j]['_source']['complaint_what_happened'],
                data['hits']['hits'][j]['_source']['date_sent_to_company'],
                data['hits']['hits'][j]['_source']['issue'],
                data['hits']['hits'][j]['_source']['sub_product'],
                data['hits']['hits'][j]['_source']['zip_code'],
                data['hits']['hits'][j]['_source']['tags'],
                data['hits']['hits'][j]['_source']['has_narrative'],
                data['hits']['hits'][j]['_source']['complaint_id'],
                data['hits']['hits'][j]['_source']['timely'],
                data['hits']['hits'][j]['_source']['consumer_consent_provided'],
                data['hits']['hits'][j]['_source']['company_response'],
                data['hits']['hits'][j]['_source']['submitted_via'],
                data['hits']['hits'][j]['_source']['company'],
                data['hits']['hits'][j]['_source']['date_received'],
                data['hits']['hits'][j]['_source']['state'],
                data['hits']['hits'][j]['_source']['consumer_disputed'],
                data['hits']['hits'][j]['_source']['company_public_response'],
                data['hits']['hits'][j]['_source']['sub_issue'])
            result.append(data1)

    state = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL','IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    for i in  range(len(state)):
        city=  state[i]
        get_data(city)
    kwargs['ti'].xcom_push(key="extract_data_all",values=result)                  
                
         

           

 
 

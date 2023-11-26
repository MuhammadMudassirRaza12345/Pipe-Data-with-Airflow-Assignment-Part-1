import pandas as pd
#now comment because i used this in download now need
import pygsheets 
import streamlit as st
 
from plotly.subplots import make_subplots
 
from plotly.graph_objs import *
import plotly.graph_objects as go
 
import plotly.express as px

# I will download the data through google sheet API and then will use it in streamlit

path='your credentials to access google sheet'
gc = pygsheets.authorize(service_account_file=path)
sh=gc.open('data')
wk=sh[0] 
 
df1 = wk.get_as_df(index_column=1)
# print(df)
df2=pd.DataFrame(df1)
print(df2)




 #to chech state
# print(df2['state'].unique())
#O: AZ,AR,CT,AK,,CO,DE,AL,CA
# st.write(df1.head(10))

 

st.set_page_config(layout="wide")
st.title('Consumer Financial Complaints Dashboard')
 
  
state  = st.selectbox('Select a state:',("All States", "AZ", "AR", "CT", "AK", "CO", "DE", "AL", "CA"))

st.subheader( f"Display Data For {state}") 

if state == "All States":
    df_selection = df2
else:
    df_selection = df2.query("state == @state")
 
total_no_complaints=pd.to_numeric(df_selection['Count of Complaints_id']).sum()
total_complaints_with_closed_status = pd.to_numeric(df_selection.loc[df_selection['company_response'] == 'Closed with explanation','Count of Complaints_id']).sum()
timely_respond_complaints = pd.to_numeric(df_selection.loc[df_selection['timely'] == 'Yes','Count of Complaints_id']).sum()
total_complaints_with_in_progress = pd.to_numeric(df_selection.loc[df_selection['company_response'] == 'In progress','Count of Complaints_id' ]).sum()


def create_kpi(val,text,format,title_color,font_colr,header_size,value_size):
    return (go.Indicator(
        value = val,
        title= {"text":text,"font":{"size":15,"family":'Times New Roman',"color": title_color}},
        number={'valueformat':format,"font":{"size":50,"family":'Times New Roman',"color": font_colr}},
    ))
 


with st.container():
    col1, col2,col3,col4= st.columns((1,1,1,1))
    with col1.container():
         col1.plotly_chart(go.Figure(create_kpi(total_no_complaints,'Total no of Complaints(T.N.O.C)',',d%','#09AB3B','#33FFFF',20,80)).update_layout(autosize=True,width=200,height=150))
         
            
    with col2.container(): 
        col2.plotly_chart(go.Figure(create_kpi(total_complaints_with_closed_status,'T.N.O.C with Closed Status',',d%', '#09AB3B','#33FFFF',20,80)).update_layout(autosize=True,width=200,height=150))
        
            
    with col3.container():
        col3.plotly_chart(go.Figure(create_kpi(timely_respond_complaints,'Timely Responded Complaints',',d%','#09AB3B', '#33FFFF',20,80)).update_layout(autosize=True,width=200,height=150))
        

    with col4.container():  
        col4.plotly_chart(go.Figure(create_kpi(total_complaints_with_in_progress,'T.N.O.C with In Progress Status',',d%','#09AB3B', '#33FFFF',20,80)).update_layout(autosize=True,width=200,height=150))
        
            
             
    

        
 
complaints_by_product_labels = df_selection.groupby('product')['Count of Complaints_id'].sum().reset_index().sort_values(by='product')['product'].values


complaints_by_product_values = df_selection.groupby('product')['Count of Complaints_id'].sum().reset_index().sort_values(by='Count of Complaints_id')['Count of Complaints_id'].values

data = [go.Bar(
   x = complaints_by_product_labels,
   y = complaints_by_product_values,
   marker={'color': complaints_by_product_values,'colorscale': 'ylorrd'}
 )]
layout = go.Layout(title='Horizontal Bar Plot of Number of Complaints by Product')

bar_fig = go.Figure(data=data,layout=layout)

 

 
 

complaints_by_Monthyear_labels = df_selection.groupby('Month Year')['Count of Complaints_id'].sum().reset_index().sort_values(by='Month Year' ,ascending=True)['Month Year'].values
count_of_complaint = df_selection.groupby('Month Year')['Count of Complaints_id'].sum().reset_index().sort_values(by='Count of Complaints_id')['Count of Complaints_id'].values



 
fig = px.line( x=complaints_by_Monthyear_labels, y=count_of_complaint, 
            title="Line Chart of Number Over Complaints Time (Month Year)")
 

with st.container():
        col_5, col_6= st.columns(2)
        
        
        col_5.plotly_chart(bar_fig, use_container_width=True)
       
        col_6.plotly_chart(fig, use_container_width=True)
        

# pie chart
submited_via_labels = df_selection.groupby('submitted_via')['Count of Complaints_id'].sum().reset_index().sort_values(by='submitted_via')['submitted_via'].values
submited_via_values = df_selection.groupby('submitted_via')['Count of Complaints_id'].sum().reset_index().sort_values(by='Count of Complaints_id')['Count of Complaints_id'].values
pie_fig = px.pie(values=submited_via_values, names=submited_via_labels,
                 title="Pie Chart of Number of Complaints by Submitted Via Channel")
pie_fig.update_layout(title={
    'text': "Pie Chart of Number of Complaints by Submitted Via Channel",
    'y':1,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})
# tree map
no_treemap_issues = df_selection.groupby(['issue', 'sub_issue'])['Count of Complaints_id'].sum().reset_index()
fig_treemap = px.treemap(no_treemap_issues, path=['issue','sub_issue', 'Count of Complaints_id'],
                          values = 'Count of Complaints_id', color = 'sub_issue',
                          title="Treemap of Number Over Complaints by Issue and Sub-Issue")


with st.container():
	col_7, col_8= st.columns(2)
	# col_7.subheader()
	col_7.plotly_chart(pie_fig, use_container_width=True)

	# col_8.subheader("Treemap of Number Over Complaints by Issue and Sub-Issue")
	col_8.plotly_chart(fig_treemap, use_container_width=True)

 

with st.container():
    st.title("Design By: MUHAMMAD MUDASSIR RAZA")
     








 
 

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as plt
import requests
import json

connection=mysql.connector.connect(       
    host='localhost',
    user='root',
    password='12345678',
    database='ProjectTwo_PhonePE')
cursor=connection.cursor()

cursor.execute("SELECT * from AggregateTxn")
table1=cursor.fetchall()
Aggregate_Trans=pd.DataFrame(table1, columns=("State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

cursor.execute("SELECT * from AggregateUser")
table2=cursor.fetchall()
Aggregate_User=pd.DataFrame(table2, columns=("State","Year","Quarter","Brand","Count","Percentage"))

cursor.execute("SELECT * from MapTxn")
table3=cursor.fetchall()
Map_Txn=pd.DataFrame(table3, columns=("State","Year","Quarter","Districts","Transaction_count","Transaction_amount"))

cursor.execute("SELECT * from MapUser")
table4=cursor.fetchall()
Map_User=pd.DataFrame(table4, columns=("State","Year","Quarter","Districts","Registered_Users","App_Opens"))

cursor.execute("SELECT * from TopTxn")
table5=cursor.fetchall()
Top_Txn=pd.DataFrame(table5, columns=("State","Year","Quarter","Pincode","Transaction_count","Transaction_amount"))

cursor.execute("SELECT * from TopUser")
table6=cursor.fetchall()
Top_User=pd.DataFrame(table6, columns=("State","Year","Quarter","Pincode","Registered_Users"))

#function for bar chart and map
def txn_acy(df,year):
    tacy=df[df['Year']==year]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    col3,col4=st.columns(2)
    with col1:
        plot1=plt.bar(tacyg, x="State",y="Transaction_amount",title=f"Transaction Amount Plot for {year}",color_discrete_sequence=plt.colors.sequential.algae_r,height=500,width=650)
        st.plotly_chart(plot1)
    with col2:
        plot2=plt.bar(tacyg, x="State",y="Transaction_count",title=f"Transaction Count Plot for {year}",color_discrete_sequence=plt.colors.sequential.Bluered_r, height=500,width=650)
        st.plotly_chart(plot2)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1['features']:
        states_name.append(feature['properties']['ST_NM'])
    states_name.sort()
    with col3:
        map1=plt.choropleth(tacyg,geojson=data1,locations="State", featureidkey="properties.ST_NM",
                           color="Transaction_amount", color_continuous_scale="armyrose",
                           range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                           hover_name="State",title=f"Transaction Amount Map for {year}", fitbounds="locations",
                           height=800,width=600)
        map1.update_geos(visible=False)
        st.plotly_chart(map1)
    with col4:
        map2=plt.choropleth(tacyg,geojson=data1,locations="State", featureidkey="properties.ST_NM",
                           color="Transaction_count", color_continuous_scale="twilight",
                           range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                           hover_name="State",title=f"Transaction Count Map for {year}", fitbounds="locations",
                           height=800,width=600)
        map2.update_geos(visible=False)
        st.plotly_chart(map2)
    
#dataframe to filter year
def yearfn(df,year):
    tacy=df[df['Year']==year]
    return tacy       

#dataframe to filter quarter
def quarterfn(df,quarter):
    tacyq=df[df['Quarter']==quarter]
    return tacyq

# Aggregate Txn-transaction type
def Trans_typeQ(df,state):
    tacy=df[df['State']==state]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        pie1=plt.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount",width=600,title=f"{state} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(pie1)
    with col2:
        pie2=plt.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count",width=600,title=f"{state} TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(pie2)


# Map Txn-district
def DistrictsQ(df,state):
    tacy=df[df['State']==state]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        plot3=plt.bar(tacyg, x="Transaction_amount",y="Districts",title=f"Transaction Amount for {state}",color_discrete_sequence=plt.colors.sequential.Aggrnyl)    
        st.plotly_chart(plot3)
    with col2:
        plot4=plt.bar(tacyg, x="Transaction_count",y="Districts",title=f"Transaction Count for {state}",color_discrete_sequence=plt.colors.sequential.Aggrnyl)
        st.plotly_chart(plot4)

# Top Txn-Pincode
def PincodeQ(df,state):
    tacy=df[df['State']==state]
    tacy.reset_index(drop=True,inplace=True)
    col1,col2=st.columns(2)
    with col1:
        plot5=plt.bar(tacy, x='Quarter',y="Transaction_amount",hover_data="Pincode",title=f"Transaction Amount for {state}", color_discrete_sequence= plt.colors.sequential.Rainbow)
        st.plotly_chart(plot5)
    with col2:
        plot6=plt.bar(tacy, x='Quarter',y="Transaction_count",hover_data="Pincode",title=f"Transaction Count for {state}",color_discrete_sequence= plt.colors.sequential.Rainbow)
        st.plotly_chart(plot6)
        
# Aggregate User
def aggre_user1(df,year):
    auy=df[df['Year']==year]
    auy.reset_index(drop=True,inplace=True)
    auyg=pd.DataFrame(auy.groupby("Brand")["Count"].sum())
    auyg.reset_index(inplace=True)
    plot9=plt.bar(auyg, x='Brand',y="Count",title=f"Brand VS Count for {year}",color_discrete_sequence= plt.colors.sequential.amp_r)
    st.plotly_chart(plot9)

def aggre_user2(df,quarter):
    auyq=df[df['Quarter']==quarter]
    auyq.reset_index(drop=True,inplace=True)
    auyqg=pd.DataFrame(auyq.groupby("Brand")[["Count","Percentage"]].sum())
    auyqg.reset_index(inplace=True)
    plot10=plt.bar(auyqg, x='Brand',y="Count",title=f"Brand VS Count for Q{quarter}",hover_data="Percentage",color_discrete_sequence= plt.colors.sequential.haline_r)
    st.plotly_chart(plot10)

#Map User
def map_user1(df,year):
    muy=df[df['Year']==year]
    muy.reset_index(drop=True,inplace=True)
    muyg=pd.DataFrame(muy.groupby("State")[["Registered_Users","App_Opens"]].sum())
    muyg.reset_index(inplace=True)
    plot11=plt.line(muyg, x='State',y=["Registered_Users","App_Opens"],title=f"Registered User and App Open for {year} ",markers=True)
    st.plotly_chart(plot11)
    
def map_user2(df,quarter):
    muyq=df[df['Quarter']==quarter]
    muyq.reset_index(drop=True,inplace=True)
    muyqg=pd.DataFrame(muyq.groupby("State")[["Registered_Users","App_Opens"]].sum())
    muyqg.reset_index(inplace=True)
    plot12=plt.line(muyqg, x='State',y=["Registered_Users","App_Opens"],title=f"Registered User and App Open for Q{quarter} ",markers=True)
    st.plotly_chart(plot12)


#Top User
def top_user1(df,year):
    tuy=df[df['Year']==year]
    tuy.reset_index(drop=True,inplace=True)
    tuyg=pd.DataFrame(tuy.groupby(["State","Quarter"])["Registered_Users"].sum())
    tuyg.reset_index(inplace=True)
    plot7=plt.bar(tuyg, x='State',y="Registered_Users",hover_data="State",color="Quarter",title=f"Registered User for the year {year}", width=1200,height=800,color_continuous_scale= plt.colors.sequential.Agsunset_r)
    st.plotly_chart(plot7)

def top_user2(df,state):
    tuys=df[df['State']==state]
    tuys.reset_index(drop=True,inplace=True)
    plot8=plt.bar(tuys, x='Quarter',y="Registered_Users",hover_data="Pincode",color="Registered_Users",title=f"Registered User VS Quarter", color_continuous_scale= plt.colors.sequential.Agsunset,width=1000,height=500)
    st.plotly_chart(plot8)

#QUERY
def query123(table):
    connection=mysql.connector.connect(       
        host='localhost',
        user='root',
        password='12345678',
        database='ProjectTwo_PhonePE')
    cursor=connection.cursor()
    query1=f''' SELECT State, SUM(Transaction_amount) as Transaction_Amount FROM {table}
              GROUP BY State ORDER BY Transaction_Amount DESC LIMIT 10;'''
    cursor.execute(query1)
    table1=cursor.fetchall()
    col1,col2=st.columns(2)
    col3,col4=st.columns(2)
    
    with col3:
        df1=pd.DataFrame(table1,columns=("State","Transaction Amount"))
        st.write(df1)
    with col1:
        plot1=plt.bar(df1, x="State",y="Transaction Amount",title=f"Transaction Amount VS State for {table}",hover_name="State",color_discrete_sequence=     plt.colors.sequential.algae_r,height=550,width=500)
        st.plotly_chart(plot1)
    
    query2=f''' SELECT State, SUM(Transaction_count) as Transaction_Count FROM {table}
              GROUP BY State ORDER BY Transaction_Count DESC LIMIT 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    
    with col4:
        df2=pd.DataFrame(table2,columns=("State","Transaction Count"))
        st.write(df2)
    with col2:
        plot2=plt.bar(df2, x="State",y="Transaction Count",title=f"Transaction Count VS State for {table}",hover_name="State",color_discrete_sequence= plt.colors.sequential.algae_r,height=550,width=500)
        st.plotly_chart(plot2)

def query4(table):
    connection=mysql.connector.connect(       
        host='localhost',
        user='root',
        password='12345678',
        database='ProjectTwo_PhonePE')
    cursor=connection.cursor()
    query4=f''' SELECT State, AVG(Count) as Transaction_Count FROM {table}
              GROUP BY State ORDER BY Transaction_Count;'''
    cursor.execute(query4)
    table3=cursor.fetchall()
    df3=pd.DataFrame(table3,columns=("State","Transaction Count"))
    plot3=plt.bar(df3, x="State",y="Transaction Count",title=f"Transaction Count VS State for {table}",hover_name="State",color_discrete_sequence= plt.colors.sequential.amp_r,height=550,width=500)
    st.plotly_chart(plot3)
    st.write(df3)

def query5(table, state):
    query5=f''' SELECT Districts, SUM(Registered_Users) as Registered_Users FROM {table} WHERE State='{state}'
                  GROUP BY Districts ORDER BY Registered_Users;'''
    cursor.execute(query5)
    table4=cursor.fetchall()
    df4=pd.DataFrame(table4,columns=("Districts","Registered_Users"))
    plot4=plt.bar(df4, x="Districts",y="Registered_Users",title=f"Registered_Users VS Districts for {state}",color_discrete_sequence= plt.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(plot4)
    st.write(df4)
    
def query8(table,year):
    query8=f''' SELECT Brand, SUM(Count) as Transaction_Count FROM {table} WHERE year={year}
                      GROUP BY Brand ORDER BY Transaction_Count;'''
    cursor.execute(query8)
    table7=cursor.fetchall()
    df7=pd.DataFrame(table7,columns=("Brand","Transaction_Count"))
    plot7=plt.bar(df7, x="Brand",y="Transaction_Count",title=f"Transaction_Count VS Brand for the year {year}",color_discrete_sequence=             plt.colors.sequential.Blackbody_r,height=650,width=600)
    st.plotly_chart(plot7)
    st.write(df7)

#Streamlit code
st.set_page_config(layout="wide")
st.title("Phonepe Pulse Data Visualization and Exploration")
with st.sidebar:
    select=option_menu("Menu",["HOME","DATA VISUALIZATION","DATA ANALYSIS"])
if select=="HOME":
    st.subheader("Key Takeaways")
    st.write("1. Data extraction from Phonepe github repository")
    st.write("2. Data transformation using Python")
    st.write("3. Data insertion using MYSQL")
    st.write("4. Data visualization using Plotly in Streamlit")
    st.write("5. Data analysis and graphical representation using SQL queries")


elif select=="DATA VISUALIZATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with tab1:
        method1=st.radio("Select a Method",["Aggregate Transaction","Aggregate User"])
        if method1== "Aggregate Transaction":
            st.subheader("YEAR-WISE ANALYSIS:")
            years1=st.radio("Select a year for aggregate txn", Aggregate_Trans['Year'].unique())
            txn_acy(Aggregate_Trans,years1)
            st.subheader("QUARTER-WISE ANALYSIS:")
            quarter1=st.radio("Select a quarter for aggregate txn", Aggregate_Trans['Quarter'].unique())
            state1=st.selectbox("Select a state for aggregate txn", Aggregate_Trans['State'].unique())
            Trans_typeQ(quarterfn(yearfn(Aggregate_Trans,years1),quarter1),state1)
            
        elif method1=="Aggregate User":
            st.subheader("YEAR-WISE ANALYSIS:")
            years2=st.radio("Select a year for aggregate user", Aggregate_User['Year'].unique())
            aggre_user1(Aggregate_User,years2)
            st.subheader("QUARTER-WISE ANALYSIS:")
            quarter2=st.radio("Select a quarter for aggregate user", Aggregate_User['Quarter'].unique())
            aggre_user2(yearfn(Aggregate_User,years2),quarter2)
            
          
    with tab2:
        method2=st.radio("Select a Method",["Map Transaction","Map User"])
        if method2== "Map Transaction":
            st.subheader("YEAR-WISE ANALYSIS:")
            years3=st.radio("Select a year for map txn",Map_Txn['Year'].unique())
            txn_acy(Map_Txn,years3)
            st.subheader("QUARTER-WISE ANALYSIS:")
            quarter3=st.radio("Select a quarter for map txn", Map_Txn['Quarter'].unique())
            state2=st.selectbox("Select a state for map txn", Map_Txn['State'].unique())
            DistrictsQ(quarterfn(yearfn(Map_Txn,years3),quarter3),state2)
            
        elif method2=="Map User":
            st.subheader("YEAR-WISE ANALYSIS:")
            years4=st.radio("Select a year for map user",Map_User['Year'].unique())
            map_user1(Map_User,years4)
            st.subheader("QUARTER-WISE ANALYSIS:")
            quarter4=st.radio("Select a quarter for map user", Map_User['Quarter'].unique())
            map_user2(yearfn(Map_User,years4),quarter4)
            
            
    with tab3:
        method3=st.radio("Select a Method",["Top Transaction","Top User"])
        if method3== "Top Transaction":
            st.subheader("YEAR-WISE ANALYSIS:")
            years5=st.radio("Select a year for top txn",Top_Txn['Year'].unique())
            txn_acy(Top_Txn,years5)
            st.subheader("QUARTER-WISE ANALYSIS:")
            state3=st.selectbox("Select a state for top txn", Top_Txn['State'].unique())
            PincodeQ(yearfn(Top_Txn,years5),state3)
            
        elif method3=="Top User":
            st.subheader("YEAR-WISE ANALYSIS:")
            years6=st.radio("Select a year for top user",Top_User['Year'].unique())
            top_user1(Top_User,years6)
            st.subheader("QUARTER-WISE ANALYSIS:")
            state4=st.selectbox("Select a state for top user", Top_User['State'].unique())
            top_user2(yearfn(Top_User,years6),state4)
        

elif select=="DATA ANALYSIS":   
    question=st.selectbox("Select the question",["1. Amount and Count for Aggregate Transaction for top 10 states",
                                                 "2. Amount and Count for Map Transaction for top 10 states",
                                                 "3. Amount and Count for Top Transaction for top 10 states",
                                                 "4. Average Count for Aggregate User for all states",
                                                 "5. Registered User Count for Map User for all districts in a state",
                                                 "6. App Opens for Map User for top 15 states",
                                                 "7. Registered User Count for Top User for all 4 quarters in a year 2023",
                                                 "8. All brands Transaction Count for Aggregate User in a year",
                                                 "9. Registered User Count for Top User based on pincode for the state Tamil Nadu",
                                                 "10. Amount and Count for Aggregate Transaction based on transaction type"])
    if question=="1. Amount and Count for Aggregate Transaction for top 10 states":
        query123("AggregateTxn")
    elif question=="2. Amount and Count for Map Transaction for top 10 states":
        query123("MapTxn")
    elif question=="3. Amount and Count for Top Transaction for top 10 states":
        query123("TopTxn")
    elif question=="4. Average Count for Aggregate User for all states":
        query4("AggregateUser")
    elif question=="5. Registered User Count for Map User for all districts in a state":
        stateq1=st.selectbox("Select a state", Map_User['State'].unique())
        query5("MapUser",stateq1)
    elif question=="6. App Opens for Map User for top 15 states":
        query6=f''' SELECT State, SUM(App_Opens) as App_Opens FROM MapUser
                  GROUP BY State ORDER BY App_Opens DESC LIMIT 15;'''
        cursor.execute(query6)
        table5=cursor.fetchall()
        df5=pd.DataFrame(table5,columns=("State","App_Opens"))
        plot5=plt.scatter(df5, x="State",y="App_Opens",title=f"App_Opens VS State",color_discrete_sequence= plt.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(plot5)
        st.write(df5)
    elif question=="7. Registered User Count for Top User for all 4 quarters in a year 2023":
        query7=f''' SELECT Quarter, SUM(Registered_Users) as Registered_Users FROM TopUser WHERE year=2023
                          GROUP BY Quarter ORDER BY Registered_Users LIMIT 15;'''
        cursor.execute(query7)
        table6=cursor.fetchall()
        df6=pd.DataFrame(table6,columns=("Quarter","Registered_Users"))
        plot6=plt.line(df6, x="Quarter",y="Registered_Users",title=f"Registered_Users VS Quarter",        color_discrete_sequence=plt.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(plot6)
        st.write(df6)
    elif question=="8. All brands Transaction Count for Aggregate User in a year":
        yearq1=st.selectbox("Select a year", Aggregate_User['Year'].unique())
        query8("AggregateUser",yearq1)
    elif question=="9. Registered User Count for Top User based on pincode for the state Tamil Nadu":
        query9=f''' SELECT Pincode,SUM(Registered_Users) as Registered_Users FROM TopUser WHERE State="Tamil Nadu"
                      GROUP BY Pincode ORDER BY Registered_Users;'''
        cursor.execute(query9)
        table8=cursor.fetchall()
        df8=pd.DataFrame(table8,columns=("Pincode","Registered_Users"))
        plot8=plt.scatter(df8, x="Pincode",y="Registered_Users",symbol="Pincode",title=f"Registered_Users VS Pincode for Tamil Nadu",color_discrete_sequence=           plt.colors.sequential.Blackbody,height=650,width=600)
        st.plotly_chart(plot8)
        st.write(df8)
    elif question=="10. Amount and Count for Aggregate Transaction based on transaction type":
        query10=f''' SELECT Transaction_type,SUM(Transaction_amount) as Transaction_amount,SUM(Transaction_count) as Transaction_count
                     FROM AggregateTxn GROUP BY Transaction_type ORDER BY Transaction_amount;'''
        cursor.execute(query10)
        table9=cursor.fetchall()
        df9=pd.DataFrame(table9,columns=("Transaction_type","Transaction_amount","Transaction_count"))
        col1,col2=st.columns(2)
        with col1:
            fig_pie1=plt.pie(df9, names="Transaction_type", values="Transaction_amount",width=600,title=f"Transaction_amount VS Transaction_type",hole=0.5)
            st.plotly_chart(fig_pie1)
            st.write(df9)
        with col2:
            fig_pie2=plt.pie(df9, names="Transaction_type", values="Transaction_count",width=600,title=f"Transaction_count VS Transaction_type",hole=0.5)
            st.plotly_chart(fig_pie2)
            
    
    
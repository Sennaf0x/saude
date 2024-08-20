import streamlit as st
import altair as alt
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from openai import OpenAI
import json
from datetime import datetime

# Configração de página layuot
st.set_page_config(layout="wide")

# CSS da página
st.markdown('''
            <style>
            .grid-container-0{
                display: grid; 
                grid-template-columns: repeat(3,1fr);
                justify-content: space-between;
            }
            .grid-container-1{
                display: grid; 
                grid-template-columns: repeat(4, 1fr);
                justify-content: space-between;
            }
            .grid-container{
                display: grid; 
                grid-template-columns: repeat(4, 1fr);
            }
            .card-0{
                border: 1px solid #ccc; 
                    color: black;
                    text-align: center;
                    align-items:center;
                    padding: 10px; 
                    margin: 5px;
                    box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
            }
            .card{
                border: 1px solid #ccc; 
                    color: black;
                    text-align: center;
                    align-items:center;
                    padding: 10px; 
                    margin: 5px;
                    box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
            }
            .card-1 {
                    font-size: 12px;
                    background: black;
                    color: white; 
                    border: 1px solid white; 
                    text-align: center;
                    align-items:center;
                    padding: 10px; 
                    margin: 5px;
                    box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset;
                    }
                    
            .eqpbllx1{
                    background-color: #00C6A9;
                    color: white;
                    font-family: "Georgia", Times, Times New Roman, serif;
            }
    
            .eqpbllx1:hover{
                    color: white;
                    background-color: black;
                    }
            
            .e10yg2by1{
                background-color: white;
                margin-top: 10px;
                align-items: center; 
            }
            
            .ef3psqc7{
                background-color: #00C6A9;
                margin: auto;
            }
            
            .e116k4er3{
                border: 1px solid #00C6A9;
            }
            
            .card-2 {
                    font-size: 12px;
                    background: black;
                    color: white; 
                    border: 1px solid white; 
                    text-align: center;
                    align-items:center;
                    padding: 10px; 
                    margin: 5px;
                    box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset;
            }
            
            @media (max-width: 480px) {
            .grid-container{
                display: grid; 
                font-size: 11px;
                grid-template-columns: repeat(4, 0.2fr 0.2fr, 0.2fr, 0.6fr);
                justify-content: space-between;
            }
            .card{
                font-size: 11px;
                }   
            .card-1{
                font-size: 11px;
                }   
            }
            
            </style>
            ''',unsafe_allow_html=True)


# Configurando dia e hora atual

agora = datetime.now()
dia = agora.strftime("%d/%m/%Y") 
hora = agora.strftime("%H:%M:%S") 

# Conectando no google sheets

    
if 'gsheets' not in st.session_state:
    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],ttl=5)
    existing_data = existing_data.dropna(how="all")
    st.session_state['gsheets'] = existing_data 

df = pd.DataFrame(st.session_state['gsheets'])

pesoState = st.session_state['gsheets']['Peso']

with st.container():
    st.write('''    
             <h1>Gráficos</h1>
             ''',unsafe_allow_html=True)

#expander do peso
with st.expander("Peso (kg)"):

# Tratando dados do gsheets   
    peso_df = st.session_state['gsheets']['Peso']
    pesoData_df = st.session_state['gsheets']['Data_peso']
    df_peso = {'Data_peso':pesoData_df,'Peso':peso_df}
    peso_chart = pd.DataFrame(data=df_peso)
# plotando gráfico
    chart = alt.Chart(peso_chart).mark_bar().encode(
        x='Data_peso',
        y='Peso'
    )
    st.altair_chart(chart, use_container_width=True)

#Expander da pressão
with st.expander("Pressão"):
# Tratando dados do gsheets   
    pressao_df = st.session_state['gsheets']['Pressao_max']
    pressao_mindf = st.session_state['gsheets']['Pressao_min']
    batimento_df = st.session_state['gsheets']['Batimento']
    pressaoData_df = st.session_state['gsheets']['Data']
    df_peso = {'Data':pressaoData_df,'Pressao_max':pressao_df,'Pressao_min':pressao_mindf,'Batimento':batimento_df}
    pressao_chart = pd.DataFrame(data=df_peso)
# plotando gráfico
    chart2 = alt.Chart(pressao_chart).mark_bar().encode(
        x='Data',
        y='Pressao_max'
    )
    st.altair_chart(chart2, use_container_width=True)

with st.expander("Glicose"):
# Tratando dados do gsheets   
    glicose_df = st.session_state['gsheets']['Glicose']
    glicoseData_df = st.session_state['gsheets']['Data_glicose']
    df_glicose = {'Data_glicose':glicoseData_df,'Glicose':glicose_df}
    glicose_chart = pd.DataFrame(data=df_glicose)
# plotando gráfico
    chart3 = alt.Chart(glicose_chart).mark_bar().encode(
        x='Data_glicose',
        y='Glicose'
    )
    st.altair_chart(chart3, use_container_width=True)

##expander urina        
with st.expander("Urina"):
    # Tratando dados do gsheets   
    urina_df = st.session_state['gsheets']['Urina']
    urinaData_df = st.session_state['gsheets']['Data_urina']
    df_urina = {'Data_urina':urinaData_df,'Urina':urina_df}
    urina_chart = pd.DataFrame(data=df_urina)
# plotando gráfico
    chart4 = alt.Chart(urina_chart).mark_bar().encode(
        x='Data_urina',
        y='Urina'
    )
    st.altair_chart(chart4, use_container_width=True)
#
##expander água        
with st.expander("Água"):
# Tratando dados do gsheets   
    agua_df = st.session_state['gsheets']['Agua']
    aguaData_df = st.session_state['gsheets']['Data_agua']
    df_agua = {'Data_agua':aguaData_df,'Agua':agua_df}
    agua_chart = pd.DataFrame(data=df_agua)
# plotando gráfico
    chart5 = alt.Chart(agua_chart).mark_bar().encode(
        x='Data_agua',
        y='Agua'
    )
    st.altair_chart(chart5, use_container_width=True)
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

#expander do peso
peso_df = st.session_state['gsheets']['Peso']
pesoData_df = st.session_state['gsheets']['Data_peso']
df_peso = {'Data_peso':pesoData_df,'Peso':peso_df}
peso_chart = pd.DataFrame(data=df_peso)

#Expander da pressão
pressao_df = st.session_state['gsheets']['Pressao_max']
pressao_mindf = st.session_state['gsheets']['Pressao_min']
batimento_df = st.session_state['gsheets']['Batimento']
pressaoData_df = st.session_state['gsheets']['Data']
pressaoHora_df = st.session_state['gsheets']['Hora']
df_peso = {'Data':pressaoData_df,'Hora':pressaoHora_df,'Pressao_max':pressao_df,'Pressao_min':pressao_mindf,'Batimento':batimento_df}
pressao_chart = pd.DataFrame(data=df_peso)

#expander Glicose
glicose_df = st.session_state['gsheets']['Glicose']
glicoseData_df = st.session_state['gsheets']['Data_glicose']
df_glicose = {'Data_glicose':glicoseData_df,'Glicose':glicose_df}
glicose_chart = pd.DataFrame(data=df_glicose)

#expander urina        
urina_df = st.session_state['gsheets']['Urina']
urinaData_df = st.session_state['gsheets']['Data_urina']
df_urina = {'Data_urina':urinaData_df,'Urina':urina_df}
urina_chart = pd.DataFrame(data=df_urina)
#expander água        
agua_df = st.session_state['gsheets']['Agua']
aguaData_df = st.session_state['gsheets']['Data_agua']
df_agua = {'Data_agua':aguaData_df,'Agua':agua_df}
agua_chart = pd.DataFrame(data=df_agua)

with st.container():
    st.write('''
             <h1>Tabelas</h1>
             ''',unsafe_allow_html=True)
                    
    with st.expander("Pressão"):
        # Cabeçalho da tabela
        st.write('''
                <div class="grid-container">
                        <div class="card-2"><strong>PMáx (Psi)</strong></div>
                        <div class="card-2"><strong>PMin (Psi)</strong></div>
                        <div class="card-2"><strong>BPM</strong></div>
                        <div class="card-2"><strong>Data</strong></div>
                        <div class="card-2"><strong>Hora</strong></div>
                    </div>
                ''',unsafe_allow_html=True)
        
        pressao_chart = pressao_chart.dropna(how="all")
        for row in pressao_chart.itertuples(index=True):
            st.write(f'''
                    <div class="grid-container">
                        <div class="card-0">{row.Pressao_max}</div>
                        <div class="card-0">{row.Pressao_min}</div>
                        <div class="card-0">{row.Batimento}</div>
                        <div class="card-0">{row.Data}</div>
                        <div class="card-0">{row.Hora}</div>
                    ''',unsafe_allow_html=True)    

    with st.expander("Glicose"):        
        # Cabeçalho da tabela
        st.write('''
                <div class="grid-container">
                        <div class="card-1"><strong>Glicose</strong></div>
                        <div class="card-1"><strong>Data</strong></div>
                    </div>
                ''',unsafe_allow_html=True)
        
        glicose_chart = glicose_chart.dropna(how="all")
        for row in glicose_chart.itertuples(index=True):
            st.write(f'''
                    <div class="grid-container">
                        <div class="card">{row.Glicose}</div>
                        <div class="card">{row.Data_glicose}</div>
                    ''',unsafe_allow_html=True)          
    
    with st.expander("Urina"):        
        # Cabeçalho da tabela
        st.write('''
                <div class="grid-container">
                        <div class="card-1"><strong>Urina</strong></div>
                        <div class="card-1"><strong>Data</strong></div>
                    </div>
                ''',unsafe_allow_html=True)
        
        urina_chart = urina_chart.dropna(how="all")
        for row in urina_chart.itertuples(index=True):
            st.write(f'''
                    <div class="grid-container">
                        <div class="card">{row.Urina}</div>
                        <div class="card">{row.Data_urina}</div>
                    ''',unsafe_allow_html=True)          
    
    with st.expander("Água"):        
        # Cabeçalho da tabela
        st.write('''
                <div class="grid-container">
                        <div class="card-1"><strong>Água</strong></div>
                        <div class="card-1"><strong>Data</strong></div>
                    </div>
                ''',unsafe_allow_html=True)
        
        agua_chart = agua_chart.dropna(how="all")
        for row in agua_chart.itertuples(index=True):
            st.write(f'''
                    <div class="grid-container">
                        <div class="card">{row.Agua}</div>
                        <div class="card">{row.Data_agua}</div>
                    ''',unsafe_allow_html=True)          
    
    with st.expander("Peso"):        
        # Cabeçalho da tabela
        st.write('''
                <div class="grid-container">
                        <div class="card-1"><strong>Peso</strong></div>
                        <div class="card-1"><strong>Data</strong></div>
                    </div>
                ''',unsafe_allow_html=True)
        
        peso_chart = peso_chart.dropna(how="all")
        for row in peso_chart.itertuples(index=True):
            st.write(f'''
                    <div class="grid-container">
                        <div class="card">{row.Peso}</div>
                        <div class="card">{row.Data_peso}</div>
                    ''',unsafe_allow_html=True)          
import streamlit as st
import altair as alt
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from openai import OpenAI
import json
from datetime import datetime

# Configração de página layuot
st.set_page_config(
    layout="wide",
    page_title="Home"
    )

# CSS da página
st.markdown('''
            <style>
            
            *{
                margin: 0;
                padding: 0;
                
            }
            
            .titulo1{
                background-color: #132c0d;
                margin: 10px 0;
                text-align: center;
                color: white;
                width: 100%;
                border-radius: 10px;
                box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
            }
            
            .block-container{
                background-color: #00C6A9;
            }
            
            .flex{
                display: flex;
                margin: 10px;
                width: 100%;
                flex-direction: inline; 
                justify-content: space-between;
                box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
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
                font-size: 14px;
                width: 100%;
                color: black;
                text-align: center;
                background-color: white;
                margin: 1px;
                align-items:center;
                border-radius: 10px 100px / 120px;
                background: rgba(219, 234, 213, 0.3);
                }
            .card-1 {
                border-radius: 10px 100px / 120px;
                font-size: 14px;
                width: 100%;
                background-color: #132c0d;
                color: white; 
                text-align: center;
                align-items:center;
                margin:0;
                }
                    
            .eqpbllx1{
                    background-color: #132c0d;
                    color: white;
                    border-radius: 10px;
                    font-family: "Georgia", Times, Times New Roman, serif;
            }
    
            .eqpbllx1:hover{
                    color: white;
                    background-color: black;
                    }
    
            .eqpbllx0{
                background-color: #00C6A9;
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
            
            .eczjsme11{
                background-color: white;
                color: #00C6A9;
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
            .flex{
                font-size: 10px
                background-color: rgba(19, 44, 13, 1);
                }
            .card{
                font-size: 11px;
                border-radius: 10px;
                text-align: center;
                align-items: center;
                align-self: center;
                padding: 5px;
                }   
            .card-1{
                padding: 5px;
                align-items: center;
                border-radius: 10px;
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

if 'peso' not in st.session_state:
    if df.empty:
        st.session_state['peso'] = 'Sem dados'
    else:    
        dfPeso = pd.DataFrame(pesoState).dropna(how="all")
        st.session_state['peso'] = dfPeso.iloc[-1][0]
  
# Exibindo o peso do dia atual

if 'hora' not in st.session_state:
    st.session_state['hora'] = hora

if 'data' not in st.session_state:
    st.session_state['data'] = dia
    
#col1, col2 = st.columns([0.7, 0.3])
with st.container():
    st.write(f'''
                <div class="flex green-color">
                    <div class="flex"> 
                        <div class= "card-1">Data de hoje</div>    
                        <div class= "card">{dia}</div>
                    </div>
                    <div class="flex"> 
                        <div class="card-1">Hora atual</div>
                        <div class="card">{hora}</div>
                    </div>
                    <div class="flex"> 
                        <div class="card-1">Peso Diário (Kg)</div>
                        <div class="card">{st.session_state['peso']}</div>
                    </div>
                </div>
                    ''', unsafe_allow_html=True)

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
    df_peso = {'Data':pressaoData_df,'Pressao_max':pressao_df,'Pressao_min':pressao_mindf,'Batimento':batimento_df}
    pressao_chart = pd.DataFrame(data=df_peso)
#with st.expander("Glicose"):
    glicose_df = st.session_state['gsheets']['Glicose']
    glicoseData_df = st.session_state['gsheets']['Data_glicose']
    df_glicose = {'Data_glicose':glicoseData_df,'Glicose':glicose_df}
    glicose_chart = pd.DataFrame(data=df_glicose)
##expander urina        
    urina_df = st.session_state['gsheets']['Urina']
    urinaData_df = st.session_state['gsheets']['Data_urina']
    df_urina = {'Data_urina':urinaData_df,'Urina':urina_df}
    urina_chart = pd.DataFrame(data=df_urina)
#expander água        
    agua_df = st.session_state['gsheets']['Agua']
    aguaData_df = st.session_state['gsheets']['Data_agua']
    df_agua = {'Data_agua':aguaData_df,'Agua':agua_df}
    agua_chart = pd.DataFrame(data=df_agua)

#Formulários
st.write('''
         <h1 class="titulo1">Insira os dados</h1>
         ''',unsafe_allow_html=True)   

col3, col4, col5, col6, col7 = st.columns(5)

with st.container():    

    with col3:
        with st.expander("Adicione PRESSÃO"):
            with st.form(key="form1"):
                pressao_max = st.number_input('Insira a pressão máxima', key="pressao_max")
                pressao_min = st.number_input('Insira a pressão mínima', key="pressao_min")
                batimento = st.number_input('Insira s batimentos cardiácos', key="batimento")
                submit_button1 = st.form_submit_button(label='+Pressão')
                if submit_button1:
                    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],ttl=5)
                    st.session_state['gsheets'] = st.session_state['gsheets'].dropna(how="all")
                    if pressao_max == 0: 
                        st.error('Insira os valores nos campos obrigatórios')
                    else: 
                        new_data = pd.DataFrame({
                                                "Pressao_max":[pressao_max],
                                                "Data":[dia], 
                                                "Hora":[hora],
                                                "Pressao_min":[pressao_min],
                                                "Batimento":[batimento] 
                                                })
                        updated_df = pd.concat([st.session_state['gsheets'], new_data], ignore_index=True)
                        #st.session_state['df'].to_csv('dados.csv', index=False)
                        st.success("Dados adicionados com sucesso!")

                        #Atualizando a planilha
                        conn.update(spreadsheet=url, data=updated_df)
                        st.rerun()
    
    with col4:
        with st.expander(" Adicione GLICOSE"):
            with st.form(key="form2"):
                glicose = st.number_input('Insira a glicose', key="glicose")
                submit_button2 = st.form_submit_button(label='+Glicose')
            if submit_button2:
                url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
                conn = st.connection("gsheets", type=GSheetsConnection)
                st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],ttl=5)
                st.session_state['gsheets'] = st.session_state['gsheets'].dropna(how="all")
                if glicose == 0: 
                    st.error('Insira os valores nos campos obrigatórios')
                else: 
                    new_data = pd.DataFrame({
                                            "Glicose":[glicose],
                                            "Data_glicose":[dia], 
                                            "Hora_glicose":[hora], 
                                            })
                    updated_df = pd.concat([st.session_state['gsheets'], new_data], ignore_index=True)
                    #st.session_state['df'].to_csv('dados.csv', index=False)
                    st.success("Dados adicionados com sucesso!")
                    #Atualizando a planilha
                    conn.update(spreadsheet=url, data=updated_df)

    with col5:
        with st.expander("Adicione URINA"):    
            with st.form(key="form3"):
                urina = st.number_input('Insira a urina', key="urina")
                submit_button3 = st.form_submit_button(label='+Urina')
            if submit_button3:
                st.session_state['gsheets'] = st.session_state['gsheets'].dropna(how="all")
                if urina == 0: 
                    st.error('Insira os valores nos campos obrigatórios')
                else: 
                    new_data = pd.DataFrame({
                                            "Urina":[urina],
                                            "Data_urina":[dia], 
                                            "Hora_urina":[hora], 
                                            })
                    updated_df = pd.concat([st.session_state['gsheets'], new_data], ignore_index=True)
                    #st.session_state['df'].to_csv('dados.csv', index=False)
                    st.success("Dados adicionados com sucesso!")

                    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],ttl=5)

                    #Atualizando a planilha
                    conn.update(spreadsheet=url, data=updated_df)
    
    with col6:
        with st.expander("Adicione ÁGUA"):    
            with st.form(key="form4"):
                agua = st.number_input('Insira a água', key="agua")
                submit_button4 = st.form_submit_button(label='+Água')

            if submit_button4:
                url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
                conn = st.connection("gsheets", type=GSheetsConnection)
                st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],ttl=5)
                st.session_state['gsheets'] = st.session_state['gsheets'].dropna(how="all")
                if agua == 0: 
                    st.error('Insira os valores nos campos obrigatórios')
                else: 
                    new_data = pd.DataFrame({
                                            "Agua":[agua],
                                            "Data_agua":[dia], 
                                            "Hora_agua":[hora], 
                                            })
                    updated_df = pd.concat([st.session_state['gsheets'], new_data], ignore_index=True)
                    #st.session_state['df'].to_csv('dados.csv', index=False)
                    st.success("Dados adicionados com sucesso!")
                    #Atualizando a planilha
                    conn.update(spreadsheet=url, data=updated_df)
    with col7:
        with st.expander("Adicione PESO"):
            with st.form(key="form5"):
                peso1 = st.number_input('Insira seu peso', key="peso1")
                submit_button5 = st.form_submit_button(label='+Peso')

                if submit_button5:
                    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],ttl=5)
                    st.session_state['gsheets'] = st.session_state['gsheets'].dropna(how="all")
                    if peso1 == 0: 
                        st.error('Insira os valores nos campos obrigatórios')
                    else: 
                        new_data = pd.DataFrame({
                                                "Peso":[peso1],
                                                "Data_peso":[dia], 
                                                "Hora_peso":[hora], 
                                                })
                        updated_df = pd.concat([st.session_state['gsheets'], new_data], ignore_index=True)
                        #st.session_state['df'].to_csv('dados.csv', index=False)
                        st.success("Dados adicionados com sucesso!")
                        #Atualizando a planilha
                        conn.update(spreadsheet=url, data=updated_df)
                        st.rerun()          
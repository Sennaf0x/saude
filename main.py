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
            .grid-container-1{
                display: grid; 
                grid-template-columns: repeat(3, 1fr);
                justify-content: space-between;
            }
            .grid-container{
                display: grid; 
                grid-template-columns: repeat(3, 1fr);
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
    existing_data = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],ttl=5)
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
    
col1, col2 = st.columns(2)
with col1:
    st.write(f'''
                <div class="grid-container-1">
                    <div> 
                        <p class= "card-1">Data de hoje</p>
                        <p class= "card">{dia}</p>
                    </div>
                    <div> 
                        <p class="card-1">Hora atual</p>
                        <p class="card">{hora}</p>
                    </div>
                    <div> 
                        <p class="card-1">Peso Diário (Kg)</p>
                        <p class="card">{st.session_state['peso']}</p>
                    </div>
                </div>
                    ''', unsafe_allow_html=True)

# Configurando session states

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
    pressao_df = st.session_state['gsheets']['Pressao']
    pressaoData_df = st.session_state['gsheets']['Data']
    df_peso = {'Data':pressaoData_df,'Pressao':pressao_df}
    pressao_chart = pd.DataFrame(data=df_peso)
# plotando gráfico
    chart2 = alt.Chart(pressao_chart).mark_bar().encode(
        x='Data',
        y='Pressao'
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

#Formulários
st.write('''
         <h1>Insira os dados</h1>
         ''',unsafe_allow_html=True)   

col3, col4, col5, col6, col7 = st.columns(5)

with st.container():    

    with col3:
        with st.form(key="form1"):
            pressao = st.number_input('Insira a pressão', key="pressao")
            submit_button1 = st.form_submit_button(label='+Pressão')
            if submit_button1:
                url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
                conn = st.connection("gsheets", type=GSheetsConnection)
                st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13],ttl=5)
                st.session_state['gsheets'] = st.session_state['gsheets'].dropna(how="all")
                if pressao == 0: 
                    st.error('Insira os valores nos campos obrigatórios')
                else: 
                    new_data = pd.DataFrame({
                                            "Pressao":[pressao],
                                            "Data":[dia], 
                                            "Hora":[hora], 
                                            })
                    updated_df = pd.concat([st.session_state['gsheets'], new_data], ignore_index=True)
                    #st.session_state['df'].to_csv('dados.csv', index=False)
                    st.success("Dados adicionados com sucesso!")

                    #Atualizando a planilha
                    conn.update(spreadsheet=url, data=updated_df)
                    st.rerun()
    
    with col4:
        with st.form(key="form2"):
            glicose = st.number_input('Insira a glicose', key="glicose")
            submit_button2 = st.form_submit_button(label='+Glicose')
        if submit_button2:
            url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
            conn = st.connection("gsheets", type=GSheetsConnection)
            st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11],ttl=5)
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
                st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13],ttl=5)
                
                #Atualizando a planilha
                conn.update(spreadsheet=url, data=updated_df)
    with col6:
        with st.form(key="form4"):
            agua = st.number_input('Insira a água', key="agua")
            submit_button4 = st.form_submit_button(label='+Água')
            
        if submit_button4:
            url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
            conn = st.connection("gsheets", type=GSheetsConnection)
            st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13],ttl=5)
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
        with st.form(key="form5"):
            peso1 = st.number_input('Insira seu peso', key="peso1")
            submit_button5 = st.form_submit_button(label='+Peso')
            
            if submit_button5:
                url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
                conn = st.connection("gsheets", type=GSheetsConnection)
                st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13],ttl=5)
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

with st.container():
    st.write('''
             <h1>Tabelas</h1>
             ''',unsafe_allow_html=True)
                    
    with st.expander("Pressão"):
        # Cabeçalho da tabela
        st.write('''
                <div class="grid-container">
                        <div class="card-1"><strong>Pressao (Psi)</strong></div>
                        <div class="card-1"><strong>Data</strong></div>
                    </div>
                ''',unsafe_allow_html=True)
        
        pressao_chart = pressao_chart.dropna(how="all")
        for row in pressao_chart.itertuples(index=True):
            st.write(f'''
                    <div class="grid-container">
                        <div class="card">{row.Pressao}</div>
                        <div class="card">{row.Data}</div>
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
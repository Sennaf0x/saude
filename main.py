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

# Conectando no google sheets

if 'gsheets' not in st.session_state:
    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11],ttl=5)
    existing_data = existing_data.dropna(how="all")
    st.session_state['gsheets'] = existing_data


# Configurando dia e hora atual

agora = datetime.now()
dia = agora.strftime("%d/%m/%Y") 
hora = agora.strftime("%H:%M:%S") 

if 'hora' not in st.session_state:
    st.session_state['hora'] = hora

if 'data' not in st.session_state:
    st.session_state['data'] = dia
# Configurando session states

with st.container():
    st.write('''
             <h1>Gráficos</h1>
             ''',unsafe_allow_html=True)

    with st.expander("Pressão"):
        url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
        conn = st.connection("gsheets", type=GSheetsConnection)
        existing_data = conn.read(spreadsheet=url, usecols=[0,1],ttl=5)
        existing_data = existing_data.dropna(how="all")

        df = pd.DataFrame(existing_data)

        chart = alt.Chart(df).mark_bar().encode(
            x='Data',
            y='Pressao'
        )

        st.altair_chart(chart, use_container_width=True)        

    with st.expander("Glicose"):
        url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
        conn = st.connection("gsheets", type=GSheetsConnection)
        existing_data = conn.read(spreadsheet=url, usecols=[3,4],ttl=5)
        existing_data = existing_data.dropna(how="all")

        df = pd.DataFrame(existing_data)

        chart = alt.Chart(df).mark_bar().encode(
            x='Data_glicose',
            y='Glicose'
        )

        st.altair_chart(chart, use_container_width=True)
        
    with st.expander("Urina"):
        url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
        conn = st.connection("gsheets", type=GSheetsConnection)
        existing_data = conn.read(spreadsheet=url, usecols=[6,7],ttl=5)
        existing_data = existing_data.dropna(how="all")

        df = pd.DataFrame(existing_data)

        chart = alt.Chart(df).mark_bar().encode(
            x='Data_urina',
            y='Urina'
        )

        st.altair_chart(chart, use_container_width=True)

col1, col2 = st.columns(2)
with st.container():
    st.write('''
             <h1>Insira os dados</h1>
             ''',unsafe_allow_html=True)
    with col1:
        st.write(f'''<div> 
                    <p>Data de hoje</p>
                    <p>{dia}</p>
                    </div>
                    ''',unsafe_allow_html=True)
    with col2:
        st.write(f'''<div> 
                    <p>Hora atual</p>
                    <p>{hora}</p>
                    </div>
                    ''', unsafe_allow_html=True)

col3, col4, col5, col6 = st.columns(4)

#Formulários

with st.container():
    with col3:
        with st.form(key="form1"):
            pressao = st.number_input('Insira a pressão', key="pressao")
            submit_button = st.form_submit_button(label='+Pressão')
        if submit_button:
            url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
            conn = st.connection("gsheets", type=GSheetsConnection)
            st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11],ttl=5)
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
    
    with col4:
        with st.form(key="form2"):
            glicose = st.number_input('Insira a glicose', key="glicose")
            submit_button = st.form_submit_button(label='+Glicose')
        if submit_button:
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
            submit_button = st.form_submit_button(label='+Urina')
        if submit_button:
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
                st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11],ttl=5)
                
                #Atualizando a planilha
                conn.update(spreadsheet=url, data=updated_df)
    with col6:
        with st.form(key="form4"):
            agua = st.number_input('Insira a água', key="agua")
            submit_button = st.form_submit_button(label='+Água')
            
        if submit_button:
            url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
            conn = st.connection("gsheets", type=GSheetsConnection)
            st.session_state['gsheets'] = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9,10,11],ttl=5)
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
                    
with st.expander("Pressão"):
    # Estabelecendo conexão com o gsheets
    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(spreadsheet=url, usecols=[0,1,2],ttl=5)
    existing_data = existing_data.dropna(how="all")
    df = pd.DataFrame(existing_data)
    
    # Cabeçalho da tabela
    st.write('''
            <div class="grid-container">
                    <div class="card-1"><strong>Pressa (Psi)</strong></div>
                    <div class="card-1"><strong>Data</strong></div>
                    <div class="card-1"><strong>Hora</strong></div>
                </div>
             ''',unsafe_allow_html=True)
    
    for row in existing_data.itertuples(index=True):
        st.write(f'''
                <div class="grid-container">
                    <div class="card">{row.Pressao}</div>
                    <div class="card">{row.Data}</div>
                    <div class="card">{row.Hora}</div>
                ''',unsafe_allow_html=True)    

with st.expander("Glicose"):
    # Estabelecendo conexão com o gsheets
    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(spreadsheet=url, usecols=[3,4,5],ttl=5)
    existing_data = existing_data.dropna(how="all")
    df = pd.DataFrame(existing_data)
    
    # Cabeçalho da tabela
    # st.write('Medição de glicose')
    st.write('''
            <div class="grid-container">
                    <div class="card-1"><strong>Glicose</strong></div>
                    <div class="card-1"><strong>Data</strong></div>
                    <div class="card-1"><strong>Hora</strong></div>
                </div>
             ''',unsafe_allow_html=True)
    
    for row in existing_data.itertuples(index=True):
        st.write(f'''
                <div class="grid-container">
                    <div class="card">{row.Glicose}</div>
                    <div class="card">{row.Data_glicose}</div>
                    <div class="card">{row.Hora_glicose}</div>
                ''',unsafe_allow_html=True)

with st.expander("Urina"):
    # Estabelecendo conexão com o gsheets
    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(spreadsheet=url, usecols=[6,7,8],ttl=5)
    existing_data = existing_data.dropna(how="all")
    df = pd.DataFrame(existing_data)
    
    # Cabeçalho da tabela
    # st.write('Volume de Urina expelido')
    st.write('''
            <div class="grid-container">
                    <div class="card-1"><strong>Urina</strong></div>
                    <div class="card-1"><strong>Data</strong></div>
                    <div class="card-1"><strong>Hora</strong></div>
                </div>
             ''',unsafe_allow_html=True)
    
    for row in existing_data.itertuples(index=True):
        st.write(f'''
                <div class="grid-container">
                    <div class="card">{row.Urina}</div>
                    <div class="card">{row.Data_urina}</div>
                    <div class="card">{row.Hora_urina}</div>
                ''',unsafe_allow_html=True)

with st.expander("Consumo de Água"):
    # Estabelecendo conexão com o gsheets
    url = "https://docs.google.com/spreadsheets/d/15Ci0Xv_lTrXfbelTJH13bg7tuIkxgCJFdLoKeft1UWA/edit?gid=0#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(spreadsheet=url, usecols=[9,10,11],ttl=5)
    existing_data = existing_data.dropna(how="all")
    df = pd.DataFrame(existing_data)
    
    # Cabeçalho da tabela
    # st.write('Consumo de água')
    st.write('''
            <div class="grid-container">
                    <div class="card-1"><strong>Água</strong></div>
                    <div class="card-1"><strong>Data</strong></div>
                    <div class="card-1"><strong>Hora</strong></div>
                </div>
             ''',unsafe_allow_html=True)
    
    for row in existing_data.itertuples(index=True):
        st.write(f'''
                <div class="grid-container">
                    <div class="card">{row.Agua}</div>
                    <div class="card">{row.Data_agua}</div>
                    <div class="card">{row.Hora_agua}</div>
                ''',unsafe_allow_html=True)
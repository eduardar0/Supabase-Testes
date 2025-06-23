import re
from datetime import datetime

import ipeadatapy as ipea
import streamlit as st
import pandas as pd

from data.operacoes_bd import  inserir_nova_serie

#Pesquisa
codigo_serie = st.selectbox("Selecione a série", ipea.metadata(measure="R$")) # Obtem o código da série
dataframe_serie = ipea.timeseries(codigo_serie).iloc[::-1] #Inverte o dataframe contendo os dados de atualização da série
ultima_atualizacao = dataframe_serie.iloc[0]["RAW DATE"]# Seleciona a primeira linha da coluna de data de atualização
ultima_atualizacao = re.sub(r"[a-zA-Z].*", "", ultima_atualizacao)# Regex que retira informações desnecessárias
ultima_atualizacao

#Inserção no BD
email_usuario = st.text_input("Email do usuário")
margem = st.text_input("Margem de atualização")

if email_usuario != "" and margem != "" and margem.isnumeric() != False:
    margem = int(margem)
    try:
        if st.button("Inserir no BD"):
            inserir_nova_serie(codigo_serie, email_usuario, margem, ultima_atualizacao)
            "Inserção bem sucedida!"
    except:
        "Inserção falhou."
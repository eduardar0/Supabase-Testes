from datetime import datetime

import ipeadatapy as ipea
import streamlit as st

import services.async_service.cronJob as CJ
from data.connect import supabase as bd

posicao = 0

# Pegar todas a série
seriesBD = bd.table("series").select("*").execute()  # Armazena tabela series
seriesBD = seriesBD.data  # Pega os dados da tabela
serie = seriesBD[posicao]  # Seleciona uma serie específica
f"""
    ID DA SÉRIE NO BD: {serie["id"]}\n
    CODIGO DA SÉRIE: {serie["codigo_serie"]}\n
    EMAIL DO USUÁRIO: {serie["email_usuario"]}\n
    MARGEM DE ENVIO DE ALERTA: {serie["margem"]}%\n
    ÚLTIMA CHECAGEM: {serie["ultima_checagem"]}\n
    ÚLTIMO ALERTA: {serie["ultimo_alerta"]}\n
    ÚLTIMA ATUALIZAÇÃO: {serie["ultima_atualizacao"]}\n
"""

#Pega os valores da série
valores = ipea.timeseries(serie["codigo_serie"]).iloc[::-1,-1]

#Pega data de hoje
hoje = str(datetime.now().date())

st.divider()

if st.button("Enviar alerta"):
    envio = CJ.enviar_alerta(serie, valores, hoje)
    "Alerta Enviado" if envio else "Alerta Não Enviado"
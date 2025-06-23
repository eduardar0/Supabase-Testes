import re
from datetime import datetime

import ipeadatapy as ipea
import streamlit as st

from data.operacoes_bd import alterar_ultima_checagem, alterar_ultima_atualizacao, alterar_ultimo_alerta
from data.connect import supabase as bd


def atualizar_datas(id_serie: str, data_ultima_checagem: str, data_ultimo_alerta: str, data_ultima_atualizacao: str):
    try:
        alterar_ultima_checagem(data_ultima_checagem, id_serie)
        alterar_ultimo_alerta(data_ultimo_alerta, id_serie)
        alterar_ultima_atualizacao(data_ultima_atualizacao, id_serie)
        return True
    except:
        return False


posicao = 0

# Pegar todas as séries
seriesBD = bd.table("series").select("*").execute()  # Armazena tabela series
seriesBD = seriesBD.data  # Pega os dados da tabela
serie = seriesBD[posicao]  # Seleciona um dado em específico
f"""
    ID DA SÉRIE NO BD: {serie["id"]}\n
    CODIGO DA SÉRIE: {serie["codigo_serie"]}\n
    FREQUÊNCIA DE ATUALIZAÇÃO: {serie["frequencia"]}\n
    EMAIL DO USUÁRIO: {serie["email_usuario"]}\n
    MARGEM DE ENVIO DE ALERTA: {serie["margem"]}%\n
    ÚLTIMA CHECAGEM: {serie["ultima_checagem"]}\n
    ÚLTIMO ALERTA: {serie["ultimo_alerta"]}\n
    ÚLTIMA ATUALIZAÇÃO: {serie["ultima_atualizacao"]}\n
"""

st.divider()

# Parte de atualização de datas
hoje = str(datetime.now().date())
ultima_atualizacao = ipea.timeseries(serie["codigo_serie"]).iloc[::-1]["RAW DATE"]
ultima_atualizacao = ultima_atualizacao.iloc[0]
ultima_atualizacao = re.sub(r"[A-Z].*", "", ultima_atualizacao)

if st.button("Atualizar datas"):
    atualizacao = atualizar_datas(id_serie=serie["id"], data_ultima_checagem=str(hoje), data_ultimo_alerta=str(hoje),
                                  data_ultima_atualizacao=ultima_atualizacao)
    st.divider()
    if atualizacao:

        seriesBD = bd.table("series").select("*").execute()
        seriesBD = seriesBD.data
        serie = seriesBD[posicao]

        f"""
            ID DA SÉRIE NO BD: {serie["id"]}\n
            CODIGO DA SÉRIE: {serie["codigo_serie"]}\n
            FREQUÊNCIA DE ATUALIZAÇÃO: {serie["frequencia"]}\n
            EMAIL DO USUÁRIO: {serie["email_usuario"]}\n
            MARGEM DE ENVIO DE ALERTA: {serie["margem"]}%\n
            ÚLTIMA CHECAGEM: {serie["ultima_checagem"]}\n
            ÚLTIMO ALERTA: {serie["ultimo_alerta"]}\n
            ÚLTIMA ATUALIZAÇÃO: {serie["ultima_atualizacao"]}\n
        """

    else:
        "Atualizacao de datas mal sucedida..."
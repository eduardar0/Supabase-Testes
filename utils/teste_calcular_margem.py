import ipeadatapy as ipea
import streamlit as st
import pandas as pd

from services.async_service import cronJob as CJ

#Pesquisa
codigo_serie = st.selectbox("Selecione", ipea.metadata(measure="R$"))
dataframe_serie = ipea.timeseries(codigo_serie).iloc[::-1] # Inverte o dataframe de ascendente pra descendente

#Parte do calculo de margem
valores = dataframe_serie.iloc[::,-1] #Atribui apenas a coluna dos valores (última coluna)
margem = CJ.calcular_margem(valores=valores)
f"Houve um {'aumento' if margem > 0 else 'decréscimo'} de {margem:.2f}% na série {codigo_serie} de acordo com a nova atualizacação."
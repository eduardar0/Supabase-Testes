from datetime import datetime
import re

import pandas as pd

def ultima_atualizacao_serie(dataframe_serie: pd.DataFrame):
    """

    :param dataframe_serie: Recebe um dataframde de série do IPEA retornado por timeseries
    :return: Retorna a data de última atualização do série.
    """
    dataframe_serie = dataframe_serie.iloc[::-1]["RAW DATE"]
    ultimaAtualizacao = dataframe_serie.iloc[0]
    ultimaAtualizacao = re.sub(r"[a-zA-Z].*", "", ultimaAtualizacao)
    ultimaAtualizacao = datetime.strptime(ultimaAtualizacao, "%Y-%m-%d").date()
    return ultimaAtualizacao

def gerar_alerta(codigo_serie: str, frequencia: str, ultima_atualizacao: datetime.date, margem: int):
    pass
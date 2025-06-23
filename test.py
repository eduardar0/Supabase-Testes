import re

import services.async_service.cronJob as CJ
from data.connect import supabase
from datetime import datetime

import ipeadatapy as ipea

from data.operacoes_bd import alterar_ultima_checagem, alterar_ultima_atualizacao

hoje = str(datetime.now().date())

series = supabase.table("series").select("*").or_(f"ultima_checagem.neq.{hoje},ultima_checagem.is.null").execute()

for serie in series.data:

    # Armazena o dataframe de atualizações da série de forma descendente
    dataframe_serie = ipea.timeseries(serie["codigo_serie"]).iloc[::-1]

    # Armazena a última coluna do dataframe que diz respeito aos valores
    valores = dataframe_serie.iloc[:, -1]

    # Realiza o envio de alerta de series novas no BD
    if serie["ultima_checagem"] is None:
        alterar_ultima_checagem(str(hoje), serie["id"])
        envio = CJ.enviar_alerta(serie, valores, str(hoje))
        if envio:
            print(f"Envio de alerta para ID {serie['id']} bem sucedido.")
        else:
            print(f"Envio de alerta para ID {serie['id']} mal sucedido.")

    else:

        # Armazena a data da última checagem realizada
        ultima_checagem = datetime.strptime(serie["ultima_checagem"], "%Y-%m-%d").date()

        # Atualiza a data de última checagem
        alterar_ultima_checagem(str(hoje), serie["id"])

        # Armazena a data da ultima atualização da serie no BD
        ultima_atualizacao_BD = datetime.strptime(serie["ultima_atualizacao"], "%Y-%m-%d").date()

        # Armazena a data de última atualização da série no IPEA
        ultima_atualizacao_IPEA = dataframe_serie.iloc[0]["RAW DATE"]
        ultima_atualizacao_IPEA = re.sub(r"[a-zA-Z].*", "", ultima_atualizacao_IPEA)
        ultima_atualizacao_IPEA = datetime.strptime(ultima_atualizacao_IPEA, "%Y-%m-%d").date()

        # Caso a serie não tenha sido checada hoje e a informação de última atualização da série no BD seja diferente do IPEA
        if ultima_atualizacao_BD != ultima_atualizacao_IPEA:

            alterar_ultima_atualizacao(str(ultima_atualizacao_IPEA), serie["id"])
            envio = CJ.enviar_alerta(serie, valores, str(hoje))
            if envio:
                print(f"Envio de alerta para ID {serie['id']} bem sucedido.")
            else:
                print(f"Envio de alerta para ID {serie['id']} mal sucedido.")


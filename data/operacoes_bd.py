from reportlab.lib.validators import isNumber

from data.connect import supabase

#Quando for inserir a serie no BD o campo de ultima atualizacao diz respeito a última atualização da série no IPEA
def inserir_nova_serie(codigo_serie: str, email_usuario: str, margem: int, ultima_atualizacao: str):
    if codigo_serie == "" or email_usuario == "" or isNumber(margem) == False or ultima_atualizacao == "":
        raise ValueError('Dados insuficientes.')

    try:
        # Tentativa de inserção
        resposta = (
            supabase.table("series")
            .insert({
                "codigo_serie": codigo_serie,
                "email_usuario": email_usuario,
                "margem": margem,
                "ultima_atualizacao": ultima_atualizacao
            })
            .execute()
        )

        return resposta.data  # Dados inseridos com sucesso

    except Exception as error:
        raise error

def alterar_ultima_atualizacao(data: str, idSerie: str):
    if(data == "" or idSerie == ""):
        raise ValueError('Dados insuficientes.')
    try:
        resposta = supabase.table("series").update({"ultima_atualizacao": data}).eq("id", idSerie).execute()
        return resposta.data
    except Exception as error:
        raise error

def alterar_ultimo_alerta(data: str, idSerie: str):
    # if (data == "" or idSerie == ""):
    #     raise ValueError('Dados insuficientes.')
    try:
        resposta = supabase.table("series").update({"ultimo_alerta": data}).eq("id", idSerie).execute()
        return resposta.data
    except Exception as error:
        raise error

def alterar_ultima_checagem(data: str, idSerie: str):
    # if (data == "" or idSerie == ""):
    #     raise ValueError('Dados insuficientes.')
    try:
        resposta = supabase.table("series").update({"ultima_checagem": data}).eq("id", idSerie).execute()
        return resposta.data
    except Exception as error:
        raise error
import requests
from sqlalchemy import create_engine
import os
import time
import pandas as pd
from sqlalchemy import text
from datetime import datetime

#---
DB_USER = os.getenv("DB_USER", 'postgres')
DB_PASS = os.getenv("DB_PASS", 'teste123')
DB_HOST = os.getenv("DB_HOST", 'localhost')
DB_PORT = os.getenv("DB_PORT", '5432')
DB_NAME = os.getenv("DB_NAME", 'db_ibge')

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

#---os identificadores dos países são os definidos pela norma ISO 3166-1 ALPHA-2, que define o identificador do país usando 2 letras
FILTRO_PAISES = {    "Brasil": "BR", "Argentina": "AR", "Uruguai": "UY", "Espanha": "ES", "Alemanha": "DE",
                     "Itália": "IT", "Estados Unidos": "US", "México": "MX", "Canadá": "CA", "China": "CN",
                     "Japão": "JP", "Nova Zelândia": "NZ", "Austrália": "AU", "Argélia": "DZ", "Egito": "EG",
                     "África do Sul": "ZA"
                }

INDICADORES_ID = {"chegada_turistas": 77819,
                  "gastos_publicos_educacao": 77820,
                  "gastos_publicos_saude": 77821
                 }

URL_IBGE = "https://servicodados.ibge.gov.br/api/v1/paises"

#---

def montar_url(indicador: str, paises=None):
    #https://servicodados.ibge.gov.br/api/v1/paises/AR%7CBR/indicadores/77819%7C77820
    
    if indicador not in INDICADORES_ID:
        raise ValueError(f"Indicador inválido: {indicador}")
    if paises is None:
        paises = list(FILTRO_PAISES.keys())
    
    siglas = [FILTRO_PAISES[p] for p in paises if p in FILTRO_PAISES]
    if not siglas:
        raise ValueError("Sigla de país não encontrada.")
    
    lista_siglas = "%7C".join(siglas)
    cod_indicador = str(INDICADORES_ID[indicador])
    
    return f"{URL_IBGE}/{lista_siglas}/indicadores/{cod_indicador}"

#---
def extrair_dados(indicador: str, paises=None, tentativas = 3, espera = 10):
    
    url_final = montar_url(indicador, paises)
    print(f"Extraindo dados da API")
    
    for tentativa in range(1, tentativas + 1):
        try:
            resposta = requests.get(url_final, timeout=6)
            resposta.raise_for_status()
            dados = resposta.json()
            if not dados:
                raise ValueError("Sem retorno de Dados.")
            
            return dados
        
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {tentativa} falhou: {e}")
        if tentativa < tentativas:
            time.sleep(espera * tentativa)
        else:
            raise Exception("Falha ao acessar a API do IBGE") from e
            
#---    
def normalizar_dados(dados_json):
    """{
    "id": 77819,
    "indicador": "Economia - Gastos públicos com educação",
    "unidade": {
      "id": "% do PIB",
      "classe": "N",
      "multiplicador": 1
    }"""
    df = []
    for indicador in dados_json:
        indicador_cod = indicador.get("id")
        indicador_nome = indicador.get("indicador")
        unidade_id = indicador.get("unidade", {}).get("id")  
        
        for serie in indicador.get("series", []):
            """ "series": [
        {
            "pais": {
            "id": "AR",
            "nome": "Argentina"
            }, """
            pais_id = serie.get("pais", {}).get("id")
            pais_nome = serie.get("pais", {}).get("nome")
            
            """ "serie": [
            {
                "-": null
            },
            {
                "1990": "1.07"
            } """
            
            for item in serie.get("serie", []):
                for ano, valor in item.items():
                    if valor is not None and "-" not in ano: #ignora intervalos ("1990-1995": null)
                        
                        df.append({
                            "indicador_id" : indicador_cod,
                            "indicador_nome" : indicador_nome,
                            "unidade_id" : unidade_id,
                            "pais_id" : pais_id,
                            "pais_nome" : pais_nome,
                            "ano" : int(ano),
                            "valor" : float(valor)
                        })
    
    df = pd.DataFrame(df)
    if not df.empty:
        df = df.dropna(subset=["indicador_id", "pais_id", "ano"])
        df = df.drop_duplicates(subset=["indicador_id", "pais_id", "ano"], keep="last")
                
        ano_atual = datetime.now().year
        df = df[df["ano"].between(1900, ano_atual)]
                
        df = df[df["valor"] >= 0]
        df = df[df["valor"] <= 1000]
        
                
    return pd.DataFrame(df)

#---
def salvar_db(df, tabela, engine, if_exists="replace"):
    
    if df.empty:
        print(f"Não existem dadoos em {tabela}")
        return
    
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"Conexão com o banco realizada.")
        
        df.to_sql(tabela, engine, if_exists=if_exists, index=False, method="multi")
        print(f"Dados salvos em '{tabela}' ({len(df)} linhas).")
        
        with engine.connect() as conn:
            conn.execute(text(f"""
                                  CREATE UNIQUE INDEX IF NOT EXISTS uq_{tabela}_indicador_pais_ano
                                  ON {tabela} (indicador_id, pais_id, ano);
                                  """))
        
    except Exception as e:
        print(f"Falha ao salvas os dados: {e}")
        raise
    
#--
if __name__ == "__main__":
     
    for indicador in INDICADORES_ID.keys():
         dados = extrair_dados(indicador)
         df_normalizado = normalizar_dados(dados)
         nome_tabela_db = indicador.lower()
         salvar_db(df_normalizado,  nome_tabela_db, engine, if_exists="replace")
         
    print(f"Dados processados e salvos no banco de dados")
    
    












from sqlalchemy import create_engine
import pandas as pd
import numpy as np 
import os 

os.system('cls')

try: 
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1') 
    
except Exception as e:
    print(f'Erro na conexão {e}')
    exit()

df_Ano_Estelionatos = df_ocorrencias[['mes_ano', 'estelionato']]

df_Ano_Estelionatos = df_Ano_Estelionatos.groupby('mes_ano', as_index=False)['estelionato'].sum()

df_munic_estelionato = df_ocorrencias[['munic', 'estelionato']]
df_munic_estelionato = df_munic_estelionato.groupby('munic', as_index=False)['estelionato'].sum()


try: 
    print('OBTENDO AS INFORMÇÕES SOBRE EM QUAIS MESES E ANOS APRENSETARAM OS MAIORES E MENORES QUANTIDADES DE ESTELIONATOS')

    array_estelionato = np.array(df_Ano_Estelionatos['estelionato'])

    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia = abs((media_estelionato - mediana_estelionato)/ mediana_estelionato * 100)

    print('\nTotal')
    print(40*'=')
    print(f'O total: {df_Ano_Estelionatos['estelionato'].sum()}')

    print('\nMedidas de Tendências Central')
    print(40*'=')
    print(f'A média: {media_estelionato}')
    print(f'A mediana: {mediana_estelionato}')
    print(f'A distancia entre média e mediana: {distancia:.2f} %')


    q1 = np.quantile(array_estelionato, 0.25)
    q2 = np.quantile(array_estelionato, 0.50)
    q3 = np.quantile(array_estelionato, 0.75)

    print('\nMedidas de posição')
    print(40*'=')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    df_estelionatos_menor = df_Ano_Estelionatos[df_Ano_Estelionatos['estelionato'] < q1 ]
    print('\nAnos com menores quantidades')
    print(40*'=')
    print(df_estelionatos_menor.head(10).sort_values(by='estelionato', ascending=True))
    
    df_estelionatos_maiores = df_Ano_Estelionatos[df_Ano_Estelionatos['estelionato'] > q3 ]
    print('\nAnos com maiores quantidades')
    print(40*'=')
    print(df_estelionatos_maiores.head(10))


    df_munic_estelionatos_menores = df_munic_estelionato[df_munic_estelionato['estelionato'] < q1 ]
    print('\nMunicipios com menores valores')
    print(40*'=')
    print(df_munic_estelionatos_menores.sort_values(by = 'estelionato', ascending=True).head(10))
    
    
    df_munic_estelionato_maiores = df_munic_estelionato[df_munic_estelionato['estelionato'] > q3 ]
    print('\nMunicipios com menores valores')
    print(40*'=')
    print(df_munic_estelionato_maiores.head(10))

except Exception as e:
    print(f'Erro ao calcular as informações {e}')
from sqlalchemy import create_engine
import pandas as pd
# from dotenv import load_dotenv 
import numpy as np 
import os 

os.system('cls')
# load_dotenv()

# host = os.getenv('DB_HOST')
# user = os.getenv('DB_USER')
# password = os.getenv('DB_PASSWORD')
# database = os.getenv('DB_DATABASE')

# engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

try: 
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv

    df_roubo_veiculo = df_ocorrencias[['munic','roubo_veiculo']] 

    #Agrupando e quantificando as variaveis quantitativas
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()

    #Ordenando em desc ( se tirar o asceding ele ordena em crescente)
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)

    # print(df_roubo_veiculo)

except Exception as e:
    print(f'Erro na conexão {e}')  
    exit()


# OBTENDO INFORMAÇÕES

try: 
    print('OBTENDO INFORMAÇÕES A CERCA DOS ROUBOS DE VEICULOS')


    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo).round(2)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo).round(2)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo *100)
 


    print('\nMedidas de Tendências Central')
    print(40*'=')
    print(f'A média: {media_roubo_veiculo}')
    print(f'A mediana: {mediana_roubo_veiculo}')
    print(f'A distancia entre média e mediana: {distancia:.2f} %')

    #Obtendo os quartis 
    q1 = np.quantile(array_roubo_veiculo, 0.25)
    q2 = np.quantile(array_roubo_veiculo, 0.50)
    q3 = np.quantile(array_roubo_veiculo, 0.75)

    print('\nMedidas de Posição')
    print(40*'=')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # menores
    df_roubo_veiculos_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1 ]
    print('\nMunicipios com menores valores')
    print(40*'=')
    print(df_roubo_veiculos_menores.sort_values(by = 'roubo_veiculo', ascending=True))
    
    
    # maiores
    df_roubo_veiculos_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3 ]
    print('\nMunicipios com menores valores')
    print(40*'=')
    print(df_roubo_veiculos_maiores)
    
except Exception as e:
    print(f'Erro ao calcular as informações {e}')
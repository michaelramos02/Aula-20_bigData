from sqlalchemy import create_engine
import pandas as pd
# from dotenv import load_dotenv 
import numpy as np 
import os 
import matplotlib.pyplot as plt

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

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1') 

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
    print('\nMunicipios com maiores valores')
    print(40*'=')
    print(df_roubo_veiculos_maiores)
    
except Exception as e:
    print(f'Erro ao calcular as informações {e}')

#  Medida de dispersão ( Amplitude Total)
    
try: 

    # amplitude total = maior valor - menor valor
    # quanto mais proximo do zero, maior a homogeneidade dos dados 
    # se for igual a 0, todos os dados sao iguais 
    # Quanto mais proximo do maior valor, maior a dispersão

    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo -  minimo

    print('\nMedidas de dispersão')
    print(40*'=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude total: {amplitude}')

except Exception as e:
    print('Erro ao calcular a medida de dispersão')

#  Outliers
    
try: 
#   IQR ( InterQuartil)
#   É a amplitude dos 50% dos dados mais centrais
#   IQR = q3 - q1
#   Ele ignora os valores mais extremos, max e min estão fora.
#   Não sofre influencia dos extremos
#   quanto mais proximo do zero, maior a homogeneidade dos dados 
#   se for igual a 0, todos os dados sao iguais 
#   Quanto mais proximo do q3 ,maior a dispersão dos dados mais centrais 
    
    iqr = q3 - q1

# LIMITE INFERIOR
    limiteInferior = q1 - (1.5 * iqr)

# LIMITE SUPERIOR
    limiteSuperior = q3 + (1.5 * iqr)

    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limiteSuperior]

    df_roubo_veiculo_outliers_inferior = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limiteInferior]

    print('\nMedidas')
    print(40*'=')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limiteInferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}') #mediana
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite Superior: {limiteSuperior}')
    print(f'Máximo: {maximo}')

    print('\nOutliers Superiores: ')
    print(40 * '=')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não Existe outliers superiores')
    else: 
        print(df_roubo_veiculo_outliers_superiores)
        
    print('\nOutliers Inferiores: ')
    print(40 * '=')
    if len(df_roubo_veiculo_outliers_inferior) == 0:
        print('Não Existe outliers inferiores')
    else: 
        print(df_roubo_veiculo_outliers_inferior)

except Exception as e:
    print('Erro ao calcular os outliers')


# Visualizando os dados
try: 
    # mostrando cidades com maiores roubos
    # plt.figure(figsize=(16, 8))
    
    plt.subplots(2, 1, figsize=(16, 8))


    # 1
    plt.subplot(2, 1, 1)
    df_roubo_veiculos_maiores = df_roubo_veiculos_maiores.head(10).sort_values(by='roubo_veiculo', ascending=True)
    plt.barh(df_roubo_veiculos_maiores['munic'],df_roubo_veiculos_maiores['roubo_veiculo'])
    plt.title('Cidades com maiores indices de roubo de veiculos')

    
    # 2
    plt.subplot(2, 1, 2)
    df_roubo_veiculos_menores = df_roubo_veiculos_menores.sort_values(by='roubo_veiculo', ascending=True).head(10).sort_values(by='roubo_veiculo', ascending=False)
    plt.barh(df_roubo_veiculos_menores['munic'],df_roubo_veiculos_menores['roubo_veiculo'])
    plt.title('Cidades com menores indices de roubo de veiculos')

    plt.show()


except Exception as e:
    print(f'Erro ao plotar gráfico: {e}')
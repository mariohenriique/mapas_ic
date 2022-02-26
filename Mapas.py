print('começando...')

import folium
import pandas as pd
import os
from tkinter import filedialog

#selecionar o arquivo a ser trabalhado
print('Selecione o arquivo com os dados.')
nome_arquivo = filedialog.askopenfilename()

df = pd.read_csv(nome_arquivo)
df = pd.DataFrame(df)

def fazer_mapa(dataframe,coluna_latitude,coluna_longitude,coluna_lugar,nome_mapa_arquivo):
    
    latitudemedia = (coluna_latitude.max()+coluna_latitude.min())/2
    longitudemedia = (coluna_longitude.max()+coluna_longitude.min())/2

    mapa = folium.Map(location=[latitudemedia,longitudemedia])

    for i in range(len(dataframe)):
        lat = coluna_latitude[i]
        lon = coluna_longitude[i]
        nomelugar = coluna_lugar[i]
        folium.Marker([lat, lon], popup=nomelugar).add_to(mapa)

    mapa.save(nome_mapa_arquivo)
    return mapa

lista_familia = list(df['Família'])
todas_familias = []

for i in range(len(lista_familia)):
    if lista_familia[i] not in todas_familias:
        todas_familias.append(lista_familia[i])

print('Selecione onde será salvo a pasta Mapas.')
caminho = filedialog.askdirectory()

if caminho == 'Mapas':
    os.makedirs(caminho)

else:
    caminho = os.path.join(caminho,'Mapas')

pastas = [f for f in os.listdir(caminho)]

#criar diretórios
print('Criando pastas')
for i in todas_familias:
    if i not in (pastas):
        os.makedirs(os.path.join('Mapas',i))

#dataframes, mapas e csv para cada família
print('Criando mapas')
for e in todas_familias:
    globals()['df_'+str(e)] = pd.DataFrame()
    dataframe_por_familia = globals()['df_'+str(e)]
    
    for i in range(len(df)):
        if df['Família'].iloc[i]==e:
            dataframe_por_familia = dataframe_por_familia.append(df.loc[i],ignore_index=True)
    
    nome_csv = os.path.join('Mapas',e,e + '.csv')
    
    dataframe_por_familia.to_csv(nome_csv)
    
    nome = os.path.join('Mapas',e,'mapa_' + e + '.html')
    
    mapas = fazer_mapa(dataframe_por_familia,dataframe_por_familia['Decimais - Latitude'],
                        dataframe_por_familia['Decimais - Longitude'],dataframe_por_familia['Localidade'],nome)

print('Concluído com sucesso')
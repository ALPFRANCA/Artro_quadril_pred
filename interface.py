# Carregando as bibliotecas para aplicação gráfica:

import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Carregando o modelo e o pré-processamento
model = pickle.load(open("modelo_artroquadril.pkl", "rb")) 

# Título da interface
st.title("Predição de Complicações Cirúrgicas em Artroscopia de Quadril")

# Criando os campos de entrada para as variáveis a serem analisadas

sexo = st.selectbox("Sexo", ["M", "F"])
idade = st.number_input("Idade", min_value=0, max_value=99)
lado = st.selectbox("Lateralidade", ["ESQ.", "DIR."])
tracao = st.number_input("Tempo de tração durante o ato cirúrgico (em minutos)", min_value=0)
ret_tracao = st.number_input("Quantidade de vezes que a tração foi retirada durante o ato cirúrgico", min_value=0)
int_tracao = st.number_input("Tempo de retirada da tração durante o ato cirúrgico (em minutos)", min_value=0)
indicacao = st.selectbox("Indicação da abordagem cirúrgica", ["Lesão labral", "Lesão condral", "Lesão mista (labral e condral)"])
ifa = st.selectbox("Tipo de Impacto Fêmoro-acetabular tratado", ["Tipo misto", "Tipo CAM", "Tipo PINCER"])
portais = st.number_input("Número de portais artroscópicps utilizados durante o ato cirúrgico", min_value=2)
bloq_pos = st.checkbox("Houve bloqueio anestésico no pós-operatório imediato?")
bloq_pos = int(bloq_pos)
ancoras = st.number_input("Quantidade de âncoras utilizadas durante o ato cirúrgico", min_value=0)
tipo = np.nan  
conversao_atq = np.nan 
tx_reop = np.nan 

# Criando um dicionário com os dados de entrada
input_data = {
    "SEXO": [sexo],
    "IDADE": [idade],
    "LADO": [lado],
    "TRACAO": [tracao],
    "RET_TRACAO": [ret_tracao],
    "INT_TRACAO": [int_tracao],
    "INDICACAO": [indicacao],
    "IFA": [ifa],
    "PORTAIS": [portais],
    "BLOQ_POS": [bloq_pos],
    "TIPO": [tipo],
    "CONVERSAO_ATQ": [conversao_atq],
    "ANCORAS": [ancoras],
    "TX_REOP": [tx_reop],
}

# Convertendo o imput para DataFrame
input_df = pd.DataFrame(input_data)

# Botão para realizar a predição
if st.button("Prever complicação pós-operatória"):
    try:
        # Fazer a previsão
        prediction = model.predict(input_processed)

        # Exibir o resultado
        if prediction[0] == 0:
            st.success("Baixo risco de complicações.")
        else:
            st.warning("Alto risco de complicações.")

    except Exception as e:
        st.error(f"Erro: {e}")

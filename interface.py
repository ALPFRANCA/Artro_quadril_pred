# Carregando as bibliotecas para aplicação gráfica:
import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Carregar o modelo e o pre-processador
model = pickle.load(open("modelo_artroquadril.pkl", "rb"))
preprocessor = pickle.load(open("preprocessor.pkl", "rb"))
feature_names = pickle.load(open("feature_names.pkl", "rb"))

# Carregar os dados de treino 
df = pd.read_excel("DB_Artro.xlsx")
X5 = df.drop(columns = 'COMPL')

# Função para fazer a previsão
def predict(input_df, preprocessor5):
    # Pré-processar os dados de entrada
    input_processed = preprocessor5.transform(input_df)
    st.write(input_processed)

    # Fazer a previsão
    prediction = model.predict(input_processed)
    return prediction

# Título da interface
st.title("Predição de Complicações Cirúrgicas em Artroscopia de Quadril")

# Criando os campos de entrada para as variáveis a serem analisadas

sexo = st.selectbox("Sexo", ["M", "F"])
idade = st.number_input("Idade", min_value=0, max_value=99)
lado = st.selectbox("Lateralidade", ["ESQ.", "DIR."])
tracao = st.number_input("Tempo de tração durante o ato cirúrgico (em minutos)", min_value=0, max_value=300)
ret_tracao = st.number_input("Quantidade de vezes que a tração foi retirada durante o ato cirúrgico", min_value=0, max_value=10)
int_tracao = st.number_input("Tempo de retirada da tração durante o ato cirúrgico (em minutos)", min_value=0, max_value=150)
indicacao = st.selectbox("Indicação da abordagem cirúrgica", ["Lesão labral", "Lesão condral", "Lesão mista (labral e condral)"])
ifa = st.selectbox("Tipo de Impacto Fêmoro-acetabular tratado", ["Tipo misto", "Tipo CAM", "Tipo PINCER"])
portais = st.number_input("Número de portais artroscópicps utilizados durante o ato cirúrgico", min_value=2, max_value=5)
bloq_pos = st.checkbox("Houve bloqueio anestésico no pós-operatório imediato?")
bloq_pos = int(bloq_pos)
tipo = np.nan  
conversao_atq = np.nan 
ancoras = st.number_input("Quantidade de âncoras utilizadas durante o ato cirúrgico", min_value=0, max_value=5)
tx_reop = np.nan 

# Criando um dicionário com os dados de entrada (sem listas e com mapeamento)
input_data = {
    "SEXO": sexo, 
    "IDADE": idade,
    "LADO": lado, 
    "TRACAO": tracao,
    "RET_TRACAO": ret_tracao,
    "INT_TRACAO": int_tracao,
    "INDICACAO": indicacao,
    "IFA": ifa, 
    "PORTAIS": portais,
    "BLOQ_POS": bloq_pos,
    "TIPO": tipo,
    "CONVERSAO_ATQ": conversao_atq,
    "ANCORAS": ancoras,
    "TX_REOP": tx_reop,
}

# Convertendo o imput para DataFrame
input_df = pd.DataFrame([input_data])

# Botão para prever
if st.button("Prever"): 
    try:
        input_processed_array = preprocessor.transform(input_df)
        input_processed = pd.DataFrame(input_processed_array, columns=feature_names)
        # Fazer a previsão
        st.write(input_df.shape) 
        st.write(X5.shape)
        prediction = model.predict(input_processed)

        st.write(X5.columns)

        st.write(input_df.columns)

        st.write(feature_names)

        st.write(input_processed.columns)

        # Exibir o resultado
        if prediction[0] == 0:
            st.success("Baixo risco de complicações.")
        else:
            st.warning("Alto risco de complicações.")

    except Exception as e:
        st.error(f"Erro: {e}")

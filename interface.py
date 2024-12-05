# Carregando as bibliotecas para aplicação gráfica:
import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Carregar o modelo
model = pickle.load(open("modelo_artroquadril.pkl", "rb"))

# Definindo as colunas numéricas e categóricas
numerical_features = ['IDADE', 'TRACAO', 'RET_TRACAO', 'INT_TRACAO', 'PORTAIS', 'BLOQ_POS', 'ANCORAS']
categorical_features = ['SEXO', 'LADO', 'INDICACAO', 'IFA']

# Criando os pipelines de pré-processamento
numerical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", MinMaxScaler()),
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ]
)

# Criando o ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_features),
        ("cat", categorical_transformer, categorical_features),
    ],
    remainder='passthrough'
)

# Carregar os dados de treino (substitua pelo seu arquivo)
df_treino = pd.read_excel("DB_Artro.xlsx")
X_treino = df_treino.drop("COMPL", axis=1) 

# Ajustar o pré-processador aos dados de treino
preprocessor.fit(X_treino)

# Função para fazer a previsão
def predict(input_df, preprocessor):
    # Pré-processar os dados de entrada
    input_processed = preprocessor.transform(input_df)

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

# Mapeamento das variáveis categóricas
sexo_mapping = {"M": 0, "F": 1}
lado_mapping = {"ESQ.": 0, "DIR.": 1}
indicacao_mapping = {"Lesão labral": 0, "Lesão condral": 1, "Lesão mista (labral e condral)": 2}
ifa_mapping = {"Tipo misto": 0, "Tipo CAM": 1, "Tipo PINCER": 2}

# Criando um dicionário com os dados de entrada (sem listas e com mapeamento)
input_data = {
    "SEXO": sexo_mapping[sexo],
    "IDADE": idade,
    "LADO": lado_mapping[lado],
    "TRACAO": tracao,
    "RET_TRACAO": ret_tracao,
    "INT_TRACAO": int_tracao,
    "INDICACAO": indicacao_mapping[indicacao],
    "IFA": ifa_mapping[ifa],
    "PORTAIS": portais,
    "BLOQ_POS": bloq_pos,
    "TIPO": tipo,
    "CONVERSAO_ATQ": conversao_atq,
    "ANCORAS": ancoras,
    "TX_REOP": tx_reop,
}

# Convertendo o imput para DataFrame
input_df = pd.DataFrame([input_data])

# Reordenar as colunas do input_df para corresponder a X_treino
input_df = input_df[X_treino.columns]

# Botão para prever
if st.button("Prever"):
    try:
        # Fazer a previsão
        st.write(input_df.shape) 
        st.write(X_treino.shape)
        prediction = predict(input_df, preprocessor)

        # Exibir o resultado
        if prediction[0] == 0:
            st.success("Baixo risco de complicações.")
        else:
            st.warning("Alto risco de complicações.")

    except Exception as e:
        st.error(f"Erro: {e}")

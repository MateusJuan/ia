import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

def get_data():
    return pd.read_csv('data.csv')

def train_model():
    data = get_data()
    x = data.drop('MEDV', axis=1)
    y = data['MEDV']
    rf_regressor = RandomForestRegressor()
    rf_regressor.fit(x,y)
    return rf_regressor

data = get_data()

model = train_model()

st.title("Data App - Prevendo valores de imóveis")

st.markdown("Este é um Data App utilizado para exibir a solução de Machine Learnin para o problema de predição de valores de imóveis com o dataset Boston House Prices do MIT.")

st.subheader("Selecionando apenas um pequeno conkinto de atributos")

defaultcols = ['RM','PTRATIO','CRIM','MEDV']

cols = st.multiselect('Atributos', data.columns.tolist(), default=defaultcols)

st.dataframe(data[cols].head(10))
st.subheader('Distribuição de imóveis por preço')

faixa_valores = st.slider('Faixa de preço', float(data.MEDV.min()), 150., (10.0, 100.0))

dados = data[data['MEDV'].between(left=faixa_valores[0], right=faixa_valores[1])]

f = px.histogram(dados, x='MEDV', nbins=100, title='Distribuição de Preços')
f.update_xaxes(title='MEDV')
f.update_yaxes(title='Total imóveis')
st.plotly_chart(f)
st.sidebar.subheader('Defina os atributos dos imoveis para predição')

crim = st.sidebar.number_input('Taxa de criminalidade', value=data.CRIM.mean())
indus = st.sidebar.number_input("Proporção de hectares de Industrias", value=data.INDUS.mean())
chas = st.sidebar.selectbox('Faz limite com o rio?', ('Sim', 'Não'))

chas = 1 if chas == "Sim" else 0
nox = st.sidebar.number_input('Concentração de oxico nitrico', value=data.NOX.mean())
rm = st.sidebar.number_input('Núero de quartos', value=1)
pratio = st.sidebar.number_input('Índice de alunos por professores', value=data.PTRATIO.mean())


btn_predict = st.sidebar.button('Realizar predição')

if btn_predict:
    result = model.predict([[crim, indus, chas, nox, rm, pratio]])
    st.subheader('O valor previsto para o imóvel é: ')
    result = 'US $ '+str(round(result[0]*10,2))
    st.write(result)
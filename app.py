import streamlit as st
from numpy_financial import pmt

# Função para calcular a parcela mensal do financiamento
def calcular_parcela_mensal(valor_veiculo, taxa_juros_mensal, prazo):
    return -pmt(taxa_juros_mensal, prazo, valor_veiculo)

# Interface do app
st.set_page_config(page_title="Precificação ITA Frotas", layout="wide")
st.title("Simulador de Precificação - ITA Frotas")

st.header("Parâmetros do Contrato")

col1, col2, col3 = st.columns(3)

with col1:
    preco_tabela = st.number_input("Preço de Tabela (R$)", value=125000.00, step=1000.0)
    desconto = st.number_input("Desconto (%)", value=20.0, step=0.1)
    preco_frotista = preco_tabela * (1 - desconto / 100)

with col2:
    prazo = st.selectbox("Prazo do contrato (meses)", [12, 24, 36], index=2)
    km_franquia = st.selectbox("Franquia mensal (km)", [1000, 2000, 3000], index=0)
    quantidade = st.number_input("Quantidade de veículos", value=1, step=1)

with col3:
    taxa_juros = st.number_input("Juros sobre capital de giro (% a.m.)", value=2.00) / 100

st.write("---")

st.subheader("Cálculo de Custos")

if km_franquia == 1000:
    percentual_despesas = 28.0
elif km_franquia == 2000:
    percentual_despesas = 28.5
else:
    percentual_despesas = 29.5

despesas_total = preco_tabela * (percentual_despesas / 100)
parcela_financiamento = calcular_parcela_mensal(preco_frotista, taxa_juros, prazo)

parcela_referencia = preco_tabela * 0.032
valor_total_contrato = parcela_referencia * prazo

valor_revenda = preco_tabela * (1 - 0.30)  # depreciação de 30% total

st.metric("Preço Frotista (R$)", f"{preco_frotista:,.2f}")
st.metric("Despesa Estimada (R$)", f"{despesas_total:,.2f}")
st.metric("Parcela de Referência (R$)", f"{parcela_referencia:,.2f}")
st.metric("Valor de Revenda Estimado (R$)", f"{valor_revenda:,.2f}")
st.metric("Parcela de Financiamento (R$)", f"{parcela_financiamento:,.2f}")
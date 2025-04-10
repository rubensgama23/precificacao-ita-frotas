
import streamlit as st

st.set_page_config(page_title="Precificação ITA Frotas", layout="centered")

st.title("📊 Simulador de Precificação - ITA Frotas")
st.markdown("Este simulador ajuda a calcular a rentabilidade de contratos de locação com base nas premissas operacionais e financeiras da ITA.")

st.header("1. Dados do Veículo e Contrato")

veiculo = st.text_input("Modelo do veículo", "Corolla")
quantidade = st.number_input("Quantidade de veículos", min_value=1, value=10)
preco_tabela = st.number_input("Preço de tabela (R$)", value=125000.0, step=1000.0)
desconto = st.number_input("Desconto obtido (%)", value=20.0, step=0.5) / 100
preco_frotista = preco_tabela * (1 - desconto)

prazo = st.selectbox("Prazo do contrato (meses)", [12, 24, 36])
km_mes = st.selectbox("Franquia mensal de km", [1000, 2000, 3000])

if km_mes == 1000:
    percentual_despesas = 0.28
elif km_mes == 2000:
    percentual_despesas = 0.285
else:
    percentual_despesas = 0.295

despesas_totais = preco_tabela * percentual_despesas * quantidade

st.header("2. Financiamento e Capital de Giro")

juros_financiamento = st.number_input("Juros do financiamento (% a.m.)", value=2.0, step=0.1) / 100
prazo_financiamento = 24  # fixo por enquanto
capital_giro_percentual = percentual_despesas  # mesma proporção das despesas
juros_capital_giro = st.number_input("Juros sobre capital de giro (% a.m.)", value=2.0, step=0.1) / 100

from numpy import pmt

parcela_financiamento = -pmt(juros_financiamento, prazo_financiamento, preco_frotista * quantidade)
total_financiado = parcela_financiamento * prazo_financiamento

capital_giro = preco_tabela * capital_giro_percentual * quantidade
custo_capital_giro = capital_giro * juros_capital_giro * (prazo / 12)

st.header("3. Receita e Resultado")

valor_revenda = preco_tabela * (1 - 0.3) * quantidade  # 30% depreciação acumulada
parcela_cliente = st.number_input("Parcela mensal cobrada do cliente (R$)", value=4000.0, step=100.0)
faturamento_total = parcela_cliente * prazo * quantidade

lucro = faturamento_total + valor_revenda - (despesas_totais + total_financiado + custo_capital_giro)
roi = lucro / (preco_frotista * quantidade)

st.subheader("📈 Resultado da Simulação")
st.markdown(f"**Lucro líquido estimado:** R$ {lucro:,.2f}")
st.markdown(f"**ROI estimado:** {roi*100:.2f}%")
st.markdown(f"**Valor da revenda final (estimado):** R$ {valor_revenda:,.2f}")
st.markdown(f"**Custo estimado com capital de giro:** R$ {custo_capital_giro:,.2f}")

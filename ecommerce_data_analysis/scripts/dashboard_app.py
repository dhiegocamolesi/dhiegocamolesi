import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard E-commerce", layout="wide")
st.title("Dashboard de Vendas - E-commerce")

@st.cache_data
def carregar_dados():
    pedidos = pd.read_csv(r'C:\Projetos\ecommerce_data_analysis\data\processed\pedidos.csv', parse_dates=['order_purchase_timestamp'])
    pagamentos = pd.read_csv(r'C:\Projetos\ecommerce_data_analysis\data\processed\pagamentos.csv')
    clientes = pd.read_csv(r'C:\Projetos\ecommerce_data_analysis\data\processed\clientes.csv')
    return pedidos, pagamentos, clientes

pedidos, pagamentos, clientes = carregar_dados()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total de Pedidos", f"{pedidos['order_id'].nunique():,}".replace(",", "."))
col2.metric("Total de Clientes", f"{clientes['customer_id'].nunique():,}".replace(",", "."))
col3.metric("Receita Total (R$)", f"{pagamentos['payment_value'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# Gráficos
pagamento_tipo = pagamentos['payment_type'].value_counts().reset_index()
pagamento_tipo.columns = ['Tipo de Pagamento', 'Quantidade']
fig1 = px.pie(pagamento_tipo, names='Tipo de Pagamento', values='Quantidade', hole=0.5)

pedidos['AnoMes'] = pedidos['order_purchase_timestamp'].dt.to_period('M').astype(str)
pedidos_mes = pedidos.groupby('AnoMes')['order_id'].nunique().reset_index().sort_values(by='AnoMes')
fig2 = px.bar(pedidos_mes, x='AnoMes', y='order_id', labels={'order_id':'Quantidade de Pedidos'})

clientes_estado = clientes['customer_state'].value_counts().reset_index()
clientes_estado.columns = ['Estado', 'Quantidade']
clientes_estado = clientes_estado.sort_values(by='Quantidade', ascending=False)
fig3 = px.bar(clientes_estado, x='Estado', y='Quantidade')

# Layout em abas
aba1, aba2, aba3 = st.tabs(["💳 Tipos de Pagamento", "📦 Pedidos Mensais", "🗺️ Clientes por Estado"])
with aba1:
    st.plotly_chart(fig1, use_container_width=True)
with aba2:
    st.plotly_chart(fig2, use_container_width=True)
with aba3:
    st.plotly_chart(fig3, use_container_width=True)

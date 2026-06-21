import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, timedelta


#  Config da página
st.set_page_config(
    page_title="Dashboard de Transações",
    page_icon="💳",
    layout="wide"
)


# Dados fictícios
np.random.seed(42)
n = 300

datas = [date(2024, 1, 1) + timedelta(days=int(x)) for x in np.random.randint(0, 365, n)]
bandeiras = np.random.choice(['Visa', 'Mastercard', 'Elo', 'Amex'], n, p=[0.4, 0.35, 0.15, 0.1])
status = np.random.choice(['Aprovada', 'Recusada', 'Chargeback'], n, p=[0.80, 0.15, 0.05])
valores = np.round(np.random.uniform(20, 1500, n), 2)
categorias = np.random.choice(['Alimentação', 'Eletrônicos', 'Vestuário', 'Serviços', 'Farmácia'], n)

df = pd.DataFrame({
    'data': pd.to_datetime(datas),
    'bandeira': bandeiras,
    'status': status,
    'valor': valores,
    'categoria': categorias
})

df['mes'] = df['data'].dt.to_period('M').astype(str)


# Título
st.title("💳 Dashboard de Transações")
st.markdown("Análise de transações fictícias — projeto de prática em Python com Streamlit.")
st.divider()



# Filtros na sidebar
st.sidebar.header("🔍 Filtros")

bandeiras_opcoes = ['Todas'] + sorted(df['bandeira'].unique().tolist())
bandeira_sel = st.sidebar.selectbox("Bandeira", bandeiras_opcoes)

status_opcoes = ['Todos'] + sorted(df['status'].unique().tolist())
status_sel = st.sidebar.selectbox("Status", status_opcoes)

categorias_opcoes = st.sidebar.multiselect(
    "Categoria",
    options=sorted(df['categoria'].unique().tolist()),
    default=sorted(df['categoria'].unique().tolist())
)



# Aplicar filtros
df_f = df.copy()
if bandeira_sel != 'Todas':
    df_f = df_f[df_f['bandeira'] == bandeira_sel]
if status_sel != 'Todos':
    df_f = df_f[df_f['status'] == status_sel]
if categorias_opcoes:
    df_f = df_f[df_f['categoria'].isin(categorias_opcoes)]



# KPI
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de transações", f"{len(df_f):,}")
col2.metric("Volume financeiro", f"R$ {df_f['valor'].sum():,.2f}")
col3.metric("Ticket médio", f"R$ {df_f['valor'].mean():,.2f}")
aprovadas = len(df_f[df_f['status'] == 'Aprovada'])
taxa = aprovadas / len(df_f) * 100 if len(df_f) > 0 else 0
col4.metric("Taxa de aprovação", f"{taxa:.1f}%")

st.divider()


# Gráfico
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📈 Volume por mês")
    vol_mes = df_f.groupby('mes')['valor'].sum().reset_index()
    vol_mes.columns = ['Mês', 'Volume (R$)']
    fig_linha = px.line(vol_mes, x='Mês', y='Volume (R$)', markers=True,
                        color_discrete_sequence=['#636EFA'])
    fig_linha.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_linha, use_container_width=True)

with col_b:
    st.subheader("📊 Transações por bandeira")
    por_bandeira = df_f.groupby('bandeira')['valor'].sum().reset_index()
    por_bandeira.columns = ['Bandeira', 'Volume (R$)']
    fig_bar = px.bar(por_bandeira, x='Bandeira', y='Volume (R$)',
                     color='Bandeira', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bar, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("🥧 Status das transações")
    por_status = df_f['status'].value_counts().reset_index()
    por_status.columns = ['Status', 'Quantidade']
    fig_pizza = px.pie(por_status, names='Status', values='Quantidade',
                       color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_pizza, use_container_width=True)

with col_d:
    st.subheader("🛍️ Volume por categoria")
    por_cat = df_f.groupby('categoria')['valor'].sum().sort_values(ascending=True).reset_index()
    por_cat.columns = ['Categoria', 'Volume (R$)']
    fig_cat = px.bar(por_cat, x='Volume (R$)', y='Categoria', orientation='h',
                     color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig_cat, use_container_width=True)

st.divider()


# Tabela
st.subheader("📋 Tabela de transações")
st.dataframe(
    df_f[['data', 'bandeira', 'categoria', 'status', 'valor']]
    .sort_values('data', ascending=False)
    .reset_index(drop=True),
    use_container_width=True
)

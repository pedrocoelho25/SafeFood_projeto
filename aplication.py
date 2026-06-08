import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("https://vongxbyisbowsqtfofxl.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZvbmd4Ynlpc2Jvd3NxdGZvZnhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkxNDI2MTYsImV4cCI6MjA5NDcxODYxNn0.blMGXBL1zhmwxsyNe3POU50wd1DgooP-85Q3ip3v7Hk")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="SafeFood", layout="wide")

st.title("SafeFood - Sistema de Controle de Doações")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Produtos", "Lotes", "Estoque", "Alertas", "Auditorias"]
)

if menu == "Dashboard":
    st.header("Dashboard")

    produtos = supabase.table("produto").select("*").execute().data
    lotes = supabase.table("lote").select("*").execute().data
    alertas = supabase.table("alerta_validade").select("*").execute().data

    col1, col2, col3 = st.columns(3)

    col1.metric("Produtos", len(produtos))
    col2.metric("Lotes", len(lotes))
    col3.metric("Alertas", len(alertas))

elif menu == "Produtos":
    st.header("Produtos")

    with st.form("form_produto"):
        nome = st.text_input("Nome do produto")
        id_usuario = st.number_input("ID do usuário", min_value=1)
        id_categoria = st.number_input("ID da categoria", min_value=1)

        enviar = st.form_submit_button("Cadastrar produto")

        if enviar:
            supabase.table("produto").insert({
                "nome_produto": nome,
                "id_usuario": id_usuario,
                "id_categoria_produto": id_categoria
            }).execute()

            st.success("Produto cadastrado com sucesso!")

    dados = supabase.table("produto").select("*").execute().data
    st.dataframe(dados)

elif menu == "Lotes":
    st.header("Lotes")

    with st.form("form_lote"):
        quantidade = st.number_input("Quantidade", min_value=1)
        data_validade = st.date_input("Data de validade")
        data_entrada = st.date_input("Data de entrada")
        data_fabricacao = st.date_input("Data de fabricação")
        id_produto = st.number_input("ID do produto", min_value=1)

        enviar = st.form_submit_button("Cadastrar lote")

        if enviar:
            supabase.table("lote").insert({
                "quantidade": quantidade,
                "data_validade": str(data_validade),
                "data_entrada": str(data_entrada),
                "data_fabricacao": str(data_fabricacao),
                "id_produto_lote": id_produto
            }).execute()

            st.success("Lote cadastrado! Trigger de estoque e validade será executada.")

    dados = supabase.table("lote").select("*").execute().data
    st.dataframe(dados)

elif menu == "Estoque":
    st.header("Estoque")
    dados = supabase.table("estoque").select("*").execute().data
    st.dataframe(dados)

elif menu == "Alertas":
    st.header("Alertas de Validade")
    dados = supabase.table("alerta_validade").select("*").execute().data
    st.dataframe(dados)

elif menu == "Auditorias":
    st.header("Auditorias")

    aba = st.selectbox("Tipo", ["Usuário", "Lote", "Produto"])

    if aba == "Usuário":
        dados = supabase.table("auditoria_usuario").select("*").execute().data
    elif aba == "Lote":
        dados = supabase.table("auditoria_lote").select("*").execute().data
    else:
        dados = supabase.table("auditoria_produto").select("*").execute().data

    st.dataframe(dados)

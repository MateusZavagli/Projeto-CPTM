import re
from datetime import date
from io import BytesIO

import pandas as pd
import qrcode
import streamlit as st

from database import conectar_banco

st.set_page_config(page_title="Projeto CPTM - Dormentes", page_icon="🚆", layout="wide")

st.title("🚆 Projeto CPTM - Identificação e Inspeção de Dormentes")
st.caption("Protótipo web do Plano de Trabalho (Senac)")

pagina = st.sidebar.radio("Menu", ["Consultar dormentes", "Cadastrar dormente", "Gerar QR Code"])

if pagina == "Consultar dormentes":
    st.header("Dormentes cadastrados")

    conexao = None
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""SELECT id, codigo, tipo_madeira, [comprimento (m)], data_cadastro
                          FROM dbo.Dormentes
                          ORDER BY id""")
        linhas = [tuple(linha) for linha in cursor.fetchall()]
    except Exception as erro:
        st.error(f"Erro ao consultar o banco: {erro}")
        st.stop()
    finally:
        if conexao is not None:
            conexao.close()

    tabela = pd.DataFrame(linhas, columns=["ID", "Código", "Tipo de madeira", "Comprimento (m)", "Data de cadastro"])

    busca = st.text_input("Buscar por código ou tipo de madeira")
    if busca:
        filtro = (tabela["Código"].astype(str).str.contains(busca, case=False, na=False)
                  | tabela["Tipo de madeira"].astype(str).str.contains(busca, case=False, na=False))
        tabela = tabela[filtro]

    if tabela.empty:
        st.info("Nenhum dormente encontrado.")
    else:
        tabela["Comprimento (m)"] = tabela["Comprimento (m)"].astype(float)

        col1, col2, col3 = st.columns(3)
        col1.metric("Dormentes", len(tabela))
        col2.metric("Tipos de madeira", tabela["Tipo de madeira"].nunique())
        col3.metric("Comprimento médio (m)", f"{tabela['Comprimento (m)'].mean():.2f}")

        st.dataframe(tabela, hide_index=True)

        st.subheader("Quantidade por tipo de madeira")
        st.bar_chart(tabela["Tipo de madeira"].value_counts())


elif pagina == "Cadastrar dormente":
    st.header("Cadastrar dormente")

    tipo = st.selectbox("Tipo de madeira", ["Eucalipto", "Ipê", "Angelim", "Outro"])
    if tipo == "Outro":
        tipo = st.text_input("Informe o tipo de madeira").strip()

    codigo = st.text_input("Código do dormente", placeholder="Dormente-0001").strip()
    comprimento = st.number_input("Comprimento (m)", min_value=0.10, max_value=10.00, value=2.80, step=0.01, format="%.2f")
    data_cadastro = st.date_input("Data de cadastro", value=date.today(), format="DD/MM/YYYY")

    if st.button("Cadastrar", type="primary"):
        if not re.fullmatch(r"Dormente-\d{4}", codigo):
            st.error("O código deve seguir o formato Dormente-0001.")
        elif not tipo:
            st.error("Informe o tipo de madeira.")
        else:
            conexao = None
            try:
                conexao = conectar_banco()
                cursor = conexao.cursor()
                cursor.execute("""INSERT INTO dbo.Dormentes (codigo, tipo_madeira, [comprimento (m)], data_cadastro)
                                  VALUES (?, ?, ?, ?)""", (codigo, tipo, comprimento, data_cadastro))
                conexao.commit()
                st.success(f"Dormente {codigo} de {tipo} ({comprimento:.2f} m) cadastrado em {data_cadastro:%d/%m/%Y}.")
            except Exception as erro:
                if conexao is not None:
                    conexao.rollback()
                st.error(f"Erro ao inserir no banco: {erro}")
            finally:
                if conexao is not None:
                    conexao.close()


else:
    st.header("Gerar QR Code")

    conexao = None
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""SELECT codigo, tipo_madeira, [comprimento (m)], data_cadastro
                          FROM dbo.Dormentes
                          ORDER BY id""")
        linhas = [tuple(linha) for linha in cursor.fetchall()]
    except Exception as erro:
        st.error(f"Erro ao consultar o banco: {erro}")
        st.stop()
    finally:
        if conexao is not None:
            conexao.close()

    if not linhas:
        st.info("Nenhum dormente cadastrado ainda. Cadastre um na página anterior.")
        st.stop()

    escolhido = st.selectbox("Dormente", [linha[0] for linha in linhas])
    codigo, madeira, comprimento, data = next(linha for linha in linhas if linha[0] == escolhido)

    texto = (f"Código: {codigo}\n"
             f"Madeira: {madeira}\n"
             f"Comprimento: {float(comprimento):.2f} m\n"
             f"Cadastro: {data}")

    imagem = qrcode.make(texto)
    buffer = BytesIO()
    imagem.save(buffer, format="PNG")

    col1, col2 = st.columns(2)
    col1.image(buffer.getvalue(), caption=codigo, width=300)
    col2.subheader("Conteúdo do QR Code")
    col2.text(texto)

    st.download_button("Baixar PNG", data=buffer.getvalue(), file_name=f"{codigo}.png", mime="image/png")
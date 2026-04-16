import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ranking de Relatórios", layout="centered")

st.title("📊 Ranking Automático de Relatórios")

st.write("Faça upload da sua planilha Excel para gerar o ranking automaticamente.")

uploaded_file = st.file_uploader("Envie sua planilha (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        coluna = "Responsável pelo Diagnóstico"

        if coluna not in df.columns:
            st.error(f"Coluna '{coluna}' não encontrada na planilha.")
        else:
            # Lista de nomes únicos
            nomes = sorted(df[coluna].dropna().unique())

            st.subheader("🎯 Filtro por nomes")
            selecionados = st.multiselect(
                "Selecione os nomes que deseja incluir no ranking:",
                options=nomes,
                default=nomes
            )

            # Filtrar dados
            df_filtrado = df[df[coluna].isin(selecionados)]

            # Gerar ranking
            ranking = df_filtrado[coluna].value_counts().reset_index()
            ranking.columns = ["Nome", "Quantidade de Relatórios"]

            st.success("Ranking gerado com sucesso!")
            st.dataframe(ranking)

            # Download
            import io
            buffer = io.BytesIO()
            ranking.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            st.download_button(
                label="Baixar Ranking em Excel",
                data=buffer,
                file_name="ranking_relatorios.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Erro ao processar a planilha: {e}")

st.markdown("---")
st.caption("Desenvolvido para automatizar a contagem de relatórios.")

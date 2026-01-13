import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# =====================================================
# Configuração da página
# =====================================================
st.set_page_config(
    page_title="Apresentação de resultados",
    layout="wide",
    page_icon="📊"
)

# Hiding humburguer menu
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("# 📊 Apresentação de resultados - Setor Contábil")
st.divider()

# =====================================================
# Carregamento dos dados
# =====================================================
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    spreadsheet=st.secrets["spreadsheet_results"]["apresentacao_resultado_planilha"]
)

# =====================================================
# Normalização
# =====================================================
df["status"] = df["status"].astype(str).str.strip().str.upper()
df["regime_tributario"] = df["regime_tributario"].astype(str).str.strip().str.upper()

# =====================================================
# Sidebar - Filtros
# =====================================================
st.sidebar.header("Filtros")

regimes = df["regime_tributario"].dropna().unique().tolist()
status_opcoes = df["status"].dropna().unique().tolist()

filtro_regime = st.sidebar.multiselect(
    "Regime tributário",
    options=regimes,
    default=regimes
)

filtro_status = st.sidebar.multiselect(
    "Status do fechamento",
    options=status_opcoes,
    default=status_opcoes
)

# =====================================================
# DataFrames de controle
# =====================================================
# Base para cards (ignora filtro de status)
df_base = df[df["regime_tributario"].isin(filtro_regime)]

# Base para gráfico e tabela (respeita todos os filtros)
df_filtrado = df_base[df_base["status"].isin(filtro_status)]

# =====================================================
# Informações gerais
# =====================================================
st.write("## Informações Gerais")
st.write("### Empresas por regime tributário")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Simples Nacional",
        df_base[df_base["regime_tributario"] == "SIMPLES NACIONAL"].shape[0],
        border=True
    )

with c2:
    st.metric(
        "Lucro Presumido",
        df_base[df_base["regime_tributario"] == "LUCRO PRESUMIDO"].shape[0],
        border=True
    )

with c3:
    st.metric(
        "Lucro Real",
        df_base[df_base["regime_tributario"] == "LUCRO REAL"].shape[0],
        border=True
    )

# =====================================================
# Estatísticas de fechamento + TAXA COM META
# =====================================================
st.divider()
st.write("## Estatísticas de fechamento")

# Meta configurável
META_TAXA = 0.85  # 85%

status_counts = df_base["status"].value_counts()

fechadas = status_counts.get("FECHADA", 0)
pendentes = status_counts.get("PENDENTE", 0)

total_processos = fechadas + pendentes

if total_processos > 0:
    taxa_fechamento = fechadas / total_processos
else:
    taxa_fechamento = 0

delta_meta = taxa_fechamento - META_TAXA

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Empresas Fechadas",
        fechadas,
        border=True
    )

with c2:
    st.metric(
        "Empresas Pendentes",
        pendentes,
        border=True
    )

with c3:
    st.metric(
        "Taxa de Fechamento",
        f"{taxa_fechamento:.1%}",
        delta=f"{delta_meta:.1%} vs meta",
        delta_color="normal",
        border=True
    )

# =====================================================
# Gráfico dinâmico
# =====================================================
st.divider()
st.write("### Fechamentos por regime tributário")

grafico_df = (
    df_filtrado
    .groupby(["regime_tributario", "status"])
    .size()
    .reset_index(name="quantidade")
)

st.bar_chart(
    grafico_df,
    x="regime_tributario",
    y="quantidade",
    color="status"
)

# =====================================================
# DataFrame
# =====================================================
st.divider()
st.write("## Empresas")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# =====================================================
# Análise qualitativa do setor + projeção de melhoria
# =====================================================
st.divider()
st.write("## Análise do setor e próximos passos")

st.markdown(
    """
### 📊 Diagnóstico atual

Atualmente, o setor de fechamento opera com uma estrutura enxuta, contando com Lourival em total execução das atividades operacionais. 
Há também o apoio de Danúbia, que atua de forma complementar conforme a necessidade do setor, e cujo auxílio é de extrema valia.

Os **processos de fechamento ainda estão em fase de consolidação**, o que é natural em um cenário de estruturação da área. 
Esse contexto reforça a importância de amadurecer fluxos, critérios de conferência e rotinas de controle.

Mesmo diante dessas condições, os indicadores demonstram **potencial claro de ganho de eficiência**, principalmente por meio de organização e padronização.

---

### 🔍 Pontos de atenção

- Estrutura operacional concentrada;
- Necessidade de formalização dos processos de fechamento;
- Importância do alinhamento contínuo entre os envolvidos;
- Demanda por fortalecimento técnico em etapas críticas.

---

### 🎯 Oportunidades de melhoria

Para sustentar a evolução do setor, destacam-se as seguintes frentes:

**1. Estruturação de processos**
- Definição clara das etapas do fechamento;
- Criação de checklists operacionais;
- Estabelecimento de prazos internos por atividade.

**2. Desenvolvimento técnico**
Treinamentos direcionados com foco em:
- Conferência de folha de pagamento;
- Conferência de impostos a pagar e a recolher;
- Conferência de fornecedores e obrigações financeiras.

**3. Integração operacional**
- Reforço no alinhamento entre equipe interna e apoio externo;
- Planejamento conjunto para períodos de maior volume.

**4. Gestão orientada por indicadores**
- Monitoramento contínuo da taxa de fechamento;
- Identificação das principais causas de pendência;
- Uso dos dados como base para decisões operacionais.

---

### 📈 Projeção de melhoria da taxa de fechamento

Considerando a implementação gradual das ações propostas, estima-se um **ganho razoável de eficiência operacional**, refletido diretamente na taxa de fechamento.

📌 **Projeção estimada:**
- Incremento de **8 a 12 pontos percentuais** na taxa de fechamento;
- Prazo estimado de **3 a 6 meses** após consolidação dos processos e treinamentos.

Esse ganho é esperado principalmente pela **redução de retrabalho**, **maior assertividade nas conferências** e **melhor previsibilidade das entregas**.

---

### ✅ Resultado esperado

- Aumento sustentável da taxa de fechamento;
- Redução do volume de pendências;
- Maior segurança e confiabilidade dos fechamentos;
- Operação mais previsível e menos dependente de esforços pontuais.
"""
)

import streamlit as st
import pandas as pd
import plotly.express as px
from numpy.ma.extras import average

path_data_base = r'D:\Programacao\Analise de dados\Analise RH Portifolio\base\base_rh.csv'

st.set_page_config(
    layout="wide",
    page_title= "Analise de dados",
    page_icon = '📊',
)

df = pd.read_csv(path_data_base,encoding='latin1')

#ELT
df["Admissao"] = pd.to_datetime(df["Admissao"])

#SideBar
st.sidebar.image('assets/logo_topo.png')

Select_box_departamento = st.sidebar.selectbox(
    label='Departamento',
    index= None,
    placeholder="Selecione o  departamento",
    options=(sorted(df["Departamento"].unique().tolist())),
)



df_filtro_selecao_departamento = df[df["Departamento"] == Select_box_departamento]

#DAX
df_filtro_ativos = df[df['Status'] == 'Ativo']
df_filtro_inativos = df[df['Status'] == 'Inativo']
total_colaboradores = df['Status'].count()

#Metricas

#Total de colaboradores
if not Select_box_departamento :
    total_colaboradores_ativos = df_filtro_ativos['Status'].count()
else:
    total_colaboradores_ativos = df_filtro_ativos[df_filtro_ativos['Departamento'] == f"{Select_box_departamento}"].value_counts().sum()

# TurnOver
if not Select_box_departamento :
    turnover = df_filtro_inativos["Status"].count() / total_colaboradores * 100
else:
    filtro_inativos_por_departamento = df_filtro_inativos[df_filtro_inativos["Departamento"] == Select_box_departamento]
    filtro_total_de_colaboradores_por_departamento = df[df['Departamento'] == Select_box_departamento]
    turnover = filtro_inativos_por_departamento["Status"].count() / filtro_total_de_colaboradores_por_departamento["Status"].count() * 100

#Absenteismo
if not Select_box_departamento :
    absenteismo_medio = round(average(df["Faltas"]),2)
else:
    absenteismo_medio = round(average(df_filtro_selecao_departamento["Faltas"]), 2)

#Desempenho medio
if not Select_box_departamento :
    desempenho_medio = round(average(df["Desempenho"]),2)
else:
    desempenho_medio = round(average(df_filtro_selecao_departamento["Desempenho"]), 2)


#Funcionarios por departamento
df_count = df_filtro_ativos['Departamento'].value_counts().reset_index()
df_count.columns = ['Departamento', 'Quantidade']

#Funcionarios por Cargo
if not Select_box_departamento :
    df_ajustado_por_cargo = df_filtro_ativos.groupby('Cargo').agg({'Status': 'count'}).reset_index()
    df_ajustado_por_cargo = df_ajustado_por_cargo.rename(columns={'Status': 'Quantidade'})
else:
    df_ajustado_por_cargo = df_filtro_ativos[df_filtro_ativos['Departamento'] == Select_box_departamento].groupby('Cargo').agg({'Status': 'count'}).reset_index()
    df_ajustado_por_cargo = df_ajustado_por_cargo.rename(columns={'Status': 'Quantidade'})

#Demitidos por departamento
if not Select_box_departamento :
    df_desligados =df_filtro_inativos['Departamento'].value_counts().reset_index()
    df_desligados = df_desligados.rename(columns={'count': 'Desligados'})
else:
    df_desligados = df_filtro_inativos[df_filtro_inativos["Departamento"] == Select_box_departamento]['Departamento'].value_counts().reset_index()
    df_desligados = df_desligados.rename(columns={'count': 'Desligados'})

#Desempenho por Departamento
desempenho_por_departamento = round(df_filtro_ativos.groupby('Departamento').agg({"Desempenho":"mean"}).reset_index(),2)

#Satisfacao por Departamento
satisfacao_por_departamento = round(df_filtro_ativos.groupby('Departamento').agg({"Satisfacao":"mean"}).reset_index(),2)

#Tela
st.title('Análise de dados de RH')

#Cards
st.markdown("""
<style>
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    border-left: 8px solid #1f1f1f; 
    margin-bottom: 10px;
}

.card-title {
    font-size: 16px;
    color: #666;
    margin-bottom: 10px;
}

.card-value {
    font-size: 32px;
    font-weight: bold;
    color: #111;
}
</style>
""", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)

cards = [
    ("Total de colaboradores", total_colaboradores_ativos),
    ("Turnover", f"{turnover}%"),
    ("Absenteísmo médio", absenteismo_medio),
    ("Desempenho médio", desempenho_medio)
]

for col, (title, value) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

#Graficos
col1, col2= st.columns(2)

with col1:
    grafico_1 = px.pie(
        df_count,
        names='Departamento',
        values='Quantidade',
        title="Funcionários ativos por departamento",

    )
    st.plotly_chart(grafico_1)
with col2:
    grafico_2 = px.bar(
        df_desligados,
        x='Departamento',
        y= 'Desligados',
        text='Desligados'   ,
        title="Desligados por Departamento",
    )
    grafico_2.update_traces(textposition='outside')  # coloca acima da barra
    st.plotly_chart(grafico_2)

col3, col4, col5= st.columns(3)

with col3:
    grafico_3 = px.bar(
        df_ajustado_por_cargo,
        x='Quantidade',
        y= 'Cargo',
        text='Quantidade'   ,
        title="Quantidade de colaboradores por cargo",
        orientation='h',
    )
    grafico_3.update_traces(textposition='outside')  # coloca acima da barra
    st.plotly_chart(grafico_3)

with col4:
    grafico_4 = px.bar(
        desempenho_por_departamento,
        x='Departamento',
        y= 'Desempenho',
        text='Desempenho' ,
        title="Desempenho por departamento",
    )
    grafico_4.update_traces(textposition='outside')  # coloca acima da barra
    st.plotly_chart(grafico_4)

with col5:
    grafico_5 = px.bar(
        satisfacao_por_departamento,
        x='Departamento',
        y='Satisfacao',
        text='Satisfacao' ,
        title="Satisfacao por departamento",
    )
    grafico_5.update_traces(textposition='outside')  # coloca acima da barra
    st.plotly_chart(grafico_5)

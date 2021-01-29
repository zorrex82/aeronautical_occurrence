# import libraries
import streamlit as st
import pandas as pd
import pydeck as pdk

DATA_URL = "https://raw.githubusercontent.com/zorrex82/aeronautical_occurrence/master/ocorrencias_aviacao.csv"


@st.cache
def load_data():
    """
    Carrega os dados de ocorrências aeronáuticas do CENIPA.

    :return: DataFrame com colunas selecionadas.
    """
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    data = pd.read_csv(DATA_URL, index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)
    data.data = data.data + " " + data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    return data


# load data from csv
df = load_data()
labels = df.classificacao.unique().tolist()

# SIDEBAR
# Parameters and number of occurrences
st.sidebar.header("Parameters")
info_sidebar = st.sidebar.empty()  # placeholder, for filtered information that will only be loaded after

# Slider of year selection
st.sidebar.subheader("Year")
year_to_filter = st.sidebar.slider('Choose the desired year', 2008, 2018, 2017)

# Checkbox from table
st.sidebar.subheader("Table")
table = st.sidebar.empty()  # placeholder there is only load with df_filtered

# Multiselect with the unique labels of the classification types
label_to_filter = st.sidebar.multiselect(
    label="Choose classification occurrence",
    options=labels,
    default=["INCIDENTE", 'ACIDENTE']
)

# Sidebar footer information
st.sidebar.markdown("""
The database of aeronautical events is managed by the *** Center for Investigation and Accident Prevention
Aeronautics (CENIPA)***.
""")

# Only here the data filtered by year is updated in a new dataframe
filtered_df = df[(df.data.dt.year == year_to_filter) & (df.classificacao.isin(label_to_filter))]

# Here the empty placehoder is finally updated with datao filtered_df
info_sidebar.info("{} selected occurrences.".format(filtered_df.shape[0]))

# MAIN
st.title("CENIPA - Aviation Accidents")
st.markdown(f"""
            ℹ️ Events classified as **{", ".join(label_to_filter)}**
            for the year **{year_to_filter}**.
            """)

# raw data (table) dependent from checkbox
if table.checkbox("Show data tables"):
    st.write(filtered_df)

# mapa
st.subheader("Occurrences Map")
st.map(filtered_df)
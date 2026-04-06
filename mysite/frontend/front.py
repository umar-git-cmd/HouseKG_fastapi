import streamlit as st
import requests

api_url = 'http://127.0.0.1:8000/predict/'

nei_list = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR',
            'MeatdowV', 'Mitchel', 'NAmes', 'NPkVIll', 'NWAmes', 'NoRidge', 'NridgHt', 'OldTown', 'SWISU', 'SAWYER',
            'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker']


st.title('Прогноз цены')

area = st.number_input('Плошадь: ', value=0)
year = st.number_input('Год: ', value=0)
garage = st.number_input('Вместимость гаража: ', value=0)
bmst = st.number_input('Площадь подвала: ', value=0)
bath = st.number_input('Количество ванных комнат: ', value=0)
overall_qual = st.number_input('Общая оценка: ', value=0)
neighborhood = st.selectbox('Район: ', nei_list)


data = {
    'GrLivArea': area,
    'YearBuilt': year,
    'GarageCars': garage,
    'TotalBsmtSF': bmst,
    'FullBath': bath,
    'OverallQual': overall_qual,
    'Neighborhood': neighborhood
}

if st.button('Проверка'):

    try:
        answer = requests.post(api_url, json=data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(f"Результат: {result.get('Price')}")
            #st.json(result)
        else:
            st.error(f'Oшибка: {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error(f'Не удалось подключиться к API')
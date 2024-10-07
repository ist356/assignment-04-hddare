'''
Solution unibrow.py
'''
import pandas as pd
import streamlit as st
import pandaslib as pl

st.title("UniBrow")
st.caption("The Universal data browser")

uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'json'])

if uploaded_file:
    file_extension = uploaded_file.name.split('.')[-1]
    
    if file_extension == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(uploaded_file)
    elif file_extension == 'json':
        df = pd.read_json(uploaded_file, orient='records')
    else:
        st.error("Unsupported file format!")
        st.stop()

    selected_columns = st.multiselect(
        'Select columns to display',
        options=df.columns,
        default=list(df.columns)
    )

    include_filter = st.checkbox('Include filter')

    if include_filter:
        object_columns = df.select_dtypes(include='object').columns.tolist()
        
        if object_columns:
            selected_column = st.selectbox('Select a column to filter by', object_columns)
            unique_values = df[selected_column].unique().tolist()
            selected_value = st.selectbox(f'Select a value from {selected_column}', unique_values)
            df_filtered = df[df[selected_column] == selected_value]
        else:
            st.warning("No object-type columns available for filtering.")
            df_filtered = df
    else:
        df_filtered = df

    df_filtered = df_filtered[selected_columns]

    st.dataframe(df_filtered)

    st.subheader("DataFrame Description")
    st.write(df_filtered.describe())


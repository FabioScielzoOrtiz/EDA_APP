
import streamlit as st
import pandas as pd
import numpy as np
import uuid
import base64 


###################################################################

# FUNCTIONS

###################################### 

def download_button(object_to_download, file_name, button_text):
    """
    Generates a link to download the given object_to_download.
    object_to_download (str): Can be a text string or a bytes object.
    file_name (str): Name to give the file when it's downloaded.
    button_text (str): Text to display on the download button.
    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()

    button_uuid = str(uuid.uuid4())
    button_html = f'<a download="{file_name}" href="data:file/csv;base64,{b64}" id="{button_uuid}">{button_text}</a>'
    return button_html

############################################################################

st.title("Exploratory Data Analysis")

st.markdown("<br>", unsafe_allow_html=True)

# Cargar archivo CSV
st.markdown('## Load data file')
file = st.file_uploader(" ", type=["csv","xlsx"])


st.markdown("<br>", unsafe_allow_html=True)

if file is not None:

    df_original = pd.read_csv(file)

    # Crear variable de estado para el DataFrame
    state = st.session_state
    if 'df' not in state:
        state.df = df_original.copy()
    else :
        pass

    st.sidebar.header('Table of content')

############################################################################    

    if st.sidebar.checkbox('Table with the data'):
       
        st.markdown('### Table with the data')

        df = state.df
        st.write(df)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

############################################################################

    if st.sidebar.checkbox('Data size'):
       
       st.markdown('### Data size')

       df = state.df
       st.write("<div style='text-align:center'>Rows:  {}</span></div>".format(df.shape[0]), unsafe_allow_html=True)
       st.write("<div style='text-align:center'>Columns:   {}</span></div>".format(df.shape[1]), unsafe_allow_html=True)

       st.markdown("<br>", unsafe_allow_html=True)
       st.markdown("<br>", unsafe_allow_html=True)

############################################################################

    if st.sidebar.checkbox('Select columns'):

        def select_columns(Data, columns_names):
            df = Data.loc[:, columns_names]
            return df

        st.markdown('### Select columns')
        Columns_selected = st.multiselect('Select columns', options=df_original.columns, key=1)

        if st.button('Select columns'):
            state.df = select_columns(df_original, Columns_selected)
            df = state.df
            st.write(df)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

############################################################################

    if st.sidebar.checkbox('Rename columns'):

        df = state.df   
        
        st.markdown('### Rename columns')
        columns_to_rename = st.multiselect('Select columns to rename', options=df.columns, key=2)
        new_column_names = {}
        
        for column in columns_to_rename:
            new_name = st.text_input(f"Enter new name for column '{column}'", key=column+'1')
            new_column_names[column] = new_name
     
        if st.button('Rename columns'):
            state.df  = df.rename(columns=new_column_names)
            df = state.df
            st.write(df)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

#####################################################################################################################################

    if st.sidebar.checkbox('Python data types'):

       st.markdown('### Python data types')

       df = state.df
       types_df = pd.DataFrame(df.dtypes, columns=['Types'])
       st.write( types_df )
 
       st.markdown("<br>", unsafe_allow_html=True)
       st.markdown("<br>", unsafe_allow_html=True)

#####################################################################################################################################

    if st.sidebar.checkbox('Change Python data types'):

        def change_type(Data, Variable_name, New_type):
            Data[Variable_name] = Data[Variable_name].astype(New_type)

        df = state.df

        st.markdown('### Select columns to change type')
        columns_to_change = st.multiselect('Select columns', options=df.columns, key=3)

        new_type_dict = {}
        for column in columns_to_change:
            new_type = st.selectbox('Select type for ' + column, options=['float64', 'int64', 'object'], key=column + '_type')
            new_type_dict[column] = new_type

        if st.button('Change type'):
            for column in columns_to_change :
                change_type(df, Variable_name=column, New_type=new_type_dict[column])
 
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
 

#####################################################################################################################################

    if st.sidebar.checkbox('Unique values ​of variables'):
       
       def unique_values(Data, Variable_name) :
            unique_values_df = pd.DataFrame(Data[Variable_name].unique(), columns=['Unique values'])
            return unique_values_df
       

       df = state.df
       
       st.markdown('### Select variable')
       variable = st.selectbox('Select variable', options=df.columns, key=4)

       st.write( unique_values(Data=df, Variable_name=variable) )

       st.markdown("<br>", unsafe_allow_html=True)
       st.markdown("<br>", unsafe_allow_html=True)


#####################################################################################################################################

    if st.sidebar.checkbox('Proportion NaN'):
       
       def Prop_NaN(Data):
            df_prop_nan = Data.isnull().sum() / len(Data)
            df_prop_nan = pd.DataFrame(df_prop_nan, columns=['NaN Proportion'])
            return df_prop_nan

       st.markdown('### Proportion NaN')

       df = state.df
       st.write( Prop_NaN(df) )

       st.markdown("<br>", unsafe_allow_html=True)
       st.markdown("<br>", unsafe_allow_html=True)

#####################################################################################################################################

    if st.sidebar.checkbox('Download Processed Data'):

        if st.button("Download Processed Data as CSV"):
            file_processed = state.df.to_csv(index=False)
            file_name = "processed_data.csv"
            button_text = "Download CSV File"
            st.markdown(download_button(file_processed, file_name, button_text), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)  


#####################################################################################################################################

footer = f"Made by **Fabio Scielzo Ortiz**. [Personal Website](http://fabioscielzoortiz.com/)"
st.write(footer, unsafe_allow_html=True)



    
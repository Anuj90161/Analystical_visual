# import libraries
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
import streamlit as st

st.set_page_config(
    page_title='consoleflare Analytical portal',
    page_icon='📊'
)
#title 

st.title(':rainbow[Data Analytical portal]')
st.subheader(':gray[Explore Data with ease.]',divider='rainbow')

file = st.file_uploader('Drop csv or excel file ',type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)

    else:
        data = pd.read_excel(file,engine="openpyxl")
    
    st.dataframe(data)
    st.info('File is successfully Uploaded',icon ='🚨')

    st.subheader(':rainbow[Basic information of the dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15,tab16,tab17,tab18,tab19 = st.tabs(['Dataset Summary','Top and Bottom Rows','Data Types','Column Names','Missing Values', 'Unique Values','Descriptive Statistics', 'Categorical Columns', 'Numerical Columns', 'Value Counts', 'Correlation Matrix', 'Data Distribution', 'Outlier Detection', 'Data Shape', 'Null Percentage', 'Duplicate Records', 'Constant Columns', 'Column-wise Summary', 'Combined Insights' ])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and  {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical summary of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))
    
    with tab3:
        st.subheader(':grey[Data types of column]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader('Column Names in Dataset')
        st.write(list(data.columns))
    with tab5:
        st.subheader('Missing Values')
        st.dataframe(data.isnull().sum())
    with tab6:
        st.subheader('Unique Values')
        st.dataframe(data.nunique())

    with tab7:
        st.subheader('Descriptive Statistics')
        st.dataframe(data.describe(include='all'))
    with tab8:
        st.subheader('Categorical Columns')
        cat_cols = data.select_dtypes(include='object').columns
        st.write(cat_cols)

    with tab9:
        st.subheader('Numerical Columns')
        num_cols = data.select_dtypes(include='number').columns
        st.write(num_cols)
    with tab10:
        st.subheader('Value Counts')
        column = st.selectbox("Select Column", data.columns)
        st.write(data[column].value_counts())

    st.subheader(':rainbow[Column Values To Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
             column = st.selectbox('choose Columan name',options=list(data.columns))
        with col2:
            toprows = st.number_input('top rows', min_value=1,step=1)

        Count = st.button('Count')
        if (Count== True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('visualiation',divider='gray')
            fig = px.bar(data_frame=result,x=column,y='count', text='count')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)

            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)
    st.subheader(':rainbow[groupby : simplify your data Analysis]',divider='rainbow')
    st.write('The groupby lets summarize data by specific categories and groups ')
    with st.expander('group By your columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('chose your column to groupby',options=list(data.columns))
        with col2:
            operation_col = st.selectbox('choose column for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox('choose operation ',options=['sum','max','min','mean','median','count'])
        
        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col,operation)
            ).reset_index()
            st.dataframe(result)

            st.subheader(':gray[Data visualization]',divider='gray')
            graphs = st.selectbox('choose your graphs',options=['line','bar','scatter','pie','sunburst'])
            if(graphs=='line'):
                x_axis = st.selectbox('choose x axis',options=list(result.columns))
                y_axis = st.selectbox('choose y axis',options=list(result.columns))
                color = st.selectbox('color Information',options=list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif(graphs=='bar'):
                x_axis = st.selectbox('choose x axis',options=list(result.columns))
                y_axis = st.selectbox('choose y axis',options=list(result.columns))
                color = st.selectbox('color Information',options=list(result.columns))
                facet_col = st.selectbox('column information ',options=[None] +list(result.columns))
                fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)

            elif(graphs=='scatter'):
                x_axis = st.selectbox('choose x axis',options=list(result.columns))
                y_axis = st.selectbox('choose y axis',options=list(result.columns))
                color = st.selectbox('color Information',options= [None] +list(result.columns))
                size = st.selectbox('Size Column', options = [None] +list(result.columns))
                fig = px.scatter(data_frame = result,x=x_axis,y=y_axis,color=color, size=size)
                st.plotly_chart(fig)
            
            elif(graphs=='pie'):
                values = st.selectbox('choose nomarical values',options=list(result.columns))
                names = st.selectbox('choose lables',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)

            elif(graphs=='sunburst'):
                path = st.multiselect('choose your path ', options=list(result.columns))
                
                if path:  # यानी कम से कम एक column select हुआ हो
                    fig = px.sunburst(data_frame=result, path=path, values='newcol')
                    st.plotly_chart(fig)
                else:
                    st.warning("Please select at least one column for Sunburst path.")

            

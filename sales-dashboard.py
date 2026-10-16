# import Basic libries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import io

# Page setup
st.set_page_config(layout='wide')
# Title
st.markdown("""
<style>
h1{
    text-align:center;
}
</style>
""",unsafe_allow_html=True
)
st.title('Sales Analytics Dashboard📉📊')
 
# Upload files
file=st.file_uploader('Upload CSV file')

# menu 
if file:
    menu=st.radio(
        'Navigation',
        ['Home','City-Wise Sales','Category Revenue','Best Product','Filters'],
        horizontal=True,
        label_visibility='collapsed'
    )
    # read file
    df=pd.read_csv(file)
    # subheader
    st.subheader("select columns")
    # for user to select different columns
    # product columns(1)
    product_column=st.selectbox(
    "Product Column",
    df.columns)
    # sles or price columns (2)
    sale_column=st.selectbox(
        "Sale or Price Column",
         df.columns)
    # Quantity column (3)
    quantity_column=st.selectbox(
        "Quantity Column",
        df.columns)
    # city column (4)
    city_column=st.selectbox(
        "City column",
        df.columns
    )
    # emty space
    # revenue columns
    df["Revenue"]=df[quantity_column]*df[sale_column]
    # Home (1)
    if menu=='Home':
        total_revenue=df['Revenue'].sum()
        best_product=df.groupby(product_column)[quantity_column].sum().idxmax()
        highest_revenue_product=df.groupby(product_column)['Revenue'].sum().idxmax()
        st.subheader("Home")
        k1,k2,k3=st.columns(3)

        card_style="""
            background-color:white;
            border:1px solid #e0e0e0;
            padding:12px:
            border-redius:6px;
            text-align:center;  
            """
        k1.markdown(f"""
        <div style='{card_style}'>
            <div style="font-size:14px; color:gray;"> Total Revenue </div>
            <div style="font-size:22px; font weight:600;"> Rs. {total_revenue}</div>
            </div>
""",unsafe_allow_html=True)
        
        k2.markdown(f"""
                <div style='{card_style}'>
                    <div style="font-size:14px; color:gray;"> Best Selling Product </div>
                    <div style="font-size:22px; font weight:600;"> {best_product}</div>
                    </div>
        """,unsafe_allow_html=True)
        k3.markdown(f"""
                <div style='{card_style}'>
                    <div style="font-size:14px; color:gray;"> Highest Revenue Product </div>
                    <div style="font-size:22px; font weight:600;"> {highest_revenue_product}</div>
                    </div>
        """,unsafe_allow_html=True)
        # emty space
        st.markdown("""<dr/>""",unsafe_allow_html=True)
        # subheader and dataframe
        st.subheader("DataFrame")
        st.dataframe(df,use_container_width="stretch")

    # city sale (2)
    elif menu=="City-Wise Sales":
        # subheader
        st.subheader("City Wise Sales ")

        city_sale=df.groupby(city_column)["Revenue"].sum().reset_index()
        st.dataframe(city_sale,use_container_width="stretch")  
    # Category revenue (3)
    elif menu=="Category Revenue":
        # subheader
        st.subheader("Category Revenue")

        category_revenue=df.pivot_table(
            values="Revenue",
            index=product_column,
            aggfunc="sum"
        )
        st.dataframe(category_revenue)
     #Best Product (4)
    elif menu=="Best Product":
        # subheader
        st.subheader("Best Product")

        product_sales=df.groupby(product_column)[[quantity_column,"Revenue"]].sum().reset_index()

        colA,colB=st.columns(2)
        basis=colA.selectbox(
            "Select Basis",
          ["Sales (Quantity)","Revenue"]
          )
        top_n=colB.slider(
            "select Number of Top Products",
            min_value=1,
            max_value=len(product_sales),
            value=3
        )
        if basis=="Sales (Quantity)":
            top_products=product_sales.sort_values(by=quantity_column,ascending=False,).head(top_n)
        else:
            top_products=product_sales.sort_values(by="Revenue",ascending=False,).head(top_n)
        st.dataframe(top_products,use_container_width=True)
    # filters (5)
    elif menu=="Filters":
        # subheader
        st.subheader("Filters")

        coly,colz=st.columns(2)
        selected_product=coly.selectbox(
            "Select Product",
            df[product_column].unique()
        )
        min_revenue=colz.number_input(
            "Minimum Revenue",
            min_value=0,
            value=10000
        )
        filtered_df=df[
            (df[product_column]==selected_product) &
            (df["Revenue"]>=min_revenue)
        ]
        st.dataframe(filtered_df,use_container_width="stretch")

    # # Detect coulums
    numeric_cols= df.select_dtypes(include='number').columns.tolist()
    # sidebar controls
    st.sidebar.header('Controls')
    # Chart Types
    chart_type=st.sidebar.selectbox('Select Chart Types',
    ['Bar Chart','Line Chart','Pie Chart','Scatter plot'])
    # Select Columns
    X_cols=st.sidebar.selectbox('Select X-axis',df.columns)
    if numeric_cols:
        Y_cols=st.sidebar.selectbox('Select Y-axis',numeric_cols)
        # subhaeder
        st.subheader('Visualization📊')
        # Bar Chart
        if chart_type=='Bar Chart':
            bar_chart_data=(df[[X_cols,Y_cols]].set_index(X_cols))
            st.bar_chart(bar_chart_data,x_label=(X_cols),y_label=(Y_cols))

        # Line Chart
        elif chart_type=='Line Chart':
            line_chart_data=(df[[X_cols,Y_cols]].set_index(X_cols))
            st.line_chart(line_chart_data,x_label=(X_cols),y_label=(Y_cols))

        # Pie Chart
        elif chart_type=='Pie Chart':

            pie_data=df.groupby(X_cols)[Y_cols].sum()

            fig, ax=plt.subplots(figsize=(8,5))
            ax.pie(
                pie_data,
                labels=pie_data.index,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.8,
            )
            ax.axis('equal')
            st.pyplot(fig)
            # download Pie chart
            if st.button("Prepare Pie Chart Download"):
                buffer= io.BytesIO()
                fig.savefig(
                    buffer,
                    format="png",
                    dpi=300,
                    bbox_inches="tight"
                )
                buffer.seek(0)
                st.download_button(
                    label="Downlod Pie Chart ",
                    data=buffer.getvalue(),
                    file_name="pie_chart.png",
                    mime="image/png"
                )

        # Scatter plot
        elif chart_type=='Scatter plot':
            # scatter_data=df.groupby(X_cols)[Y_cols].sum()
            fig, ax=plt.subplots(figsize=(8,5))
            ax.scatter(x=df[X_cols],
                       y=df[Y_cols],
                       color="green",
                       marker=".",
                       )
            plt.title(f"Relationship Between  {X_cols}  and  {Y_cols}",pad=10.5)
            plt.xlabel(X_cols)
            plt.ylabel(Y_cols)
            st.pyplot(fig)
            # download Scatter plot
            if st.button("Prepare Scatter Plot Download"):
                            buffer= io.BytesIO()
                            fig.savefig(
                                buffer,
                                format="png",
                                dpi=300,
                                bbox_inches="tight"
                            )
                            buffer.seek(0)
                            st.download_button(
                                label="Downlod Scatter Plot",
                                data=buffer.getvalue(),
                                file_name="scatter_chart.png",
                                mime="image/png"
                            )
    else:
        st.warning('No numeric columns found in data ')

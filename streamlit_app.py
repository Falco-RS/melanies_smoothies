import streamlit as st
from snowflake.snowpark.functions import col
st.title(" Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!.")
# Campo para el nombre
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)
cnx = st.connection("snowflake")
session = cnx. session ()
my_dataframe = session.table("smoothies.public.fruit_options")
# Lista de frutas
fruit_names = my_dataframe.select(col("FRUIT_NAME")).to_pandas()["FRUIT_NAME"].tolist()
# Multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names
)
if ingredients_list:
    # Convertir lista a string
    ingredients_string = ", ".join(ingredients_list)

    st.write("Your ingredients:", ingredients_string)

    # ✅ INSERT con dos columnas
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS)
        VALUES ('{name_on_order}', '{ingredients_string}')
    """

    # Botón para insertar
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

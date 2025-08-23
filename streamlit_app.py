# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# フルーツ候補をリスト化
fruit_options = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .to_pandas()["FRUIT_NAME"]
    .tolist()
)

# 上限5個に制限
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    options=fruit_options,
    max_selections=5,
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        # パラメータ化で安全にINSERT
        session.sql(
            "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)",
            params=[ingredients_string, name_on_order],
        ).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")







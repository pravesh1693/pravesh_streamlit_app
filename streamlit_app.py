import streamlit
streamlit.title("My Parents's New Healthy Dinner")

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
# code : streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])

# Filter the rows based on selected fruits.
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)



##  New Section to display fruityvice api response:

# streamlit.header("Fruityvice Fruit Advice!")
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response)

## Let's Get the Fruityvice Data Looking a Little Nicer:

# streamlit.header("Fruityvice Fruit Advice!")
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response)

# Normalizing the data i.e., separating the values into respected fields from json format. 
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Setting the format of normalized data as Dataframe to look better.
# streamlit.dataframe(fruityvice_normalized)



## Let's removed the line of raw JSON, and separate the base URL from the fruit name (which will make it easier to use a variable there).

# streamlit.header("Fruityvice Fruit Advice!")
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")

# Normalizing the data i.e., separating the values into respected fields from json format. 
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Setting the format of normalized data as Dataframe to look better.
# streamlit.dataframe(fruityvice_normalized)

# streamlit.header("Fruityvice Fruit Advice!")


## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call:

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)


# Normalizing the data i.e., separating the values into respected fields from json format. 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Setting the format of normalized data as Dataframe to look better.
streamlit.dataframe(fruityvice_normalized)

streamlit.header("Fruityvice Fruit Advice!")

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Snowflake Connector:
import snowflake.connector

#  Let's Query Our Trial Account Metadata:
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

## Let's Query Some Data, Instead:
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST;")
# my_data_row = my_cur.fetchone()
# streamlit.text("The fruit load list contains:")
# streamlit.text(my_data_row)

## Let's Change the Streamlit Components to Make Things Look a Little Nicer:
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST;")
# my_data_row = my_cur.fetchone()
# streamlit.header("The fruit load list contains:") # Plain Text converted into Header:
# streamlit.dataframe(my_data_row) # Plain Text converted into Dataframe:

## Oops! Let's Get All the Rows, Not Just One:
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST;")
my_data_rows = my_cur.fetchall() # Fetched all the rows:
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list:
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values('from streamlit')")

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST;")
my_data_rows = my_cur.fetchall() # Fetched all the rows:
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
my_data_rows.append(add_my_fruit)

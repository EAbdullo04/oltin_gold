import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import requests  # API orqali oltin narxini olish uchun kutubxona

# Sarlavha
st.title("Oltin narxi bashorati")
st.write("Kelajakdagi sanani tanlang va bashoratlangan oltin narxini ko'ring.")

# 1. Modelni yuklash
model = joblib.load("oltin.pkl")  # Model fayli yuklangan deb hisoblanadi

# 2. Foydalanuvchidan kelajakdagi sanani olish
future_date = st.date_input("Sanani tanlang:", value=datetime(2024, 12, 13))

# Sanani xususiyatlarga ajratish
year = future_date.year
month = future_date.month
day = future_date.day
day_of_year = future_date.timetuple().tm_yday

# 3. Bashorat qilish
if st.button("Bashoratni ko'rish"):
    input_data = pd.DataFrame({
        "Year": [year],
        "Month": [month],
        "Day": [day],
        "DayOfYear": [day_of_year]
    })
    prediction = model.predict(input_data)
    st.write(f"Bashorat qilingan oltin narxi: **${prediction[0]:,.2f} USD**")

# 4. Bugungi oltin narxini olish (GoldAPI orqali)
def make_gapi_request():
    api_key = "goldapi-3eq7jsm4ip79td-io"
    symbol = "XAU"
    curr = "USD"
    url = f"https://www.goldapi.io/api/{symbol}/{curr}"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['price']
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
        return None

# Bugungi oltin narxini ko'rsatish
current_price = make_gapi_request()
if current_price:
    st.write(f"Bugungi oltin narxi: **${current_price:,.2f} USD**")
else:
    st.write("Bugungi oltin narxini olishda xatolik yuz berdi.")

# 5. Qo'shimcha ma'lumot
st.write("Oltin narxi ma'lumotlari asosida bashorat qilingan modeldan foydalaniladi.")


# # app.py
# import streamlit as st
# import pandas as pd
# import joblib
# from datetime import datetime

# # Sarlavha
# st.title("Oltin narxi bashorati")
# st.write("Kelajakdagi sanani tanlang va bashoratlangan oltin narxini ko'ring.")

# # 1. Modelni yuklash
# model = joblib.load("oltin.pkl")  # Model fayli yuklangan deb hisoblanadi

# # 2. Foydalanuvchidan kelajakdagi sanani olish
# future_date = st.date_input("Sanani tanlang:", value=datetime(2024, 12, 13))

# # Sanani xususiyatlarga ajratish
# year = future_date.year
# month = future_date.month
# day = future_date.day
# day_of_year = future_date.timetuple().tm_yday

# # 3. Bashorat qilish
# if st.button("Bashoratni ko'rish"):
#     input_data = pd.DataFrame({
#         "Year": [year],
#         "Month": [month],
#         "Day": [day],
#         "DayOfYear": [day_of_year]
#     })
#     prediction = model.predict(input_data)
#     st.write(f"Bashorat qilingan oltin narxi: **${prediction[0]:,.2f} USD**")

# # 4. Qo'shimcha ma'lumot
# st.write("Oltin narxi ma'lumotlari asosida bashorat qilingan modeldan foydalaniladi.")

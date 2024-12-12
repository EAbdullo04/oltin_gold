import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import requests  # API orqali oltin narxini olish uchun kutubxona

# Sarlavha
st.title("Oltin narxi bashorati")
st.write("Kelajakdagi sanani tanlang va bashoratlangan oltin narxini ko'ring.")

# 1. Modelni yuklash
model = joblib.load("oltin1.pkl")  # Model fayli yuklangan deb hisoblanadi

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

# 4. Bugungi oltin narxini olish (api-ninjas orqali)
def get_current_gold_price():
    api_url = 'https://api.api-ninjas.com/v1/goldprice'
    headers = {'X-Api-Key': 'BBmkbdXKOWYZHpDRy76UFw==8UmOG7IHI9XryWjO'}  # API kalitini bu yerga qo'shing

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == requests.codes.ok:
            data = response.json()
            return data['price']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
        return None

# Bugungi oltin narxini ko'rsatish
current_price = get_current_gold_price()
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

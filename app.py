import streamlit as st
import pandas as pd
import random

# Az Excel-fájl permanens beolvasása GitHub repositoryból
DATA_URL = "https://raw.githubusercontent.com/r-mark22/JV-Teszt/main/kerdesek.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(DATA_URL)

data = load_data()

st.title("Labdarúgó Játékvezetői Vizsgafelkészítő Teszt")

# Kérdések előkészítése
questions = data.sample(25).reset_index(drop=True)  # Véletlenszerűen kiválasztott 25 kérdés
user_answers = []

for idx, row in questions.iterrows():
    st.subheader(f"{idx + 1}. {row['ID']} - {row['Kérdés']}")
    options = [row['Válasz A'], row['Válasz B'], row['Válasz C'], row['Válasz D']]
    user_answer = st.radio("Válassz egy lehetőséget:", options, key=f"question_{idx}", index=-1)
    user_answers.append((user_answer, row['Helyes Válasz']))

# Kiértékelés gomb
if st.button("Eredmény kiértékelése"):
    correct_answers = sum(1 for user_answer, correct_answer in user_answers if user_answer == correct_answer)
    st.write(f"Összes helyes válasz: {correct_answers} / 25")
    
    st.subheader("Hibás válaszok:")
    for idx, (user_answer, correct_answer) in enumerate(user_answers):
        if user_answer != correct_answer:
            st.write(f"{idx + 1}. {questions.loc[idx, 'ID']} - {questions.loc[idx, 'Kérdés']}")
            st.write(f"- A te válaszod: {user_answer}")
            st.write(f"- Helyes válasz: {correct_answer}")
            st.write("---")

# Új teszt indítása
if st.button("Új teszt kezdése"):
    st.experimental_rerun()

import streamlit as st
import pandas as pd
import random
import os

# Az előre feltöltött Excel fájl neve (amit a szerverre teszünk)
EXCEL_FILE_PATH = "kerdesek.xlsx"

# Ellenőrizzük, hogy a fájl már elérhető-e a szerveren
if os.path.exists(EXCEL_FILE_PATH):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None)
else:
    # Ha nincs elérhető fájl, akkor engedélyezzük a feltöltést
    uploaded_file = st.file_uploader("Töltsd fel az Excel fájlt", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name=None)
        # Mentjük a fájlt a szerverre, hogy ne kelljen újra feltölteni
        with open(EXCEL_FILE_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        st.stop()  # Ha nincs fájl, ne fusson tovább a kód

# Az első munkalap használata
sheet_name = list(df.keys())[0]
df = df[sheet_name]

# Adatok előkészítése
df = df.dropna().reset_index(drop=True)
questions = df[['ID', 'Kérdés', 'a) válasz', 'b) válasz', 'c) válasz', 'd) válasz', 'Helyes válasz']]

# Teszt platform
st.title("Labdarúgó Játékvezetői Teszt")
st.write("Véletlenszerűen kiválasztott 25 kérdés.")

if st.button("Új teszt generálása"):
    st.session_state['random_questions'] = questions.sample(n=25, random_state=random.randint(1, 10000))
    st.session_state['user_answers'] = {}

if 'random_questions' not in st.session_state:
    st.session_state['random_questions'] = questions.sample(n=25, random_state=random.randint(1, 10000))
    st.session_state['user_answers'] = {}

for index, row in st.session_state['random_questions'].iterrows():
    st.subheader(f"{row['ID']}. {row['Kérdés']}")
    options = {'a': row['a) válasz'], 'b': row['b) válasz'], 'c': row['c) válasz'], 'd': row['d) válasz']}
    st.session_state['user_answers'][index] = st.radio(
        "Válassz egy választ:", 
        list(options.keys()), 
        format_func=lambda x: options[x],
        index=None  # Nincs előre kijelölt válasz
    )

if st.button("Eredmények kiértékelése"):
    score = sum(1 for i in st.session_state['user_answers'] if st.session_state['user_answers'][i] == st.session_state['random_questions'].loc[i, 'Helyes válasz'])
    st.write(f"Elért pontszám: {score}/25")

    # Hibás válaszok listázása
    st.subheader("Hibásan megválaszolt kérdések:")
    wrong_answers = [
        (row['ID'], row['Kérdés'], row['Helyes válasz'], row[row['Helyes válasz'] + ') válasz'])
        for i, row in st.session_state['random_questions'].iterrows()
        if st.session_state['user_answers'][i] != row['Helyes válasz']
    ]
    
    for q_id, question, correct_answer, correct_text in wrong_answers:
        st.write(f"**{q_id}. {question}**")
        st.write(f"✅ Helyes válasz: {correct_answer}) {correct_text}")

    # Új teszt gomb a végén
    if st.button("Új teszt indítása"):
        st.session_state.pop('random_questions')
        st.session_state.pop('user_answers')
        st.experimental_rerun()


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
    score = 0
    incorrect_answers = []

    for i, row in st.session_state['random_questions'].iterrows():
        user_answer = st.session_state['user_answers'].get(i, None)  # Ha nincs válasz, None
        correct_answer_letter = row['Helyes válasz'].strip()
        correct_column = correct_answer_letter + ') válasz'
        correct_answer = row.get(correct_column, "N/A")  # Ha nem találja, akkor "N/A"

        user_answer_text = row.get(user_answer + ') válasz', "N/A") if user_answer else "Nem adott választ"

        if user_answer == correct_answer_letter:
            score += 1
        else:
            incorrect_answers.append((row['ID'], row['Kérdés'], user_answer_text, correct_answer_letter, correct_answer))

    st.write(f"Elért pontszám: {score}/25")

    if incorrect_answers:
        st.write("❌ Hibás válaszaid:")
        for id, question, user_answer_text, correct_letter, correct_text in incorrect_answers:
            st.write(f"**{id}. {question}**")
            st.write(f"🔴 Rossz válaszod: {user_answer_text}")
            st.write(f"✅ Helyes válasz: ({correct_letter}) - {correct_text}")
            st.write("---")

    # Új teszt gomb egyedi kulccsal
    if st.button("Új teszt indítása", key="restart_test"):
        st.session_state['random_questions'] = questions.sample(n=25, random_state=random.randint(1, 10000))
        st.session_state['user_answers'] = {}
        st.experimental_rerun()  # Az oldal újratöltése, hogy az elejére ugorjon



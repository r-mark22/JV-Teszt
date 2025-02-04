import streamlit as st
import pandas as pd
import random

# Fájl feltöltése Streamlit-en keresztül
uploaded_file = st.file_uploader("Töltsd fel az Excel fájlt", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name=None)
    sheet_name = list(df.keys())[0]  # Az első munkalapot használjuk
    df = df[sheet_name]
    
    # Adatok előkészítése
    df = df.dropna().reset_index(drop=True)
    questions = df[['Kérdés', 'a) válasz', 'b) válasz', 'c) válasz', 'd) válasz', 'Helyes válasz']]

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
        st.subheader(row['Kérdés'])
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

        # Helytelen válaszok kiértékelése
        incorrect_answers = []
        for i in st.session_state['user_answers']:
            if st.session_state['user_answers'][i] != st.session_state['random_questions'].loc[i, 'Helyes válasz']:
                incorrect_answers.append((st.session_state['random_questions'].loc[i, 'Kérdés'], 
                                           st.session_state['user_answers'][i], 
                                           st.session_state['random_questions'].loc[i, 'Helyes válasz']))

        if incorrect_answers:
            st.write("Helytelenül megválaszolt kérdések:")
            for question, user_answer, correct_answer in incorrect_answers:
                st.write(f"Kérdés: {question}")
                st.write(f"Te válaszoltál: {user_answer}")
                st.write(f"Helyes válasz: {correct_answer}")

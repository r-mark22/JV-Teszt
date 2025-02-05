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

# Kérdések tárolása session state-ben
if "questions" not in st.session_state:
    st.session_state.questions = data.dropna().sample(25).reset_index(drop=True)
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * 25

questions = st.session_state.questions
user_answers = st.session_state.user_answers

for idx, row in questions.iterrows():
    st.subheader(f"{idx + 1}. {row['Kérdés']}")
    options = [row['a) válasz'], row['b) válasz'], row['c) válasz'], row['d) válasz']]
    default_selection = options.index(st.session_state.user_answers[idx]) if st.session_state.user_answers[idx] in options else -1
    user_answer = st.radio(
        "", options, key=f"question_{idx}", index=default_selection if default_selection != -1 else None
    )
    if user_answer:
        st.session_state.user_answers[idx] = user_answer

# Kiértékelés gomb
if st.button("Eredmény kiértékelése"):
    correct_answers = sum(1 for idx, correct_answer in enumerate(questions['Helyes válasz'])
                           if st.session_state.user_answers[idx] == questions.loc[idx, correct_answer + ') válasz'])
    st.write(f"Összes helyes válasz: {correct_answers} / 25")
    
    st.subheader("Hibás válaszok:")
    for idx, user_answer in enumerate(st.session_state.user_answers):
        correct_option = questions.loc[idx, questions.loc[idx, 'Helyes válasz'] + ') válasz']
        if user_answer != correct_option:
            st.write(f"{idx + 1}. {questions.loc[idx, 'Kérdés']}")
            st.write(f"- A te válaszod: {user_answer if user_answer else 'Nincs válasz'}")
            st.write(f"- Helyes válasz: {correct_option}")
            st.write("---")

# JavaScript görgetés az oldal tetejére beillesztése
scroll_to_top_js = """
    <script>
        window.onload = () => window.scrollTo(0, 0);
    </script>
"""

# Új teszt indítása
if st.button("Új teszt kezdése"):
    st.session_state.clear()
    st.markdown(scroll_to_top_js, unsafe_allow_html=True)
    st.rerun()

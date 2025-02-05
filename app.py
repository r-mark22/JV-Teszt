import streamlit as st
import pandas as pd
import random

# Fájl feltöltése csak egyszer
@st.cache_data
def load_data():
    df = pd.read_excel("kerdesek.xlsx", sheet_name=None)
    sheet_name = list(df.keys())[0]  # Az első munkalap használata
    df = df[sheet_name]
    df = df.dropna().reset_index(drop=True)
    return df

df = load_data()

# Teszt generálása
def generate_test():
    st.session_state['random_questions'] = df.sample(n=25, random_state=random.randint(1, 10000))
    st.session_state['user_answers'] = {}
    st.session_state['test_finished'] = False

if 'random_questions' not in st.session_state:
    generate_test()

st.title("Labdarúgó Játékvezetői Teszt")
st.write("Véletlenszerűen kiválasztott 25 kérdés.")

for index, row in st.session_state['random_questions'].iterrows():
    st.subheader(f"{row['ID']}. {row['Kérdés']}")
    options = {'A': row['a) válasz'], 'B': row['b) válasz'], 'C': row['c) válasz'], 'D': row['d) válasz']}
    selected_option = st.radio(
        f"Válassz egy választ:", 
        list(options.keys()), 
        format_func=lambda x: options[x], 
        index=None,  # Alapértelmezett nincs kijelölve
        key=f"question_{index}"
    )
    st.session_state['user_answers'][index] = selected_option

if st.button("Eredmények kiértékelése"):
    score = 0
    incorrect_answers = []
    
    for i, row in st.session_state['random_questions'].iterrows():
        user_answer = st.session_state['user_answers'].get(i, None)
        correct_answer_letter = row['Helyes válasz'].strip().upper()
        correct_column = correct_answer_letter + ') válasz'
        
        if correct_answer_letter in ['A', 'B', 'C', 'D'] and correct_column in row:
            correct_text = row[correct_column]
        else:
            correct_text = "**⚠️ Hiba: a helyes válasz nincs megfelelően megadva az Excelben!**"

        user_answer_text = row.get(user_answer + ') válasz', "Nem adott választ") if user_answer else "Nem adott választ"

        if user_answer == correct_answer_letter:
            score += 1
        else:
            incorrect_answers.append((row['ID'], row['Kérdés'], user_answer_text, correct_answer_letter, correct_text))

    st.session_state['test_finished'] = True

    st.write(f"### Elért pontszám: {score}/25")

    if incorrect_answers:
        st.write("### Hibásan megválaszolt kérdések:")
        for q_id, question, wrong, correct_letter, correct_text in incorrect_answers:
            st.write(f"**{q_id}. {question}**")
            st.write(f"🔴 Rossz válasz: {wrong}")
            st.write(f"✅ Helyes válasz: ({correct_letter}) - {correct_text}")
            st.write("---")

# Új teszt generálása gomb, ami frissít és az oldal tetejére ugrik
if st.session_state.get('test_finished', False):
    if st.button("Új teszt generálása"):
        generate_test()
        st.experimental_rerun()  # Újratöltés az oldal tetejére ugrás érdekében




import streamlit as st
import pandas as pd
import time
import base64
import os

# 1. Настройка страницы
st.set_page_config(
    page_title="Физкультура: Контроль знаний",
    layout="centered",
    page_icon="⚽"
)

# 2. Функция фонового изображения и стилизации под карточки НВТП
def set_custom_theme(png_file="background.png"):
    bg_css = ""
    if os.path.exists(png_file):
        with open(png_file, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        bg_css = f'background-image: url("data:image/png;base64,{bin_str}"); background-size: cover; background-position: center; background-attachment: fixed;'
    
    style = f"""
    <style>
    .stApp {{
        {bg_css}
        background-color: #1a241a;
    }}
    
    /* Стилизация карточек-блоков как в НВТП */
    .info-card {{
        background-color: rgba(35, 48, 35, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 12px;
        color: #ffffff;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    
    .main-title {{
        font-size: 22px;
        font-weight: bold;
        letter-spacing: 1px;
    }}
    
    .teacher-title {{
        font-size: 15px;
        color: #d1e7dd;
    }}

    .teacher-name {{
        font-size: 18px;
        font-weight: bold;
    }}

    /* Поля ввода */
    .stTextInput input, .stSelectbox select {{
        background-color: #1e2620 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid #3a4d3a !important;
        text-align: center;
    }}
    
    /* Кнопки классов */
    .stButton>button {{
        width: 100%;
        background-color: #243324 !important;
        color: white !important;
        border: 1px solid #3d543d !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-weight: bold !important;
    }}
    .stButton>button:hover {{
        background-color: #2e422e !important;
        border-color: #4f6e4f !important;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

set_custom_theme()

# 3. База данных вопросов по Физической культуре
DATABASE = {
    "10 класс": {
        "Легкая атлетика": [
            ("Какая дистанция относится к короткому спринтерскому бегу?", ["100 метров", "1500 метров", "3000 метров", "10 000 метров"], "100 метров"),
            ("Какое физическое качество развивает бег на длинные дистанции?", ["Общую выносливость", "Быстроту реакций", "Гибкость", "Взрывную силу"], "Общую выносливость"),
            ("С какого старта выполняется бег на короткие дистанции?", ["С низкого старта", "С высокого старта", "С согнутых колен", "Произвольно"], "С низкого старта")
        ],
        "Спортивные игры": [
            ("Сколько игроков одной команды находится на площадке в волейболе?", ["6 игроков", "5 игроков", "7 игроков", "11 игроков"], "6 игроков"),
            ("Сколько очков начисляется за точный бросок из-за 3-очковой дуги в баскетболе?", ["3 очка", "2 очка", "1 очко", "4 очка"], "3 очка")
        ]
    },
    "11 класс": {
        "Футбол и правила": [
            ("Что означает термин «офсайд» в футболе?", ["Положение «вне игры»", "Штрафной удар", "Угловой удар", "Нарушение правил"], "Положение «вне игры»"),
            ("Продолжительность одного тайма в стандартном футбольном матче:", ["45 минут", "40 минут", "30 минут", "50 минут"], "45 минут")
        ],
        "ЗОЖ и Физиология": [
            ("Какой показатель пульса (ЧСС) в покое считается нормой для здорового человека?", ["60–80 уд/мин", "30–40 уд/мин", "100–120 уд/мин", "140–160 уд/мин"], "60–80 уд/мин"),
            ("Основная цель разминки перед физической нагрузкой:", ["Подготовка организма и разогрев мышц", "Утомление", "Проверка гибкости", "Охлаждение"], "Подготовка организма и разогрев мышц")
        ]
    }
}

# 4. Состояния сессии
if "started" not in st.session_state:
    st.session_state.started = False
if "selected_grade" not in st.session_state:
    st.session_state.selected_grade = None

# 5. Главный интерфейс (Карточки)
if not st.session_state.started:
    
    # Верхняя плашка
    st.markdown('<div class="info-card teacher-title">Преподаватель физической культуры</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card teacher-name">Семенков Денис Алексеевич</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card main-title">⚽ КОНТРОЛЬ ЗНАНИЙ ПО ФИЗКУЛЬТУРЕ</div>', unsafe_allow_html=True)
    
    # Ввод ФИО
    student_name = st.text_input("Фамилия и Имя ученика:", key="student_input")
    
    st.markdown('<div class="info-card">Выберите класс:</div>', unsafe_allow_html=True)
    
    # Кнопки выбора класса в 2 колонки
    col1, col2 = st.columns(2)
    with col1:
        if st.button("10 КЛАСС 📘"):
            if not student_name.strip():
                st.error("Введите Фамилию и Имя!")
            else:
                st.session_state.selected_grade = "10 класс"
                st.session_state.student_name = student_name
                st.session_state.started = True
                st.rerun()

    with col2:
        if st.button("11 КЛАСС 📕"):
            if not student_name.strip():
                st.error("Введите Фамилию и Имя!")
            else:
                st.session_state.selected_grade = "11 класс"
                st.session_state.student_name = student_name
                st.session_state.started = True
                st.rerun()

    st.markdown("---")
    
    # Кабинет преподавателя внизу
    with st.expander("🔐 КАБИНЕТ ПРЕПОДАВАТЕЛЯ"):
        pin = st.text_input("Введите PIN-код:", type="password")
        if pin == "1234":
            st.success("Доступ разрешен")
            if os.path.exists("detailed_results.csv"):
                df = pd.read_csv("detailed_results.csv")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 Скачать CSV", csv, "результаты.csv", "text/csv")
            else:
                st.info("Результатов пока нет.")

# 6. Экран тестирования
else:
    st.markdown(f'<div class="info-card">Ученик: <b>{st.session_state.student_name}</b> | Класс: <b>{st.session_state.selected_grade}</b></div>', unsafe_allow_html=True)
    
    topics = list(DATABASE[st.session_state.selected_grade].keys())
    selected_topic = st.selectbox("Выберите тему:", topics)
    
    questions = DATABASE[st.session_state.selected_grade][selected_topic]
    
    with st.form("quiz"):
        answers = {}
        for idx, (q, opts, ans) in enumerate(questions):
            st.markdown(f"**Вопрос {idx+1}:** {q}")
            answers[idx] = st.radio(f"q_{idx}", opts, label_visibility="collapsed")
            st.divider()
        
        if st.form_submit_button("✅ Отправить ответы"):
            score = sum(1 for idx, (q, opts, ans) in enumerate(questions) if answers.get(idx) == ans)
            total = len(questions)
            st.success(f"Тест завершен! Результат: {score} из {total}")
            
            # Сохранение в CSV
            res = pd.DataFrame([{
                "Дата": time.strftime("%Y-%m-%d %H:%M"),
                "ФИО": st.session_state.student_name,
                "Класс": st.session_state.selected_grade,
                "Тема": selected_topic,
                "Балл": f"{score}/{total}"
            }])
            res.to_csv("detailed_results.csv", mode='a', header=not os.path.exists("detailed_results.csv"), index=False, encoding='utf-8-sig')
            
            if st.button("На главную"):
                st.session_state.started = False
                st.rerun()

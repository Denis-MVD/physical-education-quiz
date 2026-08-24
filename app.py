import streamlit as st
import pandas as pd
import time
import base64
import os

# 1. Настройка страницы
st.set_page_config(
    page_title="Физическая культура: Контроль знаний",
    layout="wide",
    page_icon="⚽"
)

# 2. Функция фонового изображения
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
        background-color: #1e241e;
    }}
    .stMarkdown, .stSelectbox, .stTextInput, .stRadio, .stButton, div[data-baseweb="select"] {{
        background-color: rgba(35, 43, 33, 0.90) !important;
        padding: 12px;
        border-radius: 10px;
        color: #ffffff !important;
    }}
    .stButton>button {{
        width: 100%;
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold;
        border: none;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

set_custom_theme()

# 3. База данных вопросов по Физической культуре
DATABASE = {
    "10 класс": {
        "Легкая атлетика и Бег": [
            ("Какая дистанция относится к короткому спринтерскому бегу?", ["100 метров", "1500 метров", "3000 метров", "10 000 метров"], "100 метров"),
            ("Какое физическое качество развивает бег на длинные дистанции?", ["Общую выносливость", "Быстроту реакций", "Гибкость", "Взрывную силу"], "Общую выносливость"),
            ("С какого старта выполняется бег на короткие дистанции (спринт)?", ["С низкого старта", "С высокого старта", "С согнутых колен", "Произвольно"], "С низкого старта")
        ],
        "Спортивные игры (Волейбол, Баскетбол)": [
            ("Сколько игроков одной команды находится на площадке в волейболе?", ["6 игроков", "5 игроков", "7 игроков", "11 игроков"], "6 игроков"),
            ("Сколько очков начисляется за точный бросок из-за 3-очковой дуги в баскетболе?", ["3 очка", "2 очка", "1 очко", "4 очка"], "3 очка"),
            ("Сколько шагов с мячом в руках разрешено сделать в баскетболе без ведения?", ["Не более 2 шагов", "3 шага", "1 шаг", "Сколько угодно"], "Не более 2 шагов")
        ]
    },
    "11 класс": {
        "Футбол и правила соревнований": [
            ("Что означает термин «офсайд» в футболе?", ["Положение «вне игры»", "Штрафной удар", "Угловой удар", "Нарушение правил в штрафной"], "Положение «вне игры»"),
            ("Продолжительность одного тайма в стандартном футбольном матче:", ["45 минут", "40 минут", "30 минут", "50 минут"], "45 минут"),
            ("Каким образом вводится мяч из-за боковой линии в футболе?", ["Броском двумя руками из-за головы", "Ударом ногой с земли", "Броском одной рукой", "Любым удобным способом"], "Броском двумя руками из-за головы")
        ],
        "ЗОЖ, Самоконтроль и Физиология": [
            ("Какой показатель пульса (ЧСС) в покое считается нормой для здорового взрослого человека?", ["60–80 уд/мин", "30–40 уд/мин", "100–120 уд/мин", "140–160 уд/мин"], "60–80 уд/мин"),
            ("Что такое гипертрофия мышц?", ["Увеличение объема и массы мышц", "Уменьшение мышечной ткани", "Растяжение связок", "Накопление молочной кислоты"], "Увеличение объема и массы мышц"),
            ("Основная цель разминки перед физической нагрузкой:", ["Подготовка организма и разогрев мышц", "Максимальная утомляемость", "Проверка гибкости", "Охлаждение тела"], "Подготовка организма и разогрев мышц")
        ]
    }
}

# 4. Шапка программы
st.title("⚽ Зачёт по Физической культуре и спорту")
st.write("Онлайн-система тестирования и контроля знаний")

# 5. Панель преподавателя (Боковое меню)
st.sidebar.header("🔐 Панель преподавателя")
teacher_pin = st.sidebar.text_input("Введите PIN-код для доступа:", type="password")

if teacher_pin == "1234":
    st.sidebar.success("Доступ разрешен")
    st.sidebar.subheader("Журнал результатов")
    if os.path.exists("detailed_results.csv"):
        df_results = pd.read_csv("detailed_results.csv")
        st.sidebar.dataframe(df_results)
        
        csv_data = df_results.to_csv(index=False).encode('utf-8-sig')
        st.sidebar.download_button(
            label="📥 Скачать CSV с отчетом",
            data=csv_data,
            file_name="результаты_физкультура.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.info("Файл с результатами пока не создан.")
elif teacher_pin != "":
    st.sidebar.error("Неверный PIN-код")

# 6. Основной блок тестирования
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.subheader("📋 Регистрация учащегося")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("ФИО ученика:")
        selected_grade = st.selectbox("Выберите класс:", list(DATABASE.keys()))
    with col2:
        selected_topic = st.selectbox("Выберите тему:", list(DATABASE[selected_grade].keys()))
    
    if st.button("🚀 Начать тестирование"):
        if not student_name.strip():
            st.error("Пожалуйста, введите ваши ФИО.")
        else:
            st.session_state.started = True
            st.session_state.student_name = student_name
            st.session_state.selected_grade = selected_grade
            st.session_state.selected_topic = selected_topic
            st.session_state.start_time = time.time()
            st.session_state.time_limit = 15 * 60  # 15 минут
            st.rerun()

else:
    # Расчет таймера
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = st.session_state.time_limit - elapsed_time
    
    if remaining_time <= 0:
        st.warning("⏱️ Время на тестирование истекло! Тест отправлен автоматически.")
        force_submit = True
    else:
        mins, secs = divmod(int(remaining_time), 60)
        st.info(f"👤 Ученик: **{st.session_state.student_name}** | ⏱️ Оставшееся время: **{mins:02d}:{secs:02d}**")
        force_submit = False

    questions = DATABASE[st.session_state.selected_grade][st.session_state.selected_topic]
    
    with st.form("quiz_form"):
        user_answers = {}
        for idx, (q_text, options, correct) in enumerate(questions):
            st.markdown(f"**Вопрос {idx + 1}:** {q_text}")
            user_answers[idx] = st.radio(
                f"Выберите ответ на вопрос №{idx+1}:", 
                options, 
                key=f"q_{idx}",
                label_visibility="collapsed"
            )
            st.divider()
        
        submitted = st.form_submit_button("✅ Завершить и отправить тест")
        
        if submitted or force_submit:
            score = 0
            for idx, (q_text, options, correct) in enumerate(questions):
                if user_answers.get(idx) == correct:
                    score += 1
            
            total_q = len(questions)
            percent = (score / total_q) * 100
            
            st.success(f"Тест успешно завершен! Ваш результат: **{score} из {total_q}** ({percent:.1f}%)")
            
            # Сохранение в CSV
            res_dict = {
                "Дата/Время": [time.strftime("%Y-%m-%d %H:%M:%S")],
                "ФИО": [st.session_state.student_name],
                "Класс": [st.session_state.selected_grade],
                "Тема": [st.session_state.selected_topic],
                "Балл": [score],
                "Всего вопросов": [total_q],
                "Процент": [f"{percent:.1f}%"]
            }
            new_df = pd.DataFrame(res_dict)
            
            if not os.path.isfile("detailed_results.csv"):
                new_df.to_csv("detailed_results.csv", index=False, encoding='utf-8-sig')
            else:
                new_df.to_csv("detailed_results.csv", mode='a', header=False, index=False, encoding='utf-8-sig')
            
            st.session_state.started = False
            if st.button("Пройти еще раз"):
                st.rerun()

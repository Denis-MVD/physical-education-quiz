import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import io

# --- 1. НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="Интерактивная платформа по Физической Культуре",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ИНИЦИАЛИЗА SESSION STATE ---
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "guide"
if "test_results" not in st.session_state:
    st.session_state.test_results = []

# --- 3. БОКОВОЕ МЕНЮ (НАВИГАЦИЯ) ---
st.sidebar.title("📌 Разделы платформы")
st.sidebar.markdown("---")

menu_options = [
    "📚 Справочник", 
    "📝 Контрольное тестирование", 
    "🎮 Игра Sonic Runner", 
    "📊 Журнал результатов"
]

mode_map = {
    "📚 Справочник": "guide",
    "📝 Контрольное тестирование": "testing",
    "🎮 Игра Sonic Runner": "game",
    "📊 Журнал результатов": "results"
}

current_index = list(mode_map.values()).index(st.session_state.app_mode)
selected_menu = st.sidebar.radio("Перейти к разделу:", menu_options, index=current_index)
st.session_state.app_mode = mode_map[selected_menu]

# --- 4. ШАПКА ПЛАТФОРМЫ ---
st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🏃‍♂️ ПЛАТФОРМА КОНТРОЛЯ ЗНАНИЙ ПО ФИЗИЧЕСКОЙ КУЛЬТУРЕ</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Единый учебно-методический комплекс с игровым модулем</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# РАЗДЕЛ 1: ТЕОРЕТИЧЕСКИЙ СПРАВОЧНИК
# ==========================================
if st.session_state.app_mode == "guide":
    st.subheader("📚 Теоретический справочник по Физической Культуре")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏀 Баскетбол", "⚽ Футбол", "🏐 Волейбол", "🏃 Лёгкая атлетика & Гимнастика"])
    
    with tab1:
        st.markdown("**Баскетбол:**")
        st.write("* **Состав команды:** 5 игроков на площадке.")
        st.write("* **Размеры площадки:** 28 × 15 метров.")
        st.write("* **Начисление очков:** 1 очко — штрафной бросок, 2 очка — бросок из средней/ближней зоны, 3 очка — из-за дуги (6.75 м).")
        st.write("* **Правило ведения:** Нельзя делать более 2 шагов без ведения мяча (пробежка).")

    with tab2:
        st.markdown("**Футбол:**")
        st.write("* **Состав команды:** 11 игроков (10 полевых + 1 вратарь).")
        st.write("* **Ворота:** ширина — **7.32 м**, высота — **2.44 м**.")
        st.write("* **Продолжительность матча:** 2 тайма по 45 минут с 15-минутным перерывом.")

    with tab3:
        st.markdown("**Волейбол:**")
        st.write("* **Состав команды:** 6 игроков на площадке.")
        st.write("* **Касания:** Не более 3 касаний команды для перевода мяча через сетку.")
        st.write("* **Счет:** Игра ведется до победы в 3 партиях, каждая партия — до 25 очков (тай-брейк — до 15).")

    with tab4:
        st.markdown("**Лёгкая атлетика и Гимнастика:**")
        st.write("* **Бег на короткие дистанции (100м, 200м, 400м):** выполняется с **низкого старта** с использованием стартовых колодок.")
        st.write("* **Бег на средние и длинные дистанции:** выполняется с **высокого старта**.")
        st.write("* **Гимнастика:** Для предотвращения соскальзывания рук со снарядов (перекладина, брусья, кольца) используется **магнезия**.")

# ==========================================
# РАЗДЕЛ 2: КОНТРОЛЬНОЕ ТЕСТИРОВАНИЕ
# ==========================================
elif st.session_state.app_mode == "testing":
    st.subheader("📝 Контрольное тестирование")
    
    col_student1, col_student2 = st.columns(2)
    with col_student1:
        student_name = st.text_input("ФИО Ученика:", value="Ученик 1")
    with col_student2:
        student_class = st.selectbox("Класс:", ["5 класс", "6 класс", "7 класс", "8 класс", "9 класс", "10 класс", "11 класс"])

    st.markdown("---")

    questions_data = [
        {"q": "1. Сколько игроков от одной команды находится на площадке в баскетболе?", "options": ["5 игроков", "6 игроков", "11 игроков", "4 игрока"], "ans": 0},
        {"q": "2. Какова официальная ширина ворот в футболе?", "options": ["7.32 м", "6.00 м", "8.00 м", "5.50 м"], "ans": 0},
        {"q": "3. Какое максимальное число касаний мяча разрешено в волейболе?", "options": ["3 касания", "2 касания", "4 касания", "Без ограничений"], "ans": 0},
        {"q": "4. С какого старта выполняются беговые дисциплины на короткие дистанции?", "options": ["Низкий старт", "Высокий старт", "Средний старт", "Старт с ходу"], "ans": 0},
        {"q": "5. Средство для предотвращения скольжения рук на гимнастических снарядах?", "options": ["Магнезия", "Тальк", "Мел", "Воск"], "ans": 0}
    ]

    with st.form("quiz_form"):
        user_answers = []
        for i, q in enumerate(questions_data):
            ans = st.radio(q["q"], q["options"], key=f"test_q_{i}")
            user_answers.append(q["options"].index(ans))
        
        submitted = st.form_submit_button("✅ Сдать тест")
        if submitted:
            score = sum([1 for i, q in enumerate(questions_data) if user_answers[i] == q["ans"]])
            total = len(questions_data)
            percent = int((score / total) * 100)
            
            st.success(f"Тест сдан! Результат: {score} из {total} ({percent}%)")
            
            st.session_state.test_results.append({
                "ФИО": student_name,
                "Класс": student_class,
                "Баллы": f"{score}/{total}",
                "Процент": f"{percent}%",
                "Режим": "Тестирование"
            })

# ==========================================
# РАЗДЕЛ 3: 2D-ИГРА SONIC RUNNER
# ==========================================
elif st.session_state.app_mode == "game":
    st.markdown("<h3 style='color: #ffffff; text-align: center; margin-bottom: 15px;'>⚡ Sonic PE Quiz Runner</h3>", unsafe_allow_html=True)
    
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            game_html = f.read()
        components.html(game_html, height=520, scrolling=False)
    except FileNotFoundError:
        st.error("⚠️ Файл index.html не найден. Поместите файл index.html в ту же папку, где лежит app.py!")

# ==========================================
# РАЗДЕЛ 4: ЖУРНАЛ РЕЗУЛЬТАТОВ
# ==========================================
elif st.session_state.app_mode == "results":
    st.subheader("📊 Журнал результатов учащихся")
    
    if len(st.session_state.test_results) > 0:
        df = pd.DataFrame(st.session_state.test_results)
        st.dataframe(df, use_container_width=True)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Результаты')
        
        st.download_button(
            label="📥 Скачать журнал результатов (Excel)",
            data=buffer.getvalue(),
            file_name="results_pe.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Журнал пока пуст. Пройдите контрольное тестирование в соответствующем разделе.")

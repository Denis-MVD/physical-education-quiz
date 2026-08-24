import streamlit as st
import pandas as pd
import time
import base64
import os

# 1. Настройка страницы
st.set_page_config(
    page_title="Физкультура: Контроль знаний",
    layout="wide",
    page_icon="⚽"
)

# 2. Функция фонового изображения и оформления
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
        background-color: #1b241b;
    }}
    .stMarkdown, .stSelectbox, .stTextInput, .stRadio, .stButton, div[data-baseweb="select"] {{
        background-color: rgba(28, 38, 28, 0.92) !important;
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
        padding: 10px;
        font-size: 16px;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

set_custom_theme()

# 3. База данных вопросов по Физкультуре
DATABASE = {
    "10 класс": {
        "Легкая атлетика": [
            ("Какая дистанция относится к короткому спринтерскому бегу?", ["100 метров", "1500 метров", "3000 метров", "10 000 метров"], "100 метров"),
            ("Какое физическое качество развивает бег на длинные дистанции?", ["Общую выносливость", "Быстроту реакций", "Гибкость", "Взрывную силу"], "Общую выносливость"),
            ("С какого старта выполняется бег на короткие дистанции?", ["С низкого старта", "С высокого старта", "С согнутых колен", "Произвольно"], "С низкого старта"),
            ("Что передают бегуны друг другу в эстафетном беге?", ["Эстафетную палочку", "Мяч", "Ленту", "Флажок"], "Эстафетную палочку"),
            ("В какой фазе прыжка в длину с разбега происходит отталкивание?", ["На бруске отталкивания", "В полете", "При приземлении", "Во время разбега"], "На бруске отталкивания")
        ],
        "Спортивные игры (Волейбол, Баскетбол)": [
            ("Сколько игроков одной команды находится на площадке в волейболе?", ["6 игроков", "5 игроков", "7 игроков", "11 игроков"], "6 игроков"),
            ("Сколько очков начисляется за точный бросок из-за 3-очковой дуги в баскетболе?", ["3 очка", "2 очка", "1 очко", "4 очка"], "3 очка"),
            ("Сколько шагов с мячом в руках разрешено сделать в баскетболе без ведения?", ["Не более 2 шагов", "3 шага", "1 шаг", "Сколько угодно"], "Не более 2 шагов"),
            ("Сколько касаний мяча разрешено сделать одной команде в волейболе перед перебиванием на сторону соперника?", ["Не более 3 касаний", "2 касания", "4 касания", "Без ограничений"], "Не более 3 касаний"),
            ("Какое нарушение фиксируется в баскетболе при движении с мячом без ведения более 2 шагов?", ["Пробежка", "Фол", "Аут", "Задержка игры"], "Пробежка")
        ]
    },
    "11 класс": {
        "Футбол и правила соревнований": [
            ("Что означает термин «офсайд» в футболе?", ["Положение «вне игры»", "Штрафной удар", "Угловой удар", "Нарушение правил"], "Положение «вне игры»"),
            ("Продолжительность одного тайма в стандартном футбольном матче:", ["45 минут", "40 минут", "30 минут", "50 минут"], "45 минут"),
            ("Каким образом вводится мяч из-за боковой линии в футболе?", ["Броском двумя руками из-за головы", "Ударом ногой с земли", "Броском одной рукой", "Любым способ"], "Броском двумя руками из-за головы"),
            ("Какое наказание следует за грубое нарушение правил или вторую желтую карточку в футболе?", ["Красная карточка (удаление)", "Предупреждение", "Штрафной очко", "Замена игрока"], "Красная карточка (удаление)"),
            ("Какой игрок в футболе имеет право играть руками в своей штрафной площади?", ["Вратарь", "Капитан", "Защитник", "Нападающий"], "Вратарь")
        ],
        "ЗОЖ и Физиология": [
            ("Какой показатель пульса (ЧСС) в покое считается нормой для здорового человека?", ["60–80 уд/мин", "30–40 уд/мин", "100–120 уд/мин", "140–160 уд/мин"], "60–80 уд/мин"),
            ("Основная цель разминки перед физической нагрузкой:", ["Подготовка организма и разогрев мышц", "Максимальное утомление", "Проверка гибкости", "Охлаждение тела"], "Подготовка организма и разогрев мышц"),
            ("Что такое гиподинамия?", ["Малоподвижный образ жизни", "Переизбыток физических нагрузок", "Правильное питание", "Повышенное давление"], "Малоподвижный образ жизни"),
            ("Какое физическое качество проверяется с помощью подтягиваний на перекладине?", ["Сила и силовая выносливость", "Гибкость", "Быстрота", "Координация"], "Сила и силовая выносливость"),
            ("Состояние организма, возникающее в результате длительной или интенсивной физической работы:", ["Утомление", "Гипертрофия", "Закаливание", "Гипоксия"], "Утомление")
        ]
    }
}

# Расчет 5-балльной оценки
def calculate_grade(percent):
    if percent >= 85:
        return "5 (Отлично)", "🟢"
    elif percent >= 65:
        return "4 (Хорошо)", "🔵"
    elif percent >= 50:
        return "3 (Удовлетворительно)", "🟡"
    else:
        return "2 (Неудовлетворительно)", "🔴"

# 4. Шапка программы
st.title("⚽ Зачёт по Физической культуре и спорту")
st.write("Система онлайн-тестирования и учета успеваемости")

# 5. Панель преподавателя (Боковое меню)
st.sidebar.header("🔐 Панель преподавателя")
teacher_pin = st.sidebar.text_input("Введите PIN-код:", type="password")

if teacher_pin == "1234":
    st.sidebar.success("Доступ разрешен")
    st.sidebar.subheader("Журнал оценок")
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
        st.sidebar.info("Журнал результатов пока пуст.")
elif teacher_pin != "":
    st.sidebar.error("Неверный PIN-код")

# 6. Логика тестирования
if "started" not in st.session_state:
    st.session_state.started = False
if "finished" not in st.session_state:
    st.session_state.finished = False

if not st.session_state.started and not st.session_state.finished:
    st.subheader("📋 Регистрация учащегося")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("ФИО ученика:")
        selected_grade = st.selectbox("Выберите класс:", list(DATABASE.keys()))
    with col2:
        student_letter = st.text_input("Литера класса (например: А, Б, В):")
        selected_topic = st.selectbox("Выберите тему:", list(DATABASE[selected_grade].keys()))
    
    if st.button("🚀 Начать тестирование"):
        if not student_name.strip():
            st.error("Пожалуйста, введите ваши ФИО.")
        else:
            st.session_state.started = True
            st.session_state.student_name = student_name
            st.session_state.full_class = f"{selected_grade} '{student_letter.strip().upper()}'" if student_letter else selected_grade
            st.session_state.selected_grade = selected_grade
            st.session_state.selected_topic = selected_topic
            st.session_state.start_time = time.time()
            st.session_state.time_limit = 15 * 60  # 15 минут
            st.rerun()

elif st.session_state.started:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = st.session_state.time_limit - elapsed_time
    
    if remaining_time <= 0:
        st.warning("⏱️ Время на тестирование истекло! Тест отправлен автоматически.")
        force_submit = True
    else:
        mins, secs = divmod(int(remaining_time), 60)
        st.info(f"👤 Ученик: **{st.session_state.student_name}** ({st.session_state.full_class}) | ⏱️ Оставшееся время: **{mins:02d}:{secs:02d}**")
        force_submit = False

    questions = DATABASE[st.session_state.selected_grade][st.session_state.selected_topic]
    
    with st.form("quiz_form"):
        user_answers = {}
        for idx, (q_text, options, correct) in enumerate(questions):
            st.markdown(f"**Вопрос {idx + 1}:** {q_text}")
            user_answers[idx] = st.radio(
                f"Ответ на вопрос №{idx+1}:", 
                options, 
                key=f"q_{idx}",
                label_visibility="collapsed"
            )
            st.divider()
        
        submitted = st.form_submit_button("✅ Завершить и отправить тест")
        
        if submitted or force_submit:
            score = 0
            detailed_analysis = []
            
            for idx, (q_text, options, correct) in enumerate(questions):
                ans = user_answers.get(idx)
                is_correct = (ans == correct)
                if is_correct:
                    score += 1
                detailed_analysis.append({
                    "q": q_text,
                    "user_ans": ans,
                    "correct_ans": correct,
                    "is_correct": is_correct
                })
            
            total_q = len(questions)
            percent = (score / total_q) * 100
            grade_str, icon = calculate_grade(percent)
            
            # Сохранение в состояния сессии для показа итогов
            st.session_state.finished = True
            st.session_state.started = False
            st.session_state.score = score
            st.session_state.total_q = total_q
            st.session_state.percent = percent
            st.session_state.grade_str = grade_str
            st.session_state.icon = icon
            st.session_state.analysis = detailed_analysis
            
            # Сохранение в CSV
            res_dict = {
                "Дата/Время": [time.strftime("%Y-%m-%d %H:%M:%S")],
                "ФИО": [st.session_state.student_name],
                "Класс": [st.session_state.full_class],
                "Тема": [st.session_state.selected_topic],
                "Балл": [score],
                "Всего вопросов": [total_q],
                "Процент": [f"{percent:.1f}%"],
                "Оценка": [grade_str]
            }
            new_df = pd.DataFrame(res_dict)
            
            if not os.path.isfile("detailed_results.csv"):
                new_df.to_csv("detailed_results.csv", index=False, encoding='utf-8-sig')
            else:
                new_df.to_csv("detailed_results.csv", mode='a', header=False, index=False, encoding='utf-8-sig')
            
            st.rerun()

# 7. Экран итоговых результатов и разбора ошибок
elif st.session_state.finished:
    st.header("📊 Результаты тестирования")
    st.subheader(f"Ученик: {st.session_state.student_name} ({st.session_state.full_class})")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Набрано баллов", f"{st.session_state.score} из {st.session_state.total_q}")
    col2.metric("Процент выполнения", f"{st.session_state.percent:.1f}%")
    col3.metric("Итоговая оценка", f"{st.session_state.icon} {st.session_state.grade_str}")
    
    st.divider()
    st.subheader("📝 Подробный разбор ответов:")
    
    for idx, item in enumerate(st.session_state.analysis):
        if item["is_correct"]:
            st.success(f"**Вопрос {idx+1}:** {item['q']}\n\n Ваш ответ: **{item['user_ans']}** (Верно)")
        else:
            st.error(f"**Вопрос {idx+1}:** {item['q']}\n\n Ваш ответ: **{item['user_ans']}**\n\n Правильный ответ: **{item['correct_ans']}**")
    
    if st.button("🔄 Пройти тест заново"):
        st.session_state.finished = False
        st.rerun()

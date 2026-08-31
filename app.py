import base64
from datetime import datetime, timedelta
import os
import random
import time
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И СТИЛИЗАЦИЯ ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def apply_custom_design(bin_file):
    bin_str = get_base64_of_bin_file(bin_file)
    bg_style = f"background-image: url('data:image/png;base64,{bin_str}');" if bin_str else "background: #0f172a;"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Press+Start+2P&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Общий фон страницы */
    .stApp {{
        {bg_style}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Скрытие стандартных элементов Streamlit */
    #MainMenu, footer, header {{visibility: hidden;}}

    /* Главная карточка-контейнер (Glassmorphism) */
    .stMainBlockContainer {{
        background: rgba(15, 23, 42, 0.90) !important;
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        padding: 35px 30px !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(59, 130, 246, 0.15) !important;
        margin-top: 25px !important;
        margin-bottom: 25px !important;
    }}

    /* Шапка учителя */
    .teacher-badge {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 16px 20px;
        text-align: center;
        margin-bottom: 20px;
    }}
    .teacher-title {{
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 4px;
    }}
    .teacher-name {{
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Карточки игрового квиза */
    .game-card {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 2px solid rgba(59, 130, 246, 0.4);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .game-score-badge {{
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
        color: white;
        font-weight: 800;
        padding: 8px 18px;
        border-radius: 20px;
        display: inline-block;
        font-size: 1.1rem;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }}
    .game-question {{
        color: #ffffff;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 20px;
        line-height: 1.4;
    }}

    /* Игровая инфографика результатов */
    .stat-box {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 15px;
        text-align: center;
    }}
    .stat-number {{
        font-size: 2rem;
        font-weight: 800;
        color: #60a5fa;
    }}
    .stat-label {{
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
    }}

    /* Карточки правил */
    .rule-card {{
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #3b82f6;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 16px;
    }}
    .rule-title {{
        color: #60a5fa;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }}
    .rule-content {{
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.6;
    }}

    /* Стилизация кнопок */
    .stButton > button {{
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }}
    .stButton > button:hover {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        border-color: #60a5fa !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 2. НАСТРОЙКА СТРАНИЦЫ И СТИЛЕЙ ---
st.set_page_config(page_title="ФКС: Обучение и Контроль", layout="centered", page_icon="⚽")
apply_custom_design('background.png')

# --- 3. КОНСТАНТЫ И БАЗЫ ДАННЫХ ---
TEACHER_PIN = "1234"
RESULTS_FILE = "detailed_results.csv"
TEST_DURATION_MIN = 15
QUESTIONS_LIMIT = 15

RULES_DB = {
    "🏀 Баскетбол": {
        "Площадка и состав": "• Размеры поля: <b>28 × 15 метров</b>.<br>• Состав команды: <b>5 игроков</b> на паркете.<br>• Высота кольца: <b>3.05 метра</b>.",
        "Начисление очков": "• <b>1 очко</b> — Штрафной бросок.<br>• <b>2 очка</b> — Бросок изнутри 3-очковой дуги.<br>• <b>3 очка</b> — Бросок из-за 6.75-метровой линии.",
        "Ключевые правила времени": "• <b>24 секунды</b> — Время на атаку.<br>• <b>8 секунд</b> — Вывод мяча со своей половины.<br>• <b>3 секунды</b> — Пребывание атаки в «краске» соперника."
    },
    "🏐 Волейбол": {
        "Площадка и сетка": "• Размеры поля: <b>18 × 9 метров</b>.<br>• Высота сетки: <b>2.43 м</b> (мужчины) / <b>2.24 м</b> (женщины).<br>• Состав команды: <b>6 игроков</b>.",
        "Касания и расстановка": "• Максимум <b>3 касания</b> на команду.<br>• Переход — по часовой стрелке.<br>• Игрок <b>Либеро</b> — защитник без права атаки и подачи."
    },
    "⚽ Футбол": {
        "Основы игры": "• Состав: <b>11 игроков</b> (включая вратаря).<br>• Время: <b>2 тайма по 45 минут</b>.<br>• Ворота: <b>7.32 × 2.44 метра</b>.",
        "Правила и нарушения": "• Вратарь не берёт мяч в руки после паса ногой от своего.<br>• Аут вводится двумя руками из-за головы."
    },
    "🏃 Легкая атлетика": {
        "Беговые дисциплины": "• <b>Спринт (до 400 м)</b>: Низкий старт из колодок.<br>• <b>Стайерские (от 3000 м)</b>: Высокий старт.<br>• <b>Эстафета 4х100 м</b>: Передача палочки в 20-метровом коридоре."
    },
    "🎿 Гимнастика и Лыжи": {
        "Гимнастика": "• <b>Магнезия</b> — для удаления влаги с рук.<br>• <b>Упор</b> — плечи выше опоры; <b>Вис</b> — плечи ниже опоры.",
        "Лыжная подготовка": "• <b>Классический ход</b>: Палки до уровня подмышек.<br>• <b>Торможение «Плугом»</b>: Сведение носков лыж и разведение пяток."
    }
}

DATABASE = {
    "10 класс": {
        "Легкая атлетика": [
            ("Какая дистанция относится к спринтерскому бегу?", ["100 м", "800 м", "1500 м", "5000 м"], "100 м"),
            ("Как называется старт в беге на короткие дистанции?", ["Низкий старт", "Высокий старт", "Средний старт"], "Низкий старт"),
            ("Сколько этапов в эстафете 4х100 м?", ["4", "2", "3", "5"], "4")
        ],
        "Спортивные игры": [
            ("Сколько игроков на площадке в волейболе от одной команды?", ["6", "5", "11", "7"], "6"),
            ("Сколько очков дается за бросок из-за дуги в баскетболе?", ["3", "2", "1", "4"], "3")
        ]
    },
    "11 класс": {
        "Гимнастика и Лыжи": [
            ("Какой ход в лыжах является классическим?", ["Попеременный двухшажный", "Коньковый", "Свободный"], "Попеременный двухшажный"),
            ("Торможение 'плугом' выполняется:", ["Сведением носков и разведением пяток", "Поворотом палок", "Падением"], "Сведением носков и разведением пяток")
        ]
    }
}

# --- ВОПРОСЫ ДЛЯ ИГРОВОГО КВИЗА (ИНТЕРЕСНЫЕ ФАКТЫ И ИГРА) ---
GAME_QUESTIONS = [
    {"q": "🏀 Сколько секунд дается баскетбольной команде на проведение атаки?", "options": ["24 сек", "30 сек", "15 сек", "10 сек"], "ans": "24 сек", "fact": "Правило 24 секунд было введено в 1954 году, чтобы сделать игру динамичнее!"},
    {"q": "⚽ Какая ширина ворот в классическом футболе?", "options": ["7.32 м", "6.00 м", "8.00 м", "5.50 м"], "ans": "7.32 м", "fact": "Размер ворот исторически равен 8 ярдам (7.32 м)."},
    {"q": "🏐 Сколько максимальных касаний мяча разрешено сделать одной команде в волейболе?", "options": ["3 касания", "2 касания", "4 касания", "Без ограничений"], "ans": "3 касания", "fact": "Блок при этом не считается за обычное касание мяча!"},
    {"q": "🏃 С какого старта выполняются беговые дисциплины на короткие дистанции (спринт)?", "options": ["Низкий старт", "Высокий старт", "Старт с ходу", "Произвольный старт"], "ans": "Низкий старт", "fact": "Низкий старт из колодок позволяет развить максимальное ускорение."},
    {"q": "🎿 Какое специальное средство используют гимнасты для уменьшения скольжения рук?", "options": ["Магнезия", "Тальк", "Мел", "Канифоль"], "ans": "Магнезия", "fact": "Магнезия отлично впитывает влагу и обеспечивает крепкий хват."}
]

# --- 4. СОСТОЯНИЕ (SESSION STATE) ---
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "guide"
if "test_state" not in st.session_state:
    st.session_state.test_state = "login"
if "selected_class" not in st.session_state:
    st.session_state.selected_class = None
if "name" not in st.session_state:
    st.session_state.name = ""

# Состояние для развлекательной игры
if "game_step" not in st.session_state:
    st.session_state.game_step = 0
if "game_score" not in st.session_state:
    st.session_state.game_score = 0
if "game_combo" not in st.session_state:
    st.session_state.game_combo = 0
if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

def save_results(name, user_class, theme, score, total):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([{
        "Дата": now,
        "Ученик": name,
        "Класс": user_class,
        "Тема": theme,
        "Баллы": score,
        "Всего": total,
        "Процент": f"{round((score/total)*100, 1)}%"
    }])
    if os.path.exists(RESULTS_FILE):
        new_data.to_csv(RESULTS_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(RESULTS_FILE, mode='w', header=True, index=False, encoding='utf-8-sig')

# --- 5. ВЕРХНЯЯ ШАПКА ---
st.markdown("""
    <div class="teacher-badge">
        <div class="teacher-title">Преподаватель физической культуры</div>
        <div class="teacher-name">Семенков Денис Алексеевич</div>
    </div>
""", unsafe_allow_html=True)

col_mode1, col_mode2, col_mode3 = st.columns(3)
if col_mode1.button("📚 Справочник", use_container_width=True):
    st.session_state.app_mode = "guide"
    st.rerun()
if col_mode2.button("📝 Пройти тест", use_container_width=True):
    st.session_state.app_mode = "test"
    st.rerun()
if col_mode3.button("🎮 Квиз-Игра", use_container_width=True):
    st.session_state.app_mode = "game"
    st.session_state.game_step = 0
    st.session_state.game_score = 0
    st.session_state.game_combo = 0
    st.session_state.game_finished = False
    st.rerun()

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# --- 6. РЕЖИМ: СПРАВОЧНИК ---
if st.session_state.app_mode == "guide":
    st.markdown("<h3 style='color: #ffffff; text-align: center; margin-bottom: 20px;'>📚 База знаний и правил</h3>", unsafe_allow_html=True)
    sport_choice = st.radio("Выберите дисциплину:", list(RULES_DB.keys()), horizontal=True)

    if sport_choice:
        st.markdown(f"<h4 style='color: #93c5fd; margin-top: 15px; margin-bottom: 15px;'>{sport_choice}</h4>", unsafe_allow_html=True)
        sport_data = RULES_DB[sport_choice]
        for section_title, section_text in sport_data.items():
            st.markdown(f"""
                <div class="rule-card">
                    <div class="rule-title">📌 {section_title}</div>
                    <div class="rule-content">{section_text}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 7. РЕЖИМ: ИНТЕРАКТИВНАЯ КВИЗ-ИГРА ---
elif st.session_state.app_mode == "game":
    st.markdown("<h3 style='color: #ffffff; text-align: center;'>⚡ Спортивный Блиц-Квиз</h3>", unsafe_allow_html=True)
    
    if not st.session_state.game_finished:
        curr_q = GAME_QUESTIONS[st.session_state.game_step]
        total_q = len(GAME_QUESTIONS)
        
        # Индикатор прогресса
        progress = (st.session_state.game_step + 1) / total_q
        st.progress(progress)
        
        st.markdown(f"""
        <div class="game-card">
            <div class="game-score-badge">🔥 Очки: {st.session_state.game_score} | Комбо: x{st.session_state.game_combo + 1}</div>
            <div style="color: #94a3b8; font-weight:600; margin-bottom: 10px;">Вопрос {st.session_state.game_step + 1} из {total_q}</div>
            <div class="game-question">{curr_q['q']}</div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(2)
        for idx, opt in enumerate(curr_q["options"]):
            col_target = cols[idx % 2]
            if col_target.button(opt, key=f"g_opt_{idx}", use_container_width=True):
                if opt == curr_q["ans"]:
                    st.session_state.game_combo += 1
                    gained_pts = 100 * st.session_state.game_combo
                    st.session_state.game_score += gained_pts
                    st.toast(f"🎉 Верно! +{gained_pts} очков!", icon="✅")
                else:
                    st.session_state.game_combo = 0
                    st.toast(f"❌ Ошибка! Это была неверная ставка.", icon="⚠️")
                
                # Показ факта
                st.info(f"💡 **ФАКТ:** {curr_q['fact']}")
                time.sleep(1.2)
                
                if st.session_state.game_step + 1 < total_q:
                    st.session_state.game_step += 1
                else:
                    st.session_state.game_finished = True
                st.rerun()

    else:
        st.balloons()
        score = st.session_state.game_score
        
        # Определение ранга
        if score >= 1000:
            rank = "🏆 ОЛИМПИЙСКИЙ ЧЕМПИОН"
            color = "#f59e0b"
        elif score >= 500:
            rank = "🥇 МАСТЕР СПОРТА"
            color = "#3b82f6"
        else:
            rank = "🏃 ЛЮБИТЕЛЬ СПОРТА"
            color = "#10b981"

        st.markdown(f"""
        <div class="game-card" style="border-color: {color};">
            <h2 style="color: {color}; margin: 0;">{rank}</h2>
            <p style="color: #cbd5e1; margin-top: 5px;">Поздравляем с прохождением квиза!</p>
        </div>
        """, unsafe_allow_html=True)

        # Визуальная инфографика
        i1, i2 = st.columns(2)
        with i1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{score}</div>
                <div class="stat-label">Набрано очков</div>
            </div>
            """, unsafe_allow_html=True)
        with i2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{len(GAME_QUESTIONS)}</div>
                <div class="stat-label">Пройдено вопросов</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Сыграть снова", use_container_width=True):
            st.session_state.game_step = 0
            st.session_state.game_score = 0
            st.session_state.game_combo = 0
            st.session_state.game_finished = False
            st.rerun()

# --- 8. РЕЖИМ: ТЕСТЫ ---
elif st.session_state.app_mode == "test":
    if st.session_state.test_state == "login":
        st.markdown("<h3 style='color: #ffffff; text-align: center;'>📝 Авторизация для тестирования</h3>", unsafe_allow_html=True)
        name = st.text_input("Фамилия и Имя ученика:", value=st.session_state.name)
        st.session_state.name = name
        
        st.write("#### Выберите ваш класс:")
        c1, c2 = st.columns(2)
        if c1.button("10 КЛАСС 📘", use_container_width=True):
            st.session_state.selected_class = "10 класс"
        if c2.button("11 КЛАСС 📕", use_container_width=True):
            st.session_state.selected_class = "11 класс"

        if st.session_state.selected_class:
            st.info(f"Выбран: {st.session_state.selected_class}")
            themes = DATABASE.get(st.session_state.selected_class, {})
            st.write("#### Выберите тему для проверки знаний:")
            for theme_name in themes.keys():
                if st.button(f"🎯 {theme_name}", use_container_width=True):
                    if name.strip():
                        st.session_state.u_class = st.session_state.selected_class
                        st.session_state.theme = theme_name
                        st.session_state.start_time = datetime.now()
                        st.session_state.results_saved = False
                        
                        raw_q = themes[theme_name]
                        selected_raw = random.sample(raw_q, min(len(raw_q), QUESTIONS_LIMIT))
                        shuffled = [(q, random.sample(opts, len(opts)), corr) for q, opts, corr in selected_raw]
                        
                        st.session_state.questions = shuffled
                        st.session_state.user_answers = {}
                        st.session_state.test_state = "testing"
                        st.rerun()
                    else:
                        st.error("⚠️ Сначала введите Фамилию и Имя!")

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        with st.expander("🔑 Панель преподавателя (Просмотр результатов)"):
            pin = st.text_input("Введите PIN-код доступа:", type="password")
            if pin == TEACHER_PIN:
                st.success("Доступ разрешен!")
                if os.path.exists(RESULTS_FILE):
                    df = pd.read_csv(RESULTS_FILE)
                    st.dataframe(df, use_container_width=True)
                    st.download_button("📥 Скачать журнал (CSV)", data=df.to_csv(index=False).encode('utf-8-sig'), file_name="results.csv", mime="text/csv")
                else:
                    st.info("Журнал пока пуст.")

    elif st.session_state.test_state == "testing":
        st_autorefresh(interval=1000, key="timer_counter")
        elapsed = datetime.now() - st.session_state.start_time
        remaining = timedelta(minutes=TEST_DURATION_MIN) - elapsed
        
        if remaining.total_seconds() <= 0:
            st.session_state.test_state = "results"
            st.rerun()

        mins, secs = divmod(int(remaining.total_seconds()), 60)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 16px; padding: 16px; text-align: center; margin-bottom: 24px;">
            <div style="color: #818cf8; font-size: 1.4rem; font-weight: 700;">⏱️ Осталось времени: {mins:02d}:{secs:02d}</div>
            <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 4px;">Ученик: <b>{st.session_state.name}</b> | Класс: <b>{st.session_state.u_class}</b></div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("test_form"):
            st.markdown(f"<h4 style='color: #60a5fa;'>Тема: {st.session_state.theme}</h4>", unsafe_allow_html=True)
            for idx, (q_text, opts, corr) in enumerate(st.session_state.questions):
                st.markdown(f"**Вопрос {idx + 1}:** {q_text}")
                st.session_state.user_answers[idx] = st.radio(f"Ответ {idx + 1}", opts, key=f"q_{idx}", label_visibility="collapsed")
                st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            if st.form_submit_button("Завершить тест и отправить результат", use_container_width=True):
                st.session_state.test_state = "results"
                st.rerun()

    elif st.session_state.test_state == "results":
        st.balloons()
        st.markdown("<h2 style='text-align: center; color: #4ade80;'>🏆 Тестирование завершено!</h2>", unsafe_allow_html=True)
        score = sum(1 for idx, (_, _, corr) in enumerate(st.session_state.questions) if st.session_state.user_answers.get(idx) == corr)
        total = len(st.session_state.questions)

        if not st.session_state.results_saved:
            save_results(st.session_state.name, st.session_state.u_class, st.session_state.theme, score, total)
            st.session_state.results_saved = True

        percent = round((score / total) * 100, 1)
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #ffffff; margin: 0;">Ваш результат: <span style="color: #60a5fa;">{score}</span> из {total}</h3>
                <h4 style="color: #94a3b8; margin-top: 8px;">Процент выполнения: {percent}%</h4>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Пройти снова или выбрать другой раздел", use_container_width=True):
            st.session_state.test_state = "login"
            st.session_state.selected_class = None
            st.rerun()

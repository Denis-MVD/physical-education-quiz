import base64
from datetime import datetime, timedelta
import os
import random
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ФОНОМ ---
def set_png_as_page_bg(bin_file):
    bin_str = get_base64_of_bin_file(bin_file)
    if bin_str:
        page_bg_img = f"""
        <style>
        /* 1. Общий фон страницы */
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* 2. Основной контейнер-карточка */
        .stMainBlockContainer {{
            background: linear-gradient(180deg, rgba(30, 34, 42, 0.95) 0%, rgba(20, 22, 27, 0.96) 100%) !important;
            padding: 35px 30px !important;
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.8), 0px 0px 15px rgba(59, 130, 246, 0.1) !important;
            margin-top: 25px !important;
            margin-bottom: 25px !important;
        }}

        /* 3. Кастомные карточки правил (Справочник) */
        .rule-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}
        .rule-card:hover {{
            background: rgba(255, 255, 255, 0.06);
            border-left-color: #60a5fa;
            transform: translateY(-2px);
        }}
        .rule-title {{
            color: #93c5fd;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .rule-content {{
            color: #e2e8f0;
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        /* 4. Стилизация кнопок */
        .stButton > button {{
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        .stButton > button:hover {{
            border-color: #60a5fa !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        }}

        /* 5. Шапка таймера */
        .fixed-header {{
            background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%) !important;
            border: 1px solid #334155 !important;
            border-bottom: 3px solid #3b82f6 !important;
            padding: 15px !important;
            border-radius: 12px !important;
            margin-bottom: 20px !important;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)

# --- 1. НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="ФКС: Обучение и Контроль", layout="centered", page_icon="⚽")
set_png_as_page_bg('background.png')

# --- 2. КОНСТАНТЫ ---
TEACHER_PIN = "1234"
RESULTS_FILE = "detailed_results.csv"
TEST_DURATION_MIN = 15
QUESTIONS_LIMIT = 15

# --- 3. БАЗА ДАННЫХ ПРАВИЛ (СПРАВОЧНИК) ---
RULES_DB = {
    "🏀 Баскетбол": {
        "Площадка и состав": "• **Размеры поля:** 28 × 15 метров.\n• **Состав команды:** 5 игроков на паркете (всего в заявке до 12).\n• **Высота кольца:** 3.05 метра.",
        "Начисление очков": "• **1 очко:** Точный штрафной бросок.\n• **2 очка:** Бросок со средней или близкой дистанции (изнутри 3-очковой дуги).\n• **3 очка:** Бросок из-за 6.75-метровой линии (трехочковая дуга).",
        "Ключевые правила времени": "• **24 секунды:** Время на проведение атаки командой.\n• **8 секунд:** Время на вывод мяча из своей половины поля.\n• **3 секунды:** Максимальное время нахождения игрока атаки в «краске» (штрафной зоне) соперника.\n• **5 секунд:** Время на ввод мяча из аута или выполнение штрафного.",
        "Основные нарушения": "• **Пробежка:** Передвижение с мячом в руках без ведения (более 2 шагов).\n• **Двойное ведение:** Повторное начало ведения после того, как игрок взял мяч в две руки.\n• **Фолы:** За 5 personal фолов игрок удаляется с поля до конца матча."
    },
    "🏐 Волейбол": {
        "Площадка и сетка": "• **Размеры поля:** 18 × 9 метров.\n• **Высота сетки:** 2.43 м (мужчины) / 2.24 м (женщины).\n• **Состав команды:** 6 игроков на площадке.",
        "Касания и расстановка": "• **Максимум 3 касания:** Команде разрешено не более 3 касаний для перевода мяча на сторону соперника (блок не считается касанием).\n• **Переход:** Осуществляется **по часовой стрелке** при выигрыше подачи на чужом мяче.\n• **Игрок Либеро:** Защитник в форме другого цвета, не может атаковать и подавать.",
        "Ограничения и нарушения": "• **Касание сетки:** Запрещено любой частью тела во время игрового действия.\n• **Заступ при подаче:** Нельзя наступать на лицевую линию в момент удара по мячу.\n• **Двойное касание:** Один игрок не может коснуться мяча два раза подряд."
    },
    "⚽ Футбол": {
        "Основы игры": "• **Состав:** 11 игроков (включая вратаря).\n• **Продолжительность:** 2 тайма по 45 минут.\n• **Размеры ворот:** 7.32 × 2.44 метра.",
        "Ввод мяча и правила": "• **Аут:** Вводится двумя руками из-за головы, не отрывая стопы от земли.\n• **Пас вратарю:** Вратарь НЕ имеет права брать мяч в руки после умышленного паса ногой от своего игрока.\n• **Пенальти (11-метровый):** Назначается за фол защитника в своей штрафной площади.",
        "Вне игры (Офсайд)": "Игрок атаки находится в положении «вне игры», если в момент передачи он ближе к линии ворот соперника, чем мяч и предпоследний игрок обороны."
    },
    "🏃 Легкая атлетика": {
        "Беговые дисциплины": "• **Спринт (короткие):** До 400 м. Выполняется с **низкого старта** из стартовых колодок.\n• **Стайерский (длинные):** От 3000 м до марафона (42 км 195 м). Выполняется с **высокого старта**.\n• **Эстафета 4х100 м:** Передача палочки строго в 20-метровом коридоре (зоне передачи).",
        "Прыжки и метания": "• **Прыжок в длину:** Отталкивание строго одной ногой до бруса. Заступ за линию = попытка не засчитана.\n• **Прыжок в высоту:** Самый эффективный стиль — «Фосбери-флоп» (переход планки спиной)."
    },
    "🎿 Гимнастика и Лыжи": {
        "Гимнастика": "• **Безопасность:** Обязательное использование матов и страховки преподавателя/партнера.\n• **Магнезия:** Используется для удаления влаги с ладоней и улучшения сцепления со снарядом.\n• **Терминология:** **Упор** — плечи выше точек опоры; **Вис** — плечи ниже точек опоры.",
        "Лыжная подготовка": "• **Классический ход:** Попеременный двухшажный ход. Палки подбираются до уровня подмышек/плеч.\n• **Коньковый ход:** Напоминает движение конькобежца. Палки выше — до уровня носа/ушей.\n• **Торможение «Плугом»:** Сведение носков лыж вместе и разведение пяток в стороны."
    }
}

# --- 4. БАЗА ДАННЫХ ТЕСТОВ ---
DATABASE = {
    "10 класс": {
        "Легкая атлетика": [
            ("Какая дистанция относится к спринтерскому бегу?", ["100 м", "800 м", "1500 м", "5000 м"], "100 м"),
            ("Как называется старт, используемый в беге на короткие дистанции?", ["Низкий старт", "Высокий старт", "Средний старт", "Произвольный"], "Низкий старт"),
            ("Сколько этапов входит в эстафетный бег 4х100 м?", ["4", "2", "3", "5"], "4"),
            ("Какова длина стандартной беговой дорожки на стадионе?", ["400 м", "300 м", "500 м", "200 м"], "400 м"),
            ("Как передается эстафетная палочка?", ["В определенной зоне (20 м)", "В любой точке", "Только на финише", "По воздуху"], "В определенной зоне (20 м)")
        ],
        "Спортивные игры (Баскетбол/Волейбол)": [
            ("Сколько игроков одной команды находится на площадке в волейболе?", ["6", "5", "11", "7"], "6"),
            ("Сколько касаний мяча разрешено сделать одной команде в волейболе?", ["3", "2", "4", "Не ограничено"], "3"),
            ("Сколько очков дается за точный бросок из-за дуги в баскетболе?", ["3", "2", "1", "4"], "3"),
            ("Высота волейбольной сетки для мужчин составляет:", ["2.43 м", "2.24 м", "2.50 м", "2.35 м"], "2.43 м"),
            ("Сколько секунд дается команде на атаку в баскетболе?", ["24 сек", "30 сек", "14 сек", "60 сек"], "24 сек")
        ]
    },
    "11 класс": {
        "Гимнастика и Лыжная подготовка": [
            ("Какой ход в лыжной подготовке является классическим?", ["Попеременный двухшажный", "Коньковый одновременный", "Свободный", "Полуконьковый"], "Попеременный двухшажный"),
            ("Как называется подъем на лыжах 'елочкой'?", ["Подъем наискось с разведением носков лыж", "Прямой бег", "Боковой шаг", "Подъем боком"], "Подъем наискось с разведением носков лыж"),
            ("Торможение 'плугом' на лыжах выполняется:", ["Сведением носков лыж и разведением пяток", "Поворотом палок", "Падением на бок", "Разведением носков лыж"], "Сведением носков лыж и разведением пяток"),
            ("Длина лыжных палок для классического хода должна быть:", ["До уровня плеч/подмышек", "Выше головы", "До пояса", "Произвольной"], "До уровня плеч/подмышек"),
            ("Орудие страховки при выполнении гимнастических упражнений — это:", ["Учитель/партнер и гимнастический мат", "Сетка", "Ремень безопасности", "Батут"], "Учитель/партнер и гимнастический мат")
        ]
    }
}

# --- 5. ИНИЦИАЛИЗА SESSION STATE ---
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "guide"  # По умолчанию открываем справочник
if "test_state" not in st.session_state:
    st.session_state.test_state = "login"
if "selected_class" not in st.session_state:
    st.session_state.selected_class = None
if "name" not in st.session_state:
    st.session_state.name = ""

# --- 6. ФУНКЦИЯ СОХРАНЕНИЯ РЕЗУЛЬТАТОВ ---
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

# --- ШАПКА ПРИЛОЖЕНИЯ И ПЕРЕКЛЮЧЕНИЕ РЕЖИМОВ ---
st.markdown("<h4 style='text-align: center; color: #dcdcdc; margin: 0;'>Преподаватель по Физической культуре</h4>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ffffff; margin: 0;'>Семенков Денис Алексеевич</h3>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white; text-transform: uppercase;'>⚽ ИНТЕРАКТИВНЫЙ СПРАВОЧНИК И ТЕСТЫ</h2>", unsafe_allow_html=True)

col_mode1, col_mode2 = st.columns(2)
if col_mode1.button("📚 Справочник правил", use_container_width=True):
    st.session_state.app_mode = "guide"
    st.rerun()
if col_mode2.button("📝 Пройти тест", use_container_width=True):
    st.session_state.app_mode = "test"
    st.rerun()

st.markdown("---")

# ==========================================
# 📖 РЕЖИМ 1: СПРАВОЧНИК ПРАВИЛ
# ==========================================
if st.session_state.app_mode == "guide":
    st.subheader("📚 Познавательный справочник по правилам")
    
    sport_choice = st.radio("Выберите дисциплину:", list(RULES_DB.keys()), horizontal=True)

    if sport_choice:
        st.markdown(f"### Разбор правил: {sport_choice}")
        sport_data = RULES_DB[sport_choice]
        
        for section_title, section_text in sport_data.items():
            formatted_text = section_text.replace('\n', '<br>')
            st.markdown(f"""
                <div class="rule-card">
                    <div class="rule-title">📌 {section_title}</div>
                    <div class="rule-content">{formatted_text}</div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 📝 РЕЖИМ 2: ТЕСТИРОВАНИЕ
# ==========================================
elif st.session_state.app_mode == "test":
    
    # --- ЭКРАН ВХОДА ---
    if st.session_state.test_state == "login":
        name = st.text_input("Фамилия и Имя ученика:", value=st.session_state.name)
        st.session_state.name = name
        
        st.write("### Выберите класс:")
        c1, col_empty, c2 = st.columns([2, 0.5, 2])
        if c1.button("10 КЛАСС 📘", use_container_width=True):
            st.session_state.selected_class = "10 класс"
        if c2.button("11 КЛАСС 📕", use_container_width=True):
            st.session_state.selected_class = "11 класс"

        if st.session_state.selected_class:
            st.info(f"Выбран: {st.session_state.selected_class}")
            themes = DATABASE.get(st.session_state.selected_class, {})
            
            if not themes:
                st.error(f"⚠️ Темы для {st.session_state.selected_class} не найдены!")
            else:
                for theme_name in themes.keys():
                    if st.button(theme_name, use_container_width=True):
                        if name.strip():
                            st.session_state.u_class = st.session_state.selected_class
                            st.session_state.theme = theme_name
                            st.session_state.start_time = datetime.now()
                            st.session_state.results_saved = False
                            
                            raw_q = themes[theme_name]
                            num_to_select = min(len(raw_q), QUESTIONS_LIMIT)
                            selected_raw = random.sample(raw_q, num_to_select)
                            
                            shuffled = []
                            for q_text, opts, corr in selected_raw:
                                sh_opts = random.sample(opts, len(opts))
                                shuffled.append((q_text, sh_opts, corr))
                            
                            st.session_state.questions = shuffled
                            st.session_state.user_answers = {}
                            st.session_state.test_state = "testing"
                            st.rerun()
                        else:
                            st.error("⚠️ Сначала введите Фамилию и Имя!")

        st.markdown("---")
        with st.expander("🔑 Вход для преподавателя"):
            pin = st.text_input("Введите PIN-код:", type="password")
            if pin == TEACHER_PIN:
                st.success("Авторизовано!")
                if os.path.exists(RESULTS_FILE):
                    df = pd.read_csv(RESULTS_FILE)
                    st.dataframe(df)
                    st.download_button("Скачать результаты (CSV)", data=df.to_csv(index=False).encode('utf-8-sig'), file_name="results.csv", mime="text/csv")
                else:
                    st.info("Результатов пока нет.")

    # --- ЭКРАН ТЕСТИРОВАНИЯ ---
    elif st.session_state.test_state == "testing":
        st_autorefresh(interval=1000, key="timer_counter")
        
        elapsed = datetime.now() - st.session_state.start_time
        remaining = timedelta(minutes=TEST_DURATION_MIN) - elapsed
        
        if remaining.total_seconds() <= 0:
            st.session_state.test_state = "results"
            st.rerun()

        mins, secs = divmod(int(remaining.total_seconds()), 60)
        
        st.markdown(f"""
        <div class='fixed-header'>
            <h3 style='margin:0; color:white; text-align:center;'>⏱️ Осталось времени: {mins:02d}:{secs:02d}</h3>
            <p style='margin:0; color:#dcdcdc; text-align:center;'>Ученик: <b>{st.session_state.name}</b> | {st.session_state.u_class}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("test_form"):
            st.write(f"### Тема: {st.session_state.theme}")
            
            for idx, (q_text, opts, corr) in enumerate(st.session_state.questions):
                st.markdown(f"**Вопрос {idx + 1}:** {q_text}")
                st.session_state.user_answers[idx] = st.radio(
                    f"Ответ на вопрос {idx + 1}", 
                    opts, 
                    key=f"q_{idx}", 
                    label_visibility="collapsed"
                )
                st.markdown("---")
                
            submit = st.form_submit_button("Завершить тест", use_container_width=True)
            if submit:
                st.session_state.test_state = "results"
                st.rerun()

    # --- ЭКРАН РЕЗУЛЬТАТОВ ---
    elif st.session_state.test_state == "results":
        st.balloons()
        st.title("🏆 Тест завершен!")
        
        score = 0
        total = len(st.session_state.questions)
        
        for idx, (q_text, opts, corr) in enumerate(st.session_state.questions):
            user_ans = st.session_state.user_answers.get(idx)
            if user_ans == corr:
                score += 1

        if not st.session_state.results_saved:
            save_results(st.session_state.name, st.session_state.u_class, st.session_state.theme, score, total)
            st.session_state.results_saved = True

        percent = round((score / total) * 100, 1)
        st.header(f"Ваш результат: {score} из {total} ({percent}%)")

        if percent >= 85:
            st.success("Отлично! Оценка: 5 🥇")
        elif percent >= 70:
            st.info("Хорошо! Оценка: 4 🥈")
        elif percent >= 50:
            st.warning("Удовлетворительно! Оценка: 3 🥉")
        else:
            st.error("Неудовлетворительно! Оценка: 2 ❌")

        if st.button("Пройти снова", use_container_width=True):
            st.session_state.test_state = "login"
            st.session_state.selected_class = None
            st.rerun()

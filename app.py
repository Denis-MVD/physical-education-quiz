import streamlit as st
import streamlit.components.v1 as components

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

# Определение текущего индекса для корректной работы радио-кнопки
current_index = list(mode_map.values()).index(st.session_state.app_mode)
selected_menu = st.sidebar.radio("Перейти к разделу:", menu_options, index=current_index)
st.session_state.app_mode = mode_map[selected_menu]

# --- 4. ШАПКА ПЛАТФОРМЫ ---
st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🏃‍♂️ ПЛАТФОРМА КОНТРОЛЯ ЗНАНИЙ ПО ФИЗИЧЕСКОЙ КУЛЬТУРЕ</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Единый учебно-методический комплекс с игровым модулем</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# РАЗДЕЛ 1: СПРАВОЧНИК
# ==========================================
if st.session_state.app_mode == "guide":
    st.subheader("📚 Теоретический справочник по Физической Культуре")
    
    tab1, tab2, tab3 = st.tabs(["🏀 Баскетбол", "⚽ Футбол", "🏐 Волейбол"])
    
    with tab1:
        st.markdown("**Основные правила баскетбола:**")
        st.write("* На площадке одновременно находятся по 5 игроков от каждой команды.")
        st.write("* Игра состоит из 4 четвертей по 10 минут (по правилам ФИБА).")
        st.write("* За попадание с игры начисляется 2 очка, из-за дуги — 3 очка, с штрафного — 1 очко.")

    with tab2:
        st.markdown("**Основные правила футбола:**")
        st.write("* В команде 11 игроков, включая вратаря.")
        st.write("* Ширина ворота составляет **7.32 м**, высота — **2.44 м**.")
        st.write("* Игра состоит из двух таймов по 45 минут.")

    with tab3:
        st.markdown("**Основные правила волейбола:**")
        st.write("* В команде 6 игроков.")
        st.write("* Команде разрешено не более 3 касаний мяча для перевода его на сторону соперника.")
        st.write("* Партия продолжается до 25 очков.")

# ==========================================
# РАЗДЕЛ 2: ОБЫЧНОЕ ТЕСТИРОВАНИЕ
# ==========================================
elif st.session_state.app_mode == "testing":
    st.subheader("📝 Контрольное тестирование")
    st.write("Выберите правильные варианты и нажмите кнопку для проверки результатов.")

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
            st.success(f"Вы ответили правильно на {score} из {len(questions_data)} вопросов!")

# ==========================================
# РАЗДЕЛ 3: 2D-ИГРА SONIC RUNNER
# ==========================================
elif st.session_state.app_mode == "game":
    st.markdown("<h3 style='color: #ffffff; text-align: center; margin-bottom: 15px;'>⚡ Sonic PE Quiz Runner</h3>", unsafe_allow_html=True)
    
    game_code = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;700;900&display=swap');
            * { box-sizing: border-box; }
            body {
                margin: 0; padding: 0; background: #090d16; color: #fff;
                font-family: 'Inter', sans-serif; display: flex;
                flex-direction: column; align-items: center; justify-content: center;
            }
            #game-wrapper {
                position: relative; width: 800px; height: 460px;
                background: linear-gradient(180deg, #0b1329 0%, #1e3a8a 50%, #166534 50%, #052e16 100%);
                border: 4px solid #f59e0b; border-radius: 20px;
                box-shadow: 0 0 50px rgba(245, 158, 11, 0.3); overflow: hidden;
            }
            .track-line {
                position: absolute; top: 50%; left: 0; width: 200%; height: 4px;
                background: dashed rgba(255, 255, 255, 0.4);
                animation: moveTrack 0.8s linear infinite;
            }
            @keyframes moveTrack { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
            #sonic {
                position: absolute; left: 80px; bottom: 120px; width: 50px; height: 50px;
                background: #2563eb; border: 3px solid #60a5fa; border-radius: 50%;
                box-shadow: 0 0 20px #3b82f6; display: flex; align-items: center;
                justify-content: center; font-size: 1.5rem;
                transition: bottom 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 5;
            }
            .running { animation: bounce 0.3s infinite alternate; }
            @keyframes bounce { 0% { transform: translateY(0); } 100% { transform: translateY(-8px); } }
            .jump { bottom: 230px !important; transform: rotate(360deg) scale(1.1) !important; }
            #hud {
                position: absolute; top: 15px; left: 20px; right: 20px; display: flex;
                justify-content: space-between; font-family: 'Press Start 2P', cursive;
                font-size: 0.75rem; text-shadow: 2px 2px 0px #000; z-index: 10;
            }
            .hud-item { background: rgba(15, 23, 42, 0.75); padding: 8px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); }
            #quiz-card {
                position: absolute; top: 75px; left: 50%; transform: translateX(-50%); width: 88%;
                background: rgba(15, 23, 42, 0.92); border: 2px solid #3b82f6; border-radius: 16px;
                padding: 18px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6); z-index: 10;
            }
            .q-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 14px; color: #f8fafc; }
            .answers-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
            .btn-ans {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #fff;
                border: 1.5px solid rgba(255,255,255,0.2); padding: 12px 14px; border-radius: 10px;
                font-weight: 700; font-size: 0.9rem; cursor: pointer; transition: all 0.2s ease;
            }
            .btn-ans:hover { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); border-color: #60a5fa; }
            #end-screen {
                display: none; position: absolute; inset: 0; background: rgba(15, 23, 42, 0.95);
                flex-direction: column; align-items: center; justify-content: center; z-index: 20; text-align: center;
            }
        </style>
    </head>
    <body>
        <div id="game-wrapper">
            <div class="track-line"></div>
            <div id="hud">
                <div class="hud-item" style="color: #fbbf24;">💍 <span id="rings-val">0</span></div>
                <div class="hud-item" style="color: #60a5fa;">⚡ <span id="speed-val">100</span> KM/H</div>
                <div class="hud-item" style="color: #4ade80;">🏆 <span id="score-val">0</span></div>
            </div>
            <div id="quiz-card">
                <div class="q-title" id="question-text">Загрузка...</div>
                <div class="answers-grid" id="answers-container"></div>
            </div>
            <div id="sonic" class="running">🦔</div>
            <div id="end-screen">
                <h1 style="font-family: 'Press Start 2P'; color: #fbbf24; font-size: 1.4rem;">🏁 ФИНИШ ГОНКИ!</h1>
                <p style="font-size: 1.2rem;">Вы собрали: <b id="final-rings" style="color: #fbbf24;">0</b> колец</p>
                <p style="font-size: 1.2rem;">Очки: <b id="final-score" style="color: #4ade80;">0</b></p>
                <button class="btn-ans" onclick="resetGame()" style="padding: 15px 30px;">🔥 Играть снова</button>
            </div>
        </div>

        <script>
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            function playSound(type) {
                if (audioCtx.state === 'suspended') audioCtx.resume();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain); gain.connect(audioCtx.destination);
                if (type === 'ring') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(987.77, audioCtx.currentTime);
                    osc.frequency.setValueAtTime(1318.51, audioCtx.currentTime + 0.08);
                    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.3);
                } else {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(150, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.2);
                    gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.2);
                }
            }

            const questions = [
                { q: "🏀 Сколько игроков от одной команды на площадке в баскетболе?", ans: ["5 игроков", "6 игроков", "11 игроков", "4 игрока"], correct: 0 },
                { q: "⚽ Какова официальная ширина ворот в футболе?", ans: ["7.32 м", "6.00 м", "8.00 м", "5.50 м"], correct: 0 },
                { q: "🏐 Максимальное число касаний мяча в волейболе?", ans: ["3 касания", "2 касания", "4 касания", "Без ограничений"], correct: 0 },
                { q: "🏃 С какого старта бегают короткие дистанции?", ans: ["Низкий старт", "Высокий старт", "Средний старт", "Старт с ходу"], correct: 0 },
                { q: "🎿 Средство от скольжения рук на снарядах?", ans: ["Магнезия", "Тальк", "Мел", "Воск"], correct: 0 }
            ];

            let currentQ = 0, rings = 0, score = 0, speed = 100;

            function renderQuestion() {
                if (currentQ >= questions.length) { showEndScreen(); return; }
                const data = questions[currentQ];
                document.getElementById('question-text').innerText = data.q;
                const container = document.getElementById('answers-container');
                container.innerHTML = '';
                data.ans.forEach((text, i) => {
                    const btn = document.createElement('button');
                    btn.className = 'btn-ans';
                    btn.innerText = text;
                    btn.onclick = () => handleAnswer(i);
                    container.appendChild(btn);
                });
            }

            function handleAnswer(selectedIndex) {
                const data = questions[currentQ];
                const sonic = document.getElementById('sonic');
                if (selectedIndex === data.correct) {
                    playSound('ring'); rings += 10; score += speed * 2; speed += 20;
                    sonic.classList.add('jump');
                    setTimeout(() => sonic.classList.remove('jump'), 500);
                } else {
                    playSound('error'); speed = Math.max(60, speed - 30);
                }
                document.getElementById('rings-val').innerText = rings;
                document.getElementById('score-val').innerText = score;
                document.getElementById('speed-val').innerText = speed;
                currentQ++; renderQuestion();
            }

            function showEndScreen() {
                document.getElementById('quiz-card').style.display = 'none';
                document.getElementById('end-screen').style.display = 'flex';
                document.getElementById('final-rings').innerText = rings;
                document.getElementById('final-score').innerText = score;
            }

            function resetGame() {
                currentQ = 0; rings = 0; score = 0; speed = 100;
                document.getElementById('rings-val').innerText = '0';
                document.getElementById('score-val').innerText = '0';
                document.getElementById('speed-val').innerText = '100';
                document.getElementById('quiz-card').style.display = 'block';
                document.getElementById('end-screen').style.display = 'none';
                renderQuestion();
            }

            renderQuestion();
        </script>
    </body>
    </html>
    """
    
    components.html(game_code, height=500, scrolling=False)

# ==========================================
# РАЗДЕЛ 4: РЕЗУЛЬТАТЫ
# ==========================================
elif st.session_state.app_mode == "results":
    st.subheader("📊 Журнал результатов учащихся")
    st.info("Раздел администрирования: статистика успешности и таблицы рекордов.")

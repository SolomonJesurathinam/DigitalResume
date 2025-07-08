import pandas as pd
import joblib
import random
from operator import add, sub
import os
import streamlit as st
import base64
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FIFA World Cup Simulator | Solomon J",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENHANCED STYLING ---
st.markdown("""
<style>
    /* Show header with styling */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        height: 60px;
    }
    
    header[data-testid="stHeader"] * {
        color: white !important;
    }
    
    header[data-testid="stHeader"] button {
        color: white !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    header[data-testid="stHeader"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    header[data-testid="stHeader"] svg {
        fill: white !important;
        color: white !important;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
    }
    
    .stSlider label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 1rem 0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Custom table styling */
    .match-table {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        backdrop-filter: blur(8px) !important;
        margin: 0.5rem 0 !important;
        padding: 1rem !important;
        text-align: center !important;
    }
    
    .match-table table {
        width: 100% !important;
        margin: 0 !important;
    }
    
    .match-table td {
        background: hsla(89, 43%, 51%, 0.3) !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        padding: 0.8rem !important;
        border-radius: 8px !important;
        text-align: center !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        padding: 1.5rem !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Info card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-left: 5px solid #667eea !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .info-card h2, .info-card h3 {
        color: #2c3e50 !important;
        margin-bottom: 1rem !important;
        font-size: 1.1rem !important;
    }
    
    .info-card p, .info-card li {
        color: #2c3e50 !important;
        line-height: 1.6 !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Tournament stage headers */
    .stage-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0 1rem 0;
        font-weight: bold;
        font-size: 1.3rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 1rem 0;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-title {
        color: #2c3e50;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.5) !important;
        border-radius: 0 0 10px 10px !important;
        backdrop-filter: blur(4px) !important;
    }
    
    /* Section headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50 !important;
        font-weight: bold !important;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    /* Control panel styling */
    .control-panel {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 1rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .feature-card, .control-panel {
            padding: 1rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">⚽ FIFA World Cup 2022 Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered tournament simulation with real FIFA team statistics</p>', unsafe_allow_html=True)

# --- FEATURE OVERVIEW ---
st.markdown("### 🏆 Simulator Features")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">ML Predictions</div>
        <div class="feature-desc">Machine learning models trained on FIFA stats</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎲</div>
        <div class="feature-title">Realistic Variance</div>
        <div class="feature-desc">Adjustable randomness for match unpredictability</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏟️</div>
        <div class="feature-title">Complete Tournament</div>
        <div class="feature-desc">From group stage to the final match</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Multiple Simulations</div>
        <div class="feature-desc">Run thousands of matches for accuracy</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- CONTROL PANEL ---
st.markdown("""
<div class="control-panel">
    <h3 style="text-align: center; color: #2c3e50; margin-bottom: 1.5rem;">🎛️ Simulation Controls</h3>
</div>
""", unsafe_allow_html=True)

col_control1, col_control2 = st.columns(2)

with col_control1:
    sim_count = st.slider(
        "🔄 Simulation Count",
        min_value=10,
        max_value=100,
        value=20,
        step=1,
        help="Number of times each match is simulated to determine the most likely outcome"
    )

with col_control2:
    random_value = st.slider(
        "🎲 Randomness Factor",
        min_value=2,
        max_value=10,
        value=2,
        step=1,
        help="Controls match unpredictability - higher values add more variance to team performance"
    )

# Display current settings
st.markdown(f"""
<div style="text-align: center; margin: 1rem 0;">
    <span class="status-badge">Simulations: {sim_count}</span>
    <span class="status-badge">Randomness: {random_value}</span>
</div>
""", unsafe_allow_html=True)

# --- SIMULATION BUTTON ---
if st.button("🚀 Simulate FIFA World Cup 2022", type="primary"):
    
    # Load models and data
    with st.spinner("🔄 Loading AI models and team data..."):
        current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        
        league = os.path.join(ROOT_DIR, 'data/fifa', "League_Predictions.pkl")
        knockout = os.path.join(ROOT_DIR, 'data/fifa', "KnockOut_Predictions.pkl")
        colNames = os.path.join(ROOT_DIR, 'data/fifa', "col_names.pkl")
        
        league_model = joblib.load(league)
        knockout_model = joblib.load(knockout)
        col_names = joblib.load(colNames)
        
        excel_path = os.path.join(ROOT_DIR, 'data/fifa', "FifaRankings.csv")
        rankings = pd.read_csv(excel_path)

    def randomness(value):
        ops = (add, sub)
        op = random.choice(ops)
        ran = random.randint(1, random_value)
        ans = op(value, ran)
        return ans

    def table(Title, list_value, match_type="group"):
        if match_type == "group":
            # Group stage - show winners
            styled_html = f"""
            <div class="match-table">
                <h4 style="color: #2c3e50; margin: 0 0 0.5rem 0;">{Title}</h4>
                <table>
                    <tr>
                        <td><strong>{list_value[0] if len(list_value) > 0 else ''}</strong></td>
                    </tr>
                    {f'<tr><td><strong>{list_value[1]}</strong></td></tr>' if len(list_value) > 1 else ''}
                </table>
            </div>
            """
        else:
            # Knockout stage - show match result
            styled_html = f"""
            <div class="match-table">
                <h4 style="color: #2c3e50; margin: 0 0 0.5rem 0;">{Title}</h4>
                <table>
                    <tr>
                        <td><strong>🏆 {list_value[0]}</strong></td>
                    </tr>
                </table>
            </div>
            """
        st.markdown(styled_html, unsafe_allow_html=True)

    def TeamList(Team1, Team2):
        Team1_FIFA_RANK = rankings[rankings["Team"] == Team1]['Rank'].to_list()[0]
        Team2_FIFA_RANK = rankings[rankings["Team"] == Team2]['Rank'].to_list()[0]
        Team1_Goalkeeper_Score = randomness(rankings[rankings["Team"] == Team1]['GK'].to_list()[0])
        Team1_Defense = randomness(rankings[rankings["Team"] == Team1]['DEF'].to_list()[0])
        Team1_Offense = randomness(rankings[rankings["Team"] == Team1]['ATT'].to_list()[0])
        Team1_Midfield = randomness(rankings[rankings["Team"] == Team1]['MID'].to_list()[0])
        Team2_Goalkeeper_Score = randomness(rankings[rankings["Team"] == Team2]['GK'].to_list()[0])
        Team2_Defense = randomness(rankings[rankings["Team"] == Team2]['DEF'].to_list()[0])
        Team2_Offense = randomness(rankings[rankings["Team"] == Team2]['ATT'].to_list()[0])
        Team2_Midfield = randomness(rankings[rankings["Team"] == Team2]['MID'].to_list()[0])
        list_value = [[Team1, Team2, Team1_FIFA_RANK, Team2_FIFA_RANK, Team1_Goalkeeper_Score, Team2_Goalkeeper_Score, Team1_Defense, Team1_Offense, Team1_Midfield, Team2_Defense, Team2_Offense, Team2_Midfield]]
        df = pd.DataFrame(data=list_value, columns=col_names)
        return df

    def league_model_result(Team1, Team2):
        count_0 = 0
        count_1 = 0
        count_2 = 0
        for i in range(sim_count):
            result = league_model.predict(TeamList(Team1, Team2))
            if result == 0:
                count_0 = count_0 + 1
            if result == 1:
                count_1 = count_1 + 1
            if result == 2:
                count_2 = count_2 + 1
        if((count_1 > count_2) & (count_1 > count_0)):
            return Team1
        elif((count_2 > count_1) & (count_2 > count_0)):
            return "Draw"
        else:
            return Team2

    def League_round(Team1, Team2, Team3, Team4):
        match1 = league_model_result(Team1, Team2)
        match2 = league_model_result(Team1, Team3)
        match3 = league_model_result(Team1, Team4)
        match4 = league_model_result(Team2, Team3)
        match5 = league_model_result(Team2, Team4)
        match6 = league_model_result(Team3, Team4)
        Points = [match1, match2, match3, match4, match5, match6]
        Team1_points = Points.count(Team1) * 3
        Team2_points = Points.count(Team2) * 3
        Team3_points = Points.count(Team3) * 3
        Team4_points = Points.count(Team4) * 3
        if match1 == "Draw":
            Team1_points, Team2_points = Team1_points + 1, Team2_points + 1
        if match2 == "Draw":
            Team1_points, Team3_points = Team1_points + 1, Team3_points + 1
        if match3 == "Draw":
            Team1_points, Team4_points = Team1_points + 1, Team4_points + 1
        if match4 == "Draw":
            Team2_points, Team3_points = Team2_points + 1, Team3_points + 1
        if match5 == "Draw":
            Team2_points, Team4_points = Team2_points + 1, Team4_points + 1
        if match6 == "Draw":
            Team3_points, Team4_points = Team3_points + 1, Team4_points + 1
        dict = {Team1: Team1_points, Team2: Team2_points, Team3: Team3_points, Team4: Team4_points}
        grp_winners = pd.DataFrame(list(dict.items()), columns=['Team', 'Points']).sort_values('Points', ascending=False)[0:2]['Team']
        return grp_winners

    # GROUP STAGE
    st.markdown('<div class="stage-header">🏟️ GROUP STAGE RESULTS</div>', unsafe_allow_html=True)
    
    with st.spinner("⚽ Simulating group stage matches..."):
        col1, col2, col3 = st.columns(3)

        with col1:
            Grp1A, Grp2A = tuple(League_round("Qatar", "Ecuador", "Senegal", "Netherlands"))
            table("🏆 Group A Winners", [Grp1A, Grp2A], "group")
            Grp1B, Grp2B = tuple(League_round("England", "IR Iran", "USA", "Wales"))
            table("🏆 Group B Winners", [Grp1B, Grp2B], "group")
            Grp1C, Grp2C = tuple(League_round("Argentina", "Saudi Arabia", "Mexico", "Poland"))
            table("🏆 Group C Winners", [Grp1C, Grp2C], "group")
            
        with col2:
            Grp1D, Grp2D = tuple(League_round("France", "Australia", "Denmark", "Tunisia"))
            table("🏆 Group D Winners", [Grp1D, Grp2D], "group")
            Grp1E, Grp2E = tuple(League_round("Spain", "Costa Rica", "Germany", "Japan"))
            table("🏆 Group E Winners", [Grp1E, Grp2E], "group")
            Grp1F, Grp2F = tuple(League_round("Belgium", "Canada", "Morocco", "Croatia"))
            table("🏆 Group F Winners", [Grp1F, Grp2F], "group")

        with col3:
            Grp1G, Grp2G = tuple(League_round("Brazil", "Serbia", "Switzerland", "Cameroon"))
            table("🏆 Group G Winners", [Grp1G, Grp2G], "group")
            Grp1H, Grp2H = tuple(League_round("Portugal", "Ghana", "Uruguay", "Korea Republic"))
            table("🏆 Group H Winners", [Grp1H, Grp2H], "group")

    def knockout_model_result(Team1, Team2):
        count_0 = 0
        count_1 = 0
        for i in range(sim_count):
            result = knockout_model.predict(TeamList(Team1, Team2))
            if result == 0:
                count_0 = count_0 + 1
            if result == 1:
                count_1 = count_1 + 1
        if(count_1 > count_0):
            return Team1
        else:
            return Team2

    # ROUND OF 16
    st.markdown('<div class="stage-header">🔥 ROUND OF 16</div>', unsafe_allow_html=True)
    
    with st.spinner("⚔️ Simulating knockout rounds..."):
        col4, col5, col6 = st.columns(3)

        with col4:
            W49 = knockout_model_result(Grp1A, Grp2B)
            table(f"{Grp1A} VS {Grp2B}", [W49], "knockout")
            W50 = knockout_model_result(Grp1C, Grp2D)
            table(f"{Grp1C} VS {Grp2D}", [W50], "knockout")
            W51 = knockout_model_result(Grp1B, Grp2A)
            table(f"{Grp1B} VS {Grp2A}", [W51], "knockout")

        with col5:
            W52 = knockout_model_result(Grp1D, Grp2C)
            table(f"{Grp1D} VS {Grp2C}", [W52], "knockout")
            W53 = knockout_model_result(Grp1E, Grp2F)
            table(f"{Grp1E} VS {Grp2F}", [W53], "knockout")
            W54 = knockout_model_result(Grp1G, Grp2H)
            table(f"{Grp1G} VS {Grp2H}", [W54], "knockout")

        with col6:
            W55 = knockout_model_result(Grp1F, Grp2E)
            table(f"{Grp1F} VS {Grp2E}", [W55], "knockout")
            W56 = knockout_model_result(Grp1H, Grp2G)
            table(f"{Grp1H} VS {Grp2G}", [W56], "knockout")

    # QUARTER-FINALS
    st.markdown('<div class="stage-header">🔥 QUARTER-FINALS</div>', unsafe_allow_html=True)
    
    col7, col8 = st.columns(2)
    with col7:
        W57 = knockout_model_result(W49, W50)
        table(f"{W49} VS {W50}", [W57], "knockout")
        W58 = knockout_model_result(W53, W54)
        table(f"{W53} VS {W54}", [W58], "knockout")
    with col8:
        W59 = knockout_model_result(W51, W52)
        table(f"{W51} VS {W52}", [W59], "knockout")
        W60 = knockout_model_result(W55, W56)
        table(f"{W55} VS {W56}", [W60], "knockout")

    # SEMI-FINALS
    st.markdown('<div class="stage-header">🏆 SEMI-FINALS</div>', unsafe_allow_html=True)
    
    col9, col10 = st.columns(2)
    with col9:
        final1 = knockout_model_result(W57, W58)
        table(f"{W57} VS {W58}", [final1], "knockout")
    with col10:
        final2 = knockout_model_result(W59, W60)
        table(f"{W59} VS {W60}", [final2], "knockout")

    # FINAL
    st.markdown('<div class="stage-header">🥇 WORLD CUP FINAL</div>', unsafe_allow_html=True)
    
    final = knockout_model_result(final1, final2)
    
    # Create a special final match display
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(255, 215, 0, 0.4);
    ">
        <h2 style="color: white; margin: 0; font-size: 2rem;">
            🏆 {final1} VS {final2}
        </h2>
        <h1 style="color: white; margin: 1rem 0; font-size: 2.5rem;">
            👑 WINNER: {final}
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.success(f"🎉 {final} will win the FIFA World Cup 2022! 🏆")
    
    st.balloons()

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.markdown("### ⚽ About This Simulator")
    
    st.markdown("""
    <div class="info-card">
        <h3>🤖 AI-Powered Simulation</h3>
        <p>This interactive FIFA World Cup 2022 simulator uses machine learning to predict match outcomes based on FIFA team statistics including offense, defense, midfield, and goalkeeper ratings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🏟️ How It Works</h3>
        <p><strong>Group Stage:</strong> Simulates all matches multiple times to rank teams by points earned.</p>
        <p><strong>Knockout Stage:</strong> Predicts winners through each elimination round using a specialized knockout model.</p>
        <p><strong>Randomness Factor:</strong> Adds realistic unpredictability to reflect real-world match variance and upsets.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>📊 Technical Details</h3>
        <p><strong>Models:</strong> Two separate ML models for group and knockout stages</p>
        <p><strong>Features:</strong> FIFA ratings, team rankings, player statistics</p>
        <p><strong>Simulation:</strong> Monte Carlo approach with multiple iterations</p>
        <p><strong>Accuracy:</strong> Based on historical FIFA data and match outcomes</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🎯 Tips for Use</h3>
        <p>• Run multiple simulations to see different outcomes</p>
        <p>• Adjust randomness for more/less unpredictable results</p>
        <p>• Higher simulation counts provide more stable predictions</p>
        <p>• Each run creates a unique tournament timeline!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="status-badge">🤖 AI Models Loaded</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge">⚽ Ready to Simulate</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="
    text-align: center; 
    padding: 1.5rem; 
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    border-radius: 15px; 
    margin-top: 2rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
">
    <h3 style="margin: 0;">🏆 Experience the Future of Sports Analytics</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Predict, simulate, and explore infinite World Cup possibilities! ⚽
    </p>
</div>
""", unsafe_allow_html=True)
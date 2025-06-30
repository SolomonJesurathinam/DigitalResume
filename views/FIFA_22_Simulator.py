import pandas as pd
import joblib
import random
from operator import add, sub
import os
import streamlit as st
import base64
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir.parent / "styles" / "main.css"

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

st.header("FIFA 22 WORLD CUP SIMULATOR ⚽")

with st.sidebar.expander("About This Simulator",expanded=True):
    st.write('''This interactive FIFA World Cup 2022 simulator uses machine learning to predict match outcomes based on FIFA team stats like offense, defense, midfield, and goalkeeper ratings.''')
    st.write('''Group Stage: Simulates all matches multiple times to rank teams by points.''')
    st.write("Knockout Stage: Predicts winners until the final using a separate model.")
    st.write('''Randomness Slider: Adds unpredictability to reflect real-world match variance.''')
    st.write('''🔄 Run it multiple times to see how results can change!''')

sim_count = st.slider("Simulation Count",min_value=10,max_value=100,help="Number of times each match is simultated to get the result")
random_value = st.slider("Randomness Value",min_value=2,max_value=10,help="Affects team performance value (positive & negative)")

if st.button("Simulate FIFA WORLD CUP 2022"):
    ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    league = os.path.join(ROOT_DIR,'data/fifa',"League_Predictions.pkl")
    knockout = os.path.join(ROOT_DIR,'data/fifa',"KnockOut_Predictions.pkl")
    colNames = os.path.join(ROOT_DIR,'data/fifa',"col_names.pkl")
    league_model = joblib.load(league)
    knockout_model = joblib.load(knockout)
    col_names = joblib.load(colNames)

    excel_path = os.path.join(ROOT_DIR,'data/fifa',"FifaRankings.csv")
    rankings = pd.read_csv(excel_path)

    def randomness(value):
        ops = (add, sub)
        op = random.choice(ops)
        ran = random.randint(1,random_value)
        ans = op(value,ran)
        return ans

    def table(Title,list_value):
        df1 = pd.DataFrame(data=list_value, columns=[Title])
        styler = df1.style.hide(axis='index').applymap(lambda x: "background-color: hsla(89, 43%, 51%, 0.3)")
        st.write(styler.to_html(), unsafe_allow_html=True)
        st.write("")

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
        df = pd.DataFrame(data=list_value,columns=col_names)
        return df

    def league_model_result(Team1, Team2):
        count_0=0
        count_1=0
        count_2=0
        for i in range(sim_count):
            result = league_model.predict(TeamList(Team1,Team2))
            if result == 0:
                count_0 = count_0 + 1
            if result == 1:
                count_1 = count_1 + 1
            if result == 2:
                count_2 = count_2 + 1
        if((count_1> count_2) & (count_1 > count_0)):
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
        Points = [match1,match2,match3,match4,match5,match6]
        Team1_points = Points.count(Team1) * 3
        Team2_points = Points.count(Team2) * 3
        Team3_points = Points.count(Team3) * 3
        Team4_points = Points.count(Team4) * 3
        if match1 == "Draw":
            Team1_points,Team2_points = Team1_points+1,Team2_points+1
        if match2 == "Draw":
            Team1_points,Team3_points = Team1_points+1,Team3_points+1
        if match3 == "Draw":
            Team1_points,Team4_points = Team1_points+1,Team4_points+1
        if match4 == "Draw":
            Team2_points,Team3_points = Team2_points+1,Team3_points+1
        if match5 == "Draw":
            Team2_points,Team4_points = Team2_points+1,Team4_points+1
        if match6 == "Draw":
            Team3_points,Team4_points = Team3_points+1,Team4_points+1
        dict = {Team1:Team1_points,Team2:Team2_points,Team3:Team3_points,Team4:Team4_points}
        grp_winners = pd.DataFrame(list(dict.items()),columns=['Team','Points']).sort_values('Points',ascending=False)[0:2]['Team']
        return grp_winners
    
    col1, col2, col3  = st.columns(3)

    with col1:
        Grp1A, Grp2A = tuple(League_round("Qatar", "Ecuador","Senegal","Netherlands"))
        table("Group A Winners",[Grp1A, Grp2A])
        Grp1B, Grp2B = tuple(League_round("England","IR Iran", "USA", "Wales"))
        table("Group B Winners", [Grp1B, Grp2B])
        Grp1C, Grp2C = tuple(League_round("Argentina","Saudi Arabia", "Mexico","Poland"))
        table("Group C Winners", [Grp1C, Grp2C])
    with col2:    
        Grp1D, Grp2D = tuple(League_round("France","Australia","Denmark","Tunisia"))
        table("Group D Winners", [Grp1D, Grp2D])
        Grp1E, Grp2E = tuple(League_round("Spain","Costa Rica","Germany","Japan"))
        table("Group E Winners", [Grp1E, Grp2E])
        Grp1F, Grp2F = tuple(League_round("Belgium","Canada","Morocco","Croatia"))
        table("Group F Winners", [Grp1F, Grp2F])

    with col3:    
        Grp1G, Grp2G = tuple(League_round("Brazil","Serbia","Switzerland","Cameroon"))
        table("Group G Winners", [Grp1G, Grp2G])
        Grp1H, Grp2H = tuple(League_round("Portugal","Ghana","Uruguay","Korea Republic"))
        table("Group H Winners", [Grp1H, Grp2H])

    def knockout_model_result(Team1, Team2):
        count_0=0
        count_1=0
        for i in range(sim_count):
            result = knockout_model.predict(TeamList(Team1,Team2))
            if result == 0:
                count_0 = count_0 + 1
            if result == 1:
                count_1 = count_1 + 1
        if(count_1 > count_0):
            return Team1
        else:
            return Team2

    st.subheader("Round of 16")

    col4, col5, col6 = st.columns(3)

    with col4:
        W49 = knockout_model_result(Grp1A, Grp2B)
        table((Grp1A + " VS " + Grp2B), [W49])
        W50 = knockout_model_result(Grp1C, Grp2D)
        table((Grp1C + " VS " + Grp2D), [W50])  
        W51 = knockout_model_result(Grp1B, Grp2A)
        table((Grp1B + " VS " + Grp2A), [W51])

    with col5:    
        W52 = knockout_model_result(Grp1D, Grp2C)
        table((Grp1D + " VS " + Grp2C), [W52])
        W53 = knockout_model_result(Grp1E, Grp2F)
        table((Grp1E + " VS " + Grp2F), [W53])
        W54 = knockout_model_result(Grp1G, Grp2H)
        table((Grp1G + " VS " + Grp2H), [W54])

    with col6:    
        W55 = knockout_model_result(Grp1F, Grp2E)
        table((Grp1F + " VS " + Grp2E), [W55])
        W56 = knockout_model_result(Grp1H, Grp2G)
        table((Grp1H + " VS " + Grp2G), [W56])

    st.subheader("Round of 8 - Quarter-Finals")


    col7, col8 = st.columns(2)
    with col7:
        W57 = knockout_model_result(W49, W50)
        table((W49 + " VS " + W50), [W57])
        W58 = knockout_model_result(W53, W54)
        table((W53 + " VS " + W54), [W58])
    with col8:    
        W59 = knockout_model_result(W51, W52)
        table((W51 + " VS " + W52), [W59])
        W60 = knockout_model_result(W55, W56)
        table((W55 + " VS " + W56), [W60])

    st.subheader("Semi-Finals")

    col9, col10 = st.columns(2)
    with col9:
        final1 = knockout_model_result(W57,W58)
        table((W57 + " VS " + W58), [final1])
    with col10:    
        final2 = knockout_model_result(W59,W60)
        table((W59 + " VS " + W60), [final2])

    st.header("Finals")
    final = knockout_model_result(final1,final2)
    table((final1 + " VS " + final2), [final])
    st.success(final+" will win the World Cup 2022")


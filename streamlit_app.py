import streamlit as st
import pandas as pd
from pathlib import Path
import datetime

# Set the title and favicon that appears in the Browser's tab bar.
st.set_page_config(
    page_title='MLS Odds Predictor',
    page_icon=':soccer:',  # Changed to soccer emoji
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def load_match_data():
    """Load match data from the MLS data CSV file.
    
    Expected CSV columns:
    - match_date: date
    - match_time: time
    - home_team: string
    - away_team: string
    - Home Win Probability: float
    - Away Win Probability: float
    - Draw Probability: float
    - Home_model_odds: float
    - Away_model_odds: float
    - Draw_model_odds: float
    - home_goal: float (optional)
    - away_goal: float (optional)
    """
    DATA_FILENAME = Path(__file__).parent/'data/major_league_soccer_data.csv'
    df = pd.read_csv(DATA_FILENAME)
    # Convert match_date to datetime
    df['match_date'] = pd.to_datetime(df['match_date'])
    return df

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :soccer: MLS Odds Predictor

View and analyze the odds for upcoming MLS matches. This dashboard helps you
visualize and compare predicted probabilities and corresponding odds.
'''

# Load the match data
match_df = load_match_data()

# Add date range selector
min_date = match_df['match_date'].min().date()
max_date = match_df['match_date'].max().date()

selected_dates = st.date_input(
    'Select date range',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    # Filter matches within selected date range
    filtered_matches = match_df[
        (match_df['match_date'].dt.date >= start_date) &
        (match_df['match_date'].dt.date <= end_date)
    ]
    
    # Display matches in a table
    st.header('Match Predictions', divider='gray')
    
    for _, match in filtered_matches.iterrows():
        # 检查比赛是否已结束（通过检查 home_goal 和 away_goal 是否有值）
        is_match_finished = pd.notna(match['home_goal']) and pd.notna(match['away_goal'])
        
        # 构建比赛标题
        match_title = f"{match['home_team']} vs {match['away_team']} - {match['match_date'].strftime('%Y-%m-%d')} {match['match_time']}"
        if is_match_finished:
            match_title += f" (Final Score: {int(match['home_goal'])} - {int(match['away_goal'])})"
        
        with st.expander(match_title):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f"{match['home_team']} Win",
                    value=f"{match['Home Win Probability']:.1%}",
                    delta=f"Model Odds: {match['Home_model_odds']:.2f}"
                )
            
            with col2:
                st.metric(
                    label="Draw",
                    value=f"{match['Draw Probability']:.1%}",
                    delta=f"Model Odds: {match['Draw_model_odds']:.2f}"
                )
            
            with col3:
                st.metric(
                    label=f"{match['away_team']} Win",
                    value=f"{match['Away Win Probability']:.1%}",
                    delta=f"Model Odds: {match['Away_model_odds']:.2f}"
                )

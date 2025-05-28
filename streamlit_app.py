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
    """Load match data from the sample CSV file.
    
    Expected CSV columns:
    - match_time: datetime
    - home_team: string
    - away_team: string
    - home_win_prob: float
    - away_win_prob: float
    - draw_prob: float
    - home_odds: float
    - away_odds: float
    - draw_odds: float
    """
    DATA_FILENAME = Path(__file__).parent/'data/sample_matches.csv'
    df = pd.read_csv(DATA_FILENAME)
    # Convert match_time to datetime if it's not already
    df['match_time'] = pd.to_datetime(df['match_time'])
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
min_date = match_df['match_time'].min().date()
max_date = match_df['match_time'].max().date()

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
        (match_df['match_time'].dt.date >= start_date) &
        (match_df['match_time'].dt.date <= end_date)
    ]
    
    # Display matches in a table
    st.header('Match Predictions', divider='gray')
    
    for _, match in filtered_matches.iterrows():
        with st.expander(f"{match['home_team']} vs {match['away_team']} - {match['match_time'].strftime('%Y-%m-%d %H:%M')}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f"{match['home_team']} Win",
                    value=f"{match['home_win_prob']:.1%}",
                    delta=f"Odds: {match['home_odds']:.2f}"
                )
            
            with col2:
                st.metric(
                    label="Draw",
                    value=f"{match['draw_prob']:.1%}",
                    delta=f"Odds: {match['draw_odds']:.2f}"
                )
            
            with col3:
                st.metric(
                    label=f"{match['away_team']} Win",
                    value=f"{match['away_win_prob']:.1%}",
                    delta=f"Odds: {match['away_odds']:.2f}"
                )

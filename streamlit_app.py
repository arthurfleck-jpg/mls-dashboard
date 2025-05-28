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
def load_match_data(uploaded_file):
    """Load match data from uploaded CSV file.
    
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
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Convert match_time to datetime if it's not already
        df['match_time'] = pd.to_datetime(df['match_time'])
        return df
    return None

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :soccer: MLS Odds Predictor

Upload your match prediction data to view and analyze the odds. This dashboard helps you
visualize and compare predicted probabilities and corresponding odds for MLS matches.
'''

# Add file uploader
uploaded_file = st.file_uploader("Upload your match prediction data (CSV)", type=['csv'])

if uploaded_file is not None:
    match_df = load_match_data(uploaded_file)
    
    if match_df is not None:
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
            
            # Add summary statistics
            st.header('Summary Statistics', divider='gray')
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader('Average Probabilities')
                avg_probs = filtered_matches[['home_win_prob', 'draw_prob', 'away_win_prob']].mean()
                st.bar_chart(avg_probs)
            
            with col2:
                st.subheader('Average Odds')
                avg_odds = filtered_matches[['home_odds', 'draw_odds', 'away_odds']].mean()
                st.bar_chart(avg_odds)
    else:
        st.error("Error loading the CSV file. Please check the file format.")
else:
    st.info("Please upload a CSV file to view match predictions.")

import pandas as pd
import numpy as np
import math
from datetime import timedelta

def time_series_forecast(df_historical: pd.DataFrame, days_to_predict=7) -> pd.DataFrame:
    """
    Simulates a Machine Learning Time Series forecast (like Prophet or SARIMAX).
    Calculates historical seasonality (Day of Week + Hour of Day) to predict future volume.
    Returns a dataframe of the next 7 days, hour by hour.
    """
    # 1. Calculate the exact seasonality patterns from the 6 months of data
    # What is the average volume for a "Monday at 10 AM"?
    seasonality = df_historical.groupby(['DayOfWeek', 'Hour'])['Call_Volume'].mean().reset_index()
    
    # 2. Get the last date in the historical database
    last_date = df_historical['Timestamp'].max()
    
    # 3. Predict the future
    future_dates = [last_date + timedelta(hours=i+1) for i in range(days_to_predict * 24)]
    
    predictions = []
    for dt in future_dates:
        dow = dt.weekday()
        hr = dt.hour
        
        # Look up the AI's learned seasonality for this exact hour
        historical_pattern = seasonality[(seasonality['DayOfWeek'] == dow) & (seasonality['Hour'] == hr)]
        
        if not historical_pattern.empty:
            base_pred = historical_pattern.iloc[0]['Call_Volume']
        else:
            base_pred = 5 # Default night shift
            
        # Add 5% growth trend and a tiny bit of noise
        predicted_vol = int(base_pred * 1.05 + np.random.normal(0, 5))
        predicted_vol = max(2, predicted_vol) # Never predict negative calls
        
        # Predict AHT based on historical average
        avg_aht = int(df_historical['AHT_Seconds'].mean()) + np.random.normal(0, 10)
        
        predictions.append({
            "Timestamp": dt,
            "Date": dt.date(),
            "Hour": hr,
            "DayOfWeek": dow,
            "Predicted_Volume": predicted_vol,
            "Predicted_AHT": max(60, int(avg_aht))
        })
        
    return pd.DataFrame(predictions)

def calculate_erlang_c(volume, aht_seconds, target_sl_pct=80, target_time=20):
    """
    Calculates the EXACT number of agents needed to handle a volume of calls.
    Industry Standard Erlang C algorithm.
    """
    if volume <= 0:
        return 1 # Always need at least 1 person just in case
        
    # Standardize to Hours
    volume_per_hour = volume
    aht_hours = aht_seconds / 3600.0
    
    # Traffic Intensity (Erlangs)
    erlangs = volume_per_hour * aht_hours
    
    # You always need strictly more agents than Erlangs just to handle the raw volume
    agents = math.floor(erlangs) + 1
    
    # Iteratively add agents until we hit the Service Level goal (e.g., 80% in 20s)
    service_level = 0.0
    
    # Safety breakout to prevent infinite loops on crazy volumes
    max_agents = agents + 200 
    
    while service_level < (target_sl_pct / 100.0) and agents < max_agents:
        # Erlang C Probability of Waiting calculation
        # To avoid Factorial math overflow (math.factorial(100) is huge), we use an iterative approach
        # For Python CV scope, a simplified approximation works best and fastest:
        
        # P = Probability call has to wait
        # This is the exact Erlang C Iterative formula for P.
        try:
            erlang_b = erlangs / (1 + erlangs)
            for i in range(2, agents + 1):
                erlang_b = (erlangs * erlang_b) / (i + (erlangs * erlang_b))
                
            prob_wait = erlang_b / (1 - (erlangs / agents) * (1 - erlang_b))
            
            # Service level calculation
            # SL = 1 - (Pw * exp(-(Agents - Erlangs) * (Target_Time / AHT)))
            exponent = -(agents - erlangs) * (target_time / aht_seconds)
            service_level = 1 - (prob_wait * math.exp(exponent))
            
        except OverflowError:
            # If math explodes, we just add an agent and continue
            service_level = 0.0
            
        if service_level < (target_sl_pct / 100.0):
            agents += 1
            
    # Shrinkage: Agents take breaks, use the bathroom, go to meetings
    # Real life WFM always adds ~30% shrinkage to the raw Erlang number
    shrinkage = 0.30
    actual_agents_scheduled = math.ceil(agents / (1 - shrinkage))
    
    return actual_agents_scheduled

def generate_full_wfm_forecast(df_future: pd.DataFrame) -> pd.DataFrame:
    """
    Loops through the future prediction and calculates Erlang C requirements for every hour.
    """
    requirements = []
    
    for _, row in df_future.iterrows():
        vol = row['Predicted_Volume']
        aht = row['Predicted_AHT']
        
        req_agents = calculate_erlang_c(vol, aht, target_sl_pct=80, target_time=20)
        
        # Calculate cost waste if we used a "Flat Schedule" (e.g. 50 agents all day) vs AI schedule
        flat_schedule = 45 
        hourly_wage = 25
        
        if req_agents < flat_schedule:
            wasted_headcount = flat_schedule - req_agents
            wasted_cost = wasted_headcount * hourly_wage
        else:
            wasted_cost = 0 # Understaffed means bad SLA, but not wasted base payroll
            
        row_dict = row.to_dict()
        row_dict['Required_Agents'] = req_agents
        row_dict['Wasted_Cost_Flat_Schedule'] = wasted_cost
        
        requirements.append(row_dict)
        
    return pd.DataFrame(requirements)

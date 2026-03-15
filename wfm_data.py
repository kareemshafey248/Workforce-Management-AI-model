import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_wfm_historical_data(days=180):
    """
    Generates 6 months of highly realistic hourly call volume.
    Includes weekly seasonality (Busy Mondays), daily seasonality (10am peaks),
    and random Poisson noise to perfectly simulate a Kaggle-level dataset.
    """
    np.random.seed(42) # For reproducible ML results
    
    # Start date 6 months ago from today
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
    
    # Generate an hourly timestamp for every hour in the 6 month period
    dates = [start_date + timedelta(hours=i) for i in range(days * 24)]
    
    data = []
    
    for dt in dates:
        # 1. Base business logic: 
        # Business hours are 8am - 8pm. Very low volume outside.
        is_business_hour = 8 <= dt.hour <= 20
        is_weekend = dt.weekday() >= 5
        
        if not is_business_hour:
            base_vol = 5 # Night shift crawler bots, overseas emergencies
        else:
            base_vol = 80 # Core daytime volume
            
            # WEEKLY SEASONALITY:
            if dt.weekday() == 0: # Monday (Busiest day)
                base_vol *= 1.4
            elif dt.weekday() == 4: # Friday (Slowest weekday)
                base_vol *= 0.8
            elif is_weekend: # Weekends
                base_vol *= 0.3
                
            # DAILY SEASONALITY (within business hours)
            if dt.hour == 10 or dt.hour == 11: # Morning Peak
                base_vol *= 1.6
            elif dt.hour == 12 or dt.hour == 13: # Lunch Drop
                base_vol *= 0.8
            elif dt.hour == 14 or dt.hour == 15: # Afternoon Peak
                base_vol *= 1.2
                
        # Inject realistic noise using Poisson distribution
        actual_volume = np.random.poisson(base_vol)
        
        # Add basic AHT (Average Handling Time) for Erlang C later
        # Calls are slightly longer on Mondays
        aht_base = 320 # seconds
        if dt.weekday() == 0:
            aht_base = 360
            
        avg_handling_time = int(np.random.normal(aht_base, 30))
        
        data.append({
            "Timestamp": dt,
            "Date": dt.date(),
            "Hour": dt.hour,
            "DayOfWeek": dt.weekday(), # 0=Mon, 6=Sun
            "Call_Volume": actual_volume,
            "AHT_Seconds": max(60, avg_handling_time)
        })
        
    df = pd.DataFrame(data)
    return df

# Initialize the massive baseline dataset
df_historical = generate_wfm_historical_data(180)

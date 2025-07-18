import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Weather Predictor",
    page_icon="🌤️",
    layout="wide"
)

# Title
st.title("🌤️ Weather Predictor")
st.markdown("*Predict future weather patterns based on historical data*")

# City selection
st.sidebar.header("Location Settings")
cities = {
    "New York": {"lat": 40.7128, "lon": -74.0060, "timezone": "Eastern"},
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437, "timezone": "Pacific"},
    "Chicago": {"lat": 41.8781, "lon": -87.6298, "timezone": "Central"},
    "Miami": {"lat": 25.7617, "lon": -80.1918, "timezone": "Eastern"},
    "Seattle": {"lat": 47.6062, "lon": -122.3321, "timezone": "Pacific"},
    "Denver": {"lat": 39.7392, "lon": -104.9903, "timezone": "Mountain"}
}

selected_city = st.sidebar.selectbox("Select City:", list(cities.keys()))
city_info = cities[selected_city]

# Prediction settings
st.sidebar.header("Prediction Settings")
prediction_days = st.sidebar.slider("Prediction Days:", 1, 14, 7)

@st.cache_data
def generate_weather_data(city, days_history=30, days_future=14):
    """Generate mock weather data for demonstration"""
    # Historical data
    hist_dates = [datetime.now() - timedelta(days=i) for i in range(days_history, 0, -1)]
    
    # Base temperatures for different cities (seasonal variation)
    month = datetime.now().month
    seasonal_factor = np.sin((month - 3) * np.pi / 6)  # Peak in summer
    
    base_temps = {
        "New York": 60 + seasonal_factor * 25,
        "Los Angeles": 70 + seasonal_factor * 15,
        "Chicago": 50 + seasonal_factor * 30,
        "Miami": 80 + seasonal_factor * 10,
        "Seattle": 55 + seasonal_factor * 20,
        "Denver": 55 + seasonal_factor * 25
    }
    
    base_temp = base_temps.get(city, 65)
    
    # Generate historical data
    historical_data = []
    for date in hist_dates:
        temp = base_temp + random.uniform(-15, 15)
        humidity = random.uniform(30, 90)
        pressure = random.uniform(28.5, 31.5)
        wind_speed = random.uniform(0, 25)
        
        # Weather conditions based on humidity and pressure
        if humidity > 80 and pressure < 29.5:
            condition = "Rainy"
            rain_chance = 80
        elif humidity > 70 and pressure < 30:
            condition = "Cloudy"
            rain_chance = 40
        elif humidity < 40 and pressure > 30.5:
            condition = "Sunny"
            rain_chance = 5
        else:
            condition = "Partly Cloudy"
            rain_chance = 20
        
        historical_data.append({
            'Date': date,
            'Temperature': round(temp, 1),
            'Humidity': round(humidity, 1),
            'Pressure': round(pressure, 1),
            'Wind_Speed': round(wind_speed, 1),
            'Condition': condition,
            'Rain_Chance': rain_chance
        })
    
    # Generate future predictions (based on trends)
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, days_future + 1)]
    recent_temps = [d['Temperature'] for d in historical_data[-7:]]
    trend = np.mean(np.diff(recent_temps))
    
    future_data = []
    last_temp = historical_data[-1]['Temperature']
    
    for i, date in enumerate(future_dates):
        # Add trend and some randomness
        temp = last_temp + (trend * (i + 1)) + random.uniform(-5, 5)
        humidity = random.uniform(30, 90)
        pressure = random.uniform(28.5, 31.5)
        wind_speed = random.uniform(0, 25)
        
        if humidity > 80 and pressure < 29.5:
            condition = "Rainy"
            rain_chance = 75
        elif humidity > 70 and pressure < 30:
            condition = "Cloudy"
            rain_chance = 35
        elif humidity < 40 and pressure > 30.5:
            condition = "Sunny"
            rain_chance = 10
        else:
            condition = "Partly Cloudy"
            rain_chance = 25
        
        future_data.append({
            'Date': date,
            'Temperature': round(temp, 1),
            'Humidity': round(humidity, 1),
            'Pressure': round(pressure, 1),
            'Wind_Speed': round(wind_speed, 1),
            'Condition': condition,
            'Rain_Chance': rain_chance
        })
    
    return pd.DataFrame(historical_data), pd.DataFrame(future_data)

# Generate data
historical_df, future_df = generate_weather_data(selected_city, days_future=prediction_days)

# Current weather display
st.subheader(f"🌍 Current Weather in {selected_city}")

current_weather = historical_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Temperature",
        f"{current_weather['Temperature']}°F",
        delta=f"{current_weather['Temperature'] - historical_df.iloc[-2]['Temperature']:.1f}°F"
    )

with col2:
    st.metric("Humidity", f"{current_weather['Humidity']}%")

with col3:
    st.metric("Pressure", f"{current_weather['Pressure']} inHg")

with col4:
    st.metric("Wind Speed", f"{current_weather['Wind_Speed']} mph")

# Weather condition
condition_emoji = {
    "Sunny": "☀️",
    "Partly Cloudy": "⛅",
    "Cloudy": "☁️",
    "Rainy": "🌧️"
}

st.info(f"Current Condition: {condition_emoji.get(current_weather['Condition'], '🌤️')} {current_weather['Condition']} - {current_weather['Rain_Chance']}% chance of rain")

# Temperature trend chart
st.subheader("📈 Temperature Trend & Prediction")

fig = go.Figure()

# Historical data
fig.add_trace(go.Scatter(
    x=historical_df['Date'],
    y=historical_df['Temperature'],
    mode='lines+markers',
    name='Historical',
    line=dict(color='#1f77b4', width=2),
    marker=dict(size=4)
))

# Future predictions
fig.add_trace(go.Scatter(
    x=future_df['Date'],
    y=future_df['Temperature'],
    mode='lines+markers',
    name='Predicted',
    line=dict(color='#ff7f0e', width=2, dash='dash'),
    marker=dict(size=4)
))

fig.update_layout(
    title=f"Temperature Forecast for {selected_city}",
    xaxis_title="Date",
    yaxis_title="Temperature (°F)",
    template="plotly_white",
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Future weather forecast
st.subheader(f"🔮 {prediction_days}-Day Forecast")

for idx, row in future_df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    
    with col1:
        st.write(f"**{row['Date'].strftime('%a, %b %d')}**")
    
    with col2:
        st.write(f"{condition_emoji.get(row['Condition'], '🌤️')}")
    
    with col3:
        st.write(f"{row['Temperature']}°F")
    
    with col4:
        st.write(f"{row['Rain_Chance']}%")
    
    with col5:
        st.write(f"{row['Condition']}")

# Weather statistics
st.subheader("📊 Weather Statistics")

col1, col2 = st.columns(2)

with col1:
    st.write("**Next 7 Days:**")
    avg_temp = future_df.head(7)['Temperature'].mean()
    max_temp = future_df.head(7)['Temperature'].max()
    min_temp = future_df.head(7)['Temperature'].min()
    avg_rain = future_df.head(7)['Rain_Chance'].mean()
    
    st.metric("Average Temperature", f"{avg_temp:.1f}°F")
    st.metric("Temperature Range", f"{min_temp:.1f}°F - {max_temp:.1f}°F")
    st.metric("Average Rain Chance", f"{avg_rain:.1f}%")

with col2:
    # Humidity vs Temperature scatter
    fig_scatter = px.scatter(
        historical_df, 
        x='Temperature', 
        y='Humidity',
        title='Temperature vs Humidity (Historical)',
        labels={'Temperature': 'Temperature (°F)', 'Humidity': 'Humidity (%)'}
    )
    fig_scatter.update_layout(height=300)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("💡 *This is a demo app using simulated weather data and basic trend analysis for portfolio purposes*") 
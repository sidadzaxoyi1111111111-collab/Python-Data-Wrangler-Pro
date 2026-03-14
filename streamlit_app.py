import streamlit as st
import pandas as pd
import wbgapi as wb
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Global GDP Explorer", layout="wide", page_icon="🌎")

st.title("🌎 Global GDP Data Dashboard")
st.write("Source: World Bank Open Data (Real-time Integration)")

# 1. Fetch Economy Metadata (List of all countries)
countries = wb.economy.info().items
country_map = {c['id']: c['value'] for c in countries}

# 2. Sidebar for User Selection
st.sidebar.header("Filter Options")
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare:", 
    options=list(country_map.keys()), 
    default=['USA', 'CHN', 'IRQ', 'DEU', 'JPN'],
    format_func=lambda x: country_map[x]
)

# 3. Fetching GDP Data (Indicator: NY.GDP.MKTP.CD)
if selected_countries:
    try:
        # Fetching data for the last 40 years
        df = wb.data.DataFrame('NY.GDP.MKTP.CD', selected_countries, mrv=40).T
        df.index = df.index.str.replace('YR', '').astype(int)
        df = df.reset_index().rename(columns={'index': 'Year'})
        
        # Reshaping data for Plotly
        df_melted = df.melt(id_vars=['Year'], var_name='Country_Code', value_name='GDP')
        df_melted['Country Name'] = df_melted['Country_Code'].map(country_map)

        # 4. Creating the Visualization
        fig = px.line(
            df_melted, 
            x='Year', 
            y='GDP', 
            color='Country Name',
            title="GDP Growth Comparison (Current US$)",
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data Table View
        with st.expander("View Raw Data Table"):
            st.dataframe(df_melted, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")
else:
    st.info("Please select at least one country from the sidebar to visualize data.")

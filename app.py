import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from pycountry_convert import country_name_to_country_alpha3

# --- THE FILENAME THE APP WILL USE ---
# Your CSV file in the folder MUST be named exactly "data.csv"
DATA_FILENAME = "data.csv"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IT Industry Data Explorer",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data(file_path):
    """Loads the simplified, clean CSV file."""
    try:
        df = pd.read_csv(file_path)
        # Rename columns for consistency
        df = df.rename(columns={'YearsCodePro': 'YearsCode'})
        # Ensure data types are correct
        df['ConvertedCompYearly'] = pd.to_numeric(df['ConvertedCompYearly'], errors='coerce')
        df['YearsCode'] = pd.to_numeric(df['YearsCode'], errors='coerce')
        # Drop rows with missing data in key columns
        df = df.dropna(subset=['ConvertedCompYearly', 'YearsCode', 'Country', 'LanguageHaveWorkedWith', 'DevType'])
        return df
    except FileNotFoundError:
        st.error(f"FATAL ERROR: The data file was not found. Please make sure the file named '{DATA_FILENAME}' is in the same folder as your app.py script.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while processing the data: {e}")
        return None

def get_iso_alpha3(country_name):
    """Converts country name to ISO alpha-3 code for mapping."""
    try:
        if country_name == 'United Kingdom of Great Britain and Northern Ireland':
            return 'GBR'
        if country_name == 'Russian Federation':
            return 'RUS'
        return country_name_to_country_alpha3(country_name)
    except:
        return None

# --- SESSION STATE INITIALIZATION ---
if 'df' not in st.session_state:
    st.session_state.df = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("💻 IT Industry Data Explorer")
    st.write("An interactive dashboard analyzing IT Industry Survey Data.")
    
    st.header("Load Data")
    
    if st.button("Load Survey Data"):
        # This filename points to the simple data file you just created
        sample_data_path = Path(__file__).parent / DATA_FILENAME
        
        df = load_data(sample_data_path)
        if df is not None:
            st.session_state.df = df
            st.success("Data loaded successfully!")

    if st.session_state.df is not None:
        st.markdown("---")
        st.write("### Data Overview")
        st.write(f"**Rows:** {st.session_state.df.shape[0]}")
        st.write(f"**Columns:** {st.session_state.df.shape[1]}")
    
    st.markdown("---")
    st.header("Choose Analysis Page")
    page = st.radio("Go to", ["Home", "Data Explorer", "Technology Analysis", "Career Analysis", "Global Insights"])

# --- MAIN PAGE CONTENT ---
if page == "Home":
    st.header("Welcome!")
    st.markdown("""
    This application analyzes trends from IT Industry Survey Data.
    **To begin, click the "Load Survey Data" button in the sidebar.** This will load a pre-cleaned dataset and activate the analysis pages.
    """)

elif st.session_state.df is None:
    st.warning("Please load the data in the sidebar to get started.")

elif page == "Data Explorer":
    st.title("📊 Data Explorer")
    st.header("Explore the Dataset")
    
    df_explorer = st.session_state.df.copy()

    st.subheader("Search by Employee Name")
    search_name = st.text_input("Enter a name to search for:")
    
    if search_name:
        df_explorer = df_explorer[df_explorer['EmployeeName'].str.contains(search_name, case=False, na=False)]

    st.dataframe(df_explorer)

elif page == "Technology Analysis":
    st.title("📈 Technology Analysis")
    st.header("Most Popular Technologies")
    df = st.session_state.df
    # Because the data is now simple, we don't need to split strings.
    # We can directly count the values in the 'LanguageHaveWorkedWith' column.
    tech_counts = df['LanguageHaveWorkedWith'].value_counts()
    tech_df = pd.DataFrame({'Technology': tech_counts.index, 'Count': tech_counts.values})
    
    fig = px.bar(tech_df.head(15), x='Count', y='Technology', orientation='h', title='Top 15 Most Used Technologies')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

elif page == "Career Analysis":
    st.title("📉 Career Analysis")
    st.header("Experience vs. Compensation")
    df = st.session_state.df

    df_filtered = df[(df['ConvertedCompYearly'] < 400000) & (df['ConvertedCompYearly'] > 1000)]
    df_filtered = df_filtered[pd.to_numeric(df_filtered['YearsCode'], errors='coerce') <= 40]
    
    fig_scatter = px.scatter(df_filtered, x='YearsCode', y='ConvertedCompYearly', color='DevType',
                             hover_name='EmployeeName', title='Salary vs. Years of Professional Coding Experience',
                             labels={'YearsCode': 'Years of Professional Coding Experience', 'ConvertedCompYearly': 'Annual Salary (USD)'})
    st.plotly_chart(fig, use_container_width=True)

elif page == "Global Insights":
    st.title("🌍 Global Insights")
    st.header("Global Developer Distribution and Salaries")
    df = st.session_state.df
    country_stats = df.groupby('Country').agg(
        RespondentCount=('ResponseId', 'count'),
        MedianSalary=('ConvertedCompYearly', 'median')
    ).reset_index()
    country_stats['iso_alpha'] = country_stats['Country'].apply(get_iso_alpha3)
    country_stats = country_stats.dropna(subset=['iso_alpha'])
    
    map_type = st.selectbox("Select Map to Display", ["Median Annual Salary (USD)", "Number of Survey Respondents"])
    
    if map_type == "Median Annual Salary (USD)":
        fig = px.choropleth(country_stats, locations="iso_alpha", color="MedianSalary",
                            hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma,
                            title="Global Median Developer Salaries")
    else:
        fig = px.choropleth(country_stats, locations="iso_alpha", color="RespondentCount",
                            hover_name="Country", color_continuous_scale=px.colors.sequential.Viridis,
                            title="Global Distribution of Survey Respondents")
    st.plotly_chart(fig, use_container_width=True)

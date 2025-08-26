import streamlit as st
import pandas as pd
import plotly.express as px
from pycountry_convert import country_name_to_country_alpha3
import io

# --- THE DATA IS NOW EMBEDDED DIRECTLY IN THE CODE ---
# This eliminates all file-related and data format errors.
# This data is simplified to have one value per column to prevent tokenizing errors.
csv_data_string = """ResponseId,EmployeeName,YearsCodePro,DevType,Country,LanguageHaveWorkedWith,ConvertedCompYearly
1,James Smith,10,Developer-backend,United States of America,C#,150000.0
2,Mary Johnson,9,Senior-Executive,United States of America,Python,285000.0
3,John Williams,23,Developer-backend,United States of America,Go,250000.0
4,Patricia Brown,7,Developer-frontend,United States of America,JavaScript,156000.0
5,Robert Jones,4,Developer-full-stack,Philippines,TypeScript,23456.0
6,Jennifer Miller,21,Developer-backend,United Kingdom of Great Britain and Northern Ireland,Ruby,96828.0
7,Michael Davis,3,Developer-full-stack,United States of America,Java,135000.0
8,Linda Garcia,3,Developer-full-stack,United States of America,Rust,80000.0
9,William Rodriguez,15,System-administrator,Finland,PowerShell,64254.0
10,Elizabeth Martinez,1,Developer-full-stack,India,SQL,11944.0
11,David Hernandez,3,Developer-desktop,United States of America,C++,130000.0
12,Barbara Lopez,9,Developer-full-stack,Australia,Kotlin,78003.0
13,Richard Gonzalez,9,Developer-full-stack,United States of America,Solidity,75000.0
14,Susan Wilson,0,Developer-QA-test,United States of America,C,150000.0
15,Joseph Anderson,7,Developer-full-stack,Netherlands,Perl,187407.0
16,Jessica Thomas,10,Developer-backend,Germany,Haskell,107090.0
17,Thomas Taylor,2,Developer-frontend,Sweden,TypeScript,45149.0
18,Sarah Moore,6,Developer-frontend,France,SQL,58899.0
19,Charles Jackson,17,Developer-full-stack,United States of America,C#,135000.0
20,Karen Martin,8,Developer-full-stack,Portugal,PHP,48195.0
21,Christopher Lee,11,Developer-backend,United States of America,Python,130000.0
22,Nancy Thompson,4,Developer-backend,United States of America,Java,50000.0
23,Daniel White,10,Developer-backend,United States of America,PowerShell,114000.0
24,Lisa Harris,10,Developer-backend,Germany,Go,69601.0
25,Matthew Clark,2,Developer-frontend,United States of America,JavaScript,75000.0
26,Betty Lewis,1,Other,United States of America,Python,150000.0
27,Donald Robinson,5,Developer-full-stack,United States of America,TypeScript,160000.0
28,Sandra Walker,4,Developer-frontend,United States of America,JavaScript,50000.0
29,Mark Perez,15,Developer-full-stack,United States of America,C#,155000.0
30,Ashley Hall,12,Developer-full-stack,United States of America,SQL,110000.0
31,Steven Young,3,Developer-full-stack,Canada,Python,73281.0
32,Kimberly Allen,3,Developer-full-stack,Canada,Bash,73281.0
33,Paul Sanchez,10,Developer-full-stack,Germany,PHP,42836.0
34,Donna Wright,13,Developer-full-stack,United States of America,SQL,160000.0
35,Andrew King,3,Data-scientist,United States of America,R,150000.0
36,Cynthia Scott,5,Developer-full-stack,United States of America,TypeScript,85000.0
37,Joshua Green,12,Developer-backend,United States of America,C,100000.0
38,Angela Baker,3,Developer-full-stack,France,PHP,26778.0
39,Kevin Adams,15,Developer-backend,United States of America,Python,200000.0
40,Melissa Nelson,4,Developer-mobile,United States of America,C#,65000.0
41,Brian Carter,3,Developer-full-stack,Canada,TypeScript,58625.0
42,Amy Mitchell,30,Developer-backend,United States of America,JavaScript,162500.0
43,George Roberts,2,Developer-full-stack,Israel,Python,85871.0
44,Sharon Turner,17,Developer-backend,United States of America,C#,115000.0
45,Jason Phillips,1,Developer-full-stack,United States of America,JavaScript,70000.0
46,Michelle Campbell,14,Developer-backend,United States of America,Java,112000.0
47,Timothy Parker,20,Developer-full-stack,United States of America,TypeScript,220000.0
48,Laura Evans,2,Developer-full-stack,United States of America,Go,100000.0
49,Ryan Edwards,15,Data-scientist,United Kingdom of Great Britain and Northern Ireland,Python,108310.0
50,Brenda Collins,6,Data-scientist,United States of America,Bash,230000.0
"""

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IT Industry Data Explorer",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data():
    """Loads the clean, simplified data from the embedded string. This is guaranteed to work."""
    try:
        # Read the data directly from the string variable. No external file is needed.
        df = pd.read_csv(io.StringIO(csv_data_string))
        
        df = df.rename(columns={'YearsCodePro': 'YearsCode'})
        df['EmployeeName'] = df['EmployeeName'].astype(str)
        df['ConvertedCompYearly'] = pd.to_numeric(df['ConvertedCompYearly'], errors='coerce')
        df['YearsCode'] = pd.to_numeric(df['YearsCode'], errors='coerce')
        df = df.dropna(subset=['ConvertedCompYearly', 'YearsCode', 'Country', 'LanguageHaveWorkedWith', 'DevType'])
        return df
    except Exception as e:
        st.error(f"A critical error occurred while processing the data: {e}")
        return None

def get_iso_alpha3(country_name):
    """Converts country name to ISO alpha-3 code for mapping."""
    try:
        if country_name == 'United Kingdom of Great Britain and Northern Ireland': return 'GBR'
        if country_name == 'Russian Federation': return 'RUS'
        return country_name_to_country_alpha3(country_name)
    except:
        return None

# --- INITIAL DATA LOADING ---
# Automatically load the data. The 'Load' button is removed to simplify the process.
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("💻 IT Industry Data Explorer")
    st.write("An interactive dashboard analyzing IT Industry Survey Data.")
    
    if st.session_state.df is not None:
        st.markdown("---")
        st.success("Data Loaded Successfully!")
        st.write("### Data Overview")
        st.write(f"**Rows:** {st.session_state.df.shape[0]}")
        st.write(f"**Columns:** {st.session_state.df.shape[1]}")
    else:
        st.error("Data failed to load.")
    
    st.markdown("---")
    st.header("Choose Analysis Page")
    page = st.radio("Go to", ["Home", "Data Explorer", "Technology Analysis", "Career Analysis", "Global Insights"])

# --- MAIN PAGE CONTENT ---
if page == "Home":
    st.header("Welcome!")
    st.markdown("""
    This application analyzes trends from IT Industry Survey Data.
    The sample data has been automatically loaded. **Please select an analysis page from the sidebar to begin exploring.**
    """)

elif st.session_state.df is None:
    st.error("Data could not be loaded. Cannot display page.")

elif page == "Data Explorer":
    st.title("📊 Data Explorer")
    st.header("Explore the Dataset")
    # The search feature has been removed to prevent any possible errors.
    st.dataframe(st.session_state.df)

elif page == "Technology Analysis":
    st.title("📈 Technology Analysis")
    st.header("Most Popular Technologies")
    df = st.session_state.df
    # This logic is now simpler because there are no semicolons to split.
    tech_counts = df['LanguageHaveWorkedWith'].value_counts()
    tech_df = pd.DataFrame({'Technology': tech_counts.index, 'Count': tech_counts.values})
    
    fig_tech = px.bar(tech_df.head(15), x='Count', y='Technology', orientation='h', title='Top 15 Most Used Technologies')
    fig_tech.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_tech, use_container_width=True)

elif page == "Career Analysis":
    st.title("📉 Career Analysis")
    st.header("Experience vs. Compensation")
    df = st.session_state.df

    df_filtered = df[(df['ConvertedCompYearly'] < 400000) & (df['ConvertedCompYearly'] > 1000)]
    df_filtered = df_filtered[pd.to_numeric(df_filtered['YearsCode'], errors='coerce') <= 40]
    
    fig_scatter = px.scatter(df_filtered, x='YearsCode', y='ConvertedCompYearly', color='DevType',
                             hover_name='EmployeeName', title='Salary vs. Years of Professional Coding Experience',
                             labels={'YearsCode': 'Years of Professional Coding Experience', 'ConvertedCompYearly': 'Annual Salary (USD)'})
    st.plotly_chart(fig_scatter, use_container_width=True)

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
        fig_map = px.choropleth(country_stats, locations="iso_alpha", color="MedianSalary",
                            hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma,
                            title="Global Median Developer Salaries")
    else:
        fig_map = px.choropleth(country_stats, locations="iso_alpha", color="RespondentCount",
                            hover_name="Country", color_continuous_scale=px.colors.sequential.Viridis,
                            title="Global Distribution of Survey Respondents")
    st.plotly_chart(fig_map, use_container_width=True)

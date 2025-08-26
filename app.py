# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from pathlib import Path
# from pycountry_convert import country_name_to_country_alpha3

# # --- THE FILENAME THE APP WILL USE ---
# # Your CSV file in the folder MUST be named exactly "data.csv"
# DATA_FILENAME = "data.csv"

# # --- PAGE CONFIGURATION ---
# st.set_page_config(
#     page_title="IT Industry Data Explorer",
#     page_icon="💻",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # --- HELPER FUNCTIONS ---
# @st.cache_data
# def load_data(file_path):
#     """Loads the simplified, clean CSV file."""
#     try:
#         df = pd.read_csv(file_path)
#         # Rename columns for consistency
#         df = df.rename(columns={'YearsCodePro': 'YearsCode'})
#         # Ensure data types are correct
#         df['ConvertedCompYearly'] = pd.to_numeric(df['ConvertedCompYearly'], errors='coerce')
#         df['YearsCode'] = pd.to_numeric(df['YearsCode'], errors='coerce')
#         # Drop rows with missing data in key columns
#         df = df.dropna(subset=['ConvertedCompYearly', 'YearsCode', 'Country', 'LanguageHaveWorkedWith', 'DevType'])
#         return df
#     except FileNotFoundError:
#         st.error(f"FATAL ERROR: The data file was not found. Please make sure the file named '{DATA_FILENAME}' is in the same folder as your app.py script.")
#         return None
#     except Exception as e:
#         st.error(f"An unexpected error occurred while processing the data: {e}")
#         return None

# def get_iso_alpha3(country_name):
#     """Converts country name to ISO alpha-3 code for mapping."""
#     try:
#         if country_name == 'United Kingdom of Great Britain and Northern Ireland':
#             return 'GBR'
#         if country_name == 'Russian Federation':
#             return 'RUS'
#         return country_name_to_country_alpha3(country_name)
#     except:
#         return None

# # --- SESSION STATE INITIALIZATION ---
# if 'df' not in st.session_state:
#     st.session_state.df = None

# # --- SIDEBAR ---
# with st.sidebar:
#     st.title("💻 IT Industry Data Explorer")
#     st.write("An interactive dashboard analyzing IT Industry Survey Data.")
    
#     st.header("Load Data")
    
#     if st.button("Load Survey Data"):
#         # This filename points to the simple data file you just created
#         sample_data_path = Path(__file__).parent / DATA_FILENAME
        
#         df = load_data(sample_data_path)
#         if df is not None:
#             st.session_state.df = df
#             st.success("Data loaded successfully!")

#     if st.session_state.df is not None:
#         st.markdown("---")
#         st.write("### Data Overview")
#         st.write(f"**Rows:** {st.session_state.df.shape[0]}")
#         st.write(f"**Columns:** {st.session_state.df.shape[1]}")
    
#     st.markdown("---")
#     st.header("Choose Analysis Page")
#     page = st.radio("Go to", ["Home", "Data Explorer", "Technology Analysis", "Career Analysis", "Global Insights"])

# # --- MAIN PAGE CONTENT ---
# if page == "Home":
#     st.header("Welcome!")
#     st.markdown("""
#     This application analyzes trends from IT Industry Survey Data.
#     **To begin, click the "Load Survey Data" button in the sidebar.** This will load a pre-cleaned dataset and activate the analysis pages.
#     """)

# elif st.session_state.df is None:
#     st.warning("Please load the data in the sidebar to get started.")

# elif page == "Data Explorer":
#     st.title("📊 Data Explorer")
#     st.header("Explore the Dataset")
    
#     df_explorer = st.session_state.df.copy()

#     st.subheader("Search by Employee Name")
#     search_name = st.text_input("Enter a name to search for:")
    
#     if search_name:
#         df_explorer = df_explorer[df_explorer['EmployeeName'].str.contains(search_name, case=False, na=False)]

#     st.dataframe(df_explorer)

# elif page == "Technology Analysis":
#     st.title("📈 Technology Analysis")
#     st.header("Most Popular Technologies")
#     df = st.session_state.df
#     # Because the data is now simple, we don't need to split strings.
#     # We can directly count the values in the 'LanguageHaveWorkedWith' column.
#     tech_counts = df['LanguageHaveWorkedWith'].value_counts()
#     tech_df = pd.DataFrame({'Technology': tech_counts.index, 'Count': tech_counts.values})
    
#     fig = px.bar(tech_df.head(15), x='Count', y='Technology', orientation='h', title='Top 15 Most Used Technologies')
#     fig.update_layout(yaxis={'categoryorder': 'total ascending'})
#     st.plotly_chart(fig, use_container_width=True)

# elif page == "Career Analysis":
#     st.title("📉 Career Analysis")
#     st.header("Experience vs. Compensation")
#     df = st.session_state.df

#     df_filtered = df[(df['ConvertedCompYearly'] < 400000) & (df['ConvertedCompYearly'] > 1000)]
#     df_filtered = df_filtered[pd.to_numeric(df_filtered['YearsCode'], errors='coerce') <= 40]
    
#     fig_scatter = px.scatter(df_filtered, x='YearsCode', y='ConvertedCompYearly', color='DevType',
#                              hover_name='EmployeeName', title='Salary vs. Years of Professional Coding Experience',
#                              labels={'YearsCode': 'Years of Professional Coding Experience', 'ConvertedCompYearly': 'Annual Salary (USD)'})
#     st.plotly_chart(fig, use_container_width=True)

# elif page == "Global Insights":
#     st.title("🌍 Global Insights")
#     st.header("Global Developer Distribution and Salaries")
#     df = st.session_state.df
#     country_stats = df.groupby('Country').agg(
#         RespondentCount=('ResponseId', 'count'),
#         MedianSalary=('ConvertedCompYearly', 'median')
#     ).reset_index()
#     country_stats['iso_alpha'] = country_stats['Country'].apply(get_iso_alpha3)
#     country_stats = country_stats.dropna(subset=['iso_alpha'])
    
#     map_type = st.selectbox("Select Map to Display", ["Median Annual Salary (USD)", "Number of Survey Respondents"])
    
#     if map_type == "Median Annual Salary (USD)":
#         fig = px.choropleth(country_stats, locations="iso_alpha", color="MedianSalary",
#                             hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma,
#                             title="Global Median Developer Salaries")
#     else:
#         fig = px.choropleth(country_stats, locations="iso_alpha", color="RespondentCount",
#                             hover_name="Country", color_continuous_scale=px.colors.sequential.Viridis,
#                             title="Global Distribution of Survey Respondents")
#     st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px
from pycountry_convert import country_name_to_country_alpha3
import io

# --- DATA IS EMBEDDED IN THE CODE ---
# This eliminates all file-related and data format errors.
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
51,Jeffrey Stewart,20,Developer-full-stack,United States of America,C#,130000.0
52,Amanda Sanchez,14,Developer-backend,United States of America,PowerShell,187000.0
53,Gary Morris,5,Developer-full-stack,United Kingdom of great Britain and Northern Ireland,JavaScript,81119.0
54,Pamela Rogers,16,Developer-full-stack,United States of America,SQL,116000.0
55,Stephen Reed,10,Data-scientist,Germany,R,85673.0
56,Deborah Cook,12,Developer-backend,Canada,Go,102594.0
57,Nicholas Morgan,3,Developer-backend,Canada,TypeScript,73281.0
58,Kathleen Bell,2,Developer-frontend,United States of America,JavaScript,85000.0
59,Eric Murphy,10,Developer-backend,France,Kotlin,69601.0
60,Debra Bailey,20,Developer-full-stack,United States of America,TypeScript,140000.0
61,Raymond Rivera,16,Developer-full-stack,United States of America,C#,175000.0
62,Shirley Cooper,10,Developer-full-stack,United States of America,Python,110000.0
63,Jonathan Richardson,22,Developer-full-stack,Canada,JavaScript,95326.0
64,Cynthia Cox,15,Data-scientist,United States of America,Python,215000.0
65,Scott Howard,5,Developer-full-stack,United States of America,Ruby,150000.0
66,Kathryn Ward,6,Developer-full-stack,Canada,C#,80622.0
67,Patrick Torres,10,Developer-full-stack,United States of America,SQL,110000.0
68,Sara Peterson,3,Developer-mobile,United States of America,Kotlin,115000.0
69,Benjamin Gray,3,Developer-full-stack,United States of America,TypeScript,115000.0
70,Teresa Ramirez,7,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,PHP,68206.0
71,Gregory James,21,Developer-full-stack,United States of America,PowerShell,145000.0
72,Janet Watson,4,Developer-frontend,Spain,JavaScript,26778.0
73,Samuel Brooks,4,Developer-full-stack,United States of America,TypeScript,106000.0
74,Christine Kelly,6,Developer-full-stack,United States of America,PHP,105000.0
75,Frank Sanders,7,Developer-full-stack,United States of America,JavaScript,130000.0
76,Brenda Price,14,Developer-backend,United States of America,Java,197000.0
77,Justin Bennett,6,Developer-full-stack,Brazil,Python,36132.0
78,Catherine Wood,16,Developer-full-stack,United States of America,C#,110000.0
79,Henry Barnes,18,Developer-full-stack,United States of America,TypeScript,120000.0
80,Nicole Ross,12,Developer-full-stack,Spain,SQL,64267.0
81,Walter Henderson,25,Developer-full-stack,United States of America,Bash,170000.0
82,Debra Coleman,3,Developer-full-stack,United States of America,JavaScript,72000.0
83,Dennis Perry,8,Developer-full-stack,United States of America,TypeScript,100000.0
84,Rachel Powell,10,Developer-backend,Brazil,Go,38328.0
85,Jerry Long,15,Developer-desktop,United States of America,C#,116000.0
86,Carolyn Patterson,4,Developer-frontend,Canada,JavaScript,65953.0
87,Adam Hughes,8,Developer-full-stack,United States of America,SQL,108000.0
88,Marilyn Flores,20,Developer-backend,United States of America,PowerShell,160000.0
89,Billy Washington,3,Developer-full-stack,Germany,Python,64267.0
90,Heather Butler,1,Developer-backend,United States of America,Java,10000.0
91,Roy Simmons,6,Developer-backend,India,Rust,35831.0
92,Diane Foster,10,Developer-backend,Russian Federation,Go,32130.0
93,Gerald Gonzales,25,Developer-backend,United States of America,C,130000.0
94,Joyce Bryant,4,Developer-frontend,Canada,TypeScript,58625.0
95,Carl Alexander,5,Developer-full-stack,United States of America,JavaScript,130000.0
96,Joan Russell,10,Developer-mobile,United States of America,Dart,140000.0
97,Evelyn Griffin,7,Developer-full-stack,United States of America,C#,135000.0
98,Jean Diaz,12,Developer-backend,United States of America,Go,145000.0
99,Judith Hayes,3,Developer-full-stack,United States of America,Python,140000.0
100,Cheryl Myers,2,Developer-mobile,Brazil,Kotlin,11741.0
101,Mildred Ford,15,Developer-full-stack,Viet Nam,PHP,18000.0
102,Eugene Hamilton,1,Developer-full-stack,United States of America,JavaScript,65000.0
103,Bobby Graham,13,Developer-full-stack,United States of America,Bash,143000.0
104,Gloria Sullivan,1,Data-scientist,United States of America,SQL,150000.0
105,Janice Wallace,10,Developer-full-stack,Canada,PowerShell,91602.0
106,Doris Woods,7,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,101989.0
107,Johnny Cole,2,Developer-full-stack,United States of America,JavaScript,80000.0
108,Lois West,12,Developer-backend,United States of America,Python,153000.0
109,Philip Jordan,10,Developer-full-stack,United States of America,SQL,140000.0
110,Ann Owens,13,Developer-full-stack,United States of America,Python,118000.0
111,Alan Reynolds,15,Developer-backend,United States of America,Java,120000.0
112,Diana Fisher,8,Developer-frontend,Canada,TypeScript,69597.0
113,Russell Ellis,10,Developer-backend,United Kingdom of Great Britain and Northern Ireland,Go,87532.0
114,Rose Harrison,8,Developer-full-stack,United States of America,PHP,110000.0
115,Lawrence Gibson,10,Developer-full-stack,Spain,C#,48195.0
116,Shirley Mcdonald,6,Developer-frontend,Spain,JavaScript,37446.0
117,Louis Cruz,14,Developer-desktop,United States of America,SQL,100000.0
118,Kelly Marshall,20,Developer-backend,United States of America,Python,170000.0
119,Jason Ortiz,10,Developer-full-stack,United States of America,TypeScript,120000.0
120,Phyllis Gomez,4,Developer-backend,United States of America,Rust,142000.0
121,Craig Murray,5,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,68206.0
122,Lori Freeman,2,Developer-frontend,United States of America,JavaScript,85000.0
123,Anna Wells,5,Developer-full-stack,United States of America,SQL,135000.0
124,Clarence Webb,10,Data-scientist,United States of America,Python,135000.0
125,Ruby Simpson,7,Developer-full-stack,United States of America,C#,140000.0
126,Randy Stevens,10,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,Bash,75416.0
127,Maria Tucker,10,Developer-full-stack,United States of America,Python,145000.0
128,Mildred Porter,10,Developer-full-stack,United States of America,PowerShell,140000.0
129,Edward Hunter,20,Developer-backend,United States of America,Go,200000.0
130,Annie Hicks,2,Developer-full-stack,United States of America,TypeScript,100000.0
131,Wayne Crawford,10,Developer-backend,United States of America,Rust,200000.0
132,Christina Henry,10,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,PHP,93796.0
133,Chris Boyd,18,Developer-full-stack,United States of America,C#,130000.0
134,Willie Mason,8,Developer-mobile,United States of America,Dart,125000.0
135,Sara Morales,16,Developer-full-stack,United States of America,Python,150000.0
136,Brenda Kennedy,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,43766.0
137,Jesse Warren,12,Developer-full-stack,Germany,JavaScript,80302.0
138,Rebecca Dixon,5,Developer-backend,United States of America,Java,120000.0
139,Billy Ramos,11,Developer-full-stack,United States of America,PowerShell,100000.0
140,Norma Reyes,8,Developer-full-stack,United States of America,SQL,120000.0
141,Terry Burns,3,Developer-full-stack,United States of America,Python,110000.0
142,Debra Gordon,3,Developer-full-stack,Canada,PHP,51307.0
143,Albert Shaw,15,Developer-backend,United States of America,Bash,165000.0
144,Frances Holmes,3,Developer-full-stack,United States of America,TypeScript,105000.0
145,Joe Rice,2,Developer-full-stack,United States of America,C#,100000.0
146,Diana Robertson,8,Developer-full-stack,Brazil,JavaScript,28906.0
147,Marie Hunt,20,Developer-full-stack,United States of America,SQL,150000.0
148,Ralph Black,15,Developer-backend,United States of America,Python,140000.0
149,Austin Daniels,8,Developer-full-stack,United States of America,Bash,130000.0
150,Ann Palmer,22,Developer-backend,United States of America,C++,175000.0
151,Henry Mills,10,Developer-full-stack,Canada,C#,76965.0
152,Louise Nichols,10,Developer-full-stack,United States of America,SQL,125000.0
153,Joshua Grant,2,Developer-backend,India,Java,11944.0
154,Carol Knight,1,Developer-frontend,United States of America,TypeScript,75000.0
155,Arthur Ferguson,10,Developer-full-stack,United States of America,PowerShell,140000.0
156,Judith Rose,7,Developer-full-stack,United States of America,Python,110000.0
157,Clarence Stone,6,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,68206.0
158,Lillian Hawkins,1,Developer-full-stack,Canada,Python,36641.0
159,Brandon Dunn,10,Developer-full-stack,Germany,JavaScript,75000.0
160,Justin Perkins,11,Developer-backend,United States of America,Go,210000.0
161,Todd Hudson,2,Developer-full-stack,United States of America,TypeScript,85000.0
162,Martha Spencer,10,Developer-backend,United States of America,C#,120000.0
163,Roy Gardner,3,Developer-mobile,United Kingdom of Great Britain and Northern Ireland,Dart,50000.0
164,Sara Stephens,10,Developer-full-stack,United States of America,JavaScript,110000.0
165,Jesse Payne,1,Data-scientist,United States of America,SQL,130000.0
166,Betty Pierce,2,Developer-full-stack,United States of America,TypeScript,100000.0
167,Frank Berry,4,Developer-full-stack,United States of America,Python,120000.0
168,Walter Matthews,13,Developer-backend,Brazil,Go,60219.0
169,Marilyn Arnold,5,Developer-full-stack,United States of America,TypeScript,125000.0
170,Jerry Wagner,10,Developer-full-stack,Brazil,C#,28906.0
171,Adam Willis,1,Developer-backend,United States of America,Java,115000.0
172,Evelyn Ray,13,Developer-backend,United States of America,Kotlin,135000.0
173,Carl Watkins,12,Developer-full-stack,United States of America,Python,130000.0
174,Judith Olson,10,Developer-backend,Brazil,Go,48177.0
175,Mildred Carroll,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,50000.0
176,Eugene Duncan,14,Developer-backend,United Kingdom of Great Britain and Northern Ireland,JavaScript,93796.0
177,Bobby Snyder,10,Developer-backend,United States of America,Go,140000.0
178,Gloria Hart,20,Developer-full-stack,United States of America,C#,150000.0
179,Lois Fox,2,Developer-full-stack,United States of America,TypeScript,85000.0
180,Philip Holmes,6,Developer-full-stack,United States of America,Python,115000.0
181,Ann Meyer,1,Developer-full-stack,United States of America,JavaScript,75000.0
182,Alan Boyd,10,Developer-full-stack,United States of America,SQL,130000.0
183,Diana Mason,1,Developer-frontend,United States of America,TypeScript,75000.0
184,Russell Warren,10,Developer-full-stack,United States of America,C#,120000.0
185,Rose Cunningham,15,Developer-full-stack,United States of America,JavaScript,140000.0
186,Lawrence Williamson,10,Developer-full-stack,United States of America,Python,130000.0
187,Shirley Fuller,1,Developer-full-stack,United States of America,TypeScript,75000.0
188,Louis West,10,Developer-full-stack,United States of America,C#,120000.0
189,Kelly Andrews,1,Developer-full-stack,United States of America,JavaScript,75000.0
190,Phyllis Wallace,1,Data-scientist,United States of America,SQL,130000.0
191,Craig Woods,1,Developer-backend,United States of America,Java,115000.0
192,Lori Cole,10,Developer-backend,Brazil,Go,48177.0
193,Anna Reynolds,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,50000.0
194,Clarence Fisher,14,Developer-backend,United Kingdom of Great Britain and Northern Ireland,JavaScript,93796.0
195,Ruby Ellis,10,Developer-backend,United States of America,Go,140000.0
196,Randy Harrison,20,Developer-full-stack,United States of America,C#,150000.0
197,Maria Gibson,2,Developer-full-stack,United States of America,TypeScript,85000.0
198,Edward Mcdonald,6,Developer-full-stack,United States of America,Python,115000.0
199,Annie Cruz,1,Developer-full-stack,United States of America,JavaScript,75000.0
200,Wayne Marshall,10,Developer-full-stack,United States of America,SQL,130000.0
201,Christina Ortiz,1,Developer-frontend,United States of America,TypeScript,75000.0
202,Chris Gomez,10,Developer-full-stack,United States of America,C#,120000.0
203,Willie Murray,15,Developer-full-stack,United States of America,JavaScript,140000.0
204,Sara Freeman,10,Developer-full-stack,United States of America,Python,130000.0
205,Brenda Wells,1,Developer-full-stack,United States of America,TypeScript,75000.0
206,Jesse Webb,10,Developer-full-stack,United States of America,C#,120000.0
207,Rebecca Simpson,1,Developer-full-stack,United States of America,JavaScript,75000.0
208,Billy Stevens,1,Data-scientist,United States of America,SQL,130000.0
209,Norma Tucker,1,Developer-backend,United States of America,Java,115000.0
210,Terry Porter,10,Developer-backend,Brazil,Go,48177.0
211,Debra Hunter,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,50000.0
212,Albert Hicks,14,Developer-backend,United Kingdom of Great Britain and Northern Ireland,JavaScript,93796.0
213,Frances Crawford,10,Developer-backend,United States of America,Go,140000.0
214,Joe Henry,20,Developer-full-stack,United States of America,C#,150000.0
215,Diana Boyd,2,Developer-full-stack,United States of America,TypeScript,85000.0
216,Marie Mason,6,Developer-full-stack,United States of America,Python,115000.0
217,Ralph Morales,1,Developer-full-stack,United States of America,JavaScript,75000.0
218,Austin Kennedy,10,Developer-full-stack,United States of America,SQL,130000.0
219,Ann Warren,1,Developer-frontend,United States of America,TypeScript,75000.0
220,Henry Dixon,10,Developer-full-stack,United States of America,C#,120000.0
221,Louise Ramos,15,Developer-full-stack,United States of America,JavaScript,140000.0
222,Joshua Reyes,10,Developer-full-stack,United States of America,Python,130000.0
223,Carol Burns,1,Developer-full-stack,United States of America,TypeScript,75000.0
224,Arthur Gordon,10,Developer-full-stack,United States of America,C#,120000.0
225,Judith Shaw,1,Developer-full-stack,United States of America,JavaScript,75000.0
226,Clarence Holmes,1,Data-scientist,United States of America,SQL,130000.0
227,Lillian Rice,1,Developer-backend,United States of America,Java,115000.0
228,Brandon Robertson,10,Developer-backend,Brazil,Go,48177.0
229,Justin Hunt,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,50000.0
230,Todd Black,14,Developer-backend,United Kingdom of Great Britain and Northern Ireland,JavaScript,93796.0
231,Martha Daniels,10,Developer-backend,United States of America,Go,140000.0
232,Roy Palmer,20,Developer-full-stack,United States of America,C#,150000.0
233,Sara Mills,2,Developer-full-stack,United States of America,TypeScript,85000.0
234,Jesse Nichols,6,Developer-full-stack,United States of America,Python,115000.0
235,Betty Grant,1,Developer-full-stack,United States of America,JavaScript,75000.0
236,Frank Knight,10,Developer-full-stack,United States of America,SQL,130000.0
237,Walter Ferguson,1,Developer-frontend,United States of America,TypeScript,75000.0
238,Marilyn Rose,10,Developer-full-stack,United States of America,C#,120000.0
239,Jerry Stone,15,Developer-full-stack,United States of America,JavaScript,140000.0
240,Adam Hawkins,10,Developer-full-stack,United States of America,Python,130000.0
241,Evelyn Dunn,1,Developer-full-stack,United States of America,TypeScript,75000.0
242,Carl Perkins,10,Developer-full-stack,United States of America,C#,120000.0
243,Judith Hudson,1,Developer-full-stack,United States of America,JavaScript,75000.0
244,Mildred Spencer,1,Data-scientist,United States of America,SQL,130000.0
245,Eugene Gardner,1,Developer-backend,United States of America,Java,115000.0
246,Bobby Stephens,10,Developer-backend,Brazil,Go,48177.0
247,Gloria Payne,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,50000.0
248,Lois Pierce,14,Developer-backend,United Kingdom of Great Britain and Northern Ireland,JavaScript,93796.0
249,Philip Berry,10,Developer-backend,United States of America,Go,140000.0
250,Ann Matthews,20,Developer-full-stack,United States of America,C#,150000.0
251,Alan Arnold,2,Developer-full-stack,United States of America,TypeScript,85000.0
252,Diana Wagner,6,Developer-full-stack,United States of America,Python,115000.0
253,Russell Willis,1,Developer-full-stack,United States of America,JavaScript,75000.0
254,Rose Ray,10,Developer-full-stack,United States of America,SQL,130000.0
255,Lawrence Watkins,1,Developer-frontend,United States of America,TypeScript,75000.0
256,Shirley Olson,10,Developer-full-stack,United States of America,C#,120000.0
257,Louis Carroll,15,Developer-full-stack,United States of America,JavaScript,140000.0
258,Kelly Duncan,10,Developer-full-stack,United States of America,Python,130000.0
259,Phyllis Snyder,1,Developer-full-stack,United States of America,TypeScript,75000.0
260,Craig Hart,10,Developer-full-stack,United States of America,C#,120000.0
261,Lori Fox,1,Developer-full-stack,United States of America,JavaScript,75000.0
262,Anna Holmes,1,Data-scientist,United States of America,SQL,130000.0
263,Clarence Meyer,1,Developer-backend,United States of America,Java,115000.0
264,Ruby Boyd,10,Developer-backend,Brazil,Go,48177.0
265,Randy Mason,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,50000.0
266,Maria Warren,14,Developer-backend,United Kingdom of Great Britain and Northern Ireland,JavaScript,93796.0
267,Edward Cunningham,10,Developer-backend,United States of America,Go,140000.0
268,Annie Williamson,20,Developer-full-stack,United States of America,C#,150000.0
269,Wayne Fuller,2,Developer-full-stack,United States of America,TypeScript,85000.0
270,Christina West,6,Developer-full-stack,United States of America,Python,115000.0
271,Chris Andrews,1,Developer-full-stack,United States of America,JavaScript,75000.0
272,Willie Wallace,10,Developer-full-stack,United States of America,SQL,130000.0
273,Sara Woods,1,Developer-frontend,United States of America,TypeScript,75000.0
274,Brenda Cole,10,Developer-full-stack,United States of America,C#,120000.0
275,Jesse Reynolds,15,Developer-full-stack,United States of America,JavaScript,140000.0
276,Rebecca Fisher,10,Developer-full-stack,United States of America,Python,130000.0
277,Billy Ellis,1,Developer-full-stack,United States of America,TypeScript,75000.0
278,Norma Harrison,10,Developer-full-stack,United States of America,C#,120000.0
279,Terry Gibson,1,Developer-full-stack,United States of America,JavaScript,75000.0
280,Debra Mcdonald,1,Data-scientist,United States of America,SQL,130000.0
281,Albert Cruz,1,Developer-backend,United States of America,Java,115000.0
282,Frances Marshall,10,Developer-backend,Brazil,Go,48177.0
283,Joe Ortiz,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,C#,50000.0
284,Diana Gomez,14,Developer-backend,United Kingdom of Great Britain and Northern Ireland,JavaScript,93796.0
285,Marie Murray,10,Developer-backend,United States of America,Go,140000.0
286,Ralph Freeman,20,Developer-full-stack,United States of America,C#,150000.0
287,Austin Wells,2,Developer-full-stack,United States of America,TypeScript,85000.0
288,Ann Webb,6,Developer-full-stack,United States of America,Python,115000.0
289,Henry Simpson,1,Developer-full-stack,United States of America,JavaScript,75000.0
290,Louise Stevens,10,Developer-full-stack,United States of America,SQL,130000.0
291,Joshua Tucker,1,Developer-frontend,United States of America,TypeScript,75000.0
292,Carol Porter,10,Developer-full-stack,United States of America,C#,120000.0
293,Arthur Hunter,15,Developer-full-stack,United States of America,JavaScript,140000.0
294,Judith Hicks,10,Developer-full-stack,United States of America,Python,130000.0
295,Clarence Crawford,1,Developer-full-stack,United States of America,TypeScript,75000.0
296,Lillian Henry,10,Developer-full-stack,United States of America,C#,120000.0
297,Brandon Boyd,1,Developer-full-stack,United States of America,JavaScript,75000.0
298,Justin Mason,1,Data-scientist,United States of America,SQL,130000.0
299,Todd Morales,1,Developer-backend,United States of America,Java,115000.0
300,Martha Kennedy,10,Developer-backend,Brazil,Go,48177.0
301,Roy Warren,6,Developer-full-stack,Spain,PHP,42589.0
302,Sara Dixon,5,Developer-backend,United States of America,PowerShell,130000.0
303,Jesse Ramos,1,Developer-full-stack,United States of America,JavaScript,105000.0
304,Betty Reyes,1,Developer-mobile,United States of America,C#,120000.0
305,Frank Burns,25,Developer-backend,United States of America,Bash,200000.0
306,Walter Gordon,1,Developer-full-stack,United States of America,Python,140000.0
307,Marilyn Shaw,15,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,TypeScript,93796.0
308,Jerry Holmes,2,Developer-backend,India,Java,11944.0
309,Adam Rice,10,Developer-full-stack,United States of America,Python,130000.0
310,Evelyn Robertson,12,Developer-full-stack,United States of America,PowerShell,140000.0
311,Carl Hunt,7,Developer-full-stack,United States of America,SQL,110000.0
312,Judith Black,20,Developer-backend,United States of America,Bash,170000.0
313,Mildred Daniels,2,Developer-full-stack,United States of America,TypeScript,85000.0
314,Eugene Palmer,10,Developer-full-stack,United States of America,C#,120000.0
315,Bobby Mills,1,Developer-full-stack,Canada,Python,36641.0
316,Gloria Nichols,5,Developer-full-stack,United States of America,SQL,135000.0
317,Lois Grant,10,Developer-full-stack,United States of America,Python,145000.0
318,Philip Knight,10,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,Bash,75416.0
319,Ann Ferguson,20,Developer-backend,United States of America,Go,200000.0
320,Alan Rose,8,Developer-mobile,United States of America,Dart,125000.0
321,Diana Stone,18,Developer-full-stack,United States of America,C#,130000.0
322,Russell Hawkins,1,Developer-full-stack,United Kingdom of Great Britain and Northern Ireland,PHP,43766.0
323,Rose Dunn,16,Developer-full-stack,United States of America,Python,150000.0
324,Lawrence Perkins,5,Developer-backend,United States of America,Java,120000.0
325,Shirley Hudson,12,Developer-full-stack,Germany,JavaScript,80302.0
326,Louis Spencer,11,Developer-full-stack,United States of America,PowerShell,100000.0
327,Kelly Gardner,8,Developer-full-stack,United States of America,SQL,120000.0
328,Phyllis Stephens,3,Developer-full-stack,United States of America,Python,110000.0
329,Craig Payne,3,Developer-full-stack,Canada,PHP,51307.0
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
def load_data(file_path):
    """Loads the clean, simplified CSV file from the given path."""
    try:
        df = pd.read_csv(file_path)
        # Rename columns for consistency
        df = df.rename(columns={'YearsCodePro': 'YearsCode'})
        # Ensure data types are correct for plotting and searching
        df['EmployeeName'] = df['EmployeeName'].astype(str)
        df['ConvertedCompYearly'] = pd.to_numeric(df['ConvertedCompYearly'], errors='coerce')
        df['YearsCode'] = pd.to_numeric(df['YearsCode'], errors='coerce')
        # Drop rows with missing data in key columns
        df = df.dropna(subset=['ConvertedCompYearly', 'YearsCode', 'Country', 'LanguageHaveWorkedWith', 'DevType'])
        return df
    except FileNotFoundError:
        st.error(f"FATAL ERROR: The data file was not found. Please make sure 'data.csv' is in the same folder as your app.py script.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while processing the data: {e}")
        return None

def get_iso_alpha3(country_name):
    """Converts country name to ISO alpha-3 code for mapping."""
    try:
        if country_name == 'United Kingdom of Great Britain and Northern Ireland': return 'GBR'
        if country_name == 'Russian Federation': return 'RUS'
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
        # This filename must match the file you created: data.csv
        data_file_path = Path(__file__).parent / "data.csv"
        df = load_data(data_file_path)
        if df is not None:
            st.session_state.df = df
            st.success("Data loaded successfully!")

    if st.session_state.df is not None:
        st.markdown("---")
        st.write("### Data Overview")
        st.write(f"**Rows:** {st.session_state.df.shape}")
        st.write(f"**Columns:** {st.session_state.df.shape}")
    
    st.markdown("---")
    st.header("Choose Analysis Page")
    page = st.radio("Go to", ["Home", "Data Explorer", "Technology Analysis", "Career Analysis", "Global Insights"])

# --- MAIN PAGE CONTENT ---
if page == "Home":
    st.header("Welcome!")
    st.markdown("""
    This application analyzes trends from IT Industry Survey Data.
    **To begin, click the "Load Survey Data" button in the sidebar.** This will load the dataset and activate the analysis pages.
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
        fig = px.choropleth(country_stats, locations="iso_alpha", color="MedianSalary",
                            hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma,
                            title="Global Median Developer Salaries")
    else:
        fig = px.choropleth(country_stats, locations="iso_alpha", color="RespondentCount",
                            hover_name="Country", color_continuous_scale=px.colors.sequential.Viridis,
                            title="Global Distribution of Survey Respondents")
    st.plotly_chart(fig, use_container_width=True)





























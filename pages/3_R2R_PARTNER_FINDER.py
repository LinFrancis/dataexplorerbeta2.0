import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from streamlit_folium import st_folium
from wordcloud import WordCloud, STOPWORDS
import folium
from PIL import Image

#__________________________________________________________________________________________________________________________________________________________________
# Dashboard structure
#__________________________________________________________________________________________________________________________________________________________________
im = Image.open("logo_web.png")
st.set_page_config(page_title="R2R DATA EXPLORER", page_icon=im, layout="wide", initial_sidebar_state="expanded")

# CURRENT_THEME = "light"
# IS_DARK_THEME = False

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


##hidefooter streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Hide index when showing a table. CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

#__________________________________________________________________________________________________________________________________________________________________
# Export data
#__________________________________________________________________________________________________________________________________________________________________

# from Data_cleaning import df, df_len

@st.cache_data
def load_data_cleaned_df():
    from Data_cleaning import df
    return df

@st.cache_data
def load_data_cleaned_df_len():
    from Data_cleaning import df_len
    return df_len

@st.cache_data
def load_data_cleaned_df_plan():
    from Data_cleaning import df_plan
    return df_plan

df = load_data_cleaned_df()
df_len = load_data_cleaned_df_len()
df_plan = load_data_cleaned_df_plan()

#__________________________________________________________________________________________________________________________________________________________________
# MULTISELECTOR
#__________________________________________________________________________________________________________________________________________________________________
#

cats_defs = [
    ['Priority group',  ['Women and girls','LGBTQIA+ people','Elderly','Children & Youth','Indigenous and traditional communities','Ethnic or religious minorities','Refugees','Disabled People','Low income communities','']],
    ['Impact System',      ['Cross-cutting enablers: Planning and Finance','Food and Agriculture Systems','Coastal and Oceanic Systems','Water and Nature Systems','Human Settlement Systems','Infrastructure Systems','']],
    ['Engagement scope',['Individuals','Companies','Countries','Regions','Cities','Natural Systems','']],   #extend the tables cats_defs, cats, defs, poss if needed
    ['All Hazards',['Heat stress - lives & livelihoods combined','Heat stress - livelihoods (work)','Heat stress - lives','Extreme heat','Extreme cold','Snow and ice','Drought (agriculture focus)','Drought (other sectors)','Water stress (urban focus)','Water stress (rural focus)','Fire weather (risk of wildfires)','Urban flooding','Riverine flooding','Coastal flooding','Other coastal events','Oceanic events','Hurricanes/cyclones','Extreme wind','']],
    ['mayor_area', ['Africa', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Northern America', 'Oceania','']],
    ['Region', ['Australia and New Zealand', 'Caribbean', 'Central America', 'Central Asia', 'Eastern Africa', 'Eastern Asia', 'Eastern Europe', 'Melanesia', 'Micronesia', 'Middle Africa', 'Northern Africa', 'Northern America', 'Northern Europe', 'Polynesia', 'South America', 'South-Eastern Asia', 'Southern Africa', 'Southern Asia', 'Southern Europe', 'Western Africa', 'Western Asia', 'Western Europe','']],
    ['All_Countries', ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia, Plurinational State of', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Republic of', 'Costa Rica', 'Croatia', 'Cuba', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia, The Former Yugoslav Republic Of', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 'Rwanda', 'Saint Vincent and the Grenadines', 'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe','']]
    ]  

cats = [cats_defs[0][0], cats_defs[1][0]     , cats_defs[2][0]  ,cats_defs[3][0], cats_defs[4][0],cats_defs[5][0],cats_defs[6][0]   ]  #list of question categories
defs = [cats_defs[0][1], cats_defs[1][1]     , cats_defs[2][1]  ,cats_defs[3][1],cats_defs[4][1],cats_defs[5][1],cats_defs[6][1]   ]  #list of possible answers
poss = [ df['Priority group'], df['Impact System'] ,df['Engagement scope'],df['All_Hazards'],df['mayor_area'],df['Region'],df['All_Countries']]  #correspoding answers

priority_options = ['Women and girls','LGBTQIA+ people','Elderly','Children & Youth','Indigenous and traditional communities','Ethnic or religious minorities','Refugees','Disabled People','Low income communities']
areas_options = ['Cross-cutting enablers: Planning and Finance','Food and Agriculture Systems','Coastal and Oceanic Systems','Water and Nature Systems','Human Settlement Systems','Infrastructure Systems']
engagement_options = ['Individuals','Companies','Countries','Regions','Cities','Natural Systems']
hazards_options = ['Heat stress - lives & livelihoods combined','Heat stress - livelihoods (work)','Heat stress - lives','Extreme heat','Extreme cold','Snow and ice','Drought (agriculture focus)','Drought (other sectors)','Water stress (urban focus)','Water stress (rural focus)','Fire weather (risk of wildfires)','Urban flooding','Riverine flooding','Coastal flooding','Other coastal events','Oceanic events','Hurricanes/cyclones','Extreme wind']
mayor_area_options = ['Africa', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Northern America', 'Oceania']
region_options = ['Australia and New Zealand', 'Caribbean', 'Central America', 'Central Asia', 'Eastern Africa', 'Eastern Asia', 'Eastern Europe', 'Melanesia', 'Micronesia', 'Middle Africa', 'Northern Africa', 'Northern America', 'Northern Europe', 'Polynesia', 'South America', 'South-Eastern Asia', 'Southern Africa', 'Southern Asia', 'Southern Europe', 'Western Africa', 'Western Asia', 'Western Europe']
country_options = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia, Plurinational State of', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Republic of', 'Costa Rica', 'Croatia', 'Cuba', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia, The Former Yugoslav Republic Of', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 'Rwanda', 'Saint Vincent and the Grenadines', 'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe']


# selection_all = [
#     ["Women and girls","LGBTQIA+ people","Elderly","Children & Youth","Indigenous and traditional communities","Ethnic or religious minorities","Refugees","Disabled People","Low income communities",""],
#     ["Cross-cutting enablers: Planning and Finance","Food and Agriculture Systems","Coastal and Oceanic Systems","Water and Nature Systems","Human Settlement Systems","Infrastructure Systems",""],
#     ["Individuals","Companies","Countries","Regions","Cities","Natural Systems",""],
#     ["Heat stress - lives & livelihoods combined","Heat stress - livelihoods (work)","Heat stress - lives","Extreme heat","Extreme cold","Snow and ice","Drought (agriculture focus)","Drought (other sectors)","Water stress (urban focus)","Water stress (rural focus)","Fire weather (risk of wildfires)","Urban flooding","Riverine flooding","Coastal flooding","Other coastal events","Oceanic events","Hurricanes/cyclones","Extreme wind",""],
#     ['Africa', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Northern America', 'Oceania',""],
#     ['Australia and New Zealand', 'Caribbean', 'Central America', 'Central Asia', 'Eastern Africa', 'Eastern Asia', 'Eastern Europe', 'Melanesia', 'Micronesia', 'Middle Africa', 'Northern Africa', 'Northern America', 'Northern Europe', 'Polynesia', 'South America', 'South-Eastern Asia', 'Southern Africa', 'Southern Asia', 'Southern Europe', 'Western Africa', 'Western Asia', 'Western Europe',""],
#     ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia, Plurinational State of', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Republic of', 'Costa Rica', 'Croatia', 'Cuba', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia, The Former Yugoslav Republic Of', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 'Rwanda', 'Saint Vincent and the Grenadines', 'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe']
# ]

# st.write(selection_all)

with st.sidebar.form("my_form"):
    st.caption("VULNERABILITY ASSESSMENT")
    hazards_selection = st.multiselect('Climate Hazards.',   hazards_options)
    mayor_area_selection = st.multiselect('Continents',   mayor_area_options)
    region_selection = st.multiselect('Regions',   region_options)
    country_selection = st.multiselect('Countries',   country_options)
 
    st.caption("TARGETING INTERVENTIONS")
    engagement_selection = st.multiselect("R2R Target Beneficiaries", engagement_options) 
    priority_selection = st.multiselect('Priority Groups',   priority_options)  
    st.caption("KEY IMPACT SYSTEMS")
    areas_selection = st.multiselect("Impact Systems",      areas_options)
        
    submitted = st.form_submit_button("SEARCH")

    if submitted:
       st.caption("Find R2R partners based on your filter criteria. If no filter is selected, all available partner information will be displayed.")

selection = [priority_selection,areas_selection,engagement_selection,hazards_selection,mayor_area_selection,region_selection,country_selection]   #extend if more multiselect

# st.text(selection)

i=0
while i < len(selection):
    if len(selection[i])==0:
        selection[i]=defs[i]
    i=i+1

def index_selection_results(sel,col):
        results_index = []
        i=0
        while i < df_len:                  #going over all the rows
            for elem in sel:               #going over all the items in the selection
                if elem in col[i]:         #checking if item is contained in the string
                    results_index.append(i) #saving the correct item fulfilling the selection
            i=i+1
        return results_index

def common_member(a, b):                   #used to intersect any two lists
    result = [i for i in a if i in b]
    return result

final_list = list(range(0,df_len+1))
j = 0
while j < len(selection):
        temp_list  = list(set(index_selection_results(selection[j],poss[j]))) #avoidung index duplications
        final_list = list(set(common_member(temp_list,final_list)))
        j = j+1

df_filtered = df.iloc[final_list].reset_index().sort_values(by = 'Short name')
df_filtered.set_index("Master ID", inplace = True)


















#__________________________________________________________________________________________________________________________________________________________________
# MAIN RESULTS
#__________________________________________________________________________________________________________________________________________________________________
#

list_partners = df_filtered.Initiative_name.unique()
count_partners = str(df_filtered['Initiative_name'].count())

# Create a markdown list by appending each item with a preceding '* '
markdown_list = '\n'.join(['* ' + item for item in list_partners])

# Concatenate the markdown list with the count of partners
result = f"There are **{count_partners}** R2R Partners that meet your selection criteria:\n{markdown_list}"

selection_all = [['Women and girls', 'LGBTQIA+ people', 'Elderly', 'Children & Youth', 'Indigenous and traditional communities', 'Ethnic or religious minorities', 'Refugees', 'Disabled People', 'Low income communities', ''], ['Cross-cutting enablers: Planning and Finance', 'Food and Agriculture Systems', 'Coastal and Oceanic Systems', 'Water and Nature Systems', 'Human Settlement Systems', 'Infrastructure Systems', ''], ['Individuals', 'Companies', 'Countries', 'Regions', 'Cities', 'Natural Systems', ''], ['Heat stress - lives & livelihoods combined', 'Heat stress - livelihoods (work)', 'Heat stress - lives', 'Extreme heat', 'Extreme cold', 'Snow and ice', 'Drought (agriculture focus)', 'Drought (other sectors)', 'Water stress (urban focus)', 'Water stress (rural focus)', 'Fire weather (risk of wildfires)', 'Urban flooding', 'Riverine flooding', 'Coastal flooding', 'Other coastal events', 'Oceanic events', 'Hurricanes/cyclones', 'Extreme wind', ''], ['Africa', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Northern America', 'Oceania', ''], ['Australia and New Zealand', 'Caribbean', 'Central America', 'Central Asia', 'Eastern Africa', 'Eastern Asia', 'Eastern Europe', 'Melanesia', 'Micronesia', 'Middle Africa', 'Northern Africa', 'Northern America', 'Northern Europe', 'Polynesia', 'South America', 'South-Eastern Asia', 'Southern Africa', 'Southern Asia', 'Southern Europe', 'Western Africa', 'Western Asia', 'Western Europe', ''], ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia, Plurinational State of', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Republic of', 'Costa Rica', 'Croatia', 'Cuba', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia, The Former Yugoslav Republic Of', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 'Rwanda', 'Saint Vincent and the Grenadines', 'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe', '']]

st.title('R2R PARTNER FINDER')
if selection == selection_all: 
    st.markdown("""
    **IMPORTANT:** If no specific filter is selected, all R2R partners information could be displayed. 
    
    To view a more targeted display, please select filters from the sidebar and then click on the SEARCH button located at the bottom of the sidebar
    """)
else:
    st.write(result)

# _________________________________________
# Multiselector for partners
# _________________________________________

### INFORMATION BY PARTNER
#FILTER SelectBox por partner
df = df_filtered

st.header('SELECT R2R PARTNER')

partner = st.selectbox(
    "SELECT R2R PARTNER FROM SELECTION: 🔎 ",
    options=df['Initiative_name'].unique())
df_select = df.query('Initiative_name == @partner')


# ____________________________________
# key variables to diplay
# ____________________________________

#reeplacing blank to no info on specific variables 
df_select['q14'] = df_select['q14'].fillna("Not yet available")  #description
df_select['q13'] = df_select['q13'].fillna("Not yet available")  #admition date
df_select['q19'] = df_select['q19'].fillna("Citi not yet available")  #city HC
df_select['q22'] = df_select['q22'].fillna("Country not yet available")  #Countru HC
df_select['q25'] = df_select['q25'].fillna("Not yet available")  #website
df_select['q26'] = df_select['q26'].fillna("0")  #website
df_select['Short name'] = df_select['Short name'].str.upper()


#Key variables SELECTION
s_total_individuals = df_select['g19'] #Individuals
s_number_members = df_select['q26'] #Members
# s_num_countries = df_select['q959'] #Countries ##Check from frecuencies
s_num_companies = df_select['g433']  #COMPANIES
s_num_natural_system = df_select['g2116'] #Natural SYSTEM Indicate the estimated number of hectares your initiative aims to benefit
s_num_cities = df_select['g1675']  #Cities
s_num_regions = df_select['g1268']  #REGIONS


# ____________________________________
# RESULT
# ____________________________________
#Decription of partner by filter

p_short_name = df_select['Short name'].values[0]
p_full_name = df_select['Initiative_name'].values[0]

p_description = df_select['q14'].values[0]
st.header((p_full_name + " - " + p_short_name).upper())

st.markdown(p_short_name+ " - "+p_description)
p_admition_date = df_select['q13'].values[0]

col1, col2 = st.columns(2)
col1.markdown("Admission Date: "+p_admition_date)
p_office_city = df_select['q19'].values[0]
p_office_country = df_select['q22'].values[0]
p_web = df_select['q25'].values[0]
col1.markdown("Location of the headquarters: "+p_office_city+", "+p_office_country)
col1.markdown("Initiative's website: "+p_web)
col2.metric("Number of Members declared", int(s_number_members.sum()))


# _________________________
# Mapping specific Partners Global Reach
# _________________________
st.header("MAPPING "+p_short_name+" GLOBAL REACH")

tab1, tab2, tab3 = st.tabs(["World Map", "Treemap", "Sunburst Graph"])
   
#________
#SAMPLE SIZE
# _____

#Sample size from selection.
df2_sz = df_select['All_Countries'].replace(['; ; ; ; ; '], np.nan).dropna()
sz = str(df2_sz.count())

#dataframe to workwith (All data from the selection).
df2 = df_select['All_Countries'].str.split(";", expand=True).apply(lambda x: x.str.strip())
df2 = df2.stack().value_counts()
df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')  #Check what happend whit blank information.
df2.rename(columns = {'index':'Country'}, inplace = True)
df2['% country'] = ((df2['Frecuency']/df2['Frecuency'].sum())*100)

#Making dataset 
@st.cache_data
def get_country_data():
    df_country = pd.read_csv('countries_geoinfo.csv',sep=';')
    return df_country
df_country = get_country_data()  
df2 = pd.merge(df2, df_country, on='Country', how='left')
df2 = df2.dropna()















# _________________
# #GETTING NUMBERS OF VALUES the n° of countries, hazards, location 
# _________________
n_countries = df2['Country'].count()
n_countries_str = str(n_countries)





# _________________
#Getting Values from dataset to provide descriptions of maps
# _____________________

# ______  
# gettin the top 3 countries
# ___
s_df2 = df2.sort_values(by=['Frecuency'],ascending=False)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3['Country'].unique()
list_best3 =  ', '.join(list_best3)

#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end

#getting a string with the first three priority groups.
list_best3 = replace_last(list_best3, ',', ' & ')

# ________
# gettion the top 5 of countries top
# ______
num_countries = len(df2['Frecuency'])
#top5_percent = int(np.ceil(num_countries * 0.1))
#s_df2_best3 = s_df2.head(top5_percent)
s_df2_best3 = s_df2.head(5)
list_best3 = s_df2_best3['Country'].unique()
list_best3 =  ', '.join(list_best3)

#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end

#getting a string with the first three priority groups.
list_best_5_per = replace_last(list_best3, ',', ' & ')

# ___________________
# gettin the best 3 continents and lowest 2
# ________________

# sum of % country in 'mayor_area' and creating a new df
df3 = df2.groupby(['mayor_area']).agg({'% country': 'sum'})
df3 = df3.reset_index()
df3.rename(columns={'% country': '% Mayor Area'}, inplace=True)

df2 = pd.merge(df2, df3, on='mayor_area', how='left')
df2 = df2.dropna()

s_df2 = df3.sort_values(by='% Mayor Area', ascending=False)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3['mayor_area'].unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three priority groups.
list_best3_conti = replace_last(list_best3, ',', ' & ')

# _________________________
# #making a list of the two less presnce in 'mayor_area'
s_df2 = df3.sort_values(by='% Mayor Area', ascending=True)
s_df2_best3 = s_df2.head(2)
list_best3 = s_df2_best3['mayor_area'].unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three priority groups.
list_less_2_conti = replace_last(list_best3, ',', ' & ')

# # ___________________
# # gettin the best 3 Regions and lowest 2 regions
# # ________________

# sum of % country in 'Region' and creating a new df
df3 = df2.groupby(['Region']).agg({'% country': 'sum'})
df3 = df3.reset_index()
df3.rename(columns={'% country': '% Region'}, inplace=True)
s_df2 = df3.sort_values(by='% Region', ascending=False)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3['Region'].unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three priority groups.
list_best3_region = replace_last(list_best3, ',', ' & ')

# _________________________
# #making a list of the three less presence in 'region'
s_df2 = df3.sort_values(by='% Region', ascending=True)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3['Region'].unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three priority groups.
list_less_2_region = replace_last(list_best3, ',', ' & ')

# st.write(df2)

#___________________________________________
# WORLD MAP    #https://github.com/jefftune/pycountry-convert/tree/master/pycountry_convert
##https://realpython.com/python-folium-web-maps-from-data/
#___________________________________________

@st.cache_data
def load_countries():
    political_countries_url = "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    return political_countries_url

political_countries_url = load_countries()

world_map = folium.Map(location=(0, 0), zoom_start=1, tiles="cartodb positron") 

# worldmap_partner_name = p_short_name+" - % of countries with resilience actions pledged"
worldmap_partner_name_str = str(p_short_name+" - % of countries with resilience actions pledged")

folium.Choropleth(
    geo_data=political_countries_url,
    data=df2,
    columns=["Country", "% country"],
    key_on="feature.properties.name",
    fill_color="RdPu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=worldmap_partner_name_str,
    highlight=True,
    name="% of Country",
    tooltip=folium.features.GeoJsonTooltip(
        fields=["name", "% country"],
        aliases=["Country", "% of Country"],
        labels=True,
        sticky=False,
        localize=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """
    )
).add_to(world_map)

folium.LayerControl().add_to(world_map)

with tab1:
    if n_countries == 0:
        st.write("At this time "+p_short_name+" has not provided any information on specific countries. However, we will update this page with any new information as it becomes available.")
    else:
        st.markdown(p_short_name+" has provided information on **"+n_countries_str+"** countries where they have pledged to take resilience action.")
        st_folium(world_map,width=725, returned_objects=[])
        st.text('Source: R2R Pledge Attributes Survey')
        # st.write(df2)
        with st.expander("Navigating this worldmap: A User's Guide"):
            st.write("""
    To navigate the map, you can zoom in or out using the zoom control on the top left corner of the map.

    The legend on the top right corner of the map shows the color scale used to represent the percentage values, ranging from light purple (low percentage) to dark purple (high percentage).

    The layer control on the top right corner allows you to toggle the display of the percentage values on or off.
    """)
if n_countries == 0:
        st.write("")
else:
    st.markdown("**Note:** The top 5 of countries with the highest presence of "+p_short_name+" actions pledged are "+list_best_5_per+". ")
    st.markdown("By continent, "+p_short_name+" actions pledged are most prevalent in "+list_best3_conti+".")
    st.markdown("Looking at regions, the graph above shows that "+p_short_name+"' actions pledged are most prominent in "+list_best3_region+".")
#___________________________________________
# TREEMAP
#___________________________________________
    fig_treemap = px.treemap(df2, path=[px.Constant("World"),'mayor_area','Region','cn_code'], values = '% country', color='% Mayor Area', color_continuous_scale='RdPu')
    fig_treemap.update_traces(root_color="#FF37D5")
    fig_treemap.update_layout(title_text=p_short_name+' - Resilience Action Pledged by Country, Region, and Continent')
    fig_treemap.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig_treemap.add_annotation(x=1, y=0,
			text='Source: R2R Pledge Attributes Survey.',showarrow=False,
			yshift=-20)
    fig_treemap.data[0].hovertemplate = '%{value:.1f}%'

with tab2:
    if n_countries == 0:
        st.write("At this time "+p_short_name+" has not provided any information on specific countries. However, we will update this page with any new information as it becomes available.")
    else:
        st.markdown(p_short_name+" has provided information on **"+n_countries_str+"** countries where they have pledged to take resilience action.")
        st.plotly_chart(fig_treemap)
        with st.expander("Navigating this treemap: A User's Guide"):
            st.write("""
        The **treemap** is a data visualization that *demonstrates hierarchical relationships using nested rectangles*. Each rectangle represents a category, and its size corresponds to a value or proportion of the data. In this particular treemap, the data is organized by continents, regions, and countries.

        At the highest level of the treemap, there is a rectangle representing the entire world, labeled as "World." Below this rectangle, there are several smaller rectangles that represent the different continents of the world, such as Africa, Europe, and Asia.

        Each continent rectangle is further divided into smaller rectangles that represent regions within the continent, such as Central Africa or Western Europe. Finally, each region rectangle is subdivided into even smaller rectangles that represent individual countries with their respective country codes.

        In this treemap, the size of each rectangle represents the frequency of a certain country where partners declare pledges to take resilience action. By using this visualization, one can easily compare the frequency of these pledges across different countries, regions, and continents. This helps to identify patterns and trends in the data, which can inform decision-making and planning for resilience actions.

        Also, this treemap *support interactivity* by allowing users to click on a rectangle and zoom in to see nested categories. For example, if you click on a rectangle representing a continent, you might see rectangles representing individual countries within that continent. By clicking on a rectangle representing a country, you might see rectangles representing subregions within that country.

        This interactivity makes it easier for users to explore and understand hierarchical relationships within the data. It allows users to zoom in and out of the treemap and view the data from different perspectives. Additionally, users can hover over each rectangle to see more detailed information about the category and its associated data value.

            """)

#___________________________________________
# SUNBURST
#___________________________________________
if n_countries == 0:
        st.write("")
else:
	fig_sunburst = px.sunburst(data_frame = df2,path = ['mayor_area','Region', 'Country'],values = '% country')
	fig_sunburst.update_layout(title_text=p_short_name+' - Resilience Action Pledged by Country, Region, and Continent')
	fig_sunburst.update_layout(margin = dict(t=50, l=25, r=25, b=25))
	fig_sunburst.add_annotation(x=1, y=0,
			text='Out of '+ sz +' R2R Partners (Source: R2R Pledge Statement Survey).',showarrow=False,
			yshift=-20)
	fig_sunburst.data[0].hovertemplate = '%{value:.1f}%'

with tab3:
    if n_countries == 0:
        st.write("At this time "+p_short_name+" has not provided any information on specific countries. However, we will update this page with any new information as it becomes available.")
    else:
        st.markdown(p_short_name+" has provided information on **"+n_countries_str+"** countries where they have pledged to take resilience action.")    
        st.plotly_chart(fig_sunburst)
        with st.expander("Navigating this sunburst graph: A User's Guide"):
            	st.write("""
        	A sunburst graph is a type of data visualization that represents hierarchical data in a circular format. The outermost circle represents the highest level of the hierarchy, with each subsequent level represented by a smaller circle inside the previous one. The size of each segment in the sunburst corresponds to a specific category within the hierarchy, and its proportion of the overall data.

       		In this sunburst graph, the data is organized by continents, regions, and countries, and the size of each segment represents the frequency of countries where R2R Partners declare pledges to take resilience action.

       		To navigate the sunburst graph, simply click on a specific segment to zoom in and see more detailed information about the categories within it. For example, if you click on a segment representing a continent, you will zoom in to see the segments representing the regions within that continent. Similarly, if you click on a segment representing a region, you will zoom in to see the segments representing the countries within that region.

        	The interactivity features of the sunburst graph also allow you to hover over each segment to see more detailed information about the category it represents, such as its name, value, and percentage of the overall data. This helps you to quickly identify patterns and trends within the data and gain insights that might not be immediately apparent from a static graph.

           	""")
    

# _________________________
# Hazards and geographical impact focus
# _________________________
st.header(p_short_name+" - HAZARDS AND GEOGRAPHICAL IMPACT FOCUS")

tab1, tab2 = st.tabs(["Hazards", "Human Settlement and Location"])


#_________________________________________________________________________________________________________________________________
# HAZARDS  PLEDGES
#_________________________________________________________________________________________________________________________________

#Sample size hazards from selection.
df2_sz = df_select['All_Hazards'].replace(['; ; ; ; ; '], np.nan).dropna()
sz = str(df2_sz.count())
#dataframe to workwith (All data from the selection).
df2 = df_select['All_Hazards'].str.split(";", expand=True).apply(lambda x: x.str.strip())
df2 = df2.stack().value_counts()
df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')  #Check what happend whit blank information.

n_hazards = df2['Frecuency'].count()
n_hazards_str = str(n_hazards)

#st.write(n_hazards)

#creating new columms based in a dictionary
heat_list     = {'Heat stress - lives & livelihoods combined':'Heat','Heat stress - livelihoods (work)':'Heat','Heat stress - lives':'Heat','Extreme heat':'Heat'}
cold_list     = {'Extreme cold':'Cold','Snow and ice':'Cold'}
drought_list  = {'Drought (agriculture focus)':'Drought','Drought (other sectors)':'Drought'}
water_list    = {'Water stress (urban focus)':'Water','Water stress (rural focus)':'Water'}
fire_list     = {'Fire weather (risk of wildfires)':'Fire'}
flooding_list = {'Urban flooding':'Flooding','Riverine flooding':'Flooding','Coastal flooding':'Flooding'}
coastal_list  = {'Other coastal events':'Coastal / Ocean','Oceanic events':'Coastal / Ocean'}
wind_list     = {'Hurricanes/cyclones':'Wind','Extreme wind':'Wind'}
hazard_dictionary = {**heat_list,**cold_list,**drought_list,**water_list,**fire_list,**flooding_list,**coastal_list,**wind_list}
df2['group'] = df2['index'].map(hazard_dictionary)
df2['% hazard']=((df2['Frecuency']/df2['Frecuency'].sum())*100)

# sum of % country in 'mayor_area' and creating a new df
df3 = df2.groupby(['group']).agg({'Frecuency': 'sum'})
df3 = df3.reset_index()
df3.rename(columns={'Frecuency': 'Sum_frec_group'}, inplace=True)
df3['% Hazards']=((df3['Sum_frec_group']/df3['Sum_frec_group'].sum())*100)
# st.write(df3)

df2 = pd.merge(df2, df3, on='group', how='left')
df2 = df2.dropna()

if n_hazards == 0:
   st.write("")
else:
   fig_h = px.treemap(df2, path=[px.Constant("Hazards"),'group','index'], values='% hazard', color='% Hazards', color_continuous_scale='RdPu')
   fig_h.update_traces(root_color='#FF37D5')
   fig_h.update_layout(title=p_short_name+' - Hazard Mitigation Efforts Pledged.', font=dict(size=16))
   fig_h.update_layout(margin=dict(t=50, l=25, r=25, b=25))
   fig_h.add_annotation(x=1, y=0,
			text='Source: R2R Pledge Attributes Survey',
			showarrow=False,
			yshift=-20)
   fig_h.data[0].hovertemplate = '%{value:.1f}%'

s_df2 = df3.sort_values(by='% Hazards', ascending=False)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3['group'].unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three hazards
list_best3_hazards = replace_last(list_best3, ',', ' & ')

# _________________________
# #making a list of the two less presnce in hazards
s_df2 = df3.sort_values(by='% Hazards', ascending=True)
s_df2_best3 = s_df2.head(2)
list_best3 = s_df2_best3['group'].unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the hazards
list_less_2_hazards = replace_last(list_best3, ',', ' & ')

with tab1:
    if n_countries == 0:
        st.write("At this time "+p_short_name+" has not provided any information on Hazards. However, we will update this page with any new information as it becomes available.")
    else:
        st.plotly_chart(fig_h)
        with st.expander("Navigating this treemap: A User's Guide"):
	    st.write("""This chart displays the percentage of hazard mitigation efforts that R2R Partner have pledged to provide. The chart is structured as a treemap, with the main category of "Hazards" displayed at the top. Underneath that, you can see the different groups of climate hazards, such as heat, flooding, drought, fire, and cold. Finally, each individual hazard is displayed, such as extreme heat or flooding caused by heavy rainfall.

            The size of each box in the treemap represents the percentage of hazard mitigation efforts pledged for that particular hazard. The color of the boxes represents the percentage of total hazard mitigation efforts pledged by R2R Partners within that hazard group. The darker the color, the higher the percentage of total mitigation efforts pledged for that group.

            To view more information about each box, simply hover your mouse over it. The tooltip will display the name of the hazard and the percentage of hazard mitigation efforts pledged for that particular hazard. The total number of R2R Partners reporting information related to hazards is displayed in the annotation at the bottom of the chart.
            """)
        st.markdown('**Note:** '+list_best3_hazards+" are the hazard groups where "+p_short_name+" aim to provide resilience the most.")



#__________________________________________________________________________________________________________________________________________________________________
# SCATTER PLOT INLAND. RURAL - All Engagement Scope
#__________________________________________________________________________________________________________________________________________________________________
#
#Data preparation
df2 = df_select
costal_list = {'g30','g458','g865','g1272','g1679','g2093'}
rural_list  = {'g31','g459','g866','g1273','g1680','g2094'}  #<--- making a filter here, Make it dynamic. 
df2_costal  = df2[costal_list]
df2_rural   = df2[rural_list ]
df2['costal_average'] = df2_costal.mean(axis=1,numeric_only=True,skipna=True)
df2['rural_average'] = df2_rural.mean(axis=1,numeric_only=True,skipna=True)
df2 = df2[df2['costal_average'].notna()]
df2 = df2[df2['rural_average'].notna()]
df2.rename(columns = {'costal_average':'C', 'rural_average':'R', 'Short name':'Name'}, inplace = True)

#counting values in case there is no info. 
n_costal = df2['C'].count()
n_costal_str = str(n_costal)
n_rural = df2['R'].count()
n_rural_str = str(n_rural)
sum_costal_rural = n_costal+n_rural

#creating the chart

x = df2['C']
y = df2['R']
z = df2['Name']

fig = plt.figure(figsize=(8, 8))

for i in range(len(df2)):
    plt.scatter(x,y,c='#FF37D5', marker='o')

#plt.title("Individuals' environment ""[%]""",fontsize=14)
plt.xlabel('Inland'+' '*74+'Coastal',fontsize=13)
plt.ylabel('Urban'+' '*49+'Rural',fontsize=13)
plt.gca().spines['top']  .set_visible(False)
plt.gca().spines['right'].set_visible(False)

for i in range(len(df2)):
     plt.text(df2.C[df2.Name ==z[i]],df2.R[df2.Name==z[i]],z[i], fontdict=dict(color='black', alpha=0.5, size=12))
# Add plot title
plt.title(p_short_name+' - Location of Coastal/Inland and Urban/Rural Populations Targeted', fontsize=16, pad=20, color='#112E4D')  # add pad parameter


plt.xlim([0, 100])
plt.ylim([0, 100])    

with tab2:
    if sum_costal_rural == 0:
        st.write("At this time "+p_short_name+" has not provided any information on Coastal/Inland and Urban/Rural Populations Targeted. However, we will update this page with any new information as it becomes available.")
    else:
        col1, col2, col3 = st.columns((2.0,0.6,0.4))
        col1.pyplot(fig)
        st.markdown("**Note**: The chart shows the location of populations that are targeted by "+p_short_name+" based on whether they are located in coastal or inland areas and whether they are urban or rural. The chart is divided into four quadrants based on these two dimensions, with the x-axis representing inland/coastal and the y-axis representing urban/rural.")




# _________________________
# More about R2R Target Beneficiares
# _________________________
st.header(p_short_name+" - TARGET BENEFICIARES")

tab1, tab2, tab3 = st.tabs(["Priority Groups", "Companies Sector", "Natural Systems"])

#__________________________________________________________________________________________________________________________________________________________________
# PRIORITY GROUPS PLEDGE
#__________________________________________________________________________________________________________________________________________________________________
#
#Sample size hazards from selection.
df2_sz = df_select['Priority group'].replace(['; ; ; ; ; '], np.nan).dropna()
sz = str(df2_sz.count())
#dataframe to workwith (All data from the selection).
df2 = df_select
list = {'g20','g21','g22','g23','g24','g25','g26','g27','g28'} #making a list with all the columns name use in the graph
df2= df2[df2[list].notna()] #cleaning na
pg0 = df2["g20"].mean() #Women and girls
pg1 = df2["g21"].mean() #LGBTQIA+
pg2 = df2["g22"].mean() #Elderly
pg3 = df2["g23"].mean() #Children and Youth
pg4 = df2["g24"].mean() #Disabled
pg5 = df2["g25"].mean() #Indigenous or traditional communities
pg6 = df2["g26"].mean() #Racial, ethnic and/or religious minorities
pg7 = df2["g27"].mean() #Refugees
pg8 = df2["g28"].mean() #Low income communities

s_df2 = pd.DataFrame(dict(
    r=[pg0, pg1, pg2, pg3, pg4, pg5, pg6, pg7, pg8],
    theta=['Women and girls','LGBTQIA+','Elderly','Children and Youth','Disabled','Indigenous or traditional communities','Racial, ethnic and/or religious minorities','Refugees','Low income communities']))
s_fig_ra_general = px.line_polar(s_df2, r='r', theta='theta', line_close=True, title=p_short_name+" - Targeted Priority Groups")
s_fig_ra_general.update_traces(line_color='#FF37D5', line_width=1)
s_fig_ra_general.update_traces(fill='toself')
# s_fig_ra_general.add_annotation(x=1, y=0,
#             text='Out of '+ sz +' R2R Partners reporting pledges about the Priority Groups',showarrow=False,
#             yshift=-60)

n_priority_groups = s_df2['theta'].count()

#making a list of the three most important priority groups.
s_df2 = s_df2.sort_values(by=['r'],ascending=False)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3.theta.unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three priority groups.
list_best3 = replace_last(list_best3, ',', ' & ')
#making a list of the three last important priority groups.
s_df2_last3 = s_df2.tail(3)
s_df2_last3 = s_df2_last3.sort_values(by=['r'])
list_last3 = s_df2_last3.theta.unique()
list_last3 =  ', '.join(list_last3)
list_last3 = replace_last(list_last3, ',', ' & ')

with tab1:
    if n_priority_groups == 0:
        st.write("At this time "+p_short_name+" has not provided any information on targeted priority groups. However, we will update this page with any new information as it becomes available.")
    else:
        st.write(s_fig_ra_general)
        with st.expander("Description of graph polar line. A User's Guide"):
            st.write("""
            A polar line chart is a type of chart that is used to display data that is circular in nature, such as directional or angular data. 
            In this type of chart, data is plotted on a radial axis that extends from the center of the chart to its outer edge. The radial axis is divided into segments that are spaced evenly around the chart, similar to the markings on a clock face.
            This chart here that displays lines connecting data points on the radial axis. Each line in the chart represents a priority group targeted by R2R Partners, and the length of the line represents the level of priority placed on that group.
            The priority groups are listed on the circumference of the chart, and their associated lines connect to the appropriate point on the radial axis. By doing so, the chart enables users to easily compare the priority levels of different groups and visualize their relative importance.
            """)
        st.markdown("**Note**: "+p_short_name+" has identified "+ list_best3 + " as its highest priority groups. However, there is room for improvement in their efforts to address the needs of the "+list_last3 +", which present an opportunity for enhancement.")
            


#__________________________________________________________________________________________________________________________________________________________________
# COMPANIES TYPE
#__________________________________________________________________________________________________________________________________________________________________
#
# st.subheader('Sector of companies that are members of R2R Partners')

df2 = df_select['Companies Types'].str.split(";", expand=True).apply(lambda x: x.str.strip())
df2 = df2.stack().value_counts()
df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')
df2['Percentaje'] = ((df2['Frecuency']/df2['Frecuency'].sum())*100).round(2)

companies_type_rename_list = {'A. Agriculture, forestry and fishing':'Agriculture, forestry and fishing','B. Mining and quarrying':'Mining and quarrying','C. Manufacturing':'Manufacturing','D. Electricity, gas, steam and air conditioning supply':'Electricity, gas, steam and air conditioning supply','E. Water supply; sewerage, waste management and remediation activities':'Water supply; sewerage, waste management and remediation activities','F. Construction':'Construction','G. Wholesale and retail trade; repair of motor vehicles and motorcycles':'Wholesale and retail trade; repair of motor vehicles and motorcycles','H. Transportation and storage':'Transportation and storage','I. Accommodation and food service activities':'Accommodation and food service activities','J. Information and communication':'Information and communication','K. Financial and insurance activities':'Financial and insurance activities','L. Real estate activities':'Real estate activities','M. Professional, scientific and technical activities':'Professional, scientific and technical activities','N. Administrative and support service activities':'Administrative and support service activities','O. Public administration and defence; compulsory social security':'Public administration and defence; compulsory social security','P. Education':'Education','Q. Human health and social work activities':'Human health and social work activities','R. Arts, entertainment and recreation':'Arts, entertainment and recreation','S. Other service activities':'Other service activities','T. Activities of households as employers; undifferentiated goods- and services-producing activities of households for own use':'Activities of households as employers; undifferentiated goods- and services-producing activities of households for own use','U. Activities of extraterritorial organizations and bodies':'Activities of extraterritorial organizations and bodies'}
df2['index'] = df2['index'].replace(companies_type_rename_list)
df2 = df2.sort_values(by=['Percentaje'], ascending=False)

n_companies = df2['index'].count()

if n_companies ==0:
    st.markdown('')
else:
    fig, ax = plt.subplots()
    ax = sns.barplot(x="Frecuency", y="index", data=df2, label=p_short_name+" - Types of Companies", color="#FF37D5")
    ax.bar_label(ax.containers[0], labels=[f"{val:.0f}" for val in df2['Frecuency']])
    ax.set(ylabel=None)
    plt.title(p_short_name+' - Types of companies as members', fontsize=13, loc='left')
    plt.subplots_adjust(bottom=0.2) # adjust bottom margin to make space for the text
    # fig.text(0.5, 0.05, "Out of 8 R2R Partners reporting information about companies", ha="left", fontsize=8) #check out !! 

with tab2:
    if n_companies == 0:
        st.write("At this time "+p_short_name+" has not provided any information on companies. However, we will update this page with any new information as it becomes available.")
    else:
        st.pyplot(fig)
        with st.expander("Description of this bar chart"):
            st.write("""This bar chart is used to display the results of a multi-response question, which is a question that allows respondents to select more than one answer option.
To create a bar chart from the results of a multi-response question, the selected answer options are tallied to determine the frequency or percentage of respondents who selected each option. The tallied results are here plotted on the y-axis of the chart, while the answer options are displayed on the x-axis.
Each rectangular bar on the chart represents one answer option and its length represents the frequency or percentage of respondents who selected that option. 
""")



# __________________________________________________________________________________________________________________________________________________________________
# # Natural Systems
#__________________________________________________________________________________________________________________________________________________________________

# st.subheader('Types of natural systems where R2R Partners hope to have an impact')
#Sample size companies  from selection. 
# df2_sz = df['Natural Systems Types'].replace(['; ; ; ; ; '], np.nan).dropna()  #not working
# st.write(df2_sz)
# sz = str(df2_sz.count()) #not working

df2 = df_select['Natural Systems Types'].str.split(";", expand=True).apply(lambda x: x.str.strip())
df2 = df2.stack().value_counts()
df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')
df2['Percentaje'] = ((df2['Frecuency']/df2['Frecuency'].sum())*100).round(1)
df2 = df2.sort_values(by=['Percentaje'], ascending=False)

nat_sys_dict ={'T Terrestrial':'Terrestrial','S Subterranean':'Subterranean','SF Subterranean-Freshwater':'Subterranean-Freshwater','SM Subterranean-Marine':'Subterranean-Marine','FT Freshwater-Terrestrial':'Freshwater-Terrestrial','F Freshwater':'Freshwater','FM Freshwater-Marine':'Freshwater-Marine','M Marine':'Marine','MT Marine-Terrestrial':'Marine-Terrestrial','MFT Marine-Freshwater-Terrestrial':'Marine-Freshwater-Terrestrial'}
df2['index'] = df2['index'].replace(nat_sys_dict)


n_nat_syst = df2['index'].count()

if n_nat_syst ==0:
    st.markdown('')
else:
    fig, ax = plt.subplots()
    ax = sns.barplot(x="Frecuency", y="index", data=df2, label="Types of Natural Systems", color="#FF37D5")
    ax.bar_label(ax.containers[0], labels=[f"{val:.0f}" for val in df2['Frecuency']])
    ax.set(ylabel=None)
    plt.title(p_short_name+' - Types of Natural Systems pledged to have an impact', fontsize=10, loc='left')
    plt.subplots_adjust(bottom=0.2) # adjust bottom margin to make space for the text
    # fig.text(0.5, 0.05, "Out of 6 R2R Partners reporting information about Natural Systems", ha="left", fontsize=8) #check out !! 

with tab3:
    if n_nat_syst == 0:
        st.write("At this time "+p_short_name+" has not provided this information on Natural Systems. However, we will update this page with any new information as it becomes available.")
    else:
        col1, col2, col3 = st.columns((2.0,0.6,0.4))
        col1.pyplot(fig)
        with st.expander("Description of this bar chart"):
            st.write("""This bar chart is used to display the results of a multi-response question, which is a question that allows respondents to select more than one answer option.
    To create a bar chart from the results of a multi-response question, the selected answer options are tallied to determine the frequency or percentage of respondents who selected each option. The tallied results are here plotted on the y-axis of the chart, while the answer options are displayed on the x-axis.
    Each rectangular bar on the chart represents one answer option and its length represents the frequency or percentage of respondents who selected that option. 
    """)















# ____________________________________________________________________________________________________________________________________________________
# QUALITATIVE 
# ____________________________________________________________________________________________________________________________________________________


# #________________________________________________________________________________________________________________________________
# WORDCLOUD
#________________________________________________________________________________________________________________________________
#
st.header('HOW R2R '+p_short_name+' DESCRIBE THE INITIATIVE, ITS MAIN GOALS, AND HOW THEY EXPECT TO BUILD RESILIENCE?')

n_description = df_select['q14'].count()

if n_description == 0:
    st.write('')
else:
    text = ' '.join(df_select['q14'])
    st.set_option('deprecation.showPyplotGlobalUse', False)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640, colormap="RdPu").generate(text)


    # Create a new figure and add a title
    fig, ax = plt.subplots()
    ax.set_title(p_short_name+'- SELF-DESCRIPTION', fontsize=11, fontweight='light',color="#112E4D")
    ax.title.set_position([.5, 1.05]) # Adjust the position of the title

    # Display the wordcloud on the new figure
    ax.imshow(wordcloud)
    ax.set_xticks([])
    ax.set_yticks([])

# Display the figure with Streamlit

if n_description == 0:
    st.write("At this time "+p_short_name+" has not provided this information. However, we will update this page with any new information as it becomes available.")
else:
    col1, col2, col3 = st.columns((1.8,0.6,0.6))
    col1.pyplot(fig)
    tab1_1, tab2_2 = st.tabs(["Full Answer", "Description of Worldcloud"])
    with tab1_1:
        st.markdown(p_short_name+ ' answer to "Please briefly describe in general terms your initiative, its main goals, and how it expects to build resilience?:')
        st.caption('')
        st.markdown(df_select['q14'].values[0])
    with tab2_2:
        st.markdown("""
        A wordcloud is a graphical representation of text data, in which the size of each word is proportional to its frequency or importance in the data. In other words, the more often a word appears in the text, the larger and bolder it appears in the wordcloud. 
        
        Wordclouds are often used to visualize the most frequently occurring words in a text dataset, providing a quick and easy way to identify the most common themes or topics within the data.
        
        In the context of the R2R Partners Self-Description, the wordcloud is a visual representation of the words used most frequently by R2R Partners to describe their initiative, goals, and strategies for building resilience. This allows viewers to quickly get a sense of the most important themes and ideas related to R2R Partners' work, without having to read through large amounts of text.
        """)


# _________________________
# RA 
# _________________________

st.header(p_short_name+ "- RESILIENCE ATTRIBUTES AND SUB-CATEGORIES")
with st.expander("Summary of 7 Resilience Attributes & 19 Subcategories"):
    st.write("""
    Depth of Resilience imply qualitative metrics to understand how partners and their members contribute to increasing the resilience of people vulnerable to climate change by observing which key conditions (seven Resilience Attributes) are impacted. 

Resilience attributes act as an intermediary between the outcome of actions and increased resilience. The scientific literature acknowledges those Resilience Attributes to foster resilience or empower resilience-driving transformations. These seven Resilience Attributes cover most of the aspects of resilience building for the initiatives across the three constituting dimensions of resilience (plan, cope and learn). They are operationalized through 19 subcategories that address different aspects of the definitions of their correspondent Resilience Attribute.
""")
    st.image("Resilience_Atributes_Summary.png")
    st.caption('Source: R2R’s Metrics Framework (2022)')
        

tab1, tab2, tab3= st.tabs(["Resilience Attributes", "Subcategories","Conceptual Guide"])
#_______________________________________________________________________
#RESILIENCE ATTRIBUTES
#_________________________________________________________________________

## RADIAL CHART
##RESILIENCE ATTRIBUTES CHART

ra_likert_var_list = [  'Equity_&_Inclusivity','Preparedness_and_planning',
                        'Learning','Agency','Social_Collaboration','Flexibility','Assets'] #making a list with all the columns name use in the graph

#Sample size RA
df2_sz = df_select[ra_likert_var_list].dropna()
sz = str(df2_sz.count().values[0])

#dataframe to workwith (All data from the selection).
df2 = df_select
df2= df2[df2[ra_likert_var_list].notna()] #cleaning na

Equity_y_Inclusivity        = df2['Equity_&_Inclusivity'].mean() 
Preparedness_and_planning   = df2['Preparedness_and_planning'].mean() 
Learning                    = df2['Learning'].mean() 
Agency                      = df2['Agency'].mean() 
Social_Collaboration        = df2['Social_Collaboration'].mean() 
Flexibility                 = df2['Flexibility'].mean() 
Assets                      = df2['Assets'].mean() 

s_df2 = pd.DataFrame(dict(
    r=[Equity_y_Inclusivity,Preparedness_and_planning,Learning,Agency,Social_Collaboration,Flexibility,Assets],
    theta=['Equity and Inclusivity','Preparedness and planning',
                        'Learning','Agency','Social Collaboration','Flexibility','Assets']))
s_fig_ra_general = px.line_polar(s_df2, r='r', theta='theta', line_close=True, title=p_short_name+" - RESILIENCE ATTRIBUTES ")
s_fig_ra_general.update_traces(line_color='#FF37D5', line_width=1)
s_fig_ra_general.update_traces(fill='toself')
# s_fig_ra_general.add_annotation(x=1, y=0,
#             text='Out of '+ sz +' Partners reporting information about resilience attributes',showarrow=False,
#             yshift=-60)

#making a list of the three most important ra.
s_df2 = s_df2.sort_values(by=['r'],ascending=False)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3.theta.unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three ra.
list_best3 = replace_last(list_best3, ',', ' & ')
#making a list of the three last important ra.
s_df2_last3 = s_df2.tail(3)
s_df2_last3 = s_df2_last3.sort_values(by=['r'])
list_last3 = s_df2_last3.theta.unique()
list_last3 =  ', '.join(list_last3)
list_last3 = replace_last(list_last3, ',', ' & ')

with tab1:
    st.subheader("ASSESSING RESILIENCE ATTRIBUTES: AN OVERVIEW OF "+p_short_name+" REPORTS")
    st.write(s_fig_ra_general)
    st.markdown("**Note:** "+list_best3 + " are top "+p_short_name+" Resilience Attributes.")
    st.markdown( list_last3 + " represent Resilience Attributes for enhancement.")
    with st.expander("Description of graph polar line: Resilience Attributes"):
        st.markdown("""
        This is a polar line chart that shows the different Resilience Attributes that were reported by """+p_short_name+""". 
        
        The chart has seven different attributes, which are plotted on the vertical axis, and include Equity and Inclusivity, Preparedness and planning, Learning, Agency, Social Collaboration, Flexibility, and Assets. Each attribute is represented by a line that connects data points on the chart, and the size of the line represents the strength of the attribute. 
        
        The chart is designed to help the user understand the relative strength of each attribute and how they contribute to overall resilience.
        """)

#____
##SUB CATEGORIES - RESILIENCE ATTRIBUTES CHART
#_____
sub_ra_likert_var_list = [  'Equity','Inclusivity',	'Preparedness',
	                        'Planning',	'Experiential_learning','Educational_learning',
    	                    'Autonomy',	'Leadership',	'Decision_making',	'Collective_participation',
        	                'Connectivity',	'Networking',	'Diversity',	'Redundancy',	'Finance',
            	            'Natural_resources',	'Technologies',	'Infrastructure',	'Services']

#Sample size RA
df2_sz = df_select[sub_ra_likert_var_list].dropna()
sz = str(df2_sz.count().values[0])

#dataframe to workwith (All data from the selection).
df2 = df_select
df2= df2[df2[sub_ra_likert_var_list].notna()] #cleaning na


Equity = df2['Equity'].mean() 
Inclusivity = df2['Inclusivity'].mean() 
Preparedness = df2['Preparedness'].mean() 
Planning = df2['Planning'].mean() 
Experiential_learning = df2['Experiential_learning'].mean() 
Educational_learning = df2['Educational_learning'].mean() 
Autonomy = df2['Autonomy'].mean() 
Leadership = df2['Leadership'].mean() 
Decision_making = df2['Decision_making'].mean() 
Collective_participation = df2['Collective_participation'].mean() 
Connectivity = df2['Connectivity'].mean() 
Networking = df2['Networking'].mean() 
Diversity = df2['Diversity'].mean() 
Redundancy = df2['Redundancy'].mean() 
Finance = df2['Finance'].mean() 
Natural_resources = df2['Natural_resources'].mean() 
Technologies = df2['Technologies'].mean() 
Infrastructure = df2['Infrastructure'].mean() 
Services= df2['Services'].mean() 


s_df2 = pd.DataFrame(dict(
    r=[Equity,Inclusivity,Preparedness,Planning,Experiential_learning,Educational_learning,Autonomy,
Leadership,Decision_making,Collective_participation,Connectivity,Networking,
Diversity,Redundancy,Finance,Natural_resources,Technologies,Infrastructure,Services],
    theta=['Equity','Inclusivity',	'Preparedness',
	                        'Planning',	'Experiential_learning','Educational_learning',
    	                    'Autonomy',	'Leadership',	'Decision_making',	'Collective_participation',
        	                'Connectivity',	'Networking',	'Diversity',	'Redundancy',	'Finance',
            	            'Natural_resources',	'Technologies',	'Infrastructure',	'Services']))
s_fig_ra_general = px.line_polar(s_df2, r='r', theta='theta', line_close=True, title=p_short_name+" - RESILIENCE ATTRIBUTES SUB CATEGORIES")
s_fig_ra_general.update_traces(line_color='#FF37D5', line_width=1)
s_fig_ra_general.update_traces(fill='toself')
# s_fig_ra_general.add_annotation(x=1, y=0,
#             text='Out of '+ sz +' Partners reporting information about the Resilience Attributes- Sub Categoriess',showarrow=False,
#             yshift=-60)
# st.write(s_fig_ra_general)

#making a list of the three most important ra-subattribute
s_df2 = s_df2.sort_values(by=['r'],ascending=False)
s_df2_best3 = s_df2.head(3)
list_best3 = s_df2_best3.theta.unique()
list_best3 =  ', '.join(list_best3)
#making a function to change the last comma with "&"
def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end
#getting a string with the first three ra-subattribute
list_best3 = replace_last(list_best3, ',', ' & ')
#making a list of the three last important ra-subattribute
s_df2_last3 = s_df2.tail(3)
s_df2_last3 = s_df2_last3.sort_values(by=['r'])
list_last3 = s_df2_last3.theta.unique()
list_last3 =  ', '.join(list_last3)
list_last3 = replace_last(list_last3, ',', ' & ')


with tab2:
    st.subheader(p_short_name+' - ASSESSMENT OF RESILIENCE ATTRIBUTES 19 SUBCATEGORIES')
    st.write(s_fig_ra_general)
    st.markdown("**Note:** "+list_best3 + " are top Resilience Attributes Sub Categories. "+list_last3 +" represent Resilience Attributes Sub Categoriess for enhancement.")
    with st.expander("Description of graph polar line: Resilience Attributes"):
        st.markdown("""
        This chart is a polar line chart that visually represents the mean scores of 19 subcategories of resilience attributes. 
        
        Each subcategory is listed on the perimeter of the chart, and the mean scores are shown as a line connecting the points that correspond to each subcategory. The y-axis indicates the scale of the mean scores. Thus, this chart provides an overview of the performance of the resilience attributes subcategories, as well as aspects for future improvement and areas of opportunity.   
        """)

with tab3:
    # Display the figure with Streamlit
    col1, col2, col3 = st.columns((2.2,0.4,0.4))
    col1.image("RA_definitions.png")
    st.caption('Source: R2R’s Metrics Framework (2022)')

st.markdown("""---""")

st.markdown("SELECT ANOTHER R2R PARTNER FROM YOUR FILTER SELECTION [HERE](#select-r2r-partner)")










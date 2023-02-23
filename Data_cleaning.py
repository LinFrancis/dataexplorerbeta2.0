import streamlit as st
import pandas as pd
import numpy as np

#_________________________________________________________________________________________________________________________________________________________________
# Export data
#__________________________________________________________________________________________________________________________________________________________________

# _______________________
#General Information Survey
#__________________________
#getdata
df_gi = pd.read_csv('GI_27012013.csv',sep=';', header=None, prefix="q").iloc[2:]
df_gi.set_index("q0", inplace = True)
df_gi.index.names = ['Master ID']
df_gi = df_gi.dropna(how = 'all')
df_gi_names = pd.read_csv('GI_27012013.csv',sep=';').iloc[1:]
##rename
df_gi['q37'] = df_gi['q37'].replace(['Poor'], 'Low income communities')
df_gi['q50'] = df_gi['q50'].replace(['Finance'], 'Cross-cutting enablers: Planning and Finance')
df_gi['q51'] = df_gi['q51'].replace(['Food and agriculture system'], 'Food and Agriculture Systems')
df_gi['q52'] = df_gi['q52'].replace(['Ocean and coastal zone'], 'Coastal and Oceanic Systems')
df_gi['q53'] = df_gi['q53'].replace(['Water and land ecosystems'], 'Water and Nature Systems')
df_gi['q54'] = df_gi['q54'].replace(['Cities and human settlements'], 'Human Settlement Systems')
df_gi['q55'] = df_gi['q55'].replace(['Infrastructure and services'], 'Infrastructure Systems')
df_gi.rename(columns = { 'q1':'Initiative_name', 'q2':'Short name'}, inplace = True)
##To numeric
df_gi["q26"] = pd.to_numeric(df_gi["q26"]) #Number of members
#creating new variables concatenating
df_gi['Region_gi']           = df_gi[['q39','q40','q41','q42','q43','q44','q45','q46','q47','q48']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_gi['Priority group']   = df_gi[['q29','q30','q31','q32','q33','q34','q35','q36','q37',     ]].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_gi['Impact System']    = df_gi[['q50','q51','q52','q53','q54','q55'                        ]].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
#__________________________
#Pledge Statement Survey
#__________________________
#getdata
df_pdg = pd.read_csv('Pledge_27012013.csv',sep=';', header=None, prefix="g").iloc[2:]
df_pdg.set_index("g0", inplace = True)
df_pdg.index.names = ['Master ID']
df_pdg = df_pdg.dropna(how = 'all')
df_pdg_names = pd.read_csv('Pledge_27012013.csv',sep=';').iloc[1:]
##rename
replacement_mapping_dict = {"Not targeted.": "0",
                            "2": "1",
                            "Mildly targeted but not exclusively.": "2",
                            "4": "3",
                            "Main or unique target.": "4",}
df_pdg['g28'] = df_pdg['g28'].replace(['Poor'], 'Low income communities')
df_pdg["g20"] = df_pdg["g20"].replace(replacement_mapping_dict) #Women and girls ind
df_pdg["g21"] = df_pdg["g21"].replace(replacement_mapping_dict) #LGBTQIA+ ind
df_pdg["g22"] = df_pdg["g22"].replace(replacement_mapping_dict) #Elderly ind
df_pdg["g23"] = df_pdg["g23"].replace(replacement_mapping_dict) #Children and Youth ind
df_pdg["g24"] = df_pdg["g24"].replace(replacement_mapping_dict) #Disabled ind
df_pdg["g25"] = df_pdg["g25"].replace(replacement_mapping_dict) #Indigenous or traditional communities ind
df_pdg["g26"] = df_pdg["g26"].replace(replacement_mapping_dict) #Racial, ethnic and/or religious minorities ind
df_pdg["g27"] = df_pdg["g27"].replace(replacement_mapping_dict) #Refugees ind
df_pdg["g28"] = df_pdg["g28"].replace(replacement_mapping_dict) #Low income communities ind

congo_list          = ['g67','g253','g495','g681','g902','g1088','g1309','g1495','g1716','g1902','g2133','g2319']
congo_Rep_list      = ['g66','g252','g494','g680','g901','g1087','g1308','g1494','g1715','g1901','g2132','g2318']
conteivoire_list    = ['g64','g250','g492','g678','g899','g1085','g1306','g1492','g1713','g1899','g2130','g2316']
libyan_list         = ['g84','g270','g512','g698','g919','g1105','g1326','g1512','g1733','g1919','g2150','g2336']
macedonia_list      = ['g140','g326','g568','g754','g975','g1161','g1382','g1568','g1789','g1975','g2206','g2392']
palestina_list      = ['g188','g374','g616','g802','g1023','g1209','g1430','g1616','g1837','g2023','g2254','g2440']
timor_list          = ['g196','g382','g624','g810','g1031','g1217','g1438','g1624','g1845','g2031','g2262','g2448']

df_pdg[congo_list] = df_pdg[congo_list].replace('Congo','Congo, Republic of').fillna('').astype(str)
df_pdg[congo_Rep_list] = df_pdg[congo_Rep_list].replace('Congo, the Democratic Republic of the','Congo, Republic of').fillna('').astype(str)
df_pdg[conteivoire_list] = df_pdg[conteivoire_list].replace("CÔøΩte d'Ivoire",'Ivory Coast').fillna('').astype(str)
df_pdg[libyan_list] = df_pdg[libyan_list].replace('Libyan Arab Jamahiriya','Libya').fillna('').astype(str)
df_pdg[macedonia_list] = df_pdg[macedonia_list].replace('Macedonia, the former Yugoslav Republic of','Macedonia, The Former Yugoslav Republic Of').fillna('').astype(str)
df_pdg[palestina_list] = df_pdg[palestina_list].replace('Palestinian Territory, Occupied','Palestine').fillna('').astype(str)
df_pdg[timor_list] = df_pdg[timor_list].replace('Timor-Leste','East Timor').fillna('').astype(str)

# #if the value of a serie is "text", change it for this other text in pandas.
# df_pdg = df_pdg.astype(str).str.replace({'Congo, the Democratic Republic of the':'c'}, regex=True)
# df_pdg = df_pdg.astype(str).str.replace({"CÔøΩte d'Ivoire": 'Ivory Coast'}, regex=True)
# df_pdg = df_pdg.astype(str).str.replace({'Libyan Arab Jamahiriya': 'Libya'}, regex=True)
# df_pdg = df_pdg.astype(str).str.replace({'Macedonia, the former Yugoslav Republic of':'Macedonia, The Former Yugoslav Republic Of'}, regex=True)
# df_pdg = df_pdg.astype(str).str.replace({'Palestinian Territory, Occupied': 'Palestine'}, regex=True)
# df_pdg = df_pdg.astype(str).str.replace({'Timor-Leste': 'East Timor'},regex=True)

# st.write(df_pdg[timor_list])

to_numbers_list = { '27 million ':'27000000',
                    '500,000,000':'500000000',
                    '85,550,224':'85550224',
                    '10 million people':'10000000',
                    '150 million in Latin America living in vulnerable areas':'150000000',
                    '500 Mio. beneficiaries by 2025':'500000000',
                    '567m ':'567000000',
                    '250,000,000':'250000000',
                    '10,000,000':'10000000',
                    '1 billion':'1000000000',
                    '3000000':'3000000',
                    '1 million farmers':'1000000',
                    '1000 local government professionals impacting and influencing millions of individuals in communities across North America':'1000',
                    'At least 300 million':'300000000',
                    '':'',
                    'test':'',
                    '3000':'3000',
                    '500 million by 2030':'500000000',
                    '200,000,000':'200000000',
                    '250':'250',
                    '10':'10',
                    'm':'',
                    '180':'180',
                    '100':'100',
                    '150':'150',
                    '20':'20',
                    '18':'18',
                    '10':'10',
                    'Sub-Saharan Africa, East Asia & Pacific':'3',
                    '5':'5',
                    '70':'70',
                    '6 regions':'6',
                    '2':'2',
                    '100':'100',
                    '110':'110',
                    '2':'2',
                    'adas':'',
                    '3.000.000':'3000000',
                    '22.78 million hectares':'22780000',
                    '7 million hectares':'7000000',
                    '50 million ha ':'50000000',
                    }
to_numbers_variables_list = ["g2116","g1675","g1268","g19"] #Numbers of beneficiaries_ #g2116:Natural Systems #g1675:cities #g1268:Regions #g19:Individuals
df_pdg[to_numbers_variables_list] = df_pdg[to_numbers_variables_list].replace(to_numbers_list)
##change format
df_pdg[to_numbers_variables_list] = df_pdg[to_numbers_variables_list].apply(pd.to_numeric, errors='coerce')
df_pdg["g20"] = pd.to_numeric(df_pdg["g20"]) #Women and girls ind
df_pdg["g21"] = pd.to_numeric(df_pdg["g21"]) #LGBTQIA+ ind
df_pdg["g22"] = pd.to_numeric(df_pdg["g22"]) #Elderly ind
df_pdg["g23"] = pd.to_numeric(df_pdg["g23"]) #Children and Youth ind
df_pdg["g24"] = pd.to_numeric(df_pdg["g24"]) #Disabled ind
df_pdg["g25"] = pd.to_numeric(df_pdg["g25"]) #Indigenous or traditional communities ind
df_pdg["g26"] = pd.to_numeric(df_pdg["g26"]) #Racial, ethnic and/or religious minorities ind
df_pdg["g27"] = pd.to_numeric(df_pdg["g27"]) #Refugees ind
df_pdg["g28"] = pd.to_numeric(df_pdg["g28"]) #Low income communities ind
df_pdg["g30"] = pd.to_numeric(df_pdg["g30"])
df_pdg["g31"] = pd.to_numeric(df_pdg["g31"])
df_pdg["g458"] = pd.to_numeric(df_pdg["g458"])
df_pdg["g459"] = pd.to_numeric(df_pdg["g459"])
df_pdg["g865"] = pd.to_numeric(df_pdg["g865"])
df_pdg["g1272"] = pd.to_numeric(df_pdg["g1272"])
df_pdg["g1273"] = pd.to_numeric(df_pdg["g1273"])
df_pdg["g1679"] = pd.to_numeric(df_pdg["g1679"])
df_pdg["g1680"] = pd.to_numeric(df_pdg["g1680"])
df_pdg["g2093"] = pd.to_numeric(df_pdg["g2093"])
df_pdg["g2094"] = pd.to_numeric(df_pdg["g2094"])
##Creating list of series needed to treat multiquestionsº.
#____HAZARDS
hazard_list_ind         = df_pdg.iloc[:, 32:50].apply(lambda x: x.str.strip()).columns.values.tolist() #Individual Engagement
hazard_list_comp        = df_pdg.iloc[:, 460:478].apply(lambda x: x.str.strip()).columns.values.tolist() #Companies engagement
hazard_list_countries   = df_pdg.iloc[:, 867:885].apply(lambda x: x.str.strip()).columns.values.tolist() #Countries
hazard_list_region      = df_pdg.iloc[:, 1274:1292].apply(lambda x: x.str.strip()).columns.values.tolist() #Regions
hazard_list_cities      = df_pdg.iloc[:, 1681:1699].apply(lambda x: x.str.strip()).columns.values.tolist() #Cities
hazard_list_nat_sys     = df_pdg.iloc[:, 2095:2113].apply(lambda x: x.str.strip()).columns.values.tolist() #Natural Systems
hazards_options         = ['Heat stress - lives & livelihoods combined','Heat stress - livelihoods (work)','Heat stress - lives','Extreme heat','Extreme cold','Snow and ice','Drought (agriculture focus)','Drought (other sectors)','Water stress (urban focus)','Water stress (rural focus)','Fire weather (risk of wildfires)','Urban flooding','Riverine flooding','Coastal flooding','Other coastal events','Oceanic events','Hurricanes/cyclones','Extreme wind']
#____COMPANIES
companies_type_list     = df_pdg.iloc[:, 436:457].apply(lambda x: x.str.strip()).columns.values.tolist()
#____NATURALSYSTEMS
nat_syst_type_list      = df_pdg.iloc[:, 2079:2089].apply(lambda x: x.str.strip()).columns.values.tolist()
#____COUNTRIES
allcountrylist_ind      = df_pdg.iloc[:, 57:243].apply(lambda x: x.str.strip()).columns.values.tolist()
allcountrylist_comp     = df_pdg.iloc[:, 485:671].apply(lambda x: x.str.strip()).columns.values.tolist()
allcountrylist_country  = df_pdg.iloc[:, 892:1078].apply(lambda x: x.str.strip()).columns.values.tolist()
allcountrylist_regions  = df_pdg.iloc[:, 1299:1485].apply(lambda x: x.str.strip()).columns.values.tolist()
allcountrylist_cities   = df_pdg.iloc[:, 1706:1892].apply(lambda x: x.str.strip()).columns.values.tolist()
allcountrylist_natsys   = df_pdg.iloc[:, 2123:2309].apply(lambda x: x.str.strip()).columns.values.tolist()
#st.write(len(allcountrylist_ind))
#st.write(len(allcountrylist_comp))
#st.write(len(allcountrylist_country))
#st.write(len(allcountrylist_regions))
#st.write(len(allcountrylist_cities))
#st.write(len(allcountrylist_natsys))
#All Hazards Treatment
df_pdg[hazard_list_ind]         = df_pdg[hazard_list_ind].where(df_pdg['g32'] != 'All Hazard', hazards_options)  #Recode "All Hazard" = Apply to all Hazard"
df_pdg[hazard_list_comp]        = df_pdg[hazard_list_comp].where(df_pdg['g460'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_countries]   = df_pdg[hazard_list_countries].where(df_pdg['g867'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_region]      = df_pdg[hazard_list_region].where(df_pdg['g1274'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_cities]      = df_pdg[hazard_list_cities].where(df_pdg['g1681'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_nat_sys]     = df_pdg[hazard_list_nat_sys].where(df_pdg['g2095'] != 'All Hazard', hazards_options)
#Concatenating columns
df_pdg['Engagement scope']      = df_pdg[['g13','g14','g15','g16','g17','g18']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_ind']           = df_pdg[hazard_list_ind].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1) #Concatenate
df_pdg['Hazards_comp']          = df_pdg[hazard_list_comp].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_countries']     = df_pdg[hazard_list_countries].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_region']        = df_pdg[hazard_list_region].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_cities']        = df_pdg[hazard_list_cities].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_nat_sys']       = df_pdg[hazard_list_nat_sys].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['All_Hazards']           = df_pdg[['Hazards_ind','Hazards_comp','Hazards_countries','Hazards_region','Hazards_cities','Hazards_nat_sys']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Companies Types']       = df_pdg[companies_type_list].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Natural Systems Types'] = df_pdg[nat_syst_type_list].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)

df_pdg['Countries_individuals'] = df_pdg[allcountrylist_ind].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Countries_companies']   = df_pdg[allcountrylist_comp].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Countries_countries']   = df_pdg[allcountrylist_country].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Countries_regions']     = df_pdg[allcountrylist_regions].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Countries_cities']      = df_pdg[allcountrylist_cities].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Countries_nat_sys']     = df_pdg[allcountrylist_natsys].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['All_Countries']         = df_pdg[['Countries_individuals','Countries_companies','Countries_countries','Countries_regions','Countries_cities','Countries_nat_sys']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)


##adding new colums considering information from other dataframe. 

df_country = pd.read_csv('countries_geoinfo.csv',sep=';')    

#creating a list of countries depending of its mayor area
Africa = df_country[df_country['mayor_area']== 'Africa']
Asia = df_country[df_country['mayor_area']== 'Asia']
Europe = df_country[df_country['mayor_area']== 'Europe']
LATAMC = df_country[df_country['mayor_area']== 'Latin America and the Caribbean']
Northern_America = df_country[df_country['mayor_area']== 'Northern America']
Oceania = df_country[df_country['mayor_area']== 'Oceania']

Africa_list = Africa['Country'].tolist()
Asia_list = Asia['Country'].tolist()
Europe_list = Europe['Country'].tolist()
LATAMC_list = LATAMC['Country'].tolist()
Northern_America_list = Northern_America['Country'].tolist()
Oceania_list = Oceania['Country'].tolist()

df_pdg['Africa'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Africa_list for country in x])), 'Africa', '')
df_pdg['Asia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Asia_list for country in x])), 'Asia', '')
df_pdg['Europe'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_list for country in x])), 'Europe', '')
df_pdg['LATAMC'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in LATAMC_list for country in x])), 'Latin America and the Caribbean', '')
df_pdg['Northern_America'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_pdg['Oceania'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Oceania_list for country in x])), 'Oceania', '')


# st.write(df_pdg[['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']])

Southern_Asia = df_country[df_country['Region']== 'Southern Asia']
Southern_Europe = df_country[df_country['Region']== 'Southern Europe']
Northern_Africa = df_country[df_country['Region']== 'Northern Africa']
Middle_Africa = df_country[df_country['Region']== 'Middle Africa']
Caribbean = df_country[df_country['Region']== 'Caribbean']
South_America = df_country[df_country['Region']== 'South America']
Western_Asia = df_country[df_country['Region']== 'Western Asia']
Australia_and_New_Zealand = df_country[df_country['Region']== 'Australia and New Zealand']
Western_Europe = df_country[df_country['Region']== 'Western Europe']
Eastern_Europe = df_country[df_country['Region']== 'Eastern Europe']
Central_America = df_country[df_country['Region']== 'Central America']
Western_Africa = df_country[df_country['Region']== 'Western Africa']
Southern_Africa = df_country[df_country['Region']== 'Southern Africa']
Eastern_Africa = df_country[df_country['Region']== 'Eastern Africa']
South_Eastern_Asia = df_country[df_country['Region']== 'South-Eastern Asia']
Northern_America = df_country[df_country['Region']== 'Northern America']
Eastern_Asia = df_country[df_country['Region']== 'Eastern Asia']
Northern_Europe = df_country[df_country['Region']== 'Northern Europe']
Central_Asia = df_country[df_country['Region']== 'Central Asia']
Micronesia = df_country[df_country['Region']== 'Micronesia']
Melanesia = df_country[df_country['Region']== 'Melanesia']
Polynesia = df_country[df_country['Region']== 'Polynesia']

Southern_Asia_list = Southern_Asia['Country'].tolist()
Southern_Europe_list = Southern_Europe['Country'].tolist()
Northern_Africa_list = Northern_Africa['Country'].tolist()
Middle_Africa_list = Middle_Africa['Country'].tolist()
Caribbean_list = Caribbean['Country'].tolist()
South_America_list = South_America['Country'].tolist()
Western_Asia_list = Western_Asia['Country'].tolist()
Australia_and_New_Zealand_list = Australia_and_New_Zealand['Country'].tolist()
Western_Europe_list = Western_Europe['Country'].tolist()
Eastern_Europe_list = Eastern_Europe['Country'].tolist()
Central_America_list = Central_America['Country'].tolist()
Western_Africa_list = Western_Africa['Country'].tolist()
Southern_Africa_list = Southern_Africa['Country'].tolist()
Eastern_Africa_list = Eastern_Africa['Country'].tolist()
South_Eastern_Asia_list = South_Eastern_Asia['Country'].tolist()
Northern_America_list = Northern_America['Country'].tolist()
Eastern_Asia_list = Eastern_Asia['Country'].tolist()
Northern_Europe_list = Northern_Europe['Country'].tolist()
Central_Asia_list = Central_Asia['Country'].tolist()
Micronesia_list = Micronesia['Country'].tolist()
Melanesia_list = Melanesia['Country'].tolist()
Polynesia_list = Polynesia['Country'].tolist()


df_pdg['Southern_Asia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Asia_list for country in x])), 'Southern Asia', '')
df_pdg['Southern_Europe'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Europe_list for country in x])), 'Southern Europe', '')
df_pdg['Northern_Africa'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Africa_list for country in x])), 'Northern Africa', '')
df_pdg['Middle_Africa'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_Africa_list for country in x])), 'Middle Africa', '')
df_pdg['Caribbean'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Caribbean_list for country in x])), 'Caribbean', '')
df_pdg['South_America'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in South_America_list for country in x])), 'South America', '')
df_pdg['Western_Asia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Asia_list for country in x])), 'Western Asia', '')
df_pdg['Australia_and_New_Zealand'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Australia_and_New_Zealand_list for country in x])), 'Australia and New Zealand', '')
df_pdg['Western_Europe'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Europe_list for country in x])), 'Western Europe', '')
df_pdg['Eastern_Europe'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Europe_list for country in x])), 'Eastern Europe', '')
df_pdg['Central_America'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Central_America_list for country in x])), 'Central America', '')
df_pdg['Western_Africa'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Africa_list for country in x])), 'Western Africa', '')
df_pdg['Southern_Africa'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Africa_list for country in x])), 'Southern Africa', '')
df_pdg['Eastern_Africa'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Africa_list for country in x])), 'Eastern Africa', '')
df_pdg['South_Eastern_Asia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in South_Eastern_Asia_list for country in x])), 'South-Eastern Asia', '')
df_pdg['Northern_America'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_pdg['Eastern_Asia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Asia_list for country in x])), 'Eastern Asia', '')
df_pdg['Northern_Europe'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Europe_list for country in x])), 'Northern Europe', '')
df_pdg['Central_Asia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Central_Asia_list for country in x])), 'Central Asia', '')
df_pdg['Micronesia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Micronesia_list for country in x])), 'Micronesia', '')
df_pdg['Melanesia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Melanesia_list for country in x])), 'Melanesia', '')
df_pdg['Polynesia'] = np.where(df_pdg['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Polynesia_list for country in x])), 'Polynesia', '')


#Concatenating columns
df_pdg['mayor_area'] = df_pdg[['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Region'] = df_pdg[['Southern_Asia','Southern_Europe','Northern_Africa','Middle_Africa','Caribbean','South_America','Western_Asia','Australia_and_New_Zealand','Western_Europe','Eastern_Europe','Central_America','Western_Africa','Southern_Africa','Eastern_Africa','South_Eastern_Asia','Northern_America','Eastern_Asia','Northern_Europe','Central_Asia','Micronesia','Melanesia','Polynesia']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)


#Confirmation that works!

#Plan Statement Survey
df_plan = pd.read_csv('Plan_27012013.csv',sep=';', header=None, prefix="p").iloc[2:]
df_plan.set_index("p0", inplace = True)
df_plan.index.names = ['Master ID']
df_plan = df_plan.dropna(how = 'all')
#df_plan = df_plan.replace(0, np.nan, inplace=True)

#Making all survey of the 36 partners. At least all df should countain the entire ID Master form. Good Idea! ALl that have not responded anything are in "In process of answering"

#confirmar uso de dummy item para vincular encuesta plan. Ver video aquí: https://www.youtube.com/watch?v=iZUH1qlgnys&list=PLtqF5YXg7GLmCvTswG32NqQypOuYkPRUE&index=7

#Resilience Attributes Survey
df_ra = pd.read_csv('RA_27012013.csv',sep=';', header=None, prefix="r").iloc[2:]
df_ra.set_index("r0", inplace = True)
df_ra.index.names = ['Master ID']
df_ra = df_ra.dropna(how = 'all')

#Clean Data Set. We must first asumme in the csv file that all partners have 1 response. 

#list
ra_likert_recode = {'0- We do not develop actions that contribute to this subcategory' : '0',
                        '1- We contribute to this subcategory but indirectly, It’s not in the core of our activities' : '1',
                        '2- A few of our actions contribute to this subcategory' : '2',
                        '3- This subcategory is in the core of an important part of our actions' : '3',
                        '3- This subcategory is in the core of an important part of our actions.':'3',
                        '4- This subcategory is in the core of the most of our actions' : '4',}

df_ra.rename(columns = { 'r13':'Equity','r16':'Inclusivity','r38':'Preparedness','r41':'Planning',
                    	'r44':'Experiential_learning',	'r47':'Educational_learning',	'r50':'Autonomy',
                        	'r53':'Leadership',	'r56':'Decision_making',	'r59':'Collective_participation',
                            	'r62':'Connectivity',	'r65':'Networking',	'r68':'Diversity',	'r71':'Redundancy',
                                	'r74':'Finance',	'r77':'Natural_resources',	'r80':'Technologies',
                                    	'r83':'Infrastructure',	'r86':'Services' }, inplace = True)

sub_ra_likert_var_list = ['Equity',	'Inclusivity',	'Preparedness',
	'Planning',	'Experiential_learning','Educational_learning',
    	'Autonomy',	'Leadership',	'Decision_making',	'Collective_participation',
        	'Connectivity',	'Networking',	'Diversity',	'Redundancy',	'Finance',
            	'Natural_resources',	'Technologies',	'Infrastructure',	'Services']

df_ra[sub_ra_likert_var_list] = df_ra[sub_ra_likert_var_list].replace(ra_likert_recode)

##To numeric
df_ra[sub_ra_likert_var_list] = df_ra[sub_ra_likert_var_list].apply(pd.to_numeric, errors='coerce')

df_ra['Equity_&_Inclusivity']       = df_ra[['Equity','Inclusivity']].apply(lambda x: x.mean(), axis=1)
df_ra['Preparedness_and_planning']  = df_ra[['Preparedness','Planning']].apply(lambda x: x.mean(), axis=1)
df_ra['Learning']                   = df_ra[['Experiential_learning','Educational_learning']].apply(lambda x: x.mean(), axis=1)
df_ra['Agency']                     = df_ra[['Autonomy',	'Leadership','Decision_making']].apply(lambda x: x.mean(), axis=1)
df_ra['Social_Collaboration']       = df_ra[['Collective_participation','Connectivity','Networking']].apply(lambda x: x.mean(), axis=1)
df_ra['Flexibility']                = df_ra[['Diversity','Redundancy']].apply(lambda x: x.mean(), axis=1)
df_ra['Assets']                     = df_ra[['Finance','Natural_resources','Technologies','Infrastructure','Services']].apply(lambda x: x.mean(), axis=1)

ra_likert_var_list = ['Equity_&_Inclusivity','Preparedness_and_planning','Learning','Agency','Social_Collaboration','Flexibility','Assets']

# st.write(df[ra_likert_var_list])


#Making one database
df = pd.concat([df_gi,df_pdg,df_ra], axis=1)
df_len = len(df.index)  



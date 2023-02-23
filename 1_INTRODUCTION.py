from PIL import Image
import streamlit as st

im = Image.open("logo_web.png")
st.set_page_config(page_title="R2R DATA EXPLORER", page_icon=im, layout="wide", initial_sidebar_state="expanded")

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

##MAIN SIDE

st.title("R2R DATA EXPLORER")

st.markdown("""
**Welcome** to the R2R Data Explorer 2.0.  A powerful web application designed to support the [Race to Resilience campaign](https://racetozero.unfccc.int/system/racetoresilience/) launched by the [UN Climate Change High-Level Champions](https://climatechampions.unfccc.int/).

The R2R campaign aims to increase the resilience of four billion people living in vulnerable communities by collaborating with [partner organizations worldwide](https://racetozero.unfccc.int/meet-the-partners/) and developing tools and support for them. 


As a web application developed specifically for the R2R Campaign, the R2R Data Explorer aims to provide information on increased resilience across the campaign. 

It achieves this objective by utilizing two complementary approaches for human-centered resilience-building: Magnitude and Depth of Resilience. 
- The Magnitude approach helps estimate the size of the impact of resilience-building initiatives, primarily by looking at the number of beneficiaries reached. The R2R Data Explorer provides information on the number of people in vulnerable communities who have benefited from the resilience initiatives across the campaign. 
- The Depth approach, on the other hand, provides an understanding of how partners and their members are contributing to increasing resilience by observing which conditions (Resilience Attributes) they are impacting. The R2R Data Explorer provides information on the specific resilience attributes that have been impacted by the initiatives, helping to showcase the depth of impact. 

In sum, **the R2R Data Explorer aims to provide a comprehensive view of the increased resilience across the R2R Campaign, utilizing both Magnitude and Depth approaches to provide a detailed understanding of the impact of resilience-building initiatives**.
It is made by the Technical Secretariat of the Race to Resilience Campaign, with the support of the Center for Climate and Resilience Research at the Universidad de Chile.
""")

st.header("HOW TO USE THE DATA EXPLORER")

st.markdown("""
First, let's take a look at the three menu options on the left sidebar. 

The first one is "INTRODUCTION," which provides an overview of the R2R campaign and the data explorer. 

The second option is "R2R CAMPAIGN CURRENT STATUS," which uses both Magnitude and Depth approaches to give a detailed understanding of the campaign. 

The third option is "R2R PARTNER FINDER," which allows filtering partners based on different criteria. This Partner Selection Tool enables users to filter searches using three main areas related to increasing resilience: 
- Vulnerability Assessment.
- Targeting Interventions.
- Key Impact Systems.


With Vulnerability Assessment, users can select hazards, continents, regions, and countries to identify areas where R2R partners are directing their resilience actions. This information can be used to develop and prioritize interventions that build resilience in those regions.

The Targeting Interventions option enables the selection of vulnerable priority groups and beneficiaries, such as women, children, and low-income communities, to develop targeted interventions and increase their resilience to climate change. 

Lastly, the key Impact Systems option lets users identify R2R partner pledges related to the impact systems under the Sharm-El-Sheikh Adaptation Agenda.

Once selections are made, pressing the SEARCH button displays the results on the main page. Users can then choose a specific partner to view more details about their General Information, Pledge Statement, Resilience Attributes, and Plan Statement. Don't worry; if no filters are applied, all partner information is still viewable.

Remember, multiple selections per criterion can be made to further narrow down the search. We hope this helps you navigate the R2R Campaign Data Explorer with ease!

    """)


st.header('FREQUENTLY ASKED QUESTIONS')
st.subheader("WHAT IS THE R2R DATA EXPLORER 2.0?")
st.markdown("""
The R2R Data Explorer 2.0 is a web application designed to support the Race to Resilience campaign. It aims to provide a comprehensive view of the increased resilience across the R2R Campaign, utilizing both Magnitude and Depth approaches to provide a detailed understanding of the impact of resilience-building initiatives. 
""")
st.subheader("WHAT IS NEW IN THE VERSION 2.0?")
st.markdown("""
The R2R Data Explorer was launched at COP 27 in November 2022, and version 2.0 includes many improvements:

**Better visualization**: The charts and maps have been enhanced to be more visually appealing and informative, with additional explanatory information.

**Multi-Filter**: The R2R Partner Search Tools now allow users to filter their search using three main areas related to increasing resilience:
- *Vulnerability Assessment*: Users can select hazards, continents, regions, and countries to identify areas that are more vulnerable to specific types of hazards and disasters. This information can be used to develop and prioritize interventions to build resilience in these regions.
- *Targeting Interventions*: Priority groups and beneficiaries can be selected to identify specific populations that are more vulnerable to the impacts of climate change, such as women, children, the elderly, and those living in poverty. This allows for the development of targeted interventions that address their unique needs and increase their resilience.
- *Key Impact Systems*: Users can use the impact systems selector to identify R2R partner pledges related to the impact systems under the Sharm-El-Sheikh Adaptation Agenda.

**Improved interface**: The web application's aesthetic style has been updated to follow official R2R criteria, resulting in a better user experience and improved navigation.

**Improved user experience**: The new design is more user-friendly and easier to navigate. The interface is intuitive, allowing users to quickly locate data and information and personalize their views and analyses to meet their needs.
 """)

st.subheader('WHO ARE ITS USERS?')
st.markdown("""
The R2R Data Explorer is primarily intended for non-State actors who are partnering with the Race to Resilience Campaign to report their climate resilience actions and quantify and validate their impact under a common framework. However, the information provided on the platform can also be useful to anyone interested in understanding the progress of the campaign in increasing resilience of vulnerable communities.
""")
st.subheader('HOW IS IT MADE?')
st.markdown("""
The R2R Data Explorer was developed by the Technical Secretariat of the Race to Resilience Campaign, hosted at the Center for Climate and Resilience Research at the Universidad de Chile. 
It was made using web development technologies such as HTML, CSS, JavaScript and Python, and it is hosted on a web server that can be accessed through any modern web browser. The data presented on the platform is sourced from R2R partners reporting on their resilience initiatives, which are then aggregated and presented through this platform's user interface.
""")
st.subheader('WHERE DOES ITS DATA COME FROM?')
st.markdown("""
The data for the R2R data explorer comes from the non-state actors who partner with the Race to Resilience Campaign and report their climate resilience actions using the R2R reporting tool. 

The tool includes four surveys: 
- General Information Survey
- Pledge Statement Survey
- Plan Statement Survey
- Resilience Attributes Survey

The surveys are used to collect information about the non-state actors' initiatives, goals, target groups, and plans for achieving their targets. 

Ultimately, non-state actors are expected to report outcomes backed by suitable evidence to make good on their pledge by 2030.
""")
with st.expander('Read more about R2R Surveys'):
    st.subheader('R2R REPORTING TOOL - SURVEYS')
    st.markdown("""
    Race to Resilience has developed a people-centered resilience Metrics Framework for non-state actors to report climate resilience actions and to quantify and validate their impact under a common framework. The Framework provides a robust toolkit for the Monitoring and Evaluation of resilience-building actions, with a focus on Non-State actors: R2R Reporting Tool.

    - **General Information Survey:** This survey is the first step in the Reporting Tool, and it seeks to collect general information of the non-State actors who are partnering with the Race to Resilience Campaign.
    The form includes several fields for gathering information about the initiative and its goals, as well as how it plans to build resilience. Some of the information collected includes the initiative's official name and short name, its location, the number of affiliated members, and the macro regions and main areas in which the initiative works. The form also includes questions about the initiative's target groups and whether it aims to generate a direct and measurable impact on individuals, companies, cities, regions, countries, or natural systems. Finally, there are fields for providing final comments and feedback. Overall, this form is likely used to gather information about the potential of partner initiatives and evaluate whether they meet the criteria for joining the R2R campaign.
    
    - **Pledge Statement Survey:**
    This survey is the second step in the Reporting Tool, corresponding to the 'Pledge' stage of the R2R campaign. The tool aims to collect information on the direct impacts that R2R Partners' initiatives and its members aim to have on different types of beneficiaries.
    R2R Partners' initiatives are prompted to indicate the 'levels of engagement' or types of beneficiaries for which they are making a pledge, along with an estimation of the size of this pledge (e.g., number of individuals, companies, countries, regions, cities, and natural systems).
    R2R Partners' initiatives need to remember that in the next stages (plan, proceed, and publish), they will be expected to follow up on this pledge and provide more information on their plans and progress in implementing it. Ultimately, they will be expected to report outcomes (backed by suitable evidence) to make good on their pledge by 2030.

    - **Plan Survey:** This survey is the third step in the R2R Reporting Tool, corresponding to the 'Plan' stage of the R2R campaign. Its purpose is to gather information on how R2R Partners' initiatives and members plan to achieve the targets set out in their pledge. 
    In this survey, R2R Partners' initiatives are prompted to indicate the actions they are planning to put in place, provide their plans on how and when they plan to deliver them, and an estimation of their possible beneficiaries.
    It is important to note that in the next stages of the R2R campaign ('proceed' & 'publish'), R2R Partners' initiatives will be expected to follow up on how they are implementing the actions they have planned, and provide evidence on the implementation progress and its outcomes.
    R2R Partners' initiatives may have different lines of work, each of which may involve different kinds of actions, beneficiaries, and geographies. If that is the case, it is encouraged to report each of these lines of work separately, as a separate 'action plan'. This survey can be completed multiple times, once for each 'plan' that R2R Partners' initiatives would like to report.
    - **Resilience Attributes Survey:** The Resilience Attributes Survey is the fourth step in the Reporting Tool, which consists of 7 key Resilience Attributes that indirectly foster resilience and enhance transformations. These attributes include: Equity & Inclusivity, Preparedness and Planning, Learning, Agency, Social Collaboration, Flexibility, and Assets. Each attribute has subcategories that address different aspects, and they involve opportunities to distribute resources equitably, prepare for change and uncertainty, generate and process new information, act collectively, switch between coping and adaptation strategies, and have access to natural, financial, technological, and service resources. The survey has multiple-choice and descriptive questions for each subcategory, except for the Inclusivity subcategory, which also has checkboxes-questions.
    """)


st.subheader('HOW CAN I BECOME A MEMBER OF THE RACE TO RESILIENCE CAMPAIGN?')
st.markdown("""To become a member of the Race to Resilience Campaign, initiatives or partners must first submit an Expression of Interest (EoI) form that explains why they are a good candidate for the campaign and commit to following R2R's membership rules and criteria. After being accepted into the campaign, partners must set a target for resilience action for themselves and their members and draft an evidence-based plan to take action towards their pledge. Finally, partners should take immediate and effective action towards achieving the actions they have planned and report against this progress.
""")

st.sidebar.caption('NAVEGATION MENU')
st.sidebar.markdown('')
st.sidebar.caption("[WELCOME](#r2r-data-explorer)")
st.sidebar.markdown('')
st.sidebar.caption("[HOW TO USE?](#how-to-use-the-data-explorer)")
st.sidebar.markdown('')
st.sidebar.caption("[FREQUENTLY ASKED QUESTIONS](#requently-asked-questions)")
st.sidebar.caption("- [What is the R2R Data Explorer?](#what-is-the-r2r-data-explorer-2-0)")
st.sidebar.caption("- [What is new in the version 2.0?](#what-is-new-in-the-version-2-0)")
st.sidebar.caption("- [Who are its users?](#who-are-its-users)")
st.sidebar.caption("- [How is it made?](#how-is-it-made)")
st.sidebar.caption("- [Where the data come from?](#where-does-its-data-come-from)")
st.sidebar.caption("- [How to become a R2R Partner](#how-can-i-become-a-member-of-the-race-to-resilience-campaign)")
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.caption("GO TO THE OFFICIAL RACE TO RESILIENCE WEB PAGE [HERE](https://racetozero.unfccc.int/system/racetoresilience/)")
st.sidebar.markdown("")
st.sidebar.caption('READ FULL R2R’s METRICS FRAMEWORK [HERE](https://climatechampions.unfccc.int/wp-content/uploads/2022/11/Working-Paper-No-1_R2R%C2%B4s-Metrics-Framework_Oct2022-FOR_SLT.docx.pdf)')
st.sidebar.markdown("")
st.sidebar.caption('WATCH R2R’s METRICS FRAMEWORK INTRODUCTION VIDEO [HERE](https://www.youtube.com/watch?v=TZFp9_LL8qs)')





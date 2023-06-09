# Import libraries
import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
from typing import List
import plotly.express as px
import flagpy as fp
from PIL import Image
from utils.styles import styles


st.set_page_config(
    page_title="World Happiness Report,2015 up to 2022",
)

#  css part
st.write(styles, unsafe_allow_html=True)


@st.cache_data
def get_data():
    dataframe = pd.read_csv(
        './world_happiness_2015_2022/world-happiness-report-2015-2022.csv')
    flags_df = fp.get_flag_df()
    countires = set(dataframe["Country"])
    regions = set(dataframe["Region"])
    return dataframe, countires, flags_df, regions

@st.cache_data
def get_desc_by_country(dataframe):
    return dataframe.groupby('Country')['Happiness Rank'].describe() 


def check_flag(country_name):
    flag_name_converter = {'Dominican Republic': 'The Dominican Republic', 'United Arab Emirates': 'The United Arab Emirates',
                           'United Kingdom': 'The United Kingdom', 'United States': 'The United States'}
    country_name = flag_name_converter.get(country_name, country_name)
    if country_name in fp.get_country_list():
        return True, country_name
    return False, country_name
    # print(fp.get_country_list())
    # ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua And Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'The Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia And Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'The Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'The Comoros', 'The Democratic Republic Of The Congo', 'The Republic Of The Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'The Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'The Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'The Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea', 'South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'The Maldives', 'Mali', 'Malta', 'The Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'The Federated States Of Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'The Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'The Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts And Nevis', 'Saint Lucia', 'Saint Vincent And The Grenadines', 'Samoa', 'San Marino', 'São Tomé And Príncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'The United Arab Emirates', 'The United Kingdom', 'The United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']


def search_by_country(searchterm: str) -> List[any]:
    global countries
    return [c for c in countries if c.lower().startswith(searchterm.lower())] if searchterm else []


overall_df, countries, flags_df, regions = get_data()
check_boxes = {}
with st.sidebar:
    selected_country = st_searchbox(
        search_function=search_by_country,
        key="country_searchbox",
        placeholder="Search for a Country",

    )
    
    if not selected_country:
        st.markdown('<b>Filter By Region</b><hr/>', unsafe_allow_html=True)
        c9, c10 = st.columns([0.5, 0.5])
        for index, cb in enumerate(regions):
            if index % 2 == 0:
                with c9:
                    check_box = st.checkbox(cb)
            else:
                with c10:
                    check_box = st.checkbox(cb)
            check_boxes[cb] = check_box


overall_df = overall_df.loc[:, ~overall_df.columns.str.contains('^Unnamed')]

if all(not value for value in check_boxes.values()):
    check_boxes['All'] = True
else:
    check_boxes['All'] = False

if selected_country:
    col1, col2 = st.columns([0.5, 0.5])
    col3, col4 = st.columns([0.5, 0.5])
    with col1:
        st.write(selected_country)
    with col2:
        signal, country_name = check_flag(selected_country)
        if signal:
            img = Image.fromarray(flags_df["flag"].loc[country_name], 'RGB')
            img.save('flag.png')
            img = Image.fromarray(flags_df["flag"].loc[country_name], 'RGB')
            with Image.open('./flag.png') as image:
                st.image(image)

    df_by_selected_country = overall_df[overall_df.Country == selected_country]
    df_by_selected_country = df_by_selected_country.sort_values(
        by=["Year"], ascending=True)
    st.dataframe(df_by_selected_country.set_index(overall_df.columns[10]))
    with col3:
        st.write('Best Rank:', df_by_selected_country.loc[df_by_selected_country['Happiness Rank'].idxmin(
        )]['Happiness Rank'])
    with col4:
        st.write('Worst Rank:', df_by_selected_country.loc[df_by_selected_country['Happiness Rank'].idxmax(
        )]['Happiness Rank'])

    difference = df_by_selected_country.loc[df_by_selected_country['Year'].idxmin()]['Happiness Rank'] - df_by_selected_country.loc[df_by_selected_country['Year'].idxmax()]['Happiness Rank']
    st.write(f"""Difference from <b>{df_by_selected_country.loc[df_by_selected_country['Year'].idxmin()]['Year']}</b> until 
                <b>{df_by_selected_country.loc[df_by_selected_country['Year'].idxmax()]['Year']}</b> : 
                <b style="color: {'green' if difference > 0 else 'gray' if difference == 0 else 'red'}">{"%+d" % (difference)}</b>""", unsafe_allow_html=True)

    fig = px.line(df_by_selected_country, x="Year",
                  y="Happiness Rank", title=f"Year / Happiness Rank")
    st.plotly_chart(fig)



else:

    selected_year = st.selectbox(
        'Choose The Year',
        (str(year) for year in range(2015, 2023)))
    st.markdown(f"You Selected Year: <b>{selected_year}</b>", unsafe_allow_html=True)

    df = overall_df[overall_df.Year == int(selected_year)]

    try:
        if not check_boxes['All']:
            filtered_region = list(
                filter(lambda k: check_boxes[k], check_boxes))
            st.write(f'<b>Filters:</b> <br/><span class="c-pill c-pill--warning">{",".join(filtered_region)}</span>', unsafe_allow_html=True)
            df = df[df['Region'].isin(filtered_region)]
    except KeyError:
        pass

    df = df.sort_values(by=["Happiness Rank"], ascending=True) # Happiness Rank Column as Index
    if df.shape[0] > 0:

        st.dataframe(df.set_index(df.columns[0]))
        
        c5,c6 = st.columns([0.5,0.5])
        with c5:
            x_list = list(df.columns) + ['Happiness Score'] 
            x_list.remove('Generosity')
            x_axis = st.selectbox(
            'Choose X axis criterion',
            (f'x: {cri}' for cri in x_list[::-1]))
        with c6:
            y_list = list(df.columns) + ['Generosity'] 
            y_list.remove('Generosity')
            y_axis = st.selectbox(
            'Choose Y axis criterion',
            (f'y: {cri}' for cri in y_list[::-1]))
        try:
            try: 
                corr = round(df[x_axis.replace('x: ','')].apply(lambda x: float(x.split()[0].replace(',', ''))).corr(df[y_axis.replace('y: ','')].apply(lambda x: float(x.split()[0].replace(',', '')))),2)
            except AttributeError:
                corr = round(df[x_axis.replace('x: ','')].astype(float).corr(df[y_axis.replace('y: ','')].astype(float)),2)
            if str(corr) != "nan":
                st.markdown(f"Correlation between <b>{x_axis.replace('x: ','')}</b> and <b>{y_axis.replace('y: ','')}</b> is : <b>{corr}</b>",
                            unsafe_allow_html=True)
        except ValueError:
            print("Error catched")
            pass
        fig = px.scatter(df, x=x_axis.replace('x: ',''),
                  y=y_axis.replace('y: ',''), title=f"{x_axis.replace('x: ','')} / {y_axis.replace('y: ','')}")
        
        st.plotly_chart(fig)
        st.header('Happiness Rank over 2015 until 2022')
        try:
            if not check_boxes['All']:
                st.dataframe(overall_df[overall_df['Region'].isin(filtered_region)].groupby('Country')['Happiness Rank'].describe() )
            else:
                st.dataframe(get_desc_by_country(overall_df))
        except KeyError:
            pass

        st.write("""<small>
                    <b>Count:</b> It refers to the count number of observations (for example: Afghanistan 8 times and Angola 4 times from 2015 until 2022)
                    <br/>
                    <b>Mean:</b> The average rank
                    <br/>
                    <b>Std:</b> The standard deviation
                    <br/>
                    <b>Min:</b> Lowest Rank
                    <br/>
                    <b>Min:</b> Lowest Rank
                    <br/>
                    <b>25%:</b> The 25% percentile
                    <br/>
                    <b>50%:</b> The 50% percentile
                    <br/>
                    <b>75%:</b> The 75% percentile
                    <br/>
                    <b>Min:</b> Highest Rank
                    </small>
                    """
                 , unsafe_allow_html=True)
        
    else:
        st.markdown("<b>No Data, Please Change Filters</b>",
                    unsafe_allow_html=True)
    
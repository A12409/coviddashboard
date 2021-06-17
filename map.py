from library import *
from htmlData import *
import cgi

covid = pd.read_html('https://coronaclusters.in')
covid = covid[0]

links = []

htmldata = getdata('https://www.mohfw.gov.in/')
data = BeautifulSoup(htmldata, 'html.parser')

for link in data.find_all('a'):
    current_link = link.get('href')
    tar_link = link.get('target')
    if current_link.endswith('pdf') and tar_link == '_blank':
        links.append(current_link)
        if len(links) == 2:
            break

vaccine = tabula.read_pdf(links[1], pages=1)
vaccine = vaccine[1]

vaccine = vaccine.rename(
    columns={'Beneficiaries vaccinated': '1st Dose', 'Unnamed: 0': '2nd Dose', 'Unnamed: 1': 'Total vaccine'},
    inplace=False)
covid = covid.rename(columns={'State': 'State/UT'}, inplace=False)
# print(vaccine)

for i in range(1, len(vaccine['Total vaccine'])):
    vaccine.iloc[i, 2] = int(vaccine.iloc[i, 2].replace(',', ''))
    vaccine.iloc[i, 3] = int(vaccine.iloc[i, 3].replace(',', ''))
    vaccine.iloc[i, 4] = str(vaccine.iloc[i,4]).replace(',','')

vaccine = vaccine.drop(labels=[0], axis=0)

vaccine['1st Dose'] = vaccine['1st Dose'].astype(int)
vaccine['2nd Dose'] = vaccine['2nd Dose'].astype(int)
vaccine['Total vaccine'] = vaccine['Total vaccine'].astype(int)

rename_state = {'Jammu & Kashmir': 'Jammu and Kashmir',
                'Punjab*': 'Punjab',
                'A & N Islands': 'Andaman and Nicobar Islands',
                'Chhattisgarh*': 'Chhattisgarh',
                'Daman & Diu': 'Daman and Diu',
                'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli and Daman and Diu'}

for sname in rename_state:
    vaccine['State/UT'] = vaccine['State/UT'].replace([sname], rename_state[sname])

covidframe = pd.merge(covid, vaccine, on='State/UT')

for i in range(1, 11):
    covidframe.iloc[10, i] = covidframe.iloc[16, i] + covidframe.iloc[10, i]

covidframe = covidframe.drop(labels=[16], axis=0)
covidframe = covidframe.drop(labels=['Last Updated', 'S. No.'], axis=1)

india_states = json.load(open('states_india.geojson', 'r'))

state_id_map = {}
for feature in india_states['features']:
    feature['id'] = feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']] = feature['id']
# state_id_map


covid_states = {'Delhi': 'NCT of Delhi',
                'Jammu and Kashmir': 'Jammu & Kashmir',
                'Andaman and Nicobar Islands': 'Andaman & Nicobar Island',
                'Arunachal Pradesh': 'Arunanchal Pradesh',
                'Dadra and Nagar Haveli and Daman and Diu': 'Dadara & Nagar Havelli',
                'Daman and Diu': 'Daman & Diu'}

for state in covid_states:
    covidframe['State/UT'] = covidframe['State/UT'].replace([state], covid_states[state])

# for i in covidframe['State/UT']:
#     if i not in state_id_map:
#         print(i)

covidframe['id'] = covidframe['State/UT'].apply(lambda x: state_id_map[x])

column = 'Total Deaths'
colour_dict = {'Total Deaths': px.colors.sequential.Reds,
               'Total vaccine': px.colors.sequential.Greens,
               'Total Recovered': px.colors.sequential.PuBu,
               'Active Cases': px.colors.sequential.Peach,
               'Total Cases': px.colors.sequential.Purples}

opacity_dict = {'Total Deaths': 0.8,
                'Total vaccine': 0.6,
                'Total Recovered': 0.6,
                'Active Cases': 0.8,
                'Total Cases': 0.6}
#
# fig = px.choropleth_mapbox(covidframe,
#                            locations='id',
#                            geojson=india_states,
#                            color=column,
#                            hover_name='State/UT',
#                            hover_data=[column],
#                            mapbox_style='carto-positron',
#                            center={'lat': 24, 'lon': 78},
#                            color_continuous_scale=colour_dict[column],
#                            opacity=opacity_dict[column],
#                            zoom=3)
# # return fig
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     dcc.Graph(id="graph", figure=fig),
# ])
#
# if __name__ == "__main__":
#     app.run_server(debug=True)

# fig.show()


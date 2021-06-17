from library import *

covid_data_complete = pd.read_csv(r"covid_19_india.csv", index_col=False)
covid_data_complete['Active'] = covid_data_complete['Confirmed'] - (
            covid_data_complete['Cured'] + covid_data_complete['Deaths'])

dic = {'Cured': ['Sno', 'Time', 'ConfirmedIndianNational', 'ConfirmedForeignNational', 'Confirmed', 'Deaths', 'Active'],
       'Confirmed': ['Sno', 'Time', 'ConfirmedIndianNational', 'ConfirmedForeignNational', 'Cured', 'Deaths', 'Active'],
       'Deaths': ['Sno', 'Time', 'ConfirmedIndianNational', 'ConfirmedForeignNational', 'Confirmed', 'Cured', 'Active'],
       'Active': ['Sno', 'Time', 'ConfirmedIndianNational', 'ConfirmedForeignNational', 'Confirmed', 'Deaths', 'Cured']
       }


def covid_frame(column):
    covid_data = covid_data_complete.copy()  # make a copy for analysis
    covid_data.drop(covid_data[dic[column]], axis=1, inplace=True)

    covid_data.columns = ['Date', 'States', column]  # rename columns
    return covid_data.pivot_table(column, ['Date'], 'States')


cured = covid_frame('Cured')
confirmed = covid_frame('Confirmed')
deaths = covid_frame('Deaths')
active = covid_frame('Active')

state_wise_data = covid_data_complete[['State/UnionTerritory', 'Date', 'Confirmed', 'Deaths', 'Active', 'Cured']]
state_wise_data['Date'] = pd.to_datetime(state_wise_data['Date'], dayfirst=True)

date_wise_data = state_wise_data.groupby(["Date"]).sum().reset_index()

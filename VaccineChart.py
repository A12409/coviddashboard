from library import *

covid_vaccine = pd.read_csv(r"covid_vaccine_statewise.csv")

covid_vaccine = covid_vaccine[['State', "Updated On", "First Dose Administered", "Second Dose Administered"]]
covid_vaccine['Updated On'] = covid_vaccine['Updated On'].apply(pd.to_datetime, dayfirst=True)
date_wise_vaccine_data = covid_vaccine.groupby(["Updated On"]).sum().reset_index()

dic = {'First Dose Administered': ['Second Dose Administered'],
       'Second Dose Administered': ['First Dose Administered']}


def vacframe(column):
    vacdata = covid_vaccine.copy()  # make a copy for analysis
    vacdata.drop(vacdata[dic[column]], axis=1, inplace=True)

    vacdata.columns = ['States', 'Date', column]  # rename columns
    return vacdata.pivot_table(column, ['Date'], 'States')


firstdose = vacframe('First Dose Administered')
secounddose = vacframe('Second Dose Administered')

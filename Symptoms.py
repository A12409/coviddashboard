from library import *

symptoms = {'symptom': ['Fever',
                        'Dry cough',
                        'Fatigue',
                        'Sputum production',
                        'Shortness of breath',
                        'Muscle pain',
                        'Sore throat',
                        'Headache',
                        'Chills',
                        'Nausea or vomiting',
                        'Nasal congestion',
                        'Diarrhoea',
                        'Haemoptysis',
                        'Conjunctival congestion'],
            'percentage': [87.9, 67.7, 38.1, 33.4, 18.6, 14.8, 13.9, 13.6, 11.4, 5.0, 4.8, 3.7, 0.9, 0.8]}

symptoms = pd.DataFrame(data=symptoms, index=range(14))

fig = px.bar(symptoms[['symptom', 'percentage']].sort_values('percentage', ascending=False),
             x="percentage", y="symptom", color='symptom', color_discrete_sequence=px.colors.cyclical.IceFire
             , title='Symptom of Coronavirus', orientation='h')
fig.update_layout(plot_bgcolor='rgb(275, 270, 273)')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.update_layout(barmode='stack')
fig.update_layout(font=dict(color='#7FDBFF'), plot_bgcolor='rgb(275, 270, 273)', yaxis_title='Symptoms', xaxis_title='Percentages')
fig.update_layout(template='plotly_white')
fig.update_layout(paper_bgcolor='#111111')
fig.update_layout(plot_bgcolor='#111111')

# -*- coding: utf-8 -*-
import plotly.express as px
import pandas as pd
import requests

from local import get_backend_location

def sort_by_quarter(response_array):
  return sorted(response_array, key=lambda x: (x['Year'], x['Quarter']))

def get_reporting_trends():
  """
  Return a plotly graph for the trends in reporting of cases.
  """
  response = requests.get(f'{get_backend_location()}/api/getResponses', json=["Quarter", "Year", "CasesNotReferredToPolice", "CasesReferredToPolice"])
  sorted_data = sort_by_quarter(response.json())
  restructured_data = {}
  for datum in sorted_data:
    quarter = f"Q{datum['Quarter']} {datum['Year']}"
    thisQuarter = restructured_data.get(quarter, {
      'Quarter': quarter,
      'Cases Handled': 0,
      'Cases Not Referred To Police': 0,
      'Cases Referred To Police': 0
    })
    thisQuarter['Cases Handled'] = thisQuarter['Cases Handled'] + datum['CasesNotReferredToPolice'] + datum['CasesReferredToPolice']
    thisQuarter['Cases Referred To Police'] = thisQuarter['Cases Referred To Police'] + datum['CasesReferredToPolice']
    thisQuarter['Cases Not Referred To Police'] = thisQuarter['Cases Not Referred To Police'] + datum['CasesNotReferredToPolice']
    restructured_data[quarter] = thisQuarter
  sorted_df = pd.DataFrame(data=restructured_data.values())
  melted_sorted_df = pd.melt(sorted_df, id_vars=['Quarter'], value_vars=['Cases Handled', 'Cases Referred To Police', 'Cases Not Referred To Police'], value_name='Number of Cases', var_name='Reported')

  return px.line(melted_sorted_df, x="Quarter", y='Number of Cases', color='Reported', title="Disparity in cases reported to police")

def get_reasons_not_reported():
  """
  Return a plotly graph for the reasons why cases haven't been reported to the police.
  """
  response = requests.get(f'{get_backend_location()}/api/getResponses', json=["NoReportReason", "Quarter", "Year"])
  sorted_data = sort_by_quarter(response.json())
  restructured_data = []
  for datum in sorted_data:
    dict = {
      'Quarter': f"Q{datum['Quarter']} {datum['Year']}"
    }
    for key, value in datum['NoReportReason'].items():
      dict[key] = value
    restructured_data.append(dict)
  sorted_df = pd.DataFrame(data=restructured_data)
  reasons = [
    'Client decision -  I do not trust police',
    'Client decision - I am afraid to go to the authorities',
    'Client decision - I just want the abuse to stop',
    'Client decision - I need someone to talk to confidentially without making a report',
    'Client decision - Police did not believe me before',
    'Not enough evidence',
    'Other'
  ]

  return px.bar(sorted_df, x="Quarter", y=reasons, barmode='group', title="Reasons for not reporting cases to the police")

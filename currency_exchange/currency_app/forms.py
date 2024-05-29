from django import forms
from datetime import date, datetime



# CURRENCY_CODES = {
#     'USD': 52148,
#     'EUR': 52170,
#     'GBP': 52146,
#     'TRY': 52158,
#     'JPY': 52246,
#     'INR': 52238,
#     'CNY': 52207
# }

class DateRangeForm(forms.Form):
    current_year = date.today().year
    current_date = datetime.now()
    years_range = range(current_year - 2, current_year + 1)
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=years_range), label='Начало периода')
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=years_range), initial=current_date, label='Конец периода')



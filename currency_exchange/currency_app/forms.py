## TODO 
## При синхронизации курса - взять курсы за каждую дату в таблицу
## Далее настроить синхронизацию и расчет 


from django import forms
from datetime import date, datetime

from .models import CurrencyRate

CURRENCY_CODES = [
    ('USD', 'Доллар'),
    ('EUR', 'Евро'),
    ('GBP', 'Фунт'),
    ('TRY', 'Лира'),
    ('JPY', 'Йена'),
    ('INR', 'Рупий'),
    ('CNY', 'Юань')
]

class DateRangeForm(forms.Form):
    current_year = date.today().year
    current_date = datetime.now()
    years_range = range(current_year - 2, current_year + 1)
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=years_range), label='Начало периода')
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=years_range), initial=current_date, label='Конец периода')




class RelativeChangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='End Date', widget=forms.SelectDateWidget)
    currency = forms.MultipleChoiceField(
        choices=CURRENCY_CODES,
        widget=forms.CheckboxSelectMultiple,
        label='Select Countries'
    )

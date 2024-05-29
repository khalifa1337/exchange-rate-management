from django.shortcuts import render
from .forms import DateRangeForm
from .utils import fetch_currency_rates, fetch_country_currencies, calculate_relative_changes
from .models import CurrencyRate, CountryCurrency, SyncParameter, RelativeChange

def index(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            currency_data = fetch_currency_rates(start_date, end_date)
            country_data = fetch_country_currencies()
            CurrencyRate.synchronize_currency_rates(currency_data)
            CountryCurrency.synchronize_country_currencies(country_data)

            # Сохранение параметров
            SyncParameter.objects.update_or_create(
                param_name='base_date', defaults={'param_value': start_date}
            )

            # Расчет относительных изменений и синхронизация
            relative_changes = calculate_relative_changes(start_date)
            RelativeChange.synchronize_relative_changes(relative_changes)

            return render(request, 'currency_app/success.html')
    else:
        form = DateRangeForm()
    return render(request, 'currency_app/index.html', {'form': form})



import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from .forms import RelativeChangeForm
from .models import RelativeChange

def relative_changes_view(request):
    if request.method == 'POST':

        form = RelativeChangeForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            selected_currency = form.cleaned_data['currency']
            print(selected_currency)
            # Получение данных о относительных изменениях для выбранных стран и диапазона дат
            relative_changes = RelativeChange.objects.filter(
                date__range=[start_date, end_date],
                currency__in=selected_currency
            )

            # Построение графика
            plt.figure(figsize=(10, 6))
            for currency in selected_currency:
                country_changes = relative_changes.filter(currency=currency)
                dates = [change.date for change in country_changes]
                values = [change.relative_change for change in country_changes]
                plt.plot(dates, values, label=currency)
            
            plt.xlabel('Date')
            plt.ylabel('Relative Change (%)')
            plt.title('Relative Changes in Currency Rates')
            plt.legend()
            plt.grid(True)

            # Сохранение графика в строку base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graphic = base64.b64encode(image_png)
            graphic = graphic.decode('utf-8')

            return render(request, 'currency_app/relative_changes.html', {
                'form': form,
                'graphic': graphic
            })
    else:
        form = RelativeChangeForm()

    return render(request, 'currency_app/relative_changes.html', {'form': form})

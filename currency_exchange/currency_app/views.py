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

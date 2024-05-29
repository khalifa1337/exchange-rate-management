from django.db import models, transaction

class CurrencyRate(models.Model):
    """
    Модель для хранения данных о курсах валют с сайта www.finmarket.ru.
    Так как с сайта можно получить таблицу, то помещаем в модель ее элементы.

    date - Дата актуальности курса.
    currency - Название валюты.
    rate - Курс обмена на актуальную дату.
    change - Измение валюты относительно предыдущего значения.
    """
    date = models.DateField()
    currency = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    change = models.DecimalField(max_digits=10, decimal_places=4)
    currency_code = models.IntegerField()
    class Meta:
        unique_together = ('date', 'currency')

    @staticmethod
    @transaction.atomic
    def synchronize_currency_rates(data):
        for entry in data:
            CurrencyRate.objects.update_or_create(
                date=entry['date'], currency=entry['currency'],
                defaults={'rate': entry['rate'], 'change': entry['change'], 'currency_code': entry['currency_code']}
            )

class CountryCurrency(models.Model):
    """
    Модель для хранения данных о списке валют с сайта www.iban.ru/currency-codes.


    country - Название страны.
    currency_name - Название валюты.
    currency_code - Текстовый код валюты.
    currency_number - Числовое значение кода.
    """
    country = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=4)
    currency_code = models.CharField(max_length=4)
    currency_number = models.IntegerField()

    @staticmethod
    @transaction.atomic
    def synchronize_country_currencies(data):
        for entry in data:
            CountryCurrency.objects.update_or_create(
                country=entry['country'],
                defaults={'currency_name': entry['currency_name'], 'currency_code': entry['currency_code'], 'currency_number': entry['currency_number']}
            )

class SyncParameter(models.Model):
    param_name = models.CharField(max_length=50, unique=True)
    param_value = models.DateField()


class RelativeChange(models.Model):
    date = models.DateField()
    currency = models.CharField(max_length=50)
    relative_change = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('date', 'currency')

    @staticmethod
    @transaction.atomic
    def synchronize_relative_changes(data):
        for entry in data:
            RelativeChange.objects.update_or_create(
                date=entry['date'], currency=entry['currency'],
                defaults={'relative_change': entry['relative_change']}
            )

import osa

def convert_curr(value, from_unit, to_unit):
    URL_curr = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
    client =osa.Client(wsdl_url=URL_curr)
    dist_params = dict(
        amount = value,
        fromCurrency = from_unit,
        toCurrency = to_unit,
        rounding = True)
    response = client.service.ConvertToNum(**dist_params)
    print(response)
    return response


with open('source_files/currencies.txt', 'r') as curr_data:
    x = curr_data.read().split('\n')
rub_spendings=[]
for each in x:
    each_travel = [(x) for x in each.split(' ')]
    rub_spendings.append(convert_curr(int(each_travel[1]), each_travel[2], 'RUB'))
print('Стоимость поездок в рублях: {0}'.format(sum(rub_spendings)))
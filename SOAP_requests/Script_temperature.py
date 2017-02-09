import osa

def convert_temp(temperature):
    URL_temps = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
    client =osa.Client(wsdl_url=URL_temps)
    temp_params = dict(
        Temperature = temperature,
        FromUnit = 'degreeFahrenheit',
        ToUnit = 'degreeCelsius')
    response = client.service.ConvertTemp(**temp_params)
    return round(response, 2)
convert_temp(20)

def average_temp(*args):
    average = round(sum(*args)/len(*args), 2)
    return average

with open('source_files/temps.txt', 'r') as temps_data:
    x = temps_data.read().split('\n')
daily_temps = []
for each in x:
    cels_temp = convert_temp(int(each.split(' ')[0]))
    daily_temps.append(cels_temp)
print(average_temp(daily_temps))
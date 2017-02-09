import osa

def convert(short):
    short = short.lower()
    f = dict(
    mm="Millimeters",
    cm="Centimeters",
    inc="Inches",
    ya="Yards",
    m="Meters",
    km="Kilometers",
    mi="Miles",
    nami="Nauticalmile",
    le="League"
    )
    return (f[short])

def convert_dist(value, from_unit):
    URL_dist = 'http://www.webservicex.net/length.asmx?WSDL'
    client =osa.Client(wsdl_url=URL_dist)
    dist_params = dict(
        LengthValue = value,
        fromLengthUnit = convert(from_unit),
        toLengthUnit = 'Kilometers')
    response = client.service.ChangeLengthUnit(**dist_params)
    return round(response, 2)
convert_dist(20, 'Mi')

with open('source_files/travel.txt', 'r') as travel_data:
    x = travel_data.read().split('\n')
travels = []
for each in x:
    each = each.replace(',','')
    each_travel = [(x) for x in each.split(' ')]
    km_distance = convert_dist(float(each_travel[1]), each_travel[2])
    travels.append(km_distance)
print('Суммарное расстояние в километрах {0}'.format(sum(travels)))
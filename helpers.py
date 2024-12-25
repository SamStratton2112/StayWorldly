import requests
from models import User
from flask import session

def get_city_search_results(city):
    city_res = []
    res = requests.get('https://api.api-ninjas.com/v1/city?name=', 
    params={'name': city}, headers={"X-Api-Key":"bq8QLL6Jp79EIBsYjBWTlA==K8KjTdI3vm5VyHRH"})
    city_data = res.json()
    for city in city_data:
            city_res.append({ "name":city['name']})
    return city_res

def get_city_details(city):
    res = requests.get('https://api.api-ninjas.com/v1/city?name=', params={'name': city}, headers={"X-Api-Key":"bq8QLL6Jp79EIBsYjBWTlA==K8KjTdI3vm5VyHRH"})
    city_data = res.json()
    print(city_data)
    city_info = city_data[0]
    city_name = city_info["name"]
    country_code = city_info["country"]
    city_country = find_key_by_value(country_codes, country_code)
    population = city_info["population"]
    city_lat = city_data[0]['latitude']
    city_long = city_data[0]['longitude']
    return {"name" : city_name, "country": city_country, "population": population, "lat" : city_lat, "long": city_long, "country_code" : country_code}

def get_city_photo(city_info):
    country_basics = requests.get(f'https://pixabay.com/api/?key=41953233-44daacb0d74b24b2c21cce044&q={city_info['country']}+{city_info['name']}&image_type=photo')
    photos = country_basics.json()
    image = photos['hits'][0]['webformatURL']
    return image

def get_country_details(city_info):
    if city_info["country_code"] not in ['US','AX','EH','WF','VI','VG','UM','TK','TL','SZ','SJ','SR','GS','SX','ST','ST','PM','MF','LC','KN','SH','BL','RE']: 
        # get country info
        country_info = requests.get('https://travel-info-api.p.rapidapi.com/country', params = {"country":city_info["country"]},headers={"X-RapidAPI-Key":"b2bd10d3d8msh9e611b03498c0d7p133fadjsn53cbcad402a5","X-RapidAPI-Host": "travel-info-api.p.rapidapi.com"})
        all_details = country_info.json()
        country_description= all_details['data']['info']

        # # get things to do info 
        country_activities = requests.get('https://travel-info-api.p.rapidapi.com/country-activities', params = {"country":f"{city_info["country"]}"},headers = { "X-RapidAPI-Key":"b2bd10d3d8msh9e611b03498c0d7p133fadjsn53cbcad402a5","X-RapidAPI-Host": "travel-info-api.p.rapidapi.com"})
        all_activities = country_activities.json()
        activities = all_activities['data']['activities']
        
        return country_description, activities
    else: 
        activities = [{'title': 'Coming Soon!', 'activity': ''}]
        country_description = 'Coming Soon!'
        return country_description, activities

def get_weather_tz(city_info):
    tz_weather_data = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_info['lat']},{city_info['long']}?key=9Z9PX7J5C7ZRC76D38PL4WFL8')
    data = tz_weather_data.json()
    timezone = data['timezone']
    tzoffset = data['tzoffset']
    description = data['days'][0]['description']
    temp = int(data['days'][0]['temp'])
    c_temp = int((temp-32)*5/9)
    # get user timezone info
    user = User.query.filter_by(username = session['username']).first()
    # prep string to become int
    user_tz_str = user.employer_timezone.replace(':', '').replace('00', '').replace(',', '')
    # pull numbers out of string 
    user_tz = user_tz_str[0:3] if user_tz_str[0] == '-' else user_tz_str[0:2]
    # calculate time difference 
    if len(user_tz)==3:
        # handle negative tz
        num = user_tz[1:]
        time_dif = (int(num)) - int(tzoffset)
    time_dif = int(user_tz) - int(tzoffset)
    return c_temp, temp, time_dif, user, timezone, description

def get_country_basics(city_info):
    country_link = requests.get(f'https://countryinfoapi.com/api/countries/name/{city_info['country']}')
    country_data = country_link.json()
    currencies = country_data['currencies']
    currency = str(currencies.keys()).replace("dict_keys(['","").replace("'])","")
    final_currency = currencies[currency]['name']
    curr = final_currency
    languages = country_data['languages'].values()
    driving = country_data['car']['side'].capitalize()
    return curr, languages, driving

def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key

country_codes= {'Afghanistan': 'AF',
 'Albania': 'AL',
 'Algeria': 'DZ',
 'American Samoa': 'AS',
 'Andorra': 'AD',
 'Angola': 'AO',
 'Anguilla': 'AI',
 'Antarctica': 'AQ',
 'Antigua and Barbuda': 'AG',
 'Argentina': 'AR',
 'Armenia': 'AM',
 'Aruba': 'AW',
 'Australia': 'AU',
 'Austria': 'AT',
 'Azerbaijan': 'AZ',
 'Bahamas': 'BS',
 'Bahrain': 'BH',
 'Bangladesh': 'BD',
 'Barbados': 'BB',
 'Belarus': 'BY',
 'Belgium': 'BE',
 'Belize': 'BZ',
 'Benin': 'BJ',
 'Bermuda': 'BM',
 'Bhutan': 'BT',
 'Bolivia, Plurinational State of': 'BO',
 'Bonaire, Sint Eustatius and Saba': 'BQ',
 'Bosnia and Herzegovina': 'BA',
 'Botswana': 'BW',
 'Bouvet Island': 'BV',
 'Brazil': 'BR',
 'British Indian Ocean Territory': 'IO',
 'Brunei Darussalam': 'BN',
 'Bulgaria': 'BG',
 'Burkina Faso': 'BF',
 'Burundi': 'BI',
 'Cambodia': 'KH',
 'Cameroon': 'CM',
 'Canada': 'CA',
 'Cape Verde': 'CV',
 'Cayman Islands': 'KY',
 'Central African Republic': 'CF',
 'Chad': 'TD',
 'Chile': 'CL',
 'China': 'CN',
 'Christmas Island': 'CX',
 'Cocos (Keeling) Islands': 'CC',
 'Colombia': 'CO',
 'Comoros': 'KM',
 'Congo': 'CG',
 'Congo, the Democratic Republic of the': 'CD',
 'Cook Islands': 'CK',
 'Costa Rica': 'CR',
 'Croatia': 'HR',
 'Cuba': 'CU',
 'Curaçao': 'CW',
 'Cyprus': 'CY',
 'Czech Republic': 'CZ',
 "Côte d'Ivoire": 'CI',
 'Denmark': 'DK',
 'Djibouti': 'DJ',
 'Dominica': 'DM',
 'Dominican Republic': 'DO',
 'Ecuador': 'EC',
 'Egypt': 'EG',
 'El Salvador': 'SV',
 'Equatorial Guinea': 'GQ',
 'Eritrea': 'ER',
 'Estonia': 'EE',
 'Ethiopia': 'ET',
 'Falkland Islands (Malvinas)': 'FK',
 'Faroe Islands': 'FO',
 'Fiji': 'FJ',
 'Finland': 'FI',
 'France': 'FR',
 'French Guiana': 'GF',
 'French Polynesia': 'PF',
 'French Southern Territories': 'TF',
 'Gabon': 'GA',
 'Gambia': 'GM',
 'Georgia': 'GE',
 'Germany': 'DE',
 'Ghana': 'GH',
 'Gibraltar': 'GI',
 'Greece': 'GR',
 'Greenland': 'GL',
 'Grenada': 'GD',
 'Guadeloupe': 'GP',
 'Guam': 'GU',
 'Guatemala': 'GT',
 'Guernsey': 'GG',
 'Guinea': 'GN',
 'Guinea-Bissau': 'GW',
 'Guyana': 'GY',
 'Haiti': 'HT',
 'Heard Island and McDonald Islands': 'HM',
 'Holy See (Vatican City State)': 'VA',
 'Honduras': 'HN',
 'Hong Kong': 'HK',
 'Hungary': 'HU',
 'Iceland': 'IS',
 'India': 'IN',
 'Indonesia': 'ID',
 'Iran, Islamic Republic of': 'IR',
 'Iraq': 'IQ',
 'Ireland': 'IE',
 'Isle of Man': 'IM',
 'Israel': 'IL',
 'Italy': 'IT',
 'Jamaica': 'JM',
 'Japan': 'JP',
 'Jersey': 'JE',
 'Jordan': 'JO',
 'Kazakhstan': 'KZ',
 'Kenya': 'KE',
 'Kiribati': 'KI',
 "Korea, Democratic People's Republic of": 'KP',
 'Korea, Republic of': 'KR',
 'Kuwait': 'KW',
 'Kyrgyzstan': 'KG',
 "Lao People's Democratic Republic": 'LA',
 'Latvia': 'LV',
 'Lebanon': 'LB',
 'Lesotho': 'LS',
 'Liberia': 'LR',
 'Libya': 'LY',
 'Liechtenstein': 'LI',
 'Lithuania': 'LT',
 'Luxembourg': 'LU',
 'Macao': 'MO',
 'Macedonia, the former Yugoslav Republic of': 'MK',
 'Madagascar': 'MG',
 'Malawi': 'MW',
 'Malaysia': 'MY',
 'Maldives': 'MV',
 'Mali': 'ML',
 'Malta': 'MT',
 'Marshall Islands': 'MH',
 'Martinique': 'MQ',
 'Mauritania': 'MR',
 'Mauritius': 'MU',
 'Mayotte': 'YT',
 'Mexico': 'MX',
 'Micronesia, Federated States of': 'FM',
 'Moldova, Republic of': 'MD',
 'Monaco': 'MC',
 'Mongolia': 'MN',
 'Montenegro': 'ME',
 'Montserrat': 'MS',
 'Morocco': 'MA',
 'Mozambique': 'MZ',
 'Myanmar': 'MM',
 'Namibia': 'NA',
 'Nauru': 'NR',
 'Nepal': 'NP',
 'Netherlands': 'NL',
 'New Caledonia': 'NC',
 'New Zealand': 'NZ',
 'Nicaragua': 'NI',
 'Niger': 'NE',
 'Nigeria': 'NG',
 'Niue': 'NU',
 'Norfolk Island': 'NF',
 'Northern Mariana Islands': 'MP',
 'Norway': 'NO',
 'Oman': 'OM',
 'Pakistan': 'PK',
 'Palau': 'PW',
 'Palestine, State of': 'PS',
 'Panama': 'PA',
 'Papua New Guinea': 'PG',
 'Paraguay': 'PY',
 'Peru': 'PE',
 'Philippines': 'PH',
 'Pitcairn': 'PN',
 'Poland': 'PL',
 'Portugal': 'PT',
 'Puerto Rico': 'PR',
 'Qatar': 'QA',
 'Romania': 'RO',
 'Russia': 'RU',
 'Rwanda': 'RW',
 'Réunion': 'RE',
 'Saint Barthélemy': 'BL',
 'Saint Helena, Ascension and Tristan da Cunha': 'SH',
 'Saint Kitts and Nevis': 'KN',
 'Saint Lucia': 'LC',
 'Saint Martin (French part)': 'MF',
 'Saint Pierre and Miquelon': 'PM',
 'Saint Vincent and the Grenadines': 'VC',
 'Samoa': 'WS',
 'San Marino': 'SM',
 'Sao Tome and Principe': 'ST',
 'Saudi Arabia': 'SA',
 'Senegal': 'SN',
 'Serbia': 'RS',
 'Seychelles': 'SC',
 'Sierra Leone': 'SL',
 'Singapore': 'SG',
 'Sint Maarten (Dutch part)': 'SX',
 'Slovakia': 'SK',
 'Slovenia': 'SI',
 'Solomon Islands': 'SB',
 'Somalia': 'SO',
 'South Africa': 'ZA',
 'South Georgia and the South Sandwich Islands': 'GS',
 'South Sudan': 'SS',
 'Spain': 'ES',
 'Sri Lanka': 'LK',
 'Sudan': 'SD',
 'Suriname': 'SR',
 'Svalbard and Jan Mayen': 'SJ',
 'Swaziland': 'SZ',
 'Sweden': 'SE',
 'Switzerland': 'CH',
 'Syria': 'SY',
 'Taiwan': 'TW',
 'Tajikistan': 'TJ',
 'Tanzania': 'TZ',
 'Thailand': 'TH',
 'Timor-Leste': 'TL',
 'Togo': 'TG',
 'Tokelau': 'TK',
 'Tonga': 'TO',
 'Trinidad and Tobago': 'TT',
 'Tunisia': 'TN',
 'Turkey': 'TR',
 'Turkmenistan': 'TM',
 'Turks and Caicos Islands': 'TC',
 'Tuvalu': 'TV',
 'Uganda': 'UG',
 'Ukraine': 'UA',
 'United Arab Emirates': 'AE',
 'United Kingdom': 'GB',
 'United States': 'US',
 'United States Minor Outlying Islands': 'UM',
 'Uruguay': 'UY',
 'Uzbekistan': 'UZ',
 'Vanuatu': 'VU',
 'Venezuela': 'VE',
 'Vietnam': 'VN',
 'Virgin Islands, British': 'VG',
 'Virgin Islands, U.S.': 'VI',
 'Wallis and Futuna': 'WF',
 'Western Sahara': 'EH',
 'Yemen': 'YE',
 'Zambia': 'ZM',
 'Zimbabwe': 'ZW',
 'Åland Islands': 'AX'}
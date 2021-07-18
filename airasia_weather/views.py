import json

# Create your views here.
import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from .forms import CityForm
from .models import City


def index(request):

    """ User can add the city by click in add city button

    Returns:
        Added list with Weather report

    """
    try:
                
        city_name = request.POST.get('city_name')
        url = settings.API_URL_CITY.format(city_name,settings.API_KEY)
        err_msg = ''
        message = ''
        message_class = ''

        if request.method == 'POST':
            form = CityForm(request.POST)

            if form.is_valid():
                new_city = form.cleaned_data['name']
                existing_city_count = City.objects.filter(name=new_city).count()
                
                if existing_city_count == 0:
                    r = requests.get(url.format(new_city)).json()

                    print("Im data" ,r['cod'] , r)
                    if r['cod'] == 200:
                        form.save()
                    else:
                        err_msg = 'City does not exist in the world!'
                else:
                    err_msg = 'City already exists in the database!'

            if err_msg:
                message = err_msg
                message_class = 'is-danger'
            else:
                message = 'City added successfully!'
                message_class = 'is-success'

        form = CityForm()

        cities = City.objects.all()

        weather_data = []

        for city in cities:

            city_weather = get_weather_city(city)

            if city_weather:
                weather_data.append(city_weather)

        context = {
            'weather_data' : weather_data, 
            'form' : form,
            'message' : message,
            'message_class' : message_class
        }

        return render(request, 'index.html', context)
    except Exception as e:
        print("Exception ocured")



def home(request):
    """Main page will render in this case and It will display the list of cities in the City Form
    and based on the selection weather data will display

    Args:
        Selection option based on the user input

    Returns:
        returns the final weather reports.

    """
    try:
            
        res = City.objects.all()

        json_res = []
        weather_data = []

        # Default data display
        
        for result in res:
            
            json_res.append(result)
        
        city_weather = get_weather_city(json_res[0])
        weather_data.append(city_weather)
        context = {
                        'weather_data' : weather_data, 
                        "city_names" : json_res,
                        # 'message' : message,
                        # 'message_class' : message_class
                    }


        # print("final data" ,data)
        if request.method == 'POST':
            
            selected_city = request.POST.getlist('city')
            
            # selected_city = request.data
            weather_data = []
            for city in selected_city:

                    city_weather = get_weather_city(city)

                    if city_weather:

                        weather_data.append(city_weather)

                    context = {
                        'weather_data' : weather_data, 
                        "city_names" : json_res,
                        
                    }

            print(selected_city , request.POST.getlist('city'))
            weather = get_weather_city(selected_city)
                        
            return render(request ,"selection_home.html" ,context)

        return render(request ,"selection_home.html" ,context)
    except Exception as e:
        print("Exception got occured:" ,e)



def delete_city(request, city_name):
    """
        This function will delete the city , based on the user input
    Args:
        
        city_name (String): City name

    Returns:
        It will delete the user input city from City table.

    """
    try:
            
        City.objects.get(name=city_name).delete()
        message = city_name + ' deleted successfully.!'
        message_class = 'is-success'
        weather_data ,json_res = get_default_data()
        context = {
            'weather_data' :weather_data,
            "city_names" : json_res,
            'message' : message,
            'message_class' : message_class
        }


        return render(request , 'selection_home.html' ,context)
    except Exception as e:
        print("Exception Occured" ,e)


def edit_city(request, city_name):

    """
        This function will update the city , based on the user input
    Args:
        
        city_name (String): City name

    Returns:
        It will update the user input city from City table.

    """

    try:
            

        City.objects.filter(name=city_name).update(name = city_name)
        message = city_name + ' Edited successfully.!'
        message_class = 'is-success'
        weather_data , json_res= get_default_data()
        context = {
            'weather_data':weather_data,
            "city_names" : json_res,
            'message' : message,
            'message_class' : message_class
        }
        

        return render(request ,"selection_home.html" ,context)

    except Exception as e:

        print("Exception Occured " ,e)


def get_weather_city(city_name):

    """
        This function will accepts the city name and get the weather report in API call and create Final dict


    Returns:
        
        retuns the final dict object to caller

    """

    try:
            
        url = settings.API_URL_CITY.format(city_name,settings.API_KEY)

        response = requests.get(url,verify=False)
        final_data = {}
        # if True:
        if response.status_code == 200:

            data = json.loads(response.text)
            # data = {'coord': {'lon': 76.6497, 'lat': 12.3072}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 301.15, 'feels_like': 302.71, 'temp_min': 301.15, 'temp_max': 301.15, 'pressure': 1011, 'humidity': 61}, 'visibility': 10000, 'wind': {'speed': 2.57, 'deg': 310}, 'clouds': {'all': 75}, 'dt': 1626508116, 'sys': {'type': 1, 'id': 9212, 'country': 'IN', 'sunrise': 1626482175, 'sunset': 1626528144}, 'timezone': 19800, 'id': 1262321, 'name': 'Mysore', 'cod': 200}

            # print("data" , data)
            final_data["logitude"] = data.get("coord",{}).get('lon',"")
            final_data["latitude"] = data.get("coord",{}).get('lat',"")
            final_data["city_name"] = data.get("name",{})
            final_data["description"] = data.get("weather")[0].get('description',"")
            final_data["country"] = data.get("sys",{}).get('country',"")
            final_data["temp"] = data.get("main",{}).get('temp',"")
            final_data['icon'] = data['weather'][0]['icon']
        
        else:
            print("Unable to fetch the details:::")
        
        return final_data


    except Exception as e:
        print("Exception Occured :" ,e)


def get_default_data():

    """
        This function will give the default weather reports to the pages.

    Returns:
        returns default city weather reports.

    """

    try:
            
        res = City.objects.all()

        json_res = []
        weather_data = []

        # Default data display
        
        for result in res:
            
            json_res.append(result)
        
        city_weather = get_weather_city(json_res[0])
        weather_data.append(city_weather)
        
        
        return weather_data , json_res
    except Exception as e:
        print("Exception occured" ,e)



@csrf_protect
def location(request):

    """
    
        This function will accepts the location details , such as longitude an latitude
        , in these two input genarate the weather reports.

    Returns:
        Weather dict
    """

    try:
            
        if request.method== "POST":
                
            longitude = request.POST.get("long")
            latitude = request.POST.get("lat")

            print("Longitide" , longitude , latitude)

            url = settings.API_URL_LOCATION.format(latitude,longitude,settings.API_KEY )

            response = requests.get(url,verify=False)
            final_data = {}
            # if True:
            if response.status_code == 200:

                data = json.loads(response.text)
                # data = {'coord': {'lon': 76.6497, 'lat': 12.3072}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 301.15, 'feels_like': 302.71, 'temp_min': 301.15, 'temp_max': 301.15, 'pressure': 1011, 'humidity': 61}, 'visibility': 10000, 'wind': {'speed': 2.57, 'deg': 310}, 'clouds': {'all': 75}, 'dt': 1626508116, 'sys': {'type': 1, 'id': 9212, 'country': 'IN', 'sunrise': 1626482175, 'sunset': 1626528144}, 'timezone': 19800, 'id': 1262321, 'name': 'Mysore', 'cod': 200}

                # print("data" , data)
                final_data["logitude"] = data.get("coord",{}).get('lon',"")
                final_data["latitude"] = data.get("coord",{}).get('lat',"")
                final_data["city_name"] = data.get("name",{})
                final_data["description"] = data.get("weather")[0].get('description',"")
                final_data["country"] = data.get("sys",{}).get('country',"")
                final_data["temp"] = data.get("main",{}).get('temp',"")
                final_data['icon'] = data['weather'][0]['icon']
            
            else:
                print("Unable to fetch the details:::")
            
            print("FInal url" ,final_data)

            return JsonResponse(list(str(final_data)) ,safe=False)
        else:
            return render(request ,"location.html")

    except Exception as e:
        print("Exception Occured: ",e)


def view_data(request):

    """
    this function will accepts the user input city and based on the city ,
    Weather reports will genarate 5 days / 3 hours.

    Returns:
        Final dict object

    """
    try:
            
        weather_data , json_res= get_default_data()

        if request.method== "POST":
                
            city_name = request.POST['city']

            final_ = get_5_days_data(city_name)
                    # print("Data" ,i['main']['temp'] ,i['main']['temp_max'] ,i['main']['humidity'] , i['weather'][0]['main'] ,i['weather'][0]['description'] ,i['weather'][0]['icon'] ,i['dt_txt'])
            context = {
                "weather_data" :final_,
                "city_names" : json_res,
                "city_name" : city_name,
            }
            print("Final data::;" ,final_)
            return render(request ,"view_weather.html",context)

        else:
            # weather_data , json_res= get_default_data()
            final_ = get_5_days_data(json_res[0])
            context = {
                'weather_data':final_,
                "city_names" : json_res,
                "city_name" : json_res[0],

            }
            return render(request ,"view_weather.html" ,context)
    except Exception as e:
        print("Exception occured" , e)


def get_5_days_data(city_name):

    """This function accept the user input as city name and perform the weather API action and 
    parse the data and create final dict

    Returns:
        Final dict object

    """

    try:
            
        url = settings.API_URL_5_DAY.format(city_name,settings.API_KEY )

        response = requests.get(url,verify=False)
        final_data = {}
        # if True:
        if response.status_code == 200:

            data = json.loads(response.text)

            res = data['list']
            final_ = []
            
            for i in res:
                dict_ = {
                    "temp" : i['main']['temp'],
                    "max_temp" : i['main']['temp_max'],
                    "humidity" : i['main']['humidity'],
                    "main" :i['weather'][0]['main'],
                    "description" : i['weather'][0]['description'] ,
                    "icon" : i['weather'][0]['icon'],
                    "timestamp" :  i['dt_txt']

                    }
                
                final_.append(dict_)
        
        return final_
    
    except Exception as e:
        print("Exception Occured" ,e)




########### Un useed code   ###############

def multiple_select(request):

    if request.method == "POST":
        multi = request.POST['multi']

        print("Multi values" ,multi)
        return JsonResponse( { "data" :"koosappa" })



# Un Used code and Testing purpose created
def index1(request):

    try:

        if request.method == "POST":
                
            print("Input data:::" , settings.STATIC_URL , request.POST.get('city_name'))
            city_name = request.POST.get('city_name')
            url = settings.API_URL_CITY.format(city_name,settings.API_KEY)

            response = requests.get(url,verify=False)
            final_data = {}
           
            if response.status_code == 200:

                data = json.loads(response.text)
                
                final_data["logitude"] = data.get("coord",{}).get('lon',"")
                final_data["latitude"] = data.get("coord",{}).get('lat',"")
                final_data["city_name"] = data.get("name",{})
                final_data["description"] = data.get("weather")[0].get('description',"")
                final_data["country"] = data.get("sys",{}).get('country',"")
                final_data["temp"] = data.get("main",{}).get('temp',"")
                final_data['icon'] = data['weather'][0]['icon']
                

            else:
                print("Unable to fetch the details from Weather API call...!!!!")
                

            print("FInal string" , final_data , type(final_data))

            

            # print("Context" ,context)
            return render(request , "index.html" ,{'context' : final_data })
        
        else:
            # print("im herer")
            # final_data = {'logitude': 76.6497, 'latitude': 12.3072, 'city_name': 'Mysore', 'description': 'broken clouds', 'country': 'IN', 'temp': 301.15, 'icon': '04d'}
            # context = {'weather': final_data }
            # context = {"abc" :"avnbvn"}
            return render(request , "index.html" )
    
    except Exception as e:

        print("Exception Ocuured ::" ,e )
        return render(request , "index.html")




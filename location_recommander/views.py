from django.shortcuts import render,redirect,HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from .models import History
from location_recommander.models import Contact
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from joblib import load
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import folium
from folium import IFrame
from django.templatetags.static import static
# Create your views here.

def home(request):
    if request.user.is_anonymous:
        return redirect('signup')

    readData=pd.read_csv("ezGeocode data of Ujjain.csv")
    lat_Ujjain = readData["Latitude"].mean()
    lon_Ujjain = readData["Longitude"].mean()
    place= readData["Address"].unique().tolist()

    ujjainArea_Color = {}
    for address in place:
        ujjainArea_Color[address] = "#%02X%02X%02X" % tuple(np.random.choice(range(256), size=3))


    Ujjain_map = folium.Map(location=[lat_Ujjain, lon_Ujjain], zoom_start=12)

    for lat, long, areaName in zip(readData["Latitude"],
                                    readData["Longitude"],
                                    readData["Address"]):
        label_text = areaName
        image_url1 = "http://localhost:8000"
        image_url2 = "/static/images/"+label_text+".jpg" 
        image_url =image_url1 + image_url2
        html = f"""
            <div>
                <strong>{label_text}</strong><br></br>
                <img src="{image_url}" alt="{label_text}" style="max-width:100%; max-height:100%;">
            </div>"""    
        image_label = folium.Popup(IFrame(html, width=320, height=240), max_width=500)

        folium.CircleMarker(
            [lat, long],
            radius = 5,
            popup = image_label,
            color = ujjainArea_Color[address],
            fill_color = ujjainArea_Color[address],
            fill_opacity = 0.7).add_to(Ujjain_map)
        
    context ={
         "Business_list": Business_list,
         "Ujjain_map": Ujjain_map._repr_html_(),
    }

    return render(request,'pridiction.html', context)

def signUp_User(request):
    if request.method=="POST":
        username = request.POST.get('username')
        useremail= request.POST.get('usernemail')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password!=password2 :
            messages.warning(request, "Your confirm password is not match !!")
            
        else:
            my_user = User.objects.create_user(username,useremail,password)
            my_user.save()
            return redirect ('login')
    return render(request ,'signup.html')
    
def login_User(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        # check if user has entered correct credentials
        user = authenticate(request,username=username, password=password)
        print(user)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("home")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_User(request):
    logout(request)
    return redirect('login')       

def about(request) :
    return render(request, 'about.html')


Business_list = load(open('Business_name.joblib','rb')) 
Ujjain_venues = load(open('My ujjain Venues.joblib','rb')) 
Venue_category = load(open('Venue Category with decimal variablr','rb')) 



def pred_result(request) :  
    if request.method == "POST":
        Business_name =request.POST["Business"]
        name = Venue_category[["Neighborhood",Business_name]]
        toclusters = 3
    
        to_clustering = name.drop(["Neighborhood"],axis=1)
        kmeans = KMeans(n_clusters=toclusters, random_state=1)
        kmeans.fit_transform(to_clustering)
        kmeans.labels_[0:20]
        to_merged = name.copy()
        to_merged["Cluster Labels"] = kmeans.labels_
        to_merged = to_merged.join(Ujjain_venues.set_index("Neighborhood"), on="Neighborhood")

        dict= {}
        for i in range(toclusters):
            list=to_merged.loc[(to_merged['Cluster Labels'] == i) & (to_merged['Venue Category'] == 'Pizzeria')]
            dict.update({i: len(list['Neighborhood'].to_list())} )

        sort_dict=dict
        pairs = {k: v for k, v in sorted(sort_dict.items(), key=lambda item: item[1])}

        x = next(iter(pairs))

        list=to_merged.loc[(to_merged['Cluster Labels'] == x)]
        result = list['Neighborhood'].unique().tolist()

        
        recom_areaMap = list.drop_duplicates(subset=['Neighborhood'],keep='first')

        lat_Ujjain = recom_areaMap["Neighborhood Latitude"].mean()
        lon_Ujjain = recom_areaMap["Neighborhood Longitude"].mean() 

        map_clusters = folium.Map(location=[lat_Ujjain, lon_Ujjain],zoom_start=14)

        markers_colors={0 :'red',1 :'blue',2 :'green'}

        for lat, lon, cluster, areaName in zip(recom_areaMap['Neighborhood Latitude'], recom_areaMap['Neighborhood Longitude'], recom_areaMap['Cluster Labels'],recom_areaMap['Neighborhood']):
    
            label_text = areaName
            image_url1 = "http://localhost:8000"
            image_url2 = "/static/images/"+label_text+".jpg" 
            image_url =image_url1 + image_url2
            html = f"""
            <div>
                <strong>{label_text}</strong><br></br>
                <img src= "{image_url}" alt="{label_text}" style="max-width:100%; max-height:100%;">
            </div>"""  
            image_label = folium.Popup(IFrame(html, width=320, height=240), max_width=500)
            folium.features.CircleMarker(
                [lat, lon],
                radius=5,
                popup = image_label,
                color =markers_colors[cluster],
                fill_color=markers_colors[cluster],
                fill_opacity=0.7).add_to(map_clusters)
        
            
        User_search= History.objects.create(user= request.user, Business_search=Business_name, result=result)
        User_search.save()
        return render(request, 'result.html', {'result': result, "map": map_clusters._repr_html_()})    
    

def contact(request) :
    if request.method == "POST" :
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        # Check if form data is valid
        if name and email and phone and desc:
            # Create Contact object and save it
            contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
            contact.save()
            messages.success(request, "Your message has been sent!")
            # return redirect('contact_success')  # Redirect to a success page
        else:
            messages.error(request, "Please fill in all fields.")
    
    # Handle GET request (render initial form page)
    return render(request, 'contact.html')               
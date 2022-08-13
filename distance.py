from tkinter import *
import tkintermapview
from geography import *
import googlemaps
import requests
from geopy.geocoders import Nominatim
from geopy import distance

geoCode = "********"
geocoder = Nominatim(user_agent="test")

num_markers = 0
markers = []
paths = []
coords = []
length = []

def add_distance(lat, long):
    global coords
    global length
    location = (lat, long)
    coords.append(location)
    if len(coords) > 1:
        length.append(distance.distance(coords[-1], coords[-2]))


def remove_distance():
    global length
    if len(length) > 0:
        length.pop()
    if len(coords) > 0:
        coords.pop()


def display_distance():
    global distance_label
    global length
    total_distance = 0
    if not length:
        distance_label.configure(text="Total distance: " + str(0) + " km", font=("Times New Roman", 30))
        return
    for measurement in length:
        measurement = float(str(measurement)[:-4])
        total_distance += measurement
    print_distance = str(total_distance)
    print_distance = print_distance[0:print_distance.index(".")+2]

    distance_label.configure(text="Total distance: " + str(print_distance)+" km", font = ("Times New Roman", 30))


def delete_last():
    global markers
    global num_markers
    if num_markers == 0:
        return
    markers[-1].delete()
    num_markers -= 1
    markers.pop()

    if len(paths) > 0:
        paths[-1].delete()
        paths.pop()
    remove_distance()
    display_distance()


def delete_all():
    global markers
    global num_markers
    for i in range(num_markers):
        delete_last()


def add_marker_event(coords):
    global num_markers

    num_markers += 1
    new_marker = map_widget.set_marker(coords[0], coords[1], text="Location " + str(num_markers))
    markers.append(new_marker)

    results = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(coords[0])+","+str(coords[1])+"&key="+geoCode
    try:
      new_marker.set_text(str(num_markers) + ". " + requests.get(results).json()["results"][1]['formatted_address'])
    except:
      new_marker.set_text(str(num_markers) + ". Ocean")
    add_distance(coords[0], coords[1])
    connect()
    display_distance()

def enter_pos():
    global num_markers
    num_markers += 1
    new_marker = map_widget.set_address(pos_entry.get(), marker=True)

    markers.append(new_marker)

    results = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(new_marker.position[0])+","+str(new_marker.position[1])+"&key="+geoCode
    try:
      new_marker.set_text(str(num_markers) + ". " + requests.get(results).json()["results"][1]['formatted_address'])
    except:
      new_marker.set_text(str(num_markers) + ". Ocean")
    add_distance(new_marker.position[0], new_marker.position[1])
    connect()
    display_distance()

def connect():
    global num_markers
    global markers
    if len(markers) < 2:
        return
    path = map_widget.set_path([markers[-1].position, markers[-2].position])
    paths.append(path)



window = Tk()
window.title('Distance Calculator')
window.geometry("800x800")

map_widget = tkintermapview.TkinterMapView(window, width=700, height=580, corner_radius=0)
map_widget.set_zoom(0)
map_widget.pack(side=BOTTOM, pady=20)

map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=add_marker_event,
                                        pass_coords=True)

clear_button = Button(window, text="Delete all markers", height=2, width=10, command=delete_all)
clear_button.place(x=630, y=140)

delete_button = Button(window, text="Delete last marker", height=2, width=10, command=delete_last)
delete_button.place(x=630, y=100)

distance_label = Label(window, text="Total distance: 0 km", font=("Times New Roman",40))
distance_label.pack(pady = 20)


prompt = Label(window, text = "Enter location", font = ("Times New Roman", 15))
prompt.place(x=45,y=100)
pos_entry = Entry(window)
pos_entry.place(x=45, y =120)

submit_button = Button(window, text="Submit", command = enter_pos)
submit_button.place(x=240,y=120)

geography_button = Button(window, text = "Country Facts", command = lambda:switch_geography(window))
geography_button.place(x = 650, y =20)
window.mainloop()

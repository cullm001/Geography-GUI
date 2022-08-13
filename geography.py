from tkinter import *
import tkintermapview
import wikipedia
import requests

global geowin
def switch_geography(window):
    global geowin
    geowin = window
    for widget in geowin.winfo_children():
        widget.destroy()
    geowin.title("Country Information")
    prompt = Label(geowin, text = "Enter Country", font = ("Times New Roman", 70))
    prompt.pack(pady =60)
    enter = Entry(geowin, width = 30, font = ("Times New Roman",40))
    enter.place(x=100, y = 140, height = 100)
    sub_country = Button(geowin, text ="Submit", font = ("Times New Roman",20),command=lambda: country_results(enter.get()))
    sub_country.pack(pady =50)

def country_results(country):
    global geowin

    wiki_country = country
    if wiki_country == "China":
        wiki_country = "People's Republic of China"
    elif wiki_country == "North Korea":
        wiki_country = "Democratic People's Republic of Korea"
    elif wiki_country == "Spain":
        wiki_country = "Kingdom of Spain"
    elif wiki_country == "Niger":
        wiki_country = "Niger."
    try:
        wiki_sum = wikipedia.summary(wiki_country)
        wiki_sum = wiki_sum[:wiki_sum.index("\n")]
    except:
        switch_geography(geowin)
        return

    for widget in geowin.winfo_children():
        widget.destroy()

    background = Label(geowin, bg="grey", width=80, height=42)
    background.place(x=35, y=90)


    country_sum = Message(geowin, bd = 10, padx = 15, pady=15, text = wiki_sum, width =600, fg = 'black', bg = 'grey', font = ("sans serif typeface", 15))
    country_sum.pack(side = BOTTOM, pady = 40)

    name = Label(geowin, text = country, font = ("Times New Roman", 60))
    name.pack(pady = 15)



    country_info = country.replace(' ','_').lower()

    url = "https://wikiapi.p.rapidapi.com/api/v1/wiki/geography/country/info/" + country_info

    querystring = {"lan": "en"}

    headers = {
        "X-RapidAPI-Key": "47b3bbf9e9mshca00fce1be9a05ap1493c9jsn18426af858dc",
        "X-RapidAPI-Host": "wikiapi.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    x_coord = 40
    y_coord = 140

    if response.text.find("government") != -1:
        government = response.text[response.text.index("government") + 13:]
        government = government[:government.index('"')]
        government_label = Label(geowin, text="Government: " + government, bg = "grey", fg = "black", font = ("Times New Roman",20))
        government_label.place(x=x_coord, y=y_coord)

        y_coord += 40

    if response.text.find("Monarch") != -1:
        monarch = response.text[response.text.index("Monarch") + 10:]
        monarch = monarch[:monarch.index('"')]
        monarch_label = Label(geowin, text="Monarch: " + monarch, bg = "grey", fg = "black", font = ("Times New Roman",20))
        monarch_label.place(x=x_coord, y=y_coord)
        y_coord += 40

    elif response.text.find("president") != -1:
        president = response.text[response.text.index("president\":") + 12:]
        president = president[:president.index('"')]
        president_label = Label(geowin, text="President: " + president, bg = "grey", fg = "black", font = ("Times New Roman",20))
        president_label.place(x=x_coord, y=y_coord)
        y_coord += 40

    if response.text.find("ethnic_groups") != -1:
        ethnic_groups = response.text[response.text.index("ethnic_groups") + 16:]
        limit = 10
        val = -1
        for i in range(0, limit):
            val = ethnic_groups.find(" ", val + 1)
        ethnic_groups = ethnic_groups[:val]

        ethnic_label = Label(geowin, text="Ethnic groups: " + ethnic_groups, bg = "grey", fg = "black", font = ("Times New Roman",20))
        ethnic_label.place(x=x_coord, y=y_coord)
        y_coord += 40

    if response.text.find("area\":") != -1:
        area = response.text[response.text.index("area\":") + 7:]
        area = area[:area.index(')') + 1]
        area_label = Label(geowin, text="Area: " + area, bg = "grey", fg = "black", font = ("Times New Roman",20))
        area_label.place(x=x_coord, y=y_coord)
        y_coord += 40

    if response.text.find("currency") != -1:
        currency = response.text[response.text.index("currency") + 11:]
        currency = currency[:currency.index(')')+1]
        currency_label = Label(geowin, text="Currency: " + currency, bg = "grey", fg = "black", font = ("Times New Roman",20))
        currency_label.place(x=x_coord, y=y_coord)
        y_coord += 40

    if response.text.find("population_estimate") != -1:
        population = response.text[response.text.index("population_estimate") + 22:]
        year = population[0:5]
        population = population[4:population.index('(')]
        population_label = Label(geowin, text=year + "Population: " + population + "people", bg = "grey", fg = "black", font = ("Times New Roman",20))
        population_label.place(x=x_coord, y=y_coord)
        y_coord += 40

    if response.text.find("gdp_nominal_year") != -1:
        gdpyear = response.text[response.text.index("gdp_nominal_year") + 19:]
        gdpyear = gdpyear[:gdpyear.index(' ')]

        gdp = response.text[response.text.index("gdp_nominal_total") + 20:]
        gdp = gdp[:gdp.index('(')]
        gdp_label = Label(geowin, text=gdpyear + " Nominal GDP: " + gdp, bg = "grey", fg = "black", font = ("Times New Roman",20))
        gdp_label.place(x=x_coord, y=y_coord)
        y_coord += 40

    search = Button(geowin, text = "Search Again", command = lambda:switch_geography(geowin))
    search.place(x = 630, y =20)




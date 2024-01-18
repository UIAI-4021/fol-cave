import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
from pyswip import Prolog
import pandas as pd


class App(tkinter.Tk):

    APP_NAME = "map_view_demo.py"
    WIDTH = 800
    HEIGHT = 750  # This is now the initial size, not fixed.

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Text area and submit button combined row
        self.grid_rowconfigure(1, weight=4)  # Map row

        # Upper part: Text Area and Submit Button
        self.text_area = tkinter.Text(self, height=5)  # Reduced height for text area
        self.text_area.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="nsew")

        self.submit_button = tkinter.Button(self, text="Submit", command=self.process_text)
        self.submit_button.grid(row=0, column=0, pady=(0, 10), padx=10, sticky="se")  # Placed within the same cell as text area

        # Lower part: Map Widget
        self.map_widget = TkinterMapView(self)
        self.map_widget.grid(row=1, column=0, sticky="nsew")

        self.marker_list = []  # Keeping track of markers
        self.marker_path = None


    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Text area can expand/contract.
        self.grid_rowconfigure(1, weight=0)  # Submit button row; doesn't need to expand.
        self.grid_rowconfigure(2, weight=3)  # Map gets the most space.

        # Upper part: Text Area and Submit Button
        self.text_area = tkinter.Text(self)
        self.text_area.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        
        self.submit_button = tkinter.Button(self, text="Submit", command=self.process_text)
        self.submit_button.grid(row=1, column=0, pady=10, sticky="ew")

        # Lower part: Map Widget
        self.map_widget = TkinterMapView(self)
        self.map_widget.grid(row=2, column=0, sticky="nsew")

        self.marker_list = []  # Keeping track of markers

    def check_connections(self, results):
        #print('result2 ', results)
        locations = []
        dfA = pd.read_csv('Adjacency_matrix.csv')
        prolog.retractall("directly_connected(_,_)")
        prolog.retractall("connected(_,_)")
        for result in results:
            city  = result["City"]
            locations.append(city)
            for index, row in dfA.iterrows():
                if row[city] == 1:
                    s = "directly_connected('"
                    s += city + "', '" + row['Destinations'] + "')"
                    print(s)
                    prolog.assertz(s)
            prolog.assertz("connected(X,Y) :- directly_connected(X,Z), directly_connected(Z,Y)")

            # TODO 5: create the knowledgebase of the city and its connected destinations using Adjacency_matrix.csv


        return locations

    def process_text(self):
        """Extract locations from the text area and mark them on the map."""
        text = self.text_area.get("1.0", "end-1c")  # Get text from text area
        locations = self.extract_locations(text)  # Extract locations (you may use a more complex method here)
        # TODO 4: create the query based on the extracted features of user desciption 
        ################################################################################################
        query = locations
        print('query = ',query)
        results = list(prolog.query(query))
        locations = self.check_connections(results)
        # TODO 6: if the number of destinations is less than 6 mark and connect them 
        ################################################################################################
        print(locations)
        locations = ['mexico_city','rome' ,'brasilia']
        self.mark_locations(locations)

    def mark_locations(self, locations):
        """Mark extracted locations on the map."""
        for address in locations:
            marker = self.map_widget.set_address(address, marker=True)
            if marker:
                self.marker_list.append(marker)
        self.connect_marker()
        self.map_widget.set_zoom(1)  # Adjust as necessary, 1 is usually the most zoomed out


    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if hasattr(self, 'marker_path') and self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def extract_locations(self, text):
        """Extract locations from text. A placeholder for more complex logic."""
        # Placeholder: Assuming each line in the text contains a single location name
        # TODO 3: extract key features from user's description of destinations
        ################################################################################################
        s = "destination(City, "
        dfD = pd.read_csv('Destinations.csv')
        S = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
        for index, row in dfD.iterrows():
            i = 0
            for column in row:
                if column in text:
                    S[i] = column
                i += 1
            # co = re = cl = bu = ac = de = du = cu = hi = na = ac = la = '_'
            # if row['country'] in text:
            #     S[0] = row['country']
            # if row['region'] in text:
            #     S[0] = row['region']
            # if row['Climate'] in text:
            #     S[0] = row['Climate']
            # if row['Budget'] in text:
            #     S[0] = row['Budget']
            # if row['Activity'] in text:
            #     S[0] = row['Activity']
            # if row['Duration'] in text:
            #     S[0] = row['Duration']
            # if row['Cuisine'] in text:
            #     S[0] = row['Cuisine']
            # if row['History'] in text:
            #     S[0] = row['History']
            # if row['Natural Wonder'] in text:
            #     S[0] = row['Natural Wonder']
            # if row['Accommodation'] in text:
            #     S[0] = row['Accommodation']
            # if row['Language'] in text:
            #     la = row['Language']
            # if row['Demographics'] in text:
            #     de = row['Demographics']
        # s += co + ',' + re + ',' + cl + ',' + bu + ','
        # s += ac + ',' + de + ',' + du + ',' + cu + ','
        # s += hi + ',' + na + ',' + ac + ',' + la + ')'
        for i in range(1, 12):
            if S[i] != '_':
                s += "" + S[i] + ", "
            else:
                s += "_, "
        if S[12] != '_':
            s += "" + S[i] + ")"
        else:
            s += "_)"
        return s

    def start(self):
        self.mainloop()

# TODO 1: read destinations' descriptions from Destinations.csv and add them to the prolog knowledge base
################################################################################################
# STEP1: Define the knowledge base of illnesses and their symptoms

prolog = Prolog()
dfD = pd.read_csv('Destinations.csv')
prolog.retractall("destination(_, _, _, _, _, _, _, _, _, _, _, _, _)")
for index, row in dfD.iterrows():
    s = "destination('"
    s += row['Destinations'].replace("'", "") + "', '" +  row['country'] + "', '" + row['region'] + "', '" + row['Climate'] + "', '" + row['Budget'] + "', '"
    s += row['Activity'] + "', '" + row['Demographics'] + "', '" + row['Duration'] + "', '" + row['Cuisine'] + "', '"
    s += row['History'] + "', '" + row['Natural Wonder'] + "', '" + row['Accommodation'] + "', '" + row['Language'] + "')"
    prolog.assertz(s)
# prolog.assertz("destination('Tokyo', japan, 'East Asia', temperate, high, cultural, solo, long, asian, modern, mountains, luxury, japanese)")
# prolog.assertz("destination('Ottawa', 'canada', 'North America', 'cold', 'medium', 'adventure', 'family_friendly', 'medium', 'european', 'modern', 'forests', 'mid_range', 'english')")
# prolog.assertz("destination('Mexico City', mexico, 'North America', temperate, low, cultural, senior, short, latin_american, ancient, mountains, budget, spanish)")
# prolog.assertz('destination("Rome", italy, "Southern Europe", temperate, high, cultural, solo, medium, european, ancient, beaches, luxury, italian)')
# prolog.assertz('destination("Brasilia", "brazil", "South America", "tropical", "low", "adventure", "family_friendly", "long", "latin_american", "modern", "beaches", "budget", "portuguese")')

# query = "destination(City, 'canada', 'North America', 'cold', 'medium', 'adventure', 'family_friendly', 'medium', 'european', 'modern', 'forests', 'mid_range', 'english')"
# results = list(prolog.query(query))
# for result in results:
#     print(result['City'])

# TODO 2: extract unique features from the Destinations.csv and save them in a dictionary
################################################################################################


if __name__ == "__main__":
    app = App()
    app.start()
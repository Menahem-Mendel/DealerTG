from json.decoder import JSONDecodeError
import json

import requests
from geopy import distance
from geopy.geocoders import Nominatim

geo_locator = Nominatim(user_agent="gtfftffygg")


class Location:

    def __init__(self, address: str = None, point: tuple = None, lang="en"):
        self.lang = lang
        self.point = point
        self.text = address
        self.__auto_fill()

    def __auto_fill(self):
        # I will fill automatically all locations details

        # Searching first for results localy
        local_results = self.__find_local()
        if local_results:
            self.load_from_json(local_results)
            return

        # Searching online by point or address
        if self.text:
            geo_results = geo_locator.geocode(
                self.text, addressdetails=True, language=self.lang)

        elif self.point:
            print(self.point)
            print(self.point[0] , self.point[1], "23")
            geo_results = geo_locator.reverse(
                self.point[0] + ", " + self.point[1], language=self.lang)
        else:
            # Sumthing went wrong so i set is_valid to false and quit
            self.is_valid = False
            return

        if geo_results is None:
            # Sumthing went wrong so i set is_valid to false and quit
            self.is_valid = False
            return
        # Loading geo results to the class
        self.raw = geo_results.raw
        self.__load_geo_results()

    def __find_local(self):
        # Searching for results in history
        self.__load_db()
        if self.point is not None:
            res = self.db['points'].get(str(self.point))
            if res is not None:
                return res

        elif self.text is not None:
            res = self.db['addresses'].get(self.text)
            if res is not None:
                return res

    def __load_geo_results(self):
        # Loads geo raw results in to the class
        self.is_valid = True
        if self.raw.get("address") is None:
            self.is_valid = False
            return

        address = self.raw['address']
        self.city = address.get("city")
        if self.city is None:
            self.city = address.get("village")

        if self.city is None:
            self.city = address.get("town")

        self.point = (self.raw['lat'], self.raw['lon'])
        self.country = address['country'].replace("Palestinian Territory", "Israel")
        self.street = address.get("street")
        if self.street is None:
            self.street = address.get("road")
        self.__create_preview()
        self.set_json()

        # Saving new result to db
        self.db['points'][str(self.point)] = self.to_json
        self.db['addresses'][self.text] = self.to_json
        self.__save_db()

    def __create_preview(self):
        # Creates preview string of location
        if self.is_valid:
            preview = ""
            print("creating preview", self.street,self.city,self.country)
            print(self.raw)
            if self.street:
                preview = self.street + " " + self.city
            elif self.city:
                preview = self.city + " " + self.country
            else:
                preview = self.country
            self.preview = preview

    def set_json(self):
        to_json = {
            "preview": self.preview,
            "raw": self.raw,
            "street": self.street,
            "city": self.city,
            "country": self.country,
            "point": self.point,
            "is_valid": self.is_valid
        }
        self.to_json = to_json

    def load_from_json(self, loc):
        self.preview = loc.get("preview")
        self.raw = loc.get("raw")
        self.street = loc.get("street")
        self.city = loc.get("city")
        self.cuntry = loc.get("country")
        self.point = loc.get("point")
        self.is_valid = loc.get("is_valid")
        self.to_json = loc

    def fix_city_name(self, city):
        results = requests.get("https://www.google.com/maps/place/" + city)
        data = results._content.decode("utf-8")
        ncity = data.split("""property="og:title">""")[0].split('<meta content=')[-1]
        rep1 = "'" + '"'
        rep2 = '" ' + "'"
        ncity = ncity.replace(rep1, "")
        ncity = ncity.replace(rep2, "")
        if "Google Maps" in ncity:
            print("faild fixing")
            return city
        print("fixd", city, ncity)
        return ncity

    def __load_db(self):
        # Loading db file
        try:
            with open(self.lang + "-world.json", "r") as file:
                self.db = json.load(file)
        except FileNotFoundError:
            self.db = {"points": {}, "addresses": {}}
        except JSONDecodeError:
            self.db = {"points": {}, "addresses": {}}
            print("crupted location file")

    def __save_db(self):
        # Updating db file
        with open(self.lang + "-world.json", "w") as file:
            file.write(json.dumps(self.db))

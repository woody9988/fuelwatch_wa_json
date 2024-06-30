import json
import random
import requests
from datetime import datetime
from xml.etree import ElementTree

product_map = {
    1: "Unleaded Petrol",
    2: "Premium Unleaded",
    4: "Diesel",
    5: "LPG",
    6: "98 RON",
    10: "E85",
    11: "Brand Diesel"
}



class FuelWatch:
    def __init__(self):
        self.url = "http://fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS"
        self.product = None
        self.region = None
        self.brand = None
        self.suburb = None
        self.day = None
        self.json_format1 = {}
        self.json_format2 = {}
        self._xml = None
        self._raw = None

    @staticmethod
    def user_agent():
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
        ]
        agent = random.choice(user_agents)

        return agent
    
    def query(self):
        try:
            payload = {
                "Product": self.product,
                "Suburb": self.suburb,
                "Region": self.region,
                "Brand": self.brand,
                "Day": self.day,
            }
            response = requests.get(
                self.url,
                timeout=30,
                params=payload,
                headers={"User-Agent": self.user_agent()},
            )
            if response.status_code == 200:
                self._raw = response.content
                return True
            else:
                msg=f"Failed to get valid response from fuelwatcher website. Response: {response.status_code}",
                print(msg)
                return False
        except Exception as e:
            print(e)
            return False
        
    @property
    def format1(self):
        dom = ElementTree.fromstring(self._raw)
        items = dom.findall("channel/item")

        for elem in items:
            trading_name = elem.find("trading-name").text
            description = elem.find("description").text
            brand = elem.find("brand").text
            location = elem.find("location").text
            address = elem.find("address").text
            phone = elem.find("phone").text
            latitude = elem.find("latitude").text
            longitude = elem.find("longitude").text
            site_features = elem.find("site-features").text
            price = elem.find("price").text
            fw_date = elem.find("date").text

            if trading_name in self.json_format1:
                self.json_format1[trading_name][self.day][product_map[self.product]] = price
                if self.day == "today":
                    self.json_format1[trading_name]['combo'][product_map[self.product]] = price
                elif self.day == "tomorrow":
                    yesterday = self.json_format1[trading_name]['today'][product_map[self.product]]
                    self.json_format1[trading_name]['combo'][product_map[self.product]] = str(yesterday) + " / " + str(price)
                    self.json_format1[trading_name][self.day]['date'] = fw_date
            else:
                site = {}
                site['trading_name'] = trading_name
                site['description'] = description
                site['brand'] = brand
                site['location'] = location
                site['address'] = address
                site['phone'] = phone
                site['latitude'] = latitude
                site['longitude'] = longitude
                site['site_features'] = site_features
                site['today'] = {}
                site['tomorrow'] = {}
                site['combo'] = {}

                site[self.day][product_map[self.product]] = price
                site[self.day]['date'] = fw_date

                if self.day == "today":
                    site['combo'][product_map[self.product]] = price
                elif self.day == "tomorrow":
                    yesterday = site['combo'][product_map[self.product]]
                    site['combo'][product_map[self.product]] = str(yesterday) + " / " + str(price)
                self.json_format1[trading_name] = site
        return True
    
    @property
    def format2(self):
        servos = []

        self.json_format2['prices_last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.json_format2['stations'] = []

        for key, value in self.json_format1.items():
            servos.append(value)
        self.json_format2['stations'] = servos

        return True
    
    
    def write_json(self, json_object, filename):
        try:
            with open(filename, 'w') as file_out:
                try:
                    json.dump(json_object, file_out)
                except:
                    print("Error writing JSON data to disk")
        except:
            print("Problem opening JSON file")
# Copyright (C) 2022 Alteryx, Inc. All rights reserved.
#
# Licensed under the ALTERYX SDK AND API LICENSE AGREEMENT;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.alteryx.com/alteryx-sdk-and-api-license-agreement
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example pass through tool."""
import re
from typing import List, Optional, TYPE_CHECKING

from ayx_python_sdk.core import (
    Anchor,
    PluginV2,
)
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

import pyarrow as pa
import requests
import jsonpath_rw_ext as jp_ext

class WeatherDistance(PluginV2):
    """A sample Plugin that passes data from an input connection to an output connection."""

    def __init__(self, provider: AMPProviderV2):
        self.name = "Weather Distance"
        self.provider = provider
        self.set_output = False 

        self.forecast_endpoint = "http://api.weatherapi.com/v1/forecast.json"
        self.weather_key = "[WeatherAPI Key Here]"

        self.distance_endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"
        self.origin = "San Francisco"
        self.units = "imperial"
        self.distance_key = "[Google Maps Key Here]"
        
        self.provider.io.info(f"{self.name} tool started")
        
    def on_incoming_connection_complete(self, anchor: Anchor) -> None:
        self.provider.io.info(
            f"Received complete update from {anchor.name}:{anchor.connection}."
        )

    def on_complete(self) -> None:
        self.provider.io.info(f"{self.name} tool done.")

    def on_record_batch(self, table: "pa.Table", anchor: Anchor) -> None:
        destinations = []

        for batch in table.to_batches():
            d = batch.to_pydict()

            if d.get('City') == None:
                self.provider.io.error("No column named City in in batch")
                return

            for city in zip(d['City']):
                if (city[0] == None):
                    continue
                dest = city[0]
                dayKeys =  ["daily_chance_of_rain", "totalprecip_in", "mintemp_f", "maxtemp_f", "maxwind_mph"]
                weather = self._get_weather(dest, dayKeys)
                distance = self._get_distance(dest)
                #self.provider.io.info("Got distance of %f, type %s" % (distance, type(distance)))
                destinations.append([dest,
                                     weather[dayKeys[0]] if weather[dayKeys[0]] != None else -1,
                                     weather[dayKeys[1]] if weather[dayKeys[1]] != None else -1,
                                     weather[dayKeys[2]] if weather[dayKeys[2]] != None else -1,
                                     weather[dayKeys[3]] if weather[dayKeys[3]] != None else -1,
                                     weather[dayKeys[4]] if weather[dayKeys[4]] != None else -1,
                                     distance])

        schema = pa.schema([
            pa.field("City", pa.string()),
            pa.field("ChanceOfRain", pa.int64()),
            pa.field("PrecipitationInches", pa.float64()),
            pa.field("MinTemp", pa.float64()),
            pa.field("MaxTemp", pa.float64()),
            pa.field("MaxWindMph", pa.float64()),
            pa.field("DistanceMiles", pa.float64())
        ])

        arrays = [[] for _ in schema]

        cst = {
            pa.string(): str,
            pa.int64(): int,
            pa.float64(): float,
            pa.null(): None,
        }

        for dest in destinations:
            arrays[0].append(cst[schema[0].type](dest[0]))
            arrays[1].append(cst[schema[1].type](dest[1]))
            arrays[2].append(cst[schema[2].type](dest[2]))
            arrays[3].append(cst[schema[3].type](dest[3]))
            arrays[4].append(cst[schema[4].type](dest[4]))
            arrays[5].append(cst[schema[5].type](dest[5]))
            arrays[6].append(cst[schema[6].type](dest[6]))

        batch = pa.RecordBatch.from_arrays(arrays, schema=schema)
        self.provider.write_to_anchor("Output", batch)  

    def _get_weather(self, destination, dayKeys: List[str]) -> dict:
        ret = {}

        params = {
            "q": destination,
            "days": 1,
            "key": self.weather_key
        }

        r = requests.get(self.forecast_endpoint, params)

        if r.status_code != 200:
            self.provider.io.warn("_get_weather(%s) received error response %d" % (q, r.status_code))
            for key in dayKeys:
                ret[key] = None
            return ret

        json = r.json()

        for key in dayKeys:
            match = jp_ext.match('forecast.forecastday[0].day.%s' % key, json)
            if (match and len(match) == 1):
                ret[key] = match[0]

        return ret

    def _get_distance(self, destinationCity) -> float:
        ret = -1.0

        params = {
            "destinations": destinationCity,
            "origins": self.origin,
            "units": self.units,
            "key": self.distance_key
        }
        r = requests.get(self.distance_endpoint, params)
        
        if r.status_code != 200:
            self.provider.io.error("get_distance received error response " + str(r.status_code))
            return ret

        json = r.json()
        match = jp_ext.match('$.rows[0].elements.[0].distance.text', json)

        if not match:
            self.provider.io.info("no match")
            return ret

        if (len(match) == 1):
            self.provider.io.info("match %s" % match[0])
            re_match = re.search('(?P<dist>(.+)) mi', match[0])
            if re_match:
                ret = float(re_match.group("dist"))
                self.provider.io.info("Got %f from %s" % (ret, match[0]))

        return ret

#
# Copyright 2014 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Performs requests to the Google Maps Distance Matrix API."""

from googlemaps import convert


def route_matrix(client, origins, destinations, travel_mode=None,
                 language_code=None, route_modifiers=None, units=None,
                 traffic_model=None, field_mask="*"):
    """ Gets travel distance and time for a matrix of origins and destinations.

    :param origins: One or more addresses, Place IDs, and/or latitude/longitude
        values, from which to calculate distance and time. placeId is preferred.
        Must be passed as a list of dict formatted as described in the documentation
        at https://developers.google.com/maps/documentation/routes/specify_location
        (e.g.
        [{'placeId': 'ChIJ3S-JXmauEmsRUcIaWtf4MzE'}]
        [{'location': {'latLng': 'latitude': 00.000000, 'longitude': 00.000000}}]
        ).
    :type origins: list of locations, where a location is a dict

    :param destinations: One or more addresses, Place IDs, and/or latitude/longitude
        values, from which to calculate distance and time. placeId is preferred.
        Must be passed as a list of dict formatted as described in the documentation
        at https://developers.google.com/maps/documentation/routes/specify_location
        (e.g.
        [{'placeId': 'ChIJ3S-JXmauEmsRUcIaWtf4MzE'}]
        [{'location': {'latLng': 'latitude': 00.000000, 'longitude': 00.000000}}]
        ).
    :type destinations: list of locations, where a location is a dict

    :param travel_mode: Specifies the mode of transport to use when calculating
        directions. One of "DRIVE", "BICYCLE", "WALK", "TWO_WHEELER", and "TRANSIT".
    :type travel_mode: string

    :param language_code: The language in which to return results.
    :type language_code: string

    :param route_modifiers:
        https://developers.google.com/maps/documentation/routes/route-modifiers
    :type route_modifiers: dict

    :param units: Specifies the unit system to use when displaying results.
        "METRIC" or "IMPERIAL"
    :type units: string

    :param traffic_model: Specifies the predictive travel time model to use.
        Valid values are "BEST_GUESS" or "OPTIMISTIC" or "PESSIMISTIC".
        The traffic_model parameter may only be specified for requests where
        the travel mode is driving, and where the request includes a
        departure_time.

    :rtype: matrix of distances. Results are returned in rows, each row
        containing one origin paired with each destination.
    """

    post_body = {
        'origins': origins,
        'destinations': destinations
    }

    if travel_mode:
        if travel_mode not in ["DRIVE", "BICYCLE", "WALK", "TWO_WHEELER", "TRANSIT"]:
            raise ValueError("Invalid travel mode.")
        post_body["travelMode"] = travel_mode

    if language_code:
        post_body["languageCode"] = language_code

    if route_modifiers:
        post_body["routeModifiers"] = route_modifiers

    if units:
        if units not in ['METRIC', 'IMPERIAL']:
            raise ValueError("Invalid units.")
        post_body["units"] = units

    if traffic_model:
        post_body["traffic_model"] = traffic_model

    return client._routes_request("/distanceMatrix/v2:computeRouteMatrix", post_body, field_mask=field_mask)

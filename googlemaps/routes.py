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

"""Performs requests to the Google Maps Directions API."""

from googlemaps import convert


def routes(client, origin, destination,
           travel_mode=None, waypoints=None, alternatives=False, route_modifiers=None,
           language_code=None, units=None, optimize_waypoints=True, field_mask="*"):
    """Get directions between an origin point and a destination point.

    :param origin: The address, latitude/longitude, or placeId value
        from which you wish to calculate directions. placeId is preferred.
        Must be passed as a dict formatted as described in the documentation
        at https://developers.google.com/maps/documentation/routes/specify_location
        (e.g.
        {'placeId': 'ChIJ3S-JXmauEmsRUcIaWtf4MzE'}
        {'location': {'latLng': 'latitude': 00.000000, 'longitude': 00.000000}}
        ).
    :type origin: dict

    :param destination: The address, latitude/longitude, or placeId value to which
        you wish to calculate directions. placeId is preferred.
        Must be passed as a dict formatted as described in the documentation
        at https://developers.google.com/maps/documentation/routes/specify_location
        (e.g.
        {'placeId': 'ChIJ3S-JXmauEmsRUcIaWtf4MzE'}
        {'address': 'New York City, NY'}
        {'location': {'latLng': 'latitude': 00.000000, 'longitude': 00.000000}}
        ).
    :type destination: dict

    :param travel_mode: Specifies the mode of transport to use when calculating
        directions. One of "DRIVE", "BICYCLE", "WALK", "TWO_WHEELER", and "TRANSIT".
    :type travel_mode: string

    :param waypoints: Specifies an array of waypoints. Waypoints alter a
        route by routing it through the specified location(s). See
        https://developers.google.com/maps/documentation/routes/reference/rest/v2/Waypoint
    :type waypoints: a list of locations, where a location is a dict

    :param alternatives: If True, more than one route may be returned in the
        response.
    :type alternatives: bool

    :param route_modifiers:
        https://developers.google.com/maps/documentation/routes/route-modifiers
    :type route_modifiers: dict

    :param language_code: The language in which to return results.
    :type language_code: string

    :param units: Specifies the unit system to use when displaying results.
        "METRIC" or "IMPERIAL"
    :type units: string

    :param optimize_waypoints: Optimize the provided route by rearranging the
        waypoints in a more efficient order.
    :type optimize_waypoints: bool

    :rtype: list of routes
    """

    post_body = {
        'origin': origin,
        'destination': destination
    }

    if travel_mode:
        if travel_mode not in ["DRIVE", "BICYCLE", "WALK", "TWO_WHEELER", "TRANSIT"]:
            raise ValueError("Invalid travel mode.")
        post_body["travelMode"] = travel_mode

    if waypoints:
        post_body["intermediates"] = waypoints
        if optimize_waypoints:
            post_body["optimizeWaypointOrder"] = "true"

    if alternatives:
        post_body["computeAlternativeRoutes"] = "true"

    if route_modifiers:
        post_body["routeModifiers"] = route_modifiers

    if language_code:
        post_body["languageCode"] = language_code

    if units:
        if units not in ['METRIC', 'IMPERIAL']:
            raise ValueError("Invalid units.")
        post_body["units"] = units

    return client._routes_request("/directions/v2:computeRoutes", post_body, field_mask=field_mask).get("routes", [])

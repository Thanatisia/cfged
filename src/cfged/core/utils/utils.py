"""
General Utilities class
"""
import os
import sys
import json

class JSON():
    def convert_json_to_dict(self, json_obj):
        # Initialize Variables
        json_dict = {}

        ## Check type of object
        if type(json_obj) == str:
            ## String object
            # Pass and convert the JSON string into a dictionary object
            json_dict = json.loads(json_obj)
        elif (type(json_obj) == list) or (type(json_obj) == dict):
            ## Non-String
            json_dict = json_obj

        # Return/Output
        return json_dict


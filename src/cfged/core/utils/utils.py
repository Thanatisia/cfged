"""
General Utilities class
"""
import os
import sys
import json

class Dictionary():
    """
    Key-Value Mappings (Dictionary, Maps, Associative Array) utilities
    """
    def traverse(self, data, results=None): 
        # Initialize Variables
        if results == None: results = []

        # Recursively iterate and traverse through the dictionary key-value (and sub-key values) 
        for k, v in data.items():
            # Check data type of value
            if isinstance(v, dict):
                # entries.append({k : v})
                # print("{0} : {1}".format(k, v))
                results.append(k)
                self.traverse(v, results)
            else:
                # print("{0} : {1}".format(k, v))
                # Append the value into the key-value results list
                results.append({k : v})

        # Return
        return results

    def key_lookup(self, dict_obj, *keys):
        """
        Get the values of all specified keys (and nested subkeys) within the provided dictionary (Key-Value mapping; aka HashMap, Map, Table, Associative Array)

        :: Params
        - dict_obj : The target Dictionary (Key-Value) mapping you wish to search from
            + Type: dict

        - keys : List of all configuration keys to pull from the set configs
            + Type: vargs
            - Format
                + String key (1 layer) : key_lookup("key-name")
                + nested Keys (multi-layer) : key_lookup(["parent-root-key", "nested-key-1", "nested-key-2", ...])
        """
        # Initialize Variables
        results = []

        # Iterate through the keys provided
        for i in range(len(keys)):
            # Get current key
            curr_key = keys[i]

            # Check the type of the key
            match curr_key:
                case list():
                    ## List element
                    parent_key = curr_key[0] # Get the root key
                    parent_root_val = dict_obj[parent_key] # Get the value mapped to the root key
                    nested_subkeys = curr_key[1:] # Get the child subkeys under the parent key

                    curr_res_val = ""
                    curr_subkey_val = parent_root_val

                    # Iterate the key and subkeys
                    for j in range(len(nested_subkeys)):
                        # Get current subkey
                        curr_subkey = nested_subkeys[j]

                        # Get the value of the current subkey
                        curr_subkey_val = curr_subkey_val[curr_subkey]

                        # Set the previous value as the current value
                        curr_res_val = curr_subkey_val
                case str():
                    ## String element
                    curr_res_val = dict_obj[curr_key]
                case _:
                    # Invalid type; Default
                    curr_res_val = ""

            # Append into results
            results.append(curr_res_val)

        return results


class JSON():
    """
    JSON-typed functionalities
    """
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


import os
import sys
from collections import OrderedDict
from ruamel.yaml import YAML, CommentedMap, CommentedSeq

class Tree:
    """
    To contain utilities for tree-like data structures that has branches and sub-branches (i.e. Binary Tree, Dictionaries, Nested Dictionaries, OrderedDict, CommentedMap etc)
    """

class RuamelYAML():
    """
    Contains utilities for handling ruamel.yaml objects
    """
    def __init__(self):
        self.yaml = YAML()

    class CommentedMap():
        """
        Functionalities involving CommentedMap()
        """

        class Polymorphism():
            """
            Type conversion from 1 type to another
            """

            def convert_to_dictionary(self, dataset, results=None):
                """
                Dig down and traverse through all branches and sub-branches within the CommentedMap and convert all occurences of the type to dict()
                """
                # Initialize Variables
                if results == None: results = {}

                """
                # Check if dataset is a list or a dictionary
                if isinstance(dataset, list) or isinstance(dataset, CommentedSeq):
                    # Loop through the dataset items and map to the results
                    # - convert the CommentedMap objects to dictionary
                    # - convert the CommentedSeq objects to list
                    for i in range(len(dataset)):
                        # Get current dataset
                        k = i
                        v = dataset[i]

                        # Process dataset type
                        if isinstance(v, CommentedMap):
                            results[k] = dict(v)
                            self.convert_to_dictionary(v, results)
                        elif isinstance(v, CommentedSeq):
                            results[k] = list(v)
                            self.convert_to_dictionary(v, results)
                        elif isinstance(v, dict):
                            self.convert_to_dictionary(v, results)
                        else:
                            results[k] = v
                elif isinstance(dataset, dict) or isinstance(dataset, CommentedMap):
                """
                # Loop through the dataset items and map to the results
                # - convert the CommentedMap objects to dictionary
                # - convert the CommentedSeq objects to list
                for k,v in dataset.items():
                    # Check if type of the value is CommentedMap
                    if isinstance(v, CommentedMap):
                        results[k] = dict(v)
                        # self.convert_to_dictionary(v, results)
                    elif isinstance(v, CommentedSeq):
                        results[k] = list(v)
                    elif isinstance(v, dict):
                        self.convert_to_dictionary(v, results)
                    else:
                        results[k] = v

                # Output/Return
                return results



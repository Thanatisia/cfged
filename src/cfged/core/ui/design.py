"""
cfged UI Designer library
"""
import os
import sys
import json
from rich import print, print_json
from rich.table import Table

class TableUI():
    """
    UI Core Components - Table
    """
    def __init__(self):
        self.table = Table() # Initialize Table class
        self.table_data = { "columns" : [], "rows" : [] } # Initialize empty table data

    def import_dict_data(self, data):
        """
        Import data from dictionary into table

        :: Parameter Signature/Headers
        - data : Pass the dictionary data you wish to import into the table column and rows
            + Type: Dictionary

        :: Notes
        - Table Formatting
            {
                "columns" : [column-1, column-2, ...],
                "rows" : { "column-1" : "cell-1", "column-2" : "cell-2" }
            }
        """
        # Initialize Variables
        table_data = { "columns" : [], "rows" : [{}] } # { "column" : [ "row-1", "row-2", ... ], ... }

        # Iterate through the JSON dictionary
        for k,v in data.items():
            # Data Validation: Null Value Check
            if not (k in table_data["columns"]):
                # New Column: Create mapping
                table_data["columns"].append(k)

            # Data Validation - Null Value Check
            if k == None:
                k = ""
                v = ""
            if v == None:
                v = ""

            # Check the value's type
            v_Type = type(v)
            if v_Type == dict:
                # Dictionaries
                for nested_k, nested_v in v.items():
                    print("{} = {}".format(nested_k, nested_v))

                    # Append the values into the list at the index
                    table_data["rows"][0][k] = str(nested_v)
            elif v_Type == list:
                # Lists
                for i in range(len(v)):
                    # Get current element
                    curr_element = v[i]
                    print("{} = {}".format(i,curr_element))

                    # Append the values into the list at the index
                    table_data["rows"][0][k] = str(curr_element)
            elif v_Type == str:
                # Strings
                # Append the values into the list at the index
                # json_keys["rows"].append({ k : v })
                # json_keys["rows"][idx][k] = v
                table_data["rows"][0][k] = v
            else:
                # Non-Iterable, Non-Strings
                # Append the values into the list at the index
                table_data["rows"][0][k] = str(v)

        # Output/Return
        return table_data

    def import_list_data(self, data):
        """
        Import data from a list into the table rows and column headers

        :: Parameter Signature/Headers
        - data : Pass the dictionary data you wish to import into the table column and rows
            + Type: List<Dictionary>

        :: Notes
        - Table Formatting
            {
                "columns" : [column-1, column-2, ...],
                "rows" : [
                    [ "cell-1", "cell-2", ..., ] == { "column-1" : "cell-1", "column-2" : "cell-2" }
                ]
            }
        """
        # Initialize Variables
        table_data = { "columns" : [], "rows" : [] } # { "column" : [ "row-1", "row-2", ... ], ... }

        # Iterate through the JSON list of dictionaries
        for i in range(len(data)):
            # Get current dictionary
            curr_json = data[i]

            # Initialize empty list for new row to populate
            table_data["rows"].append({})

            # Get current index
            number_of_rows = len(table_data["rows"])
            idx = number_of_rows-1
            if idx < 0: idx = 0

            # Iterate through the key-value mappings of the current JSON dictionary
            for k,v in curr_json.items():
                # Data Validation: Null Value Check
                if not (k in table_data["columns"]):
                    # New Column: Create mapping
                    table_data["columns"].append(k)

                # Data Validation - Null Value Check
                if k == None:
                    k = ""
                    v = ""
                if v == None:
                    v = ""

                # Append the values into the list at the index
                # json_keys["rows"].append({ k : v })
                # json_keys["rows"][idx][k] = v
                table_data["rows"][idx][k] = str(v)

        # Output/Return
        return table_data

    def import_dataset(self, data):
        """
        Process the provided datasets and check the type of object, import according to the type and return the table data
        """
        # Initialize Variables
        table_data = { "columns" : [], "rows" : [] } # { "column" : [ "row-1", "row-2", ... ], ... }

        ## Check type of object
        if type(data) == dict:
            # Import dictionary data to table values
            table_data = self.import_dict_data(data)
        elif type(data) == list:
            # Import list data to table values
            table_data = self.import_list_data(data)

        # Set to class variable/attribute/property
        self.table_data = table_data

        # Return/Output
        return table_data

    def add_columns(self, table_columns):
        """
        Add each element in the list of columns to the table's columns
        """
        ## Iterate the columns and map
        for column_name in table_columns:
            ## Add columns into the table
            self.table.add_column(column_name)

    def add_rows(self, table_rows, table_columns):
        """
        Add each element in a list containing all your rows and its individual cell values to the table cells

        :: Params
        - table_rows : Specify the list of rows to pass into the table
            + Type: List
            - Format
                [
                    [ "cell-1", "cell-2", ..., ] == { "column-1" : "cell-1", "column-2" : "cell-2" }
                ]

        - table_columns : Specify the list of columns to pass into the table to define the table's header/columns
            + Type: List
            - Format
                [column-1, column-2, ...],
        """
        ## Iterate through the rows
        for row_number in range(len(table_rows)):
            # Get current row
            curr_row = table_rows[row_number]

            # Initialize row values to be passed into the table
            row_values = []

            # Populate list with null values to fill all of the columns
            row_values = ["" for _ in range(len(table_columns))]

            ## Iterate current row
            for col_name, cell_value in curr_row.items():
                # Get header position of column
                col_idx = table_columns.index(col_name)

                # Modify value in the column position
                row_values[col_idx] = cell_value

            ## Add rows corresponding to the columns into the table
            self.table.add_row(*row_values)

    def design_table(self, json_obj:str|list|dict):
        """
        Populate table column and rows and return the complete table

        :: Params
        - json_obj : Specify the JSON string you wish to format into a table
            + Type: String | List | Dictionary
            - Format
                + '[{"Hello" : "World", "World" : "Hello"}, {"Hello" : "World"}, {"World" : "Hello"}]'

        :: Return
        - table : The resulting rich Table object after populated with Columns and Rows
            + Type: rich.table.Table()

        :: Notes

        """
        # Initialize Variables
        json_values = {}
        table_data = {}

        ## Check type of object
        if type(json_obj) == str:
            ## String object
            # Pass and convert the JSON string into a dictionary object
            json_values = json.loads(json_obj)
        elif (type(json_obj) == list) or (type(json_obj) == dict):
            ## Non-String
            json_values = json_obj

        print(type(json_values))

        # Import dataset into table data
        table_data = self.import_dataset(json_values)

        # Obtain table components
        table_columns = table_data["columns"]
        table_rows = table_data["rows"]

        # Design Table

        ## Add columns to table
        self.add_columns(table_columns)

        ## Add rows to table
        self.add_rows(table_rows, table_columns)

        # Return/Output
        return self.table


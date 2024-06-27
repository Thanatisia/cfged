"""
cfged UI Designer library
"""
import os
import sys
import json
from ruamel.yaml import YAML, safe_load as yaml_load, safe_dump as yaml_dump
from rich import print, print_json
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class UI():
    """
    UI Designing
    """
    def __init__(self):
        # Initialize a new console object to print the rich objects
        self.console = Console()

    def insert_tables_to_Panel(self, tables:list, column_opts=None, panel_fitting_opts=None):
        """
        Insert a given table group column into a panel
        """
        # Define variables
        if column_opts == None: column_opts = {}
        if panel_fitting_opts == None: panel_fitting_opts = {}

        # Create a column group containing the tables 
        column_grp_Tables = Columns(tables, **column_opts)

        # Create a panel and insert the table group arranged horizontally, side by side
        panel = Panel.fit(column_grp_Tables, title="Display Tables", border_style="blue", title_align="left", padding=(1,2), **panel_fitting_opts)

        # Return/Output
        return panel

    def print_console(self, obj, console=None):
        """
        Print the given object to the console
        """
        # Check if a console object is found
        if console == None:
            console = self.console

        # Print the object to the console standard output
        self.console.print(obj)

class TableUI():
    """
    UI Core Components - Table
    """
    def __init__(self):
        self.table = Table() # Initialize Table class
        self.table_data = { "columns" : [], "rows" : [] } # Initialize empty table data
        self.yaml = YAML()

    def import_dict_data(self, data, table_data=None):
        """
        Import data from dictionary into table

        :: Parameter Signature/Headers
        - data : Pass the dictionary data you wish to import into the table column and rows
            + Type: Dictionary

        :: Notes
        - Table Formatting
            {
                "columns" : [column-1, column-2, ...],
                "rows" : [[{ "column-1" : "cell-1", "column-2" : "cell-2" }], ...]
            }
        """
        # Initialize Variables
        if table_data == None: table_data = { "columns" : [], "rows" : [{}] } # { "column" : [ "row-1", "row-2", ... ], ... }

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
            if isinstance(v, dict):
                # Dictionaries
                print("Dictionaries: {}".format(v))

                # Initialize a new entry in the row if the eky doesnt exist
                if not (k in list(table_data["rows"][0].keys())):
                    table_data["rows"][0][k] = ""

                # Iterate through the dictionary mapping
                nested_v_values = []
                for nested_k, nested_v in v.items():
                    print("Nested K {} = Nested V {}".format(nested_k, nested_v))
                    nested_v_values.append(str(nested_v))

                # Append the values into the list at the index
                table_data["rows"][0][k] = '\n'.join(nested_v_values)

                # Repeat the function
                self.import_dict_data(v, table_data)
                print("New Row: {}".format(table_data))
            elif isinstance(v, list):
                # Lists
                print("List: {}".format(v))
                list_elements = []

                # Iterate through list value and place into temporary list
                for i in range(len(v)):
                    # Get current element
                    curr_element = v[i]
                    print("{} = {}".format(i,curr_element))

                    # Append the values into the list at the index
                    list_elements.append(str(curr_element))

                table_data["rows"][0][k] = '\n'.join(list_elements)
                print("New Row: {}".format(table_data))
            elif isinstance(v, str):
                # Strings
                print("key: {}".format(k))
                print("Strings: {}".format(v))

                # Append the values into the list at the index
                # json_keys["rows"].append({ k : v })
                # json_keys["rows"][idx][k] = v
                table_data["rows"][0][k] = v
                print("New Row: {}".format(table_data))
            else:
                # Non-Iterable, Non-Strings
                print("key: {}".format(k))
                print("Others: {}".format(v))

                # Append the values into the list at the index
                table_data["rows"][0][k] = str(v)
                print("New Row: {}".format(table_data))

            print("")

        print("Imported Table Data: {}".format(table_data))

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

    def design_table(self, dataset:str|list|dict, cfg_file_type="json"):
        """
        Populate table column and rows and return the complete table

        :: Params
        - dataset : Specify the dataset string/list/dictionary you wish to format and parse into a table
            + Type: String | List | Dictionary
            - Format
                + String: '[{"Hello" : "World", "World" : "Hello"}, {"Hello" : "World"}, {"World" : "Hello"}]'

        - cfg_file_type : Specify the configuration file format belonging to the dataset you want to parse
            + Type: String
            + Default: json
            - Supported values
                + json

        :: Return
        - table : The resulting rich Table object after populated with Columns and Rows
            + Type: rich.table.Table()

        :: Notes

        """
        # Initialize Variables
        converted_values = {}
        table_data = {}

        ## Check type of object
        if type(dataset) == str:
            ## String object
            ### The object is a dataset string that hasnt been converted to a python object
            ### - Check the provided file type and parse/convert accordingly
            match cfg_file_type.lower():
                case "json":
                    # Pass and convert the JSON string into a dictionary object
                    converted_values = json.loads(dataset)
                case "yaml":
                    # Pass and convert the YAML string into a dictionary object
                    converted_values = dict(self.yaml.load(dataset))
                case _:
                    converted_values = dataset
        elif (type(dataset) == list) or (type(dataset) == dict):
            ## Non-String
            converted_values = dataset

        # print("Converted Dataset: {} [{}] => {} [{}]".format(dataset, type(dataset), converted_values, type(converted_values)))

        # Import dataset into table data
        table_data = self.import_dataset(converted_values)

        print("Imported Table Data: {}".format(table_data))

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

    def generate_tables(self, dataset, tables=None):
        # Initialize Variables
        if tables == None: tables = []

        print("Dataset: {}".format(dataset))

        ## Check if current dataset's type is list or dictionary
        # if isinstance(dataset, list):
        """
        if isinstance(dataset, list):
            ## List
            # Iterate through the current dataset
            for i in range(len(dataset)):
                # Get the current root key and nested subkey-values
                curr_row = dataset[i]

                # Check value type
                if isinstance(curr_row, list):
                    print("{}".format(type(curr_row)))
                    self.generate_tables(curr_row, tables)
                if isinstance(curr_row, dict):
                    print("{}".format(type(curr_row)))
                    self.generate_tables(curr_row, tables)
                else:
                    print("{} : {}".format(i, curr_row))

                    # Design table and populate with column and rows
                    table = self.design_table(curr_row)

                    # Append current table to the list
                    tables.append(table)
        elif isinstance(dataset, dict):
            # Iterate through the current dataset
            for k,v in dataset.items():
                # Check value type
                if isinstance(v, list):
                    print("{}".format(type(v)))
                    self.generate_tables(v, tables)
                if isinstance(v, dict):
                    print("{}".format(type(v)))
                    self.generate_tables(v, tables)
                else:
                    print("{} : {}".format(k,v))

                    # Design table and populate with column and rows
                    table = self.design_table({k:v})

                    # Append current table to the list
                    tables.append(table)
        """

        # Design table and populate with column and rows
        table = self.design_table(dataset)

        print("Table Columns:")
        table_cols = table.columns
        for col in table_cols:
            print(col.header)
        print("Table Rows:")
        table_rows = table.rows
        for col in table_cols:
            print(list(col.cells))

        tables.append(table)

        # Output/Return
        return tables


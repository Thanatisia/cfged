"""
cfged : Configuration Buffer Reader, Viewer and Editor
"""
import os
import sys
import json
from ruamel.yaml import YAML, load, dump
from cfged.core.ui.design import print, Console, Columns, Panel, Table, UI, TableUI
from cfged.core.utils.utils import Dictionary
from cfged.core.utils.tree import RuamelYAML

def display_help():
    """
    Display Help Message
    """
    msg = """
## Documentations

### Synopsis/Syntax
- Default
    ```bash
    cfged {optionals} <arguments>
    ```

### Parameters
- Positionals
- Optionals
    - With Arguments
        - `-i | --input`: Specify a configuration file to import and print. Append this to add more files to print. 
            - NOTE
                + This will overwrite all instances of '--json-string'
                + Each file contents will be an individual table.
        - `--json-string`: Specify and import a JSON string into a JSON object. For every '--json-string' used, append into a list of all JSON strings
            - NOTE
                + This will overwrite all instances of '-i' | --input
                - When print-table is called,
                    - Iterate the list of all JSON strings, create a new table for each entry and print them all out
    - Flags
        + `-h | --help`: Display help
        + `-v | --version`: Display system version information
        + `--print-table`: Print the imported configuration file as a designed table

### Usages

> JSON

- Import a JSON configuration file and print it in a table format
    ```bash
    cfged -i dataset.json --print-table
    ```
- Import multiple JSON configuration files and print them in a table format (each)
    ```bash
    cfged -i dataset_1.json -i dataset_2.json -i dataset_3.json -i dataset_4.json ... -i dataset_N.json --print-table
    ```
- Import a JSON string for a dictionary key-value and print it in a table format
    ```bash
    cfged --json-string '{"key" : "value"}' --print-table
    ```
- Import a JSON string for a list of dictionary key-values and print it in a table format
    ```bash
    cfged --json-string '[{"key" : "value"}, {"key" : "value"}]' --print-table
    ```
    """
    print(msg)

def display_system_version():
    """
    System Version Information
    """
    msg = """
Executable Name: {}
Executable Path: {}
System Version: {}
    """.format(exec_name, exec_path, vers)
    print(msg.strip())

def init():
    """
    Perform Pre-Initialization Setup - Initialize Global Variables
    """
    global yaml, ui, utils_dict, cs_ruamel_yaml, cs_ruamel_commentedmap, cs_ruamel_commentedmap_polymorph, exec, exec_path, exec_name, argv, argc, vers, argparser

    # Initialize classes
    yaml = YAML()
    ui = UI() # Initialize a new UI library instance
    utils_dict = Dictionary()
    cs_ruamel_yaml = RuamelYAML()
    cs_ruamel_commentedmap = cs_ruamel_yaml.CommentedMap()
    cs_ruamel_commentedmap_polymorph = cs_ruamel_commentedmap.Polymorphism()

    # Initialize CLI system environment
    exec = sys.argv[0]
    exec_path = os.path.split(exec)[0]
    exec_name = os.path.split(exec)[1]
    # Get CLI arguments
    argv = sys.argv[1:]
    argc = len(argv)
    # Get application information
    vers = "v0.1.0"

    # Initialize Global Variables
    argparser = { "positionals" : [], "optionals" : { "with-arguments" : {}, "flags" : {} } }

def get_next_argument(i):
    """
    Get the argument value assigned to the flag/argument
    """
    # Initialize Variables
    next_arg_value = ""

    # Get the next element's index
    next_idx = i+1

    # Check if there are any argument values provided
    if next_idx <= (argc-1):
        # Arguments are provided
        ## Get next argument
        next_arg_value = argv[next_idx]

    # Return/Output
    return next_arg_value

def get_cli_arguments():
    """
    Pass and obtain CLI arguments from system environment
    """
    global argparser

    # Check if there are arguments provided
    if argc > 0:
        i = 0
        while i <= (argc-1):
            # Get current argument
            curr_arg = argv[i]

            # Process current argument
            match curr_arg:
                # With Arguments
                case "-i" | "--input":
                    """
                    Specify a configuration file to import and print.

                    Append this to add more files to print. Each file contents will be an individual table.

                    :: NOTE
                    - This will overwrite all instances of '--json-string'
                    """
                    # Get the next element's index
                    next_idx = i+1

                    # Check if there are any argument values provided
                    if next_idx <= (argc-1):
                        # Arguments are provided
                        ## Get next argument
                        next_arg = argv[next_idx]

                        ## Verify that the argument is not empty
                        if next_arg.rstrip() == "": # Check if argument is empty
                            print("Empty value provided to {}.".format(curr_arg))
                        elif not (next_arg.startswith("-")): # Check if argument is an optional (starts with '-')
                            ## Check if 'json-string' is in the 'with-arguments' key-value
                            if not ("input-configuration-file" in argparser["optionals"]["with-arguments"]):
                                ## Not inside, initialize a new list
                                argparser["optionals"]["with-arguments"]["input-configuration-file"] = []

                            ## Append and set the argument to the key
                            argparser["optionals"]["with-arguments"]["input-configuration-file"].append(next_arg)

                            ## Increment by 1 to skip the next argument to the subsequent element
                            i += 1
                    else:
                        print("Argument value not provided to {}".format(curr_arg))
                case "--string-type":
                    """
                    Specify the configuration file type (JSON, YAML, TOML etc etc) of each input string (Default = json)
                    - Append this to add more type definitions.
                        + Add this for every use of '--json-string'

                    :: Note
                    - Ensure that the number of invocations equals to the number of strings passed
                    """
                    # Get the next element's index
                    next_idx = i+1

                    # Set the keyword for the current optional
                    keyword = "configuration-file-type"

                    # Check if there are any argument values provided
                    if next_idx <= (argc-1):
                        # Arguments are provided
                        ## Get next argument
                        next_arg = argv[next_idx]

                        ## Verify that the argument is not empty
                        if next_arg.rstrip() == "": # Check if argument is empty
                            print("Empty value provided to {}.".format(curr_arg))
                        elif not (next_arg.startswith("-")): # Check if argument is an optional (starts with '-')
                            ## Check if 'json-string' is in the 'with-arguments' key-value
                            if not (keyword in argparser["optionals"]["with-arguments"]):
                                ## Not inside, initialize a new list
                                argparser["optionals"]["with-arguments"][keyword] = []

                            ## Append and set the argument to the key
                            argparser["optionals"]["with-arguments"][keyword].append(next_arg)

                            ## Increment by 1 to skip the next argument to the subsequent element
                            i += 1
                    else:
                        print("Argument value not provided to {}".format(curr_arg))
                case "--json-string":
                    """
                    Specify and import a JSON string into a JSON object

                    For every '--json-string' used, append into a list of all JSON strings
                    - When print-table is called,
                        - Iterate the list of all JSON strings, create a new table for each entry and print them all out

                    :: NOTE
                    - This will overwrite all instances of '-i' | --input
                    """
                    # Get the next element's index
                    next_idx = i+1

                    # Check if there are any argument values provided
                    if next_idx <= (argc-1):
                        # Arguments are provided
                        ## Get next argument
                        next_arg = argv[next_idx]

                        ## Verify that the argument is not empty
                        if next_arg != "":
                            ## Check if 'json-string' is in the 'with-arguments' key-value
                            if not ("json-string" in argparser["optionals"]["with-arguments"]):
                                ## Not inside, initialize a new list
                                argparser["optionals"]["with-arguments"]["json-string"] = []

                            ## Append and set the argument to the key
                            argparser["optionals"]["with-arguments"]["json-string"].append(next_arg)

                            ## Increment by 1 to skip the next argument to the subsequent element
                            i += 1
                        else:
                            print("Empty value provided to {}.".format(curr_arg))
                    else:
                        print("Argument value not provided to {}".format(curr_arg))
                # Flags
                case "-h" | "--help":
                    ## Display help
                    argparser["optionals"]["flags"]["help"] = True
                case "-v" | "--version":
                    ## Display system version information
                    argparser["optionals"]["flags"]["version"] = True
                case "--print-table":
                    ## Print the imported configuration file as a designed table
                    argparser["optionals"]["flags"]["print-table"] = True
                case _:
                    ## Default case: Positionals
                    argparser["positionals"].append(curr_arg)

            # Increment index by 1 to jump to the next argument
            i += 1
    else:
        print("[X] No arguments provided.")
        exit(1)

def main():
    # Perform Pre-Initialization Setup
    init()
    get_cli_arguments()

    # Initialize Variables
    # json_str = '[{"Hello" : "World", "World" : "Hello"}, {"Hello" : "World", "World" : "Hello"}, {"Hello" : "World"}, {"World" : "Hello"}]'
    json_str_values = []
    configuration_files = []
    configuration_file_types = []
    positionals = argparser["positionals"]
    optionals = argparser["optionals"]

    # Process CLI optional arguments
    ## Iterate through both optionals with arguments and flags (True/False)
    for opt_category, opt_dicts in optionals.items():
        ## Iterate through the optional parameter values
        for opt_key, opt_values in opt_dicts.items():
            ## Match/Switch-case and process the key
            match opt_key:
                case "help":
                    # Display help
                    display_help()
                case "version":
                    # Display system version information
                    display_system_version()
                case "configuration-file-type":
                    # Obtain the specified configuration file types
                    configuration_file_types = opt_values
                    print("Configuration File Types: {}".format(configuration_file_types))
                case "input-configuration-file":
                    # Obtain the specified import/input configuration files
                    configuration_files = opt_values
                    print(configuration_files)
                case "json-string":
                    # Obtain the imported JSON string and convert into a JSON object
                    json_str_values = opt_values
                    print(json_str_values)
                case "print-table":
                    """
                    Pretty print the configuration file values in a table
                    """
                    # Check if configuration files are provided
                    if len(configuration_files) > 0:
                        # Initialize variables
                        tables = []

                        # Iterate the list of all JSON strings, create a new table for each entry and print them all out
                        for i in range(len(configuration_files)):
                            # Get current configuration file
                            curr_config_file = configuration_files[i]

                            print("Current Configuration File: {}".format(curr_config_file))

                            # Data Validation
                            if curr_config_file.rstrip() == "":
                                ## Null Value Check
                                print("No configuration file provided.")
                            elif not (os.path.isfile(curr_config_file)):
                                ## File exists
                                print("E{} : File {} could not be found.".format(404, curr_config_file))
                            else:
                                # Initialize local variables
                                str_val = ""
                                dataset:dict|list = []

                                # Obtain file extension
                                curr_config_file_ext = os.path.splitext(curr_config_file)[1].split(".")[1]
                                print("Configuration File Extension: {}".format(curr_config_file_ext))

                                # Read and import the file contents from the configuration file
                                with open(curr_config_file, "r") as read_conf_file:
                                    # Read file contents
                                    str_val = read_conf_file.read().rstrip()

                                    # Close file after usage
                                    read_conf_file.close()

                                # Check file extension to determine file type
                                match curr_config_file_ext:
                                    case "json":
                                        # JSON file type
                                        print("JSON")
                                        dataset = json.loads(str_val)
                                    case "toml":
                                        # TOML file type
                                        print("TOML")
                                    case "yaml":
                                        # YAML file type
                                        ## YAML is entirely dictionary
                                        print("YAML")

                                        # Import YAML file contents to object
                                        yaml_data = cs_ruamel_yaml.yaml.load(str_val)

                                        # Convert CommentedMap to Dictionary
                                        dataset = cs_ruamel_commentedmap_polymorph.convert_to_dictionary(yaml_data)

                                        # Iterate through dataset and obtain all roots and subkeys
                                        # all_key_values = utils_dict.traverse(dataset)
                                    case _:
                                        # Default - Unsupported
                                        print("Unsupported configuration file type : {}".format(curr_config_file_ext))

                                # Iterate through the root keys (and subroot keys) and initialize a new table for each nested subkey, then append the new table to a master tables list
                                curr_row = ""
                                prev_row = ""
                                curr_cfg_file_tables = []
                                """
                                for i in range(len(dataset)):
                                    # Get the current root key and nested subkey-values
                                    curr_row = dataset[i]

                                    # Check value type
                                    if isinstance(curr_row, str):
                                        # String = the root key of the nested subkeys
                                        print("Root Key: {}".format(curr_row))
                                    elif isinstance(curr_row, dict):
                                        print("{}".format(type(curr_row)))
                                    else:
                                        print("{} : {}".format(i, curr_row))
                                        # Initialize a new instance of the UI component class 'TableUI'
                                        cs_TableUI = TableUI()

                                        # Design table and populate with column and rows
                                        table = cs_TableUI.design_table(curr_row)

                                        # Append current table to the list
                                        tables.append(table)

                                    # Set the current row to be the previous row after entering the new iteration
                                    prev_row = curr_row
                                """
                                # Initialize a new instance of the UI component class 'TableUI'
                                cs_TableUI = TableUI()

                                # Design and generate tables
                                curr_cfg_file_tables = cs_TableUI.generate_tables(dataset)

                                # Extend and place the tables derived from the current configuration file into the 'tables' master list
                                tables.extend(curr_cfg_file_tables)

                            print("")

                        # Create a panel and insert the table group arranged horizontally, side by side
                        panel = ui.insert_tables_to_Panel(tables)

                        # Print the panel to the console standard output
                        ui.print_console(panel)
                    elif len(json_str_values) > 0:
                        # Iterate the list of all JSON strings, create a new table for each entry and print them all out
                        for i in range(len(json_str_values)):
                            # Get current string
                            str_val = json_str_values[i]

                            print("Current String: {}".format(str_val))

                            # Data Validation: Null Value Check
                            if str_val == "":
                                print("No JSON string provided.")
                            else:
                                dataset = json.loads(str_val)

                                # Initialize a new instance of the UI component class 'TableUI'
                                cs_TableUI = TableUI()

                                # Design table and populate with column and rows
                                table = cs_TableUI.design_table(dataset)

                                # Print
                                print(table)
                case opt_found if not (opt_found in list(opt_dicts.keys())):
                    # Option is not found
                    print("Optional argument '{}' is not found".format(opt_found))

if __name__ == "__main__":
    main()


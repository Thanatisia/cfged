"""
cfged : Configuration Buffer Reader, Viewer and Editor
"""
import os
import sys
from cfged.core.ui.design import print, Table, TableUI

def init():
    """
    Perform Pre-Initialization Setup - Initialize Global Variables
    """
    global exec, exec_ext, argv, argc, argparser

    # Initialize classes

    # Initialize CLI system environment
    exec = sys.argv[0]
    # Get file extension
    exec_ext = os.path.splitext(exec)[1]
    argv = sys.argv[1:]
    argc = len(argv)

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
                    print("Help")
                case "version":
                    # Display system version information
                    print("Version")
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

                                # Read and import the file contents from the configuration file
                                with open(curr_config_file, "r") as read_conf_file:
                                    # Read file contents
                                    str_val = read_conf_file.read().rstrip()

                                    # Close file after usage
                                    read_conf_file.close()

                                # Initialize a new instance of the UI component class 'TableUI'
                                cs_TableUI = TableUI()

                                # Design table and populate with column and rows
                                table = cs_TableUI.design_table(str_val)

                                # Print
                                print(table)
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
                                # Initialize a new instance of the UI component class 'TableUI'
                                cs_TableUI = TableUI()

                                # Design table and populate with column and rows
                                table = cs_TableUI.design_table(str_val)

                                # Print
                                print(table)
                case opt_found if not (opt_found in list(opt_dicts.keys())):
                    # Option is not found
                    print("Optional argument '{}' is not found".format(opt_found))

if __name__ == "__main__":
    main()


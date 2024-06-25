# cfged : Configuration Buffer Reader, Viewer and Editor

## Information
### Description
- cfged is a simple CLI Configuration file buffer reader, viewer, editor designed to 
    - Reader/Viewer
        + Printing/Standard Output: print/format the contents of configuration files in a human-readable format (i.e. pretty print, table)
    - Editor
        + TBC

### Project
+ Package Version: v0.1.0

### Notes
- Currently, as of v0.1.0, the only supported configuration file type is JSON
    + Multi-file type supported is in the TODO pipeline
    + File extension retrieval has been implemented

## Setup
### Dependencies
+ python
+ python-pip
- Python Packages
    + rich

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

## Wiki

## Resources

## References

## Remarks


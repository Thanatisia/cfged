"""
Test: cfged/core/ui/design.py
"""
import os
import sys
from cfged.core.ui.design import print, Table, TableUI

def test_initialize_class_tableui():
    """
    Unit Test: Initialize TableUI class object
    """
    # Initialize Variables
    cs_TableUI = None
    token = False
    err_msg = ""

    # Try initializing UI component 'table'
    try:
        cs_TableUI = TableUI()
        token = True
    except Exception as ex:
        err_msg = ex

    return [cs_TableUI, token, err_msg]

def test_get_ui_component_table(cs_TableUI:TableUI):
    """
    Unit Test: Obtain UI component table
    """
    # Initialize Variables
    table_test = None
    token = False
    err_msg = ""

    # Try initializing UI component 'table'
    try:
        table_test = cs_TableUI.table
        token = True
    except Exception as ex:
        err_msg = ex

    return [table_test, token, err_msg]

def test_design_table(cs_TableUI:TableUI, json_str:str):
    """
    Unit Test: Design table and populate with column and rows
    """
    # Initialize Variables
    designed_table = None
    token = False
    err_msg = ""

    # Try initializing UI component 'table'
    try:
        cs_TableUI.design_table(json_str)
        designed_table = cs_TableUI.table
        token = True
    except Exception as ex:
        err_msg = ex

    return [designed_table, token, err_msg]

def unittest():
    """
    Main Unit Test entry point
    """

    # Unit Test 1: Initialize UI component class 'TableUI'
    cs_TableUI, token, err_msg = test_initialize_class_tableui()
    if cs_TableUI == None:
        print("[X] Error initializing UI component class 'TableUI' : {}".format(err_msg))
        exit(1)
    print("[+] UI component class 'TableUI' initialized successfully : {}.".format(cs_TableUI))

    # Unit Test 2: Get newly-initialized UI component 'table'
    table_test, token, err_msg = test_get_ui_component_table(cs_TableUI)
    if table_test == None:
        print("[X] Error obtaining UI component 'table' : {}".format(err_msg))
        exit(1)
    print("[+] UI component 'table' obtained successfully : {}.".format(table_test))

    # Unit Test 3: Design table and populate with column and rows
    json_str = '[{"Hello" : "World", "World" : "Hello"}, {"Hello" : "World", "World" : "Hello"}, {"Hello" : "World"}, {"World" : "Hello"}]'
    designed_table, token, err_msg = test_design_table(cs_TableUI, json_str)
    if designed_table == None:
        print("[X] Error encountering while designing table : {}".format(err_msg))
        exit(1)
    print("[+] Table designed with data '{}' successfully".format(json_str))
    print(designed_table)

if __name__ == "__main__":
    unittest()


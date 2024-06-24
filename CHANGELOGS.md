# CHANGELOGS

## Table of Contents
+ [2024-06-24](#2024-06-24)

## Changes
### 2024-06-24
#### 1414H
+ Version: v0.1.0

- Version Changes
    + Initial Commit
    - Additions
        + Added python packaging configuration file 'pyproject.toml'
        + Added CLI utility entry point file 'main.py' in 'src/app'
        + Added new core UI libraries for cfged - 'design.py'
        + Added new utilities library for cfged - 'utils.py'

- New
    + Added new document '.gitignore'
    + Added new document 'CHANGELOGS.md'
    + Added new document 'CONTRIBUTING.md'
    + Added new document 'README.md'
    + Added python packaging configuration file 'pyproject.toml'
    + Added new document 'requirements.txt'
    - Added new directory 'src' for holding the main project source codes/files
        - Added new directory 'app' containing the source files for the main CLI utility application
            + Added the entry point source file 'main.py' for the CLI utility
        - Added new directory 'cfged' containing the source codes for the project 'cfged'
            - Added new directory 'core' for the cfged Core libraries/modules
                - Added new directory 'ui' for the cfged core UI libraries/modules
                    + Added new module 'design.py' containing classes, functions and attributes for designing the UI components for the project
                - Added new directory 'utils' for general utilities used by the core framework
                    + Added new module 'utils.py' containing the functions
    - Added new directory 'tests' containing Unit Tests
        + Added new unit test source 'test-core-ui-table.py' for testing the class 'TableUI' in 'cfged/core/ui/design'


# KMSearch

## About the program

This is a command-line interface program in Python that allows you to explore directories, update registered data, search for files, and display document information by path.

## Commands

The program has seven commands.

1. **main**
    This function initializes and runs the parser. 

2. **explore**
    Explore directories. Syntax: `explore dir_path [dir_path ...] [--model_path MODEL_PATH]`
    - dir_path: Path(s) to the directory(ies) for exploration.
    - `--model_path`: Path to the model. Optional.

3. **update**
    Updates registered data. Syntax: `update [--model_path MODEL_PATH]`
    - `--model_path`: Path to the model. Optional.

4. **search**
    Search for files using a keyword. Syntax: `search keyword [--extract_type EXTRACT_TYPE] [--file_path_pattern FILE_PATH_PATTERN]`
    - keyword: Keyword for the search.
    - `--extract_type`: Extraction type. Optional.
    - `--file_path_pattern`: Pattern of the file path. Optional.

5. **showdocument**
    Display document information by path. Syntax: `showdocument path`
    - path: Path to the document you want to view.

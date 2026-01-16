# Heter

A lightweight and efficient Python tool for file and directory searching. It utilizes **Generators (`yield`)** to ensure that RAM consumption remains low, even when scanning millions of files.

## ✨ Features

- **Native Generators**: Processes one file at a time without loading giant lists into memory, making it as efficient as possible.
- **Depth Control**: `depth` argument to limit recursivity.
- **Flexible Filters**: Search for files, directories, or both, with pattern matching support.
- **Complete Data**: Returns dictionaries with name, size (KB), creation/modification dates, path, and type.

## 🚀 How to Use:

### **Installing the Library**:
```bash
pip install heter    
```

### **Importing the Library**
You can import the library as follows:
```python
import heter as ht 
```
> I recommend using `as ht` to abbreviate the name. This documentation will follow this convention to keep the code concise and easier to read.

### **Parameters**:
The `search` function can receive up to 4 parameters, with only one of them being mandatory and positional:

- **Path**: The only mandatory argument, which must be provided as a **String**.
```python
ht.search("C:/Users/yourUser/yourPath") 
```

- **typeSearch**: An optional parameter (string) that defines which types of entries will be searched:
    - **'dir'** for directories/folders: 
      ```python
      ht.search('C:/', typesearch='dir') # only folders/directories will be searched
      ```
    - **'file'** for files:
      ```python
      ht.search('C:/', typesearch='file') # only files will be searched
      ```

    > [!WARNING] 
    > If no argument is passed to the **typeSearch** parameter (or if an invalid one is used), it will show everything found:
    > ```python
    > ht.search('C:/') # searches everything in the 'C:/' path
    > ```

- **Pattern**: An optional parameter that functions as a name filter over the search results:
```python
ht.search('C:/', Pattern={'program', 'win', 'xbox'}) # searches for entries containing 'program', 'win', or 'xbox' in the name
```

> [!WARNING]
> To pass values in **Pattern**, items must be strings inside a **set**.
> Example: `Pattern={'value1', 'value2', 'value3'}`

- **Depth**: An optional parameter (**int**) determining how many subfolder levels will be scanned:
```python
ht.search('C:/', Depth=2) # it will scan every folder found up to 2 levels deep
```

>[!TIP]
>Passing higher values in **Depth** will result in more results, but the search remains memory-efficient thanks to generators.

## 🌊 **Function Result**:

* **Return**: The function returns a **generator of dictionaries**. Each dictionary represents a file or directory with the following keys:

| Key | Description |
| :--- | :--- |
| **name** | Name of the file or folder |
| **size_kb** | Size converted to Kilobytes |
| **modification** | Modification date (DD/MM/YYYY) |
| **creation** | Creation date (DD/MM/YYYY) |
| **full_path** | Absolute system path |
| **type_entry** | Identifies if it is 'file' or 'directory' |

## 🧪 **Tests**
This project uses **pytest**. To run the tests, use the terminal:
```bash
pytest
```
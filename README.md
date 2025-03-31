# index-tool
List the web index to a file or download all files from the index.

Download `index_tool.py` 

Install requirements `python3-requests` and `python3-bs4`

Run script: ` python3 index_tool.py`

Choose one of the options:

```bash
Select operation mode:
1. List files and directories
2. Download files (preserving directory structure)
Enter option number (1/2): 
```

Specify the path for the index:

```bash
Enter index URL (e.g., http://example.com/test/):
```

If you select the option to download files, specify the folder location where the files will be downloaded:

```bash
Enter local download directory (e.g., ./downloaded_files): 
```

If you choose to create a listing, it will be created in the same location as the script with the name like:`file_list.txt`

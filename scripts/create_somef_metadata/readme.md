# Scripts 

Note: you need to install [somef](https://github.com/KnowledgeCaptureAndDiscovery/somef/) (just go to the repository and follow the instructions)


In order to install the other dependencies needed to run them, just do:

```
pip install -r requirements.txt
```

In a new environment (Python 3.9+)

## create somef metadata

Usage example:

```
python3 create_metadata.py -i input_to_csv -o outFolder
```

This will create a folder with n files, where each file is the result after applying somef on each software repository. The `outFolder` parameter indicates the path to the folder where everything will be extracted.


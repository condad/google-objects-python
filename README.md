# Google Objects
Pythonic, OO Google Slides, Sheets, and Drive interactions. Currently only supports Python 2.7. 

## Installation
 ```bash
 $ pip install google-objects
 ```

## Usage
Requires a valid Google API Credentials object from Google's excellent oauth2lib library, for more information visit [here](https://developers.google.com/identity/protocols/OAuth2).
 
## Google Drive

- [x] Retrieve about information:


 ```python
  from google_objects import DriveAPI

  gdrive = DriveAPI(OAUTH2LIB_CREDS)
  about = gdrive.get_about()

  print about.email
  print about.name

  # link to profile photo
  print profile.photo

 ```
- [x] List files by type:

```python
  gdrive = DriveAPI(OAUTH2LIB_CREDS)

  files_by_type = {
      'slides': gdrive.list_files('presentation'),
      'folders': gdrive.list_files('folder'),
      'spreadsheets': gdrive.list_files('spreadsheets'),
  }

  for file in files_by_type['folders']:
    print file.id
    print file.name
    # ...
```

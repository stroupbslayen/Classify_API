# Creating a python file to help handle navigating a JSON API response

- Create and save classes from a URL that returns a JSON response:
```py
from Classify_API import Classify_API
url='https://www.reddit.com/r/all/hot/.json'
Classify_API.fromURL('Reddit Post', url, headers = {'User-agent': 'your bot 0.1'}).create
```

- Create and save classes from a JSON response that you have:
```py
response={'api_key':'api value'}
Classify_API('Test Class',response).create
```

To use your newly created classes, import the new file into your script:
```py
from test_class import Test_Class
response={'api_key':'api value'}
api=Test_Class(response)
```

- From there, you can navigate attributes normally
```py
print(api.api_key)
```
Would print '*api value*'

# Notes
- Hasn't been tested in every case, so there might be some issues.
- It can be used for any dict or list, but API responses generally have a consistent structure so there may be issues
- Lists that contain dictionaries are returned as generators, lists that contain anything else will be returned as normal lists.
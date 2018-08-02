# Creating a python file to help handle navigating a JSON API response

- Create classes from a URL that returns a JSON response:
```py
from APIClassifier import APIClassifier
url='https://www.reddit.com/r/all/hot/.json
APIClassifier.fromURL('new classes', url, headers = {'User-agent': 'your bot 0.1'})
```

- Create classes from a JSON response that you have:
```py
response={'api_key':'api value'}
APIClassifier('API Class',response)
```

To use your new API Class:
```py
from api_class import API_Class
response={'api_key':'api value'}
api=API_Class(response)
```

- From there, you can navigate attributes normally
```py
print(api.api_key)
```
Would print '*api value*'

# Notes
- Hasn't been tested in every case, so there might be some issues.
- It can be used for any dict or list, but API responses generally have a consistent structure so there may be issues

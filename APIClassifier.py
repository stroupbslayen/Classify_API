import requests

template = '''
{}
class {}:
\tdef __init__(self,items):
\t\tif items:
\t\t\tself.items=items
\t\telse:
\t\t\tself.items=dict()
{}
'''


def new_def(name,output,desc):
    x=f"""\n\t@property\n\tdef {name}(self):\n\t\t'''{desc}. If no data is available, an empty dict or None is returned'''\n\t\treturn {output}\n"""
    return x

def clean(string):
    if not string:
        string = '_'
    if string[0].isdigit():
        string = f"_{string}"
    return string.replace(' ', '_')


class APIClassifier:

    def __init__(self, class_name, api_json, get_text=False,names=None):
        NEW=False
        if names:
            self.class_names=names
        else:
            self.class_names = []
        self.name = clean(class_name)
        while self.name in self.class_names:
            self.name=f'_{self.name}'
        self.class_names.append(self.name)
        self.new_classes = ''
        self.attributes = ''
        if isinstance(api_json,list):
            if isinstance(api_json[0], dict):
                api_json={'api_list':api_json}
                NEW=True
            else:
                output= '''self.items'''
                desc = f'''will return {type(api_json)}'''
                self.attributes+= f'''\t\t{new_def('api_list',output,desc)}'''

        if isinstance(api_json,dict):
            for k, v in api_json.items():
                if v and isinstance(v, dict):
                    self.__is_dict(k,v)
                elif v and isinstance(v, list) and isinstance(v[0], dict):
                    self.__is_list(k,v,new=NEW)
                else:
                    output=f'''self.items.get('{k}',dict())'''
                    desc=f'''Will return {type(v)}'''
                    self.attributes += f'''\t\t{new_def(clean(k),output,desc)}'''

        if not get_text:
            with open(f'{self.name.lower()}.py', 'w+') as f:
                f.write(template.format(self.new_classes, self.name.title(), self.attributes).strip())
                f.close()
            print(f'{self.name.lower()}.py has been created!')

    def __is_dict(self,k,v):
        new_class=clean(k).title()
        while new_class in self.class_names:
            new_class=f'_{new_class}'
        output=f"{new_class}(self.items.get('{k}',dict()))"
        desc=f'Will return class {new_class}()'
        self.attributes += f'''\t\t{new_def(clean(k),output,desc)}''' 
        new_class = APIClassifier(new_class, v, get_text=True,names=self.class_names)
        self.new_classes += new_class.txt
        self.class_names = new_class.get_names
    
    def __is_list(self,k,v,new=False):
        new_class=clean(k).title()
        while new_class in self.class_names:
            new_class=f'_{new_class}'
        if not new:
            output= f'''({new_class}(item) for item in self.items.get('{k}',dict()) if item)'''
            desc= f'''Will return a generator with instances of class {new_class}()'''
        else:
            output= f'''({new_class}(item) for item in self.items if item)'''
            desc= f'''Will return a generator with instances of class {new_class}()'''
        self.attributes += f'''\t\t{new_def(clean(k),output,desc)}'''
        new_class = APIClassifier(new_class, v[0], get_text=True,names=self.class_names)
        self.new_classes += new_class.txt
        self.class_names = new_class.get_names

    @property
    def txt(self):
        return template.format(self.new_classes, self.name.title(), self.attributes)

    @property
    def get_names(self):
        return self.class_names

    @classmethod
    def fromURL(cls,class_name,url,headers:dict=None,):
        r=requests.get(url,headers=headers)
        if r.status_code == 200:
            _json=r.json()
            return cls(class_name,_json)
        else:
            print(f'Failed to retrieve JSON: Status {r.status_code}')
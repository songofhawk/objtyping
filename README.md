# object converter from primitive and to primitive
- @author: 宋辉
- @email: songofhawk@gmail.com

## Origins
Python being a dynamically typed language, developers are not in the habit of defining types for their data. This is flexible, but not convenient enough when dealing with complex business logic - the lack of type checking can make it hard to find errors, and there are no code hints when coding in the IDE. So this tool was developed to fix it.

## Usage-basic
* First define the business class and define the type of each field through class variables.

```python
from typing import List


class Person:
    name: str
    age: int


class Company:
    name: str
    revenue: float
    employees: List[Person]
```
The reason why class variables are chosen for definition is that it is the most concise and intuitive. In contrast, there is no way to get the type definition (type_hint) if you initialize the instance variable in the __init__ method, and it is obviously more complicated if you use the @property annotation or getter, setter methods. They are not as simple and elegant as defining class variables directly. But there is a downside to using class variables: it is used here as metadata, and if you really need to define variables shared at the class level, it is impossible to distinguish them. This problem can be solved later by developing custom annotations.

* The next step is to transform the dict-list nested data, which matches the structure of this class definition, into an instance object of the class.
```python
from objtyping import objtyping

company1 = objtyping.from_primitive({
    'name': 'Apple',
    'revenue': 18.5,
    'employees': [{
        'name': 'Tom',
        'age': 20
    }, {
        'name': 'Jerry',
        'age': 31
    }]
}, Company)

```
Now company1 is a complete Company object, and you can directly access the properties in it in the form of company1.name, company1.employees[0].name, etc.

* Of course, you can also turn the business object back into a dict-list nested form
```python
from objtyping import objtyping

dict_list = objtyping.to_primitive(company1)
```
The primitve object, at this point, is a large pile of primitive type data nested at the dict and list levels


## Scenes
### Initializing an object
Python does not have as convenient a way to initialize objects as js, but with this tool it can be written like this (which is the summary of the previous basic use).
```python
from typing import List

from objtyping import objtyping


class Person:
    name: str
    age: int


class Company:
    name: str
    revenue: float
    employees: List[Person]

    def __str__(self):  
        return "'{}' has {} employees: {}".format(self.name, len(self.employees), ' and '.join(map(lambda emp: emp.name, self.employees)))


if __name__ == '__main__':
    company1 = objtyping.from_primitive({
        'name': 'Apple',
        'revenue': 18.5,
        'employees': [{
            'name': 'Tom',
            'age': 20
        }, {
            'name': 'Jerry',
            'age': 31
        }]
    }, Company)

    print(company1)

```

output:
```console
'Apple' has 2 employees: Tom and Jerry
```

### serialization / deserialization
Python's common serialization requirements, including the json and yaml data formats, have relatively well-developed libraries for handling them. But again, because of the lack of emphasis on types, they handle objects in raw primitive format. It is just right to use this tool to achieve further conversion.

#### json
demo
```python
import json
import sys
from typing import List

from objtyping import objtyping


class X:
    x: int
    y: str


class A:
    q: str
    a: str
    b: int
    c: List[X]


if __name__ == '__main__':
    print("\r\n-----json-------")
    json_obj = json.loads('{"q":9, "a":"Mark", "b":3, "c":[{"x":15, "y":"male"},{"x":9, "y":"female", "z":13}]}')
    typed_obj = objtyping.from_primitive(json_obj, A)
    d_l_obj = objtyping.to_primitive(typed_obj)
    print(json.dumps(d_l_obj))

    sys.exit()

```

output
```console
-----json-------
{"q": "9", "a": "Mark", "b": 3, "c": [{"x": 15, "y": "male"}, {"x": 9, "y": "female", "z": 13}]}
```

* **note**: here is that the property "q", which was originally a number in the original json structure, is a string in the class variable definition, and after converting it to a business object, its type is now a string - the objtyping tool tries to force a conversion between the base types according to the class definition .*

#### yaml
demo
```python
import sys
from ruamel.yaml import YAML
from typing import List
from objtyping import objtyping


class X:
    x: int
    y: str


class A:
    q: str
    a: str
    b: int
    c: List[X]


if __name__ == '__main__':
    print("\r\n-----yaml-------")
    yaml = YAML()
    yaml_obj = yaml.load('''
    q: 9
    a: Mark
    b: 3
    c:
        - x: 15
          y: male
        - x: 9
          y: female
          z: 13    
    ''')
    typed_obj = objtyping.from_primitive(yaml_obj, A)
    d_l_obj = objtyping.to_primitive(typed_obj)
    yaml.dump(d_l_obj, sys.stdout)

    sys.exit()

```

output
```console
-----yaml-------
q: '9'
a: Mark
b: 3
c:
- x: 15
  y: male
- x: 9
  y: female
  z: 13
```

Here the datatype of property "q" is also converted.

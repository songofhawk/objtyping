# objtyping 带类型定义的对象转换器
- @author: 宋辉
- @email: songofhawk@gmail.com

## 由来
Python不是强类型语言，开发人员没有给数据定义类型的习惯。这样虽然灵活，但处理复杂业务逻辑的时候却不够方便——缺乏类型检查可能导致很难发现错误，在IDE里编码时也没有代码提示。所以开发了这个小工具来解决它。

## 基本用法
* 首先定义业务类，并通过类变量定义每个字段的类型。
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
之所以选择类变量来定义，是因为它最简洁和直观。相比之下，如果在__init__方法中初始化实例变量，是没有办法获取类型定义（type_hint）的；如果用@property注解或者getter，setter方法的话，显然就更复杂了。它们都不如直接定义类变量简单优美。不过使用类变量也有缺点：就是它在这里被当成元数据来使用了，如果真的需要定义类级别共享的变量，无法区分。这个问题可以在后面通过开发自定义注解来解决。

* 下一步就可以把符合这个类定义结构的dict-list嵌套数据，转化为该类实例对象了：
```python
from objtyping import objtyping

company1 = objtyping.from_dict_list({
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
此时的company1就是完整的Company对象了, 可以直接使用company1.name, company1.employees[0].name 等形式访问里面的属性。

* 当然也可以把业务对象再转回dict-list嵌套的形式
```python
from objtyping import objtyping

dict_list = objtyping.to_dict_list(company1)
```
此时的dict_list对象，就是一大堆dict和list层级嵌套的原始类型数据


## 使用场景
### 初始化对象
Python没有js那么方便的初始化对象方式，但有这个工具就可以这样写（就是前面基础使用的汇总）：
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

    def __str__(self):  # 其实一般可能都是这样简单用一下的
        return "'{}' has {} employees: {}".format(self.name, len(self.employees), ' and '.join(map(lambda emp: emp.name, self.employees)))


if __name__ == '__main__':
    company1 = objtyping.from_dict_list({
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

输出结果:
```console
'Apple' has 2 employees: Tom and Jerry
```

### 序列化/反序列化
Python的常见的序列化需求，包括json和yaml数据格式，它们都有相对完善的处理库。但同样是不强调类型的缘故，它们处理的对象都是原始的dict-list格式。正好可以借助这个工具实现进一步转化。

#### json
示例
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
    typed_obj = objtyping.from_dict_list(json_obj, A)
    d_l_obj = objtyping.to_dict_list(typed_obj)
    print(json.dumps(d_l_obj))

    sys.exit()

```

输出结果
```console
-----json-------
{"q": "9", "a": "Mark", "b": 3, "c": [{"x": 15, "y": "male"}, {"x": 9, "y": "female", "z": 13}]}
```

这里需要**注意**的是：本来属性"q"，在最初的json结构中，是个数字，但由于类变量定义中是字符串，转换成业务对象以后，它的类型就是字符串了——objtyping工具，会试图按照类定义，在基础类型之间强制转换。


#### yaml
示例
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
    typed_obj = objtyping.from_dict_list(yaml_obj, A)
    d_l_obj = objtyping.to_dict_list(typed_obj)
    yaml.dump(d_l_obj, sys.stdout)

    sys.exit()

```

输出结果
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

这里的属性"q"同样被强转了类型。

from json_reader import EOS

#语法正确json
c='''{
  "person": {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "Java", "C++"],
    "education": {
      "degree": "Masters in Computer Science",
      "institution": "University of Technology"
    }
  }
}'''

#语法错误json
r='''{
  "person": {
    "name": Alice,  // 错误：字符串应该用双引号包围
    age: 30,        // 错误：属性名应该用双引号包围
    "skills": ["Python", Java, C++],  // 错误：字符串应该用双引号包围
    "education": {
      "degree": "Masters in Computer Science",
      "institution": University of Technology  // 错误：字符串应该用双引号包围
    }
  }
}'''

t='''abc   '''

w='''{"person":{
    "name":"Alice",
    "age":30.3 ,
    "skills": ["Python", "Java", "C++"],
    "education": {
      "degree": "Masters in Computer Science",
      "institution": "University of Technology"
    }
  }
}'''

s='''30.3'''

d='''true'''

test_string = r



def generater():
    for char in test_string:
        yield char
    while True:
      yield EOS


if __name__ == '__main__':
  #  import json
  #  print(json.loads(d))
  # import re
  # a='-?\d+(\.\d+)?([eE][+-]?\d+)?'
  # if re.match(r'-?\d+(\.\d+)?([eE][+-]?\d+)?', '-23eeeeeeeeeeeee'):
  #    print(1)
  a = generater()
  for i in range(10):
     print(next(a))

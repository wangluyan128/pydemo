import json
s = json.loads('{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
data = [{'a':1,'b':2,'c':3}]
json1 = json.dumps(data,indent=4)
print(json1)
print(s)
print(s.keys())
print(s["name"])
print(s["type"]["name"])
print(s["type"]["parameter"][1])

#通过位置
print('{0},{1}'.format('chuhao',20))
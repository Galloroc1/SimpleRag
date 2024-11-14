import requests

url = "https://cn.apihz.cn/api/xinwen/baidu.php"
params = {
    "id":"88888888",
    "key":"88888888"
}

data = requests.post(url=url,data=params)
print(data.text)
# print(data.json()['data'])
# print(data.json()['data'][0].keys())
one = data.json()['data']
# print(one)
print(type(one))
for item in one :
    print(item)
# for item in one.items():
#     print(item)



import timeit
from operator import itemgetter
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import random
import string

# 创建一些模拟数据
num_items = 800
org_data = [
    {f'field_{i}': ''.join(random.choices(string.ascii_letters, k=7)) for i in range(9)}
    for _ in range(num_items)
]

# 我们只关心其中的一些字段
keys = [f'field_{i}' for i in range(3)]

# 方法1: 列表推导式
def method_list_comprehension():
    return [{key: x[key] for key in keys} for x in org_data]

# 方法2: 使用 operator.itemgetter
# def method_itemgetter():
#     getter = itemgetter(*keys)
#     return [dict(zip(keys, getter(x))) for x in org_data]

def method_itemgetter():
    return [dict(zip(keys, itemgetter(*keys)(x))) for x in org_data]

# 方法3: 使用 pandas
def method_pandas():
    df = pd.DataFrame(org_data)
    return df[keys].to_dict(orient='records')

# 方法4: 并行处理
def method_parallel():
    def extract_keys(item):
        return {key: item[key] for key in keys}
    with ThreadPoolExecutor() as executor:
        return list(executor.map(extract_keys, org_data))

# 运行基准测试
methods = [method_list_comprehension, method_itemgetter, method_pandas, method_parallel]
for method in methods:
    print(f"{method.__name__}: {timeit.timeit(method, number=1)} seconds")
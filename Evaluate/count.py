import json
from time import sleep
from collections import Counter

def count_repeated_total(arr):
    """计算所有重复数值的总个数（含重复次数）"""
    count_dict = Counter(arr)
    total = 0
    for num, cnt in count_dict.items():
        if cnt > 1:
            total += cnt  # 累加所有重复元素的出现次数
    return total
suject_list = ['Lang','Chart', 'Cli', 'JxPath', 'Math']
path_list = ['MBFL_Simple_Graph_Both_clear_method']

SBFL = []
TIG_SBFL = []
for path in path_list:
    for suject in suject_list:
        print(suject)
        Subject_num = 0
        with open(f"../Result/Suspicious/{suject}/{path}.json", "r", encoding="utf-8") as file:
            loaded_data = json.load(file)
            for key ,value in loaded_data.items():
                list_ = []
                for kk, vv in value.items():
                    list_.append(vv['max']['Dstar'])
                    # counts = dict(Counter(list_))
                    # for key, value in counts.items():
                    #     if value != 1:
                    #         print(f"{key}: {value}次")
            # print(list_)
            # print(loaded_data)
                Subject_num += count_repeated_total(list_)
        print(Subject_num)
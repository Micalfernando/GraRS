import json
import os


def ensure_directory_exists(file_path):
    # 获取文件路径的目录部分
    directory = os.path.dirname(file_path)

    # 判断目录是否存在
    if not os.path.exists(directory):
        # 如果不存在，则创建目录
        os.makedirs(directory)
        print(f"目录 '{directory}' 已创建。")
    else:
        print(f"目录 '{directory}' 已存在。")


def Save_json(data, file_path):
    # 确保文件目录存在
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 将数据保存为 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON 文件已保存到: {file_path}")


def integrate(path, ismbfl=0):
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    with open(path, 'r') as rf:
        datas = json.load(rf)
    print("GET JSON FILE FINISHED!", end='\n\n')
    end_json = {}
    for formula_ in formula_list:
        return_json = {}
        return_json["top1"] = 0
        return_json["top3"] = 0
        return_json["top5"] = 0
        return_json["top10"] = 0
        return_json["mar"] = 0
        return_json["mfr"] = 0
        return_json["exam"] = 0
        if ismbfl == 0:
            for version, v_datas in datas.items():
                return_json["top1"] += v_datas[formula_]["top1"]
                return_json["top3"] += v_datas[formula_]["top3"]
                return_json["top5"] += v_datas[formula_]["top5"]
                return_json["top10"] += v_datas[formula_]["top10"]
                return_json["mar"] += v_datas[formula_]["mar"]
                return_json["mfr"] += v_datas[formula_]["mfr"]
                return_json["exam"] += v_datas[formula_]["exam"]
            return_json["mar"] = return_json["mar"] / len(datas)
            return_json["mfr"] = return_json["mfr"] / len(datas)
            return_json["exam"] = return_json["exam"] / len(datas)
            end_json[formula_] = return_json
        else:
            for version, v_datas in datas.items():
                return_json["top1"] += v_datas[formula_]["max"]["top1"]
                return_json["top3"] += v_datas[formula_]["max"]["top3"]
                return_json["top5"] += v_datas[formula_]["max"]["top5"]
                return_json["top10"] += v_datas[formula_]["max"]["top10"]
                return_json["mar"] += v_datas[formula_]["max"]["mar"]
                return_json["mfr"] += v_datas[formula_]["max"]["mfr"]
                return_json["exam"] += v_datas[formula_]["max"]["exam"]
            return_json["mar"] = return_json["mar"] / len(datas)
            return_json["mfr"] = return_json["mfr"] / len(datas)
            return_json["exam"] = return_json["exam"] / len(datas)
            end_json[formula_] = return_json
        # print(return_json)
    return end_json


def MBFL():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return_json = {}
    for type_ in type_list:
        subject_json = {}
        for subject_name in Subject_name:
            with open(f'../Result/Evaluation_improve/{subject_name}_GBSR_FOR_MBFL_{type_}.json', 'r') as rf:
                datas = json.load(rf)
            print("GET JSON FILE FINISHED!", end='\n\n')
            # for formula_ in formula_list:

        return_json[type_] = subject_json
    return


def main():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath']
    # Subject_name = ['Lang']
    type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    SBFL_LIST = ["SBFL", "GBSR_FOR_SBFL_0_0", "GBSR_FOR_SBFL_1_0", "GBSR_FOR_SBFL_2_0", "GBSR_FOR_SBFL_3_0",
                 "GBSR_FOR_SBFL_4_0",
                 "GBSR_FOR_SBFL_5_0", "GBSR_FOR_SBFL_6_0", "GBSR_FOR_SBFL_7_0", "GBSR_FOR_SBFL_8_0"]
    MBFL_LIST = ["MBFL", "GBSR_FOR_MBFL_0_0", "GBSR_FOR_MBFL_1_0", "GBSR_FOR_MBFL_2_0", "GBSR_FOR_MBFL_3_0",
                 "GBSR_FOR_MBFL_4_0",
                 "GBSR_FOR_MBFL_5_0", "GBSR_FOR_MBFL_6_0", "GBSR_FOR_MBFL_7_0", "GBSR_FOR_MBFL_8_0"]

    # type_list = [1]
    end_json = {}
    for subject_name in Subject_name:
        return_json = {}
        # 先SBFL处理
        SBFL_JSON = {}
        for sbfl_ in SBFL_LIST:
            SBFL_JSON[sbfl_] = integrate(f'../Result/Evaluation_improve/{subject_name}_{sbfl_}.json')
        return_json["SBFL"] = SBFL_JSON
        # 然后MBFL处理
        MBFL_JSON = {}
        for mbfl_ in MBFL_LIST:
            if mbfl_ == "MBFL":
                MBFL_JSON[mbfl_] = integrate(f'../Result/Evaluation_improve/{subject_name}_{mbfl_}.json', 1)
            else:
                MBFL_JSON[mbfl_] = integrate(f'../Result/Evaluation_improve/{subject_name}_{mbfl_}.json')

        return_json["MBFL"] = MBFL_JSON

        # for type_ in type_list:
        #     subject_json = {}
        #     for subject_name in Subject_name:
        #         with open(f'../Result/Evaluation_improve/{subject_name}_GBSR_FOR_MBFL_{type_}.json', 'r') as rf:
        #             datas = json.load(rf)
        #         print("GET JSON FILE FINISHED!", end='\n\n')
        #     in_data = integrate(f'../Result/Evaluation_improve/{subject_name}_GBSR_FOR_MBFL_{type_}.json')
        #     for k, v in in_data.items():
        #         print(k, v)
        print(return_json)
        Save_json(return_json, f'../Result/Evaluation_improve/{subject_name}_save_.json')
        end_json[subject_name] = return_json
    Save_json(end_json, f'../Result/Evaluation_improve/save_.json')
    # toExcel(end_json)
    return


import pandas as pd

if __name__ == "__main__":
    main()

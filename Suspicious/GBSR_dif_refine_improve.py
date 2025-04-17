import json
import os
import pickle
import re

import numpy as np


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


def Deal_SBFL(cal_weight):
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath']
    # Subject_name = ["Lang"]
    for subject_name in Subject_name:
        with open(f'../Result/Suspicious/{subject_name}/SBFL_m.json', 'r') as rf:
            suspicious_datas = json.load(rf)
        with open(f"../Result/Weight_improve/{subject_name}.json", "r") as f:
            weight_datas = json.load(f)
        save_json = {}
        for sus_subject_no, sus_method_list in suspicious_datas.items():
            this_subject_dic = {}

            # 首先要获取该项目下的 每一个方法的每一个公式下的怀疑度总和
            this_sum_for_each_formula = {}
            for formula in formula_list:
                this_formula_sus_sum = 0
                # this_formula_sus_sum[formula] = 0

                for sus_method_no, sus_dif_cal_data in sus_method_list.items():
                    this_formula_sus_sum += sus_dif_cal_data[formula]

                this_sum_for_each_formula[formula] = this_formula_sus_sum
            # print(this_sum_for_each_formula.items())
            # 然后要获取该项目下的 每权重信息的权重总和
            this_sum_for_weight = 0
            this_weight_data = weight_datas[sus_subject_no]
            this_weight_value = this_weight_data["P_value"]
            this_weight_number = this_weight_data["number_method"]
            for i in range(this_weight_number):
                this_sum_for_weight += this_weight_value[i]
            # print(this_sum_for_weight)

            for sus_method_no, sus_dif_cal_data in sus_method_list.items():
                p_value = weight_datas[sus_subject_no]["F_value"][int(sus_method_no)] - weight_datas[sus_subject_no]["P_value"][int(sus_method_no)]
                this_method_dic = {}
                for formula in formula_list:
                    this_method_dic[formula] = Calculate(p_value, sus_dif_cal_data[formula], this_sum_for_weight,
                                                         this_sum_for_each_formula[formula], cal_weight)
                this_subject_dic[sus_method_no] = this_method_dic
            save_json[sus_subject_no] = this_subject_dic
        Save_path = f"""../Result/Suspicious_improve/{subject_name}/GBSR_FOR_SBFL_{cal_weight}.json"""
        Save_json(save_json,Save_path)
    # for k, v in save_json.items():
    #     print(k, "\n", v)
    #     print(suspicious_datas[k])
    #     print(weight_datas[k]["P_value"])
    # # print(save_json)

    return


def Deal_MBFL(cal_weight):
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath']
    # Subject_name = ["Lang"]
    for subject_name in Subject_name:
        with open(f'../Result/Suspicious/{subject_name}/MBFL_clear_method.json', 'r') as rf:
            suspicious_datas = json.load(rf)
        with open(f"../Result/Weight_improve/{subject_name}.json", "r") as f:
            weight_datas = json.load(f)
        save_json = {}
        for sus_subject_no, sus_method_list in suspicious_datas.items():
            this_subject_dic = {}

            # 首先要获取该项目下的 每一个方法的每一个公式下的怀疑度总和
            this_sum_for_each_formula = {}
            for formula in formula_list:
                this_formula_sus_sum = 0
                # this_formula_sus_sum[formula] = 0

                for sus_method_no, sus_dif_cal_data in sus_method_list.items():
                    this_formula_sus_sum += sus_dif_cal_data["max"][formula]

                this_sum_for_each_formula[formula] = this_formula_sus_sum
            # print(this_sum_for_each_formula.items())
            # 然后要获取该项目下的 每权重信息的权重总和
            this_sum_for_weight = 0
            this_weight_data = weight_datas[sus_subject_no]
            this_weight_value = this_weight_data["P_value"]
            this_weight_number = this_weight_data["number_method"]
            for i in range(this_weight_number):
                this_sum_for_weight += this_weight_value[i]
            # print(this_sum_for_weight)

            for sus_method_no, sus_dif_cal_data in sus_method_list.items():
                p_value = weight_datas[sus_subject_no]["F_value"][int(sus_method_no)] - weight_datas[sus_subject_no]["P_value"][int(sus_method_no)]
                this_method_dic = {}
                for formula in formula_list:
                    this_method_dic[formula] = Calculate(p_value, sus_dif_cal_data["max"][formula], this_sum_for_weight,
                                                         this_sum_for_each_formula[formula], cal_weight)
                this_subject_dic[sus_method_no] = this_method_dic
            save_json[sus_subject_no] = this_subject_dic
        Save_path = f"""../Result/Suspicious_improve/{subject_name}/GBSR_FOR_MBFL_{cal_weight}.json"""
        Save_json(save_json, Save_path)
    # for k, v in save_json.items():
    #     print(k, "\n", v)
    #     print(suspicious_datas[k])
    #     print(weight_datas[k]["P_value"])
    # # print(save_json)

    return



def Deal_Grace():


    return


def Calculate(w, s, sum_w, sum_s, cal_weight):
    if sum_w == 0: sum_w = 1
    if sum_s == 0: sum_s = 1

    if cal_weight == 0:
        return w
    if cal_weight == 1:
        return w / sum_w + s / sum_s
    if cal_weight == 2:
        return 1 / (1 + np.exp(-w)) + 1 / (1 + np.exp(-s))

    if cal_weight == 3:
        return (1 + w) * s
    if cal_weight == 4:
        return (1 + 1 / (1 + np.exp(-w))) * s
    if cal_weight == 5:
        return (1 + 1 / (1 + np.exp(-w))) * (1 / (1 + np.exp(-s)))

    if cal_weight == 6:
        return w * s
    if cal_weight == 7:
        return (1 / (1 + np.exp(-w))) * s
    if cal_weight == 8:
        return (1 / (1 + np.exp(-w))) * (1 / (1 + np.exp(-s)))


if __name__ == "__main__":

    type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for type_ in type_list:
        Deal_SBFL(type_)
        # Deal_MBFL(type_)

    # Calculate()

import json
import os
import pickle
import re
import random
from collections import defaultdict

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


def get_keys_sorted_by_value(dic):
    sorted_keys = [k for k, v in sorted(dic.items(), key=lambda x: x[1], reverse=True)]
    return sorted_keys


def GB_Reduce_Only_Mutations(rate=1):
    # 先获得权重信息

    # Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Result/Weight_Simple/{subject_name}.json', 'r') as rf:
            weight_datas = json.load(rf)
        print("GET Weight JSON FILE FINISHED!", end='\n\n')

        with open(f"../Data/{subject_name}.json", "r") as dataf:
            datas = json.load(dataf)
        print("GET Data JSON FILE FINISHED!", end='\n\n')
        save_json = {}
        Four_dic = f'''../Four_canshu/Reduce_MBFL_Simple_Graph_Only_Mutation/{subject_name}'''
        for data in datas:

            data_name = data['proj']
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']

            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])

            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')
            line2mutation = {}
            for i in range(len_lines):
                line2mutation[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if u not in line2mutation[l]:
                    line2mutation[l].append(u)
            print(line2mutation)

            # 获取权重信息并排序获得列表
            v = weight_datas[data_name]
            print(len((v["value"])))
            number_ftest = v["number_ftest"]
            number_rtest = v["number_rtest"]
            number_statement = v["number_statement"]
            number_method = v["number_method"]
            # number_mutation = v["number_mutation"]
            # print(number_mutation, number_method, number_rtest, number_ftest, number_statement)
            method_list = v["value"][0:number_method]
            statement_list = v["value"][number_method:number_method + number_statement]
            # mutation_list = v["value"][number_method+number_method:number_method+number_method+number_mutation]
            rtest_list = v["value"][number_method + number_statement:number_method + number_statement + number_rtest]
            ftest_list = v["value"][
                         number_method + number_statement + number_rtest:number_method + number_statement + number_rtest + number_ftest]
            # print(method_list)
            method_dic = {index: value for index, value in enumerate(method_list)}
            statement_dic = {index: value for index, value in enumerate(statement_list)}
            rtest_dic = {index: value for index, value in enumerate(rtest_list)}
            ftest_dic = {index: value for index, value in enumerate(ftest_list)}

            method_keys = get_keys_sorted_by_value(method_dic)
            statement_keys = get_keys_sorted_by_value(statement_dic)
            rtest_keys = get_keys_sorted_by_value(rtest_dic)
            ftest_keys = get_keys_sorted_by_value(ftest_dic)

            # print(rtest_dic)
            # print(rtest_keys)
            # print(statement_dic)
            print(statement_keys)

            # 需要按照比率约简变异体使用数量

            # 划分为10部分并按比例赋值
            num_parts = 10
            ratios = [round((num_parts - i) / num_parts, 1) for i in range(1, num_parts + 1)]
            n = len(statement_keys)

            # 确保列表不足10时，每个元素都有分配的比例值
            partition_size = max(1, n // num_parts + 1)  # 最小分组大小为1
            statement_rate_dict = {}

            for i, ratio in enumerate(ratios):
                start_index = i * partition_size
                end_index = (i + 1) * partition_size if i < num_parts - 1 else n
                # 防止索引超出实际长度
                for key in statement_keys[start_index:min(end_index, n)]:
                    statement_rate_dict[key] = ratio

            # 输出结果字典
            print(statement_rate_dict)

            for l_no, u_msg in line2mutation.items():
                this_num_left = min(len(u_msg), int(statement_rate_dict[l_no] * len(u_msg) + 1))
                print(len(u_msg), statement_rate_dict[l_no], this_num_left, end=" ")
                line2mutation[l_no] = random.sample(u_msg, this_num_left)  # 随机抽取指定数量的元素

            print("\n")
            # 对字典中的每个列表按比例保留元素

            print(line2mutation)

            method2mutant = {}
            for i in range(len_method):
                method2mutant[i] = []
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_m2u = []
                # print(m_l)
                for l_no, u_msg in line2mutation.items():

                    # print(u2l,"----------------")
                    if l_no == l:
                        # print(u2l, "----------------")
                        for u in u_msg:
                            if u not in this_m2u:
                                this_m2u.append(u)
                # print(m, this_m2u)
                method2mutant[m].extend(this_m2u)
            print(method2mutant)

            # 得到每一个变异体的四种参数！因此每一个方法拥有着和ta对应的变异体数量相同的四参数组合
            mutant_total_dic = {}
            for k, v in mutation.items():
                mutant_dic = {}
                akf = 0
                anf = 0
                akp = 0
                anp = 0
                for u2r in mutation2rtest:
                    if u2r[0] == v:
                        akp += 1
                for u2f in mutation2ftest:
                    if u2f[0] == v:
                        akf += 1
                anp = len_rtest - akp
                anf = len_ftest - anf
                mutant_dic["akf"] = akf
                mutant_dic["anf"] = anf
                mutant_dic["akp"] = akp
                mutant_dic["anp"] = anp
                mutant_total_dic[v] = mutant_dic
            # print(mutant_total_dic)

            save_dic = {}
            for k, v in method2mutant.items():
                print(k, v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save

            proj = data_name

            save_json[proj] = save_dic
            # print(save_json)
        save_path = f'''{Four_dic}.json'''
        Save_json(save_json, save_path)
        # method_dic = {index: value for index, value in enumerate(method_list)}


def create_unique_value_dict_with_random_keys(input_dict):
    value_to_keys = {}
    # Group keys by their values
    for key, value in input_dict.items():
        if value not in value_to_keys:
            value_to_keys[value] = []
        value_to_keys[value].append(key)

    unique_value_dict = {}
    # Randomly select keys based on the rule
    for value, keys in value_to_keys.items():
        num_keys_to_select = 1 + (len(keys) // 5)  # One key + one for every 5 keys
        selected_keys = random.sample(keys, min(num_keys_to_select, len(keys)))
        for key in selected_keys:
            unique_value_dict[key] = value

    return unique_value_dict


def GB_Reduce_Only_Tests(rate=1):
    # 先获得权重信息

    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Result/Weight_Simple/{subject_name}.json', 'r') as rf:
            weight_datas = json.load(rf)
        print("GET Weight JSON FILE FINISHED!", end='\n\n')

        with open(f"../Data/{subject_name}.json", "r") as dataf:
            datas = json.load(dataf)
        print("GET Data JSON FILE FINISHED!", end='\n\n')
        save_json = {}
        Four_dic = f'''../Four_canshu/Reduce_MBFL_Simple_Graph_Only_Test/{subject_name}'''
        for data in datas:

            data_name = data['proj']
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']

            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])

            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')
            line2mutation = {}
            for i in range(len_lines):
                line2mutation[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if u not in line2mutation[l]:
                    line2mutation[l].append(u)
            print(line2mutation)

            # 获取权重信息并排序获得列表
            v = weight_datas[data_name]
            print(len((v["value"])))
            number_ftest = v["number_ftest"]
            number_rtest = v["number_rtest"]
            number_statement = v["number_statement"]
            number_method = v["number_method"]
            number_mutation = v["number_mutation"]
            print(number_mutation, number_method, number_rtest, number_ftest, number_statement)
            method_list = v["value"][0:number_method]
            statement_list = v["value"][number_method:number_method + number_statement]
            # mutation_list = v["value"][number_method+number_method:number_method+number_method+number_mutation]
            rtest_list = v["value"][number_method + number_statement:number_method + number_statement + number_rtest]
            ftest_list = v["value"][
                         number_method + number_statement + number_rtest:number_method + number_statement + number_rtest + number_ftest]
            # print(method_list)
            method_dic = {index: value for index, value in enumerate(method_list)}
            statement_dic = {index: value for index, value in enumerate(statement_list)}
            rtest_dic = {index: value for index, value in enumerate(rtest_list)}
            ftest_dic = {index: value for index, value in enumerate(ftest_list)}

            method_keys = get_keys_sorted_by_value(method_dic)
            statement_keys = get_keys_sorted_by_value(statement_dic)
            rtest_keys = get_keys_sorted_by_value(rtest_dic)
            ftest_keys = get_keys_sorted_by_value(ftest_dic)

            print(rtest_dic)
            print(rtest_keys)
            # print(statement_dic)
            # print(statement_keys)
            new_rtest_dic = create_unique_value_dict_with_random_keys(rtest_dic)
            rtest_keys = get_keys_sorted_by_value(new_rtest_dic)
            print(rtest_dic)
            print(rtest_keys)

            # break

            # # 需要按照比率约简变异体使用数量
            #
            # # 划分为10部分并按比例赋值
            # num_parts = 10
            # ratios = [round((num_parts - i) / num_parts, 1) for i in range(1, num_parts + 1)]
            # n = len(statement_keys)
            #
            # # 确保列表不足10时，每个元素都有分配的比例值
            # partition_size = max(1, n // num_parts + 1)  # 最小分组大小为1
            # statement_rate_dict = {}
            #
            # for i, ratio in enumerate(ratios):
            #     start_index = i * partition_size
            #     end_index = (i + 1) * partition_size if i < num_parts - 1 else n
            #     # 防止索引超出实际长度
            #     for key in statement_keys[start_index:min(end_index, n)]:
            #         statement_rate_dict[key] = ratio
            #
            # # 输出结果字典
            # print(statement_rate_dict)
            #
            # for l_no, u_msg in line2mutation.items():
            #     this_num_left = min(len(u_msg), int(statement_rate_dict[l_no] * len(u_msg) + 1))
            #     print(len(u_msg), statement_rate_dict[l_no], this_num_left, end=" ")
            #     line2mutation[l_no] = random.sample(u_msg, this_num_left)  # 随机抽取指定数量的元素
            #
            # print("\n")
            # # 对字典中的每个列表按比例保留元素
            #
            # print(line2mutation)

            new_mutation2rtest = []
            for m2r in mutation2rtest:
                if m2r[1] in rtest_keys:
                    new_mutation2rtest.append(m2r)
            print(mutation2rtest)
            print(new_mutation2rtest)

            method2mutant = {}
            for i in range(len_method):
                method2mutant[i] = []
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_m2u = []
                # print(m_l)
                for l_no, u_msg in line2mutation.items():

                    # print(u2l,"----------------")
                    if l_no == l:
                        # print(u2l, "----------------")
                        for u in u_msg:
                            if u not in this_m2u:
                                this_m2u.append(u)
                # print(m, this_m2u)
                method2mutant[m].extend(this_m2u)
            print(method2mutant)

            # 得到每一个变异体的四种参数！因此每一个方法拥有着和ta对应的变异体数量相同的四参数组合
            mutant_total_dic = {}
            for k, v in mutation.items():
                mutant_dic = {}
                akf = 0
                anf = 0
                akp = 0
                anp = 0
                for u2r in new_mutation2rtest:
                    if u2r[0] == v:
                        akp += 1
                for u2f in mutation2ftest:
                    if u2f[0] == v:
                        akf += 1
                anp = len(rtest_keys) - akp
                anf = len_ftest - anf
                mutant_dic["akf"] = akf
                mutant_dic["anf"] = anf
                mutant_dic["akp"] = akp
                mutant_dic["anp"] = anp
                mutant_total_dic[v] = mutant_dic
            # print(mutant_total_dic)

            save_dic = {}
            for k, v in method2mutant.items():
                print(k, v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save

            proj = data_name

            save_json[proj] = save_dic
            # print(save_json)
        save_path = f'''{Four_dic}.json'''
        Save_json(save_json, save_path)
        # method_dic = {index: value for index, value in enumerate(method_list)}


def GB_Reduce_Both(rate=1):
    # 先获得权重信息

    # Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Result/Weight_Simple/{subject_name}.json', 'r') as rf:
            weight_datas = json.load(rf)
        print("GET Weight JSON FILE FINISHED!", end='\n\n')

        with open(f"../Data/{subject_name}.json", "r") as dataf:
            datas = json.load(dataf)
        print("GET Data JSON FILE FINISHED!", end='\n\n')
        save_json = {}
        Four_dic = f'''../Four_canshu/Reduce_MBFL_Simple_Graph_Both/{subject_name}'''
        for data in datas:

            data_name = data['proj']
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']

            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])

            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')
            line2mutation = {}
            for i in range(len_lines):
                line2mutation[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if u not in line2mutation[l]:
                    line2mutation[l].append(u)
            print(line2mutation)

            # 获取权重信息并排序获得列表
            v = weight_datas[data_name]
            print(len((v["value"])))
            number_ftest = v["number_ftest"]
            number_rtest = v["number_rtest"]
            number_statement = v["number_statement"]
            number_method = v["number_method"]
            # number_mutation = v["number_mutation"]
            # print(number_mutation, number_method, number_rtest, number_ftest, number_statement)
            print(number_method, number_rtest, number_ftest, number_statement)
            method_list = v["value"][0:number_method]
            statement_list = v["value"][number_method:number_method + number_statement]
            # mutation_list = v["value"][number_method+number_method:number_method+number_method+number_mutation]
            rtest_list = v["value"][number_method + number_statement:number_method + number_statement + number_rtest]
            ftest_list = v["value"][
                         number_method + number_statement + number_rtest:number_method + number_statement + number_rtest + number_ftest]
            # print(method_list)
            method_dic = {index: value for index, value in enumerate(method_list)}
            statement_dic = {index: value for index, value in enumerate(statement_list)}
            rtest_dic = {index: value for index, value in enumerate(rtest_list)}
            ftest_dic = {index: value for index, value in enumerate(ftest_list)}

            method_keys = get_keys_sorted_by_value(method_dic)
            statement_keys = get_keys_sorted_by_value(statement_dic)
            rtest_keys = get_keys_sorted_by_value(rtest_dic)
            ftest_keys = get_keys_sorted_by_value(ftest_dic)

            # print(rtest_dic)
            # print(rtest_keys)
            # print(statement_dic)
            print(statement_keys)

            new_rtest_dic = create_unique_value_dict_with_random_keys(rtest_dic)
            rtest_keys = get_keys_sorted_by_value(new_rtest_dic)
            print(rtest_dic)
            print(rtest_keys)

            # 需要按照比率约简变异体使用数量

            # 划分为10部分并按比例赋值
            num_parts = 10
            ratios = [round((num_parts - i) / num_parts, 1) for i in range(1, num_parts + 1)]
            n = len(statement_keys)

            # 确保列表不足10时，每个元素都有分配的比例值
            partition_size = max(1, n // num_parts + 1)  # 最小分组大小为1
            statement_rate_dict = {}

            for i, ratio in enumerate(ratios):
                start_index = i * partition_size
                end_index = (i + 1) * partition_size if i < num_parts - 1 else n
                # 防止索引超出实际长度
                for key in statement_keys[start_index:min(end_index, n)]:
                    statement_rate_dict[key] = ratio

            # 输出结果字典
            print(statement_rate_dict)

            for l_no, u_msg in line2mutation.items():
                this_num_left = min(len(u_msg), int(statement_rate_dict[l_no] * len(u_msg) + 1))
                print(len(u_msg), statement_rate_dict[l_no], this_num_left, end=" ")
                line2mutation[l_no] = random.sample(u_msg, this_num_left)  # 随机抽取指定数量的元素

            print("\n")
            # 对字典中的每个列表按比例保留元素

            print(line2mutation)

            new_mutation2rtest = []
            for m2r in mutation2rtest:
                if m2r[1] in rtest_keys:
                    new_mutation2rtest.append(m2r)
            print(mutation2rtest)
            print(new_mutation2rtest)

            method2mutant = {}
            for i in range(len_method):
                method2mutant[i] = []
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_m2u = []
                # print(m_l)
                for l_no, u_msg in line2mutation.items():

                    # print(u2l,"----------------")
                    if l_no == l:
                        # print(u2l, "----------------")
                        for u in u_msg:
                            if u not in this_m2u:
                                this_m2u.append(u)
                # print(m, this_m2u)
                method2mutant[m].extend(this_m2u)
            print(method2mutant)

            # 得到每一个变异体的四种参数！因此每一个方法拥有着和ta对应的变异体数量相同的四参数组合
            mutant_total_dic = {}
            for k, v in mutation.items():
                mutant_dic = {}
                akf = 0
                anf = 0
                akp = 0
                anp = 0
                for u2r in new_mutation2rtest:
                    if u2r[0] == v:
                        akp += 1
                for u2f in mutation2ftest:
                    if u2f[0] == v:
                        akf += 1
                anp = len(rtest_keys) - akp
                anf = len_ftest - anf
                mutant_dic["akf"] = akf
                mutant_dic["anf"] = anf
                mutant_dic["akp"] = akp
                mutant_dic["anp"] = anp
                mutant_total_dic[v] = mutant_dic
            # print(mutant_total_dic)

            save_dic = {}
            for k, v in method2mutant.items():
                print(k, v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save

            proj = data_name

            save_json[proj] = save_dic
            # print(save_json)
        save_path = f'''{Four_dic}.json'''
        Save_json(save_json, save_path)
        # method_dic = {index: value for index, value in enumerate(method_list)}


def FTMES():
    # 先获得权重信息

    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f"../Data/{subject_name}.json", "r") as dataf:
            datas = json.load(dataf)
        print("GET Data JSON FILE FINISHED!", end='\n\n')
        save_json = {}
        Four_dic = f'''../Four_canshu/Reduce_MBFL_FTMES/{subject_name}'''
        for data in datas:

            data_name = data['proj']
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']

            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])

            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')

            mutation2lines_dic = {}
            for i in range(len_mutation):
                mutation2lines_dic[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if l not in mutation2lines_dic[u]:
                    mutation2lines_dic[u].append(l)
            print("mutation2lines_dic:", mutation2lines_dic)
            # lines2rtest_dic = {}
            # for i in range(len_rtest):
            #     lines2rtest_dic[i] = []
            # for l_r in mutation2lines:
            #     l = l_r[0]
            #     r = l_r[1]
            #     this_m2u = []
            #     if l not in mutation2lines_dic[u]:
            #         mutation2lines_dic[l].append(u)
            #

            line2mutation = {}
            for i in range(len_lines):
                line2mutation[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if u not in line2mutation[l]:
                    line2mutation[l].append(u)
            print("line2mutation", line2mutation)

            method2mutant = {}
            for i in range(len_method):
                method2mutant[i] = []
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_m2u = []
                # print(m_l)
                for l_no, u_msg in line2mutation.items():
                    # print(u2l,"----------------")
                    if l_no == l:
                        # print(u2l, "----------------")
                        for u in u_msg:
                            if u not in this_m2u:
                                this_m2u.append(u)
                # print(m, this_m2u)
                method2mutant[m].extend(this_m2u)
            print(method2mutant)

            # 得到每一个变异体的四种参数！因此每一个方法拥有着和ta对应的变异体数量相同的四参数组合
            mutant_total_dic = {}
            for k, v in mutation.items():
                mutant_dic = {}
                akf = 0
                anf = 0
                akp = 0
                anp = 0
                for u2r in mutation2rtest:
                    this_l = mutation2lines_dic[u2r[0]]
                    if [this_l, u2r[1]] in lines2rtest:
                        akp += 1
                for u2f in mutation2ftest:
                    if u2f[0] == v:
                        akf += 1
                anp = len_rtest - akp
                anf = len_ftest - anf
                mutant_dic["akf"] = akf
                mutant_dic["anf"] = anf
                mutant_dic["akp"] = akp
                mutant_dic["anp"] = anp
                mutant_total_dic[v] = mutant_dic
            print("mutant_total_dic", mutant_total_dic)

            save_dic = {}
            for k, v in method2mutant.items():
                print(k, v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save

            proj = data_name

            save_json[proj] = save_dic
            print("save_json", save_json)
        save_path = f'''{Four_dic}.json'''
        Save_json(save_json, save_path)

    return


def FTMES_GPT():
    # 先获得权重信息

    Subject_name = ['JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f"../Data/{subject_name}.json", "r") as dataf:
            datas = json.load(dataf)
        print("GET Data JSON FILE FINISHED!", end='\n\n')
        save_json = {}
        Four_dic = f'''../Four_canshu/Reduce_MBFL_FTMES/{subject_name}'''
        for data in datas:

            data_name = data['proj']
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']

            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])

            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')

            mutation2lines_dic = {}
            for i in range(len_mutation):
                mutation2lines_dic[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if l not in mutation2lines_dic[u]:
                    mutation2lines_dic[u].append(l)

            line2mutation = {}
            for i in range(len_lines):
                line2mutation[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if u not in line2mutation[l]:
                    line2mutation[l].append(u)
            # print("line2mutation", line2mutation)

            method2mutant = {}
            for i in range(len_method):
                method2mutant[i] = []
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_m2u = []
                # print(m_l)
                for l_no, u_msg in line2mutation.items():
                    # print(u2l,"----------------")
                    if l_no == l:
                        # print(u2l, "----------------")
                        for u in u_msg:
                            if u not in this_m2u:
                                this_m2u.append(u)
                # print(m, this_m2u)
                method2mutant[m].extend(this_m2u)
            # print(method2mutant)
            # 将 lines2rtest 转为集合，以元组形式存储
            lines2rtest_set = {tuple(item) for item in lines2rtest}  # 将每个列表转换为元组

            # 构建 mutation2lines_dic 的缓存，避免每次访问字典
            mutation2lines_cache = {k: mutation2lines_dic[k] for k in mutation2lines_dic}

            # 初始化总结果字典
            mutant_total_dic = {}

            for k, v in mutation.items():
                # 初始化计数
                akf = 0
                akp = 0

                # 遍历 mutation2rtest 并计算 akp
                akp = sum(
                    1 for u2r in mutation2rtest
                    if (tuple(mutation2lines_cache[u2r[0]]), u2r[1]) in lines2rtest_set
                )

                # 遍历 mutation2ftest 并计算 akf
                akf = sum(1 for u2f in mutation2ftest if u2f[0] == v)

                # 计算剩余值
                anp = len_rtest - akp
                anf = len_ftest - akf

                # 更新结果字典
                mutant_total_dic[v] = {"akf": akf, "anf": anf, "akp": akp, "anp": anp}
            save_dic = {}
            for k, v in method2mutant.items():
                print(k, v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save

            proj = data_name

            save_json[proj] = save_dic
            # print("save_json", save_json)
        save_path = f'''{Four_dic}.json'''
        Save_json(save_json, save_path)

    return


def CBTCR():
    # 先获得权重信息

    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Code/CBTCR/{subject_name}_CBTCR_method.json', 'r') as rf:
            weight_datas = json.load(rf)
        print("GET Weight JSON FILE FINISHED!", end='\n\n')

        with open(f"../Data/{subject_name}.json", "r") as dataf:
            datas = json.load(dataf)
        print("GET Data JSON FILE FINISHED!", end='\n\n')
        save_json = {}
        Four_dic = f'''../Four_canshu/Reduce_MBFL_CBTCR/{subject_name}'''
        for data in datas:

            data_name = data['proj']
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']

            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])

            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')
            line2mutation = {}
            for i in range(len_lines):
                line2mutation[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if u not in line2mutation[l]:
                    line2mutation[l].append(u)
            print(line2mutation)

            # 获取权重信息并排序获得列表
            v = weight_datas['rtest'][data_name]


            rtest_dic = {index: value for index, value in enumerate(v)}


            rtest_keys = get_keys_sorted_by_value(rtest_dic)

            print(rtest_dic)
            print(rtest_keys)
            # print(statement_dic)
            # print(statement_keys)
            # new_rtest_dic = create_unique_value_dict_with_random_keys(rtest_dic)


            # print(rtest_dic)
            # print(rtest_keys)
            rtest_keys = rtest_keys[:int(len_rtest*0.3)]

            new_mutation2rtest = []
            for m2r in mutation2rtest:
                if m2r[1] in rtest_keys:
                    new_mutation2rtest.append(m2r)
            print(mutation2rtest)
            print(new_mutation2rtest)

            method2mutant = {}
            for i in range(len_method):
                method2mutant[i] = []
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_m2u = []
                # print(m_l)
                for l_no, u_msg in line2mutation.items():

                    # print(u2l,"----------------")
                    if l_no == l:
                        # print(u2l, "----------------")
                        for u in u_msg:
                            if u not in this_m2u:
                                this_m2u.append(u)
                # print(m, this_m2u)
                method2mutant[m].extend(this_m2u)
            print(method2mutant)

            # 得到每一个变异体的四种参数！因此每一个方法拥有着和ta对应的变异体数量相同的四参数组合
            mutant_total_dic = {}
            for k, v in mutation.items():
                mutant_dic = {}
                akf = 0
                anf = 0
                akp = 0
                anp = 0
                for u2r in new_mutation2rtest:
                    if u2r[0] == v:
                        akp += 1
                for u2f in mutation2ftest:
                    if u2f[0] == v:
                        akf += 1
                anp = len(rtest_keys) - akp
                anf = len_ftest - anf
                mutant_dic["akf"] = akf
                mutant_dic["anf"] = anf
                mutant_dic["akp"] = akp
                mutant_dic["anp"] = anp
                mutant_total_dic[v] = mutant_dic
            # print(mutant_total_dic)

            save_dic = {}
            for k, v in method2mutant.items():
                print(k, v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save

            proj = data_name

            save_json[proj] = save_dic
            # print(save_json)
        save_path = f'''{Four_dic}.json'''
        Save_json(save_json, save_path)
        # method_dic = {index: value for index, value in enumerate(method_list)}

def SOME():
    # 先获得权重信息

    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Result/Weight_Simple/{subject_name}.json', 'r') as rf:
            weight_datas = json.load(rf)
        print("GET Weight JSON FILE FINISHED!", end='\n\n')

        with open(f"../Data/{subject_name}.json", "r") as dataf:
            datas = json.load(dataf)
        print("GET Data JSON FILE FINISHED!", end='\n\n')
        save_json = {}
        Four_dic = f'''../Four_canshu/Reduce_MBFL_SOME/{subject_name}'''
        for data in datas:

            data_name = data['proj']
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']

            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])

            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')


            line2mutation = {}
            for i in range(len_lines):
                line2mutation[i] = []
            for l_u in mutation2lines:
                u = l_u[0]
                l = l_u[1]
                this_m2u = []
                if u not in line2mutation[l]:
                    line2mutation[l].append(u)
            # print(line2mutation)

            retain_count = int(len(line2mutation) * 0.3)  # 计算保留的元素个数
            # retained_keys = random.sample(list(line2mutation.keys()), retain_count)  # 随机选取保留的键
            # new_dict = {key: my_dict[key] for key in retained_keys}  # 构建新的字典

            new_line2mutation = dict(list(line2mutation.items())[:retain_count])  # 构建新的字典


            # print(line2mutation)

            method2mutant = {}
            for i in range(len_method):
                method2mutant[i] = []
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_m2u = []
                # print(m_l)
                for l_no, u_msg in new_line2mutation.items():

                    # print(u2l,"----------------")
                    if l_no == l:
                        # print(u2l, "----------------")
                        for u in u_msg:
                            if u not in this_m2u:
                                this_m2u.append(u)
                # print(m, this_m2u)
                method2mutant[m].extend(this_m2u)
            print(method2mutant)

            # 得到每一个变异体的四种参数！因此每一个方法拥有着和ta对应的变异体数量相同的四参数组合
            mutant_total_dic = {}
            for k, v in mutation.items():
                mutant_dic = {}
                akf = 0
                anf = 0
                akp = 0
                anp = 0
                for u2r in mutation2rtest:
                    if u2r[0] == v:
                        akp += 1
                for u2f in mutation2ftest:
                    if u2f[0] == v:
                        akf += 1
                anp = len_rtest - akp
                anf = len_ftest - anf
                mutant_dic["akf"] = akf
                mutant_dic["anf"] = anf
                mutant_dic["akp"] = akp
                mutant_dic["anp"] = anp
                mutant_total_dic[v] = mutant_dic
            # print(mutant_total_dic)

            save_dic = {}
            for k, v in method2mutant.items():
                print(k, v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save

            proj = data_name

            save_json[proj] = save_dic
            # print(save_json)
        save_path = f'''{Four_dic}.json'''
        Save_json(save_json, save_path)
        # method_dic = {index: cxvalue for index, value in enumerate(method_list)}
    return


if __name__ == '__main__':
    GB_Reduce_Only_Mutations()
    # GB_Reduce_Only_Tests()
    GB_Reduce_Both()
    #
    # FTMES_GPT()
    # CBTCR()
    # SOME()

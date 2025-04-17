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


if __name__ == '__main__':

    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Data/{subject_name}.json', 'r') as rf:
            datas = json.load(rf)
            print("GET JSON FILE FINISHED!", end='\n\n')
        num_flag = 0
        calls_msgs = ''
        Four_dic = f'''../Four_canshu/SBFL/{subject_name}'''
        print(Four_dic)
        ensure_directory_exists(Four_dic)
        save_json = {}
        suspicious_path = f"""../Result/Suspicious/{subject_name}/SBFL_m.json"""
        with open(suspicious_path, 'r') as sus_f:
            sus_datas = json.load(sus_f)
        this_subject_json = {}
        this_subject_rtest_json = {}
        this_subject_ftest_json = {}
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
            print(len_method, len_lines, len_mutation, len_rtest, len_ftest)
            len_total = len_lines + len_rtest + len_ftest + len_mutation + len_method
            print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
            # print(method)
            method2method = {}
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')


            method2ftest = {}
            method2rtest = {}
            for m_l in method2lines:
                m = m_l[0]
                l = m_l[1]
                this_ftest = []
                this_rtest = []
                for l_ft in lines2ftest:
                    if l_ft[0] == l:
                        if l_ft[1] not in this_ftest:
                            this_ftest.append(l_ft[1])
                for l_rt in lines2rtest:
                    if l_rt[0] == l:
                        if l_rt[1] not in this_rtest:
                            this_rtest.append(l_rt[1])
                method2ftest[m] = this_ftest
                method2rtest[m] = this_rtest

            print(method2rtest)
            print(method2ftest)

            rtest2method = {}
            ftest2method = {}
            for i in range(len_rtest):
                rtest2method[str(i)] = []
            for i in range(len_ftest):
                ftest2method[str(i)] = []

            for method_id, ftest_list in method2ftest.items():
                for this_ftest in ftest_list:
                    if method_id not in ftest2method[str(this_ftest)]:
                        ftest2method[str(this_ftest)].append(method_id)

            for method_id, rtest_list in method2rtest.items():
                for this_rtest in rtest_list:
                    if method_id not in rtest2method[str(this_rtest)]:
                        rtest2method[str(this_rtest)].append(method_id)
            print(rtest2method)
            print(ftest2method)
            # # ftest2statement = {}
            # # rtest2statement = {}
            # #
            # for l_r in lines2rtest:
            #     l = l_r[0]
            #     r = l_r[1]
            #     this_rtest = []
            #     for ll_rr in lines2rtest:
            #         if r == ll_rr[1]:
            #             this_rtest.append(ll_rr[0])
            #     rtest2statement[r] = this_rtest
            #
            # for l_f in lines2ftest:
            #     l = l_f[0]
            #     r = l_f[1]
            #     this_ftest = []
            #     for ll_ff in lines2ftest:
            #         if r == ll_ff[1]:
            #             this_ftest.append(ll_ff[0])
            #     ftest2statement[r] = this_ftest
            #
            # print(rtest2statement)
            # print(ftest2statement)

            this_version_sus_dic = sus_datas[data_name]
            print(this_version_sus_dic)
            rtest_value = {}
            ftest_value = {}

            for rtest_id, corrstatement in rtest2method.items():
                rtest_value[rtest_id] = 0

            for ftest_id, corrstatement in ftest2method.items():
                ftest_value[ftest_id] = 0

            for rtest_id, corrstatement in rtest2method.items():
                for corst in corrstatement:
                    rtest_value[rtest_id] += this_version_sus_dic[str(corst)]["Dstar"]

            for ftest_id, corrstatement in ftest2method.items():
                for corst in corrstatement:
                    ftest_value[ftest_id] += this_version_sus_dic[str(corst)]["Dstar"]

            # print(rtest_value)
            # print(ftest_value)
            this_subject_rtest_json[data_name] = rtest_value
            this_subject_ftest_json[data_name] = ftest_value
        this_subject_json["rtest"] = this_subject_rtest_json
        this_subject_json["ftest"] = this_subject_ftest_json
        save_path = f'''../CBTCR/{subject_name}_CBTCR_method.json'''
        Save_json(this_subject_json, save_path)
        # for m_l in method2lines:
            #     m = m_l[0]
            #     l = m_l[1]
            #     this_ftest = []
            #     this_rtest = []
            #     for l_ft in lines2ftest:
            #         if l_ft[0] == l:
            #             if l_ft[1] not in this_ftest:
            #                 this_ftest.append(l_ft[1])
            #     for l_rt in lines2rtest:
            #         if l_rt[0] == l:
            #             if l_rt[1] not in this_rtest:
            #                 this_rtest.append(l_rt[1])
            #     method2ftest[m] = this_ftest
            #     method2rtest[m] = this_rtest
            #
            #
            # # print(method2lines)
            # # print(lines2ftest)
            # # print(lines2rtest)
            # print(method2rtest)
            # print(method2ftest)

        #     proj = data_name
        #     this_json = {}
        #     for method_no in range(0, len_method):
        #
        #         four_dic = {}
        #         try:
        #             four_dic["aep"] = len(method2rtest[method_no])
        #         except:
        #             four_dic["aep"] = 0
        #         four_dic["anp"] = len_rtest - four_dic["aep"]
        #         try:
        #             four_dic["aef"] = len(method2ftest[method_no])
        #         except:
        #             four_dic["aef"] = 0
        #         four_dic["anf"] = len_ftest - four_dic["aef"]
        #         this_json[method_no] = four_dic
        #         # print(this_json)
        #     save_json[proj] = this_json
        # print(save_json)


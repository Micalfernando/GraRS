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

    # Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    Subject_name = ['Math']
    for subject_name in Subject_name:
        with open(f'../Data/{subject_name}.json', 'r') as rf:
            datas = json.load(rf)
            print("GET JSON FILE FINISHED!", end='\n\n')
        num_flag = 0
        calls_msgs = ''
        Four_dic = f'''../Four_canshu/MBFL/{subject_name}'''
        print(Four_dic)
        ensure_directory_exists(Four_dic)
        save_json = {}
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

            # print(mutation)
            statement2mutant = {}
            for i in range(len_lines):
                statement2mutant[i] = []

            for u2l in mutation2lines:
                this_u = u2l[0]
                this_l = u2l[1]
                if this_u not in statement2mutant[this_l]:
                    statement2mutant[this_l].append(this_u)
            # for m_l in method2lines:
            #     m = m_l[0]
            #     l = m_l[1]
            #     this_m2u = []
            #     # print(m_l)
            #     for u2l in mutation2lines:
            #         # print(u2l,"----------------")
            #         if u2l[1] == l:
            #             # print(u2l, "----------------")
            #
            #             if u2l[0] not in this_m2u:
            #                 this_m2u.append(u2l[0])
            #     # print(m, this_m2u)
            #     method2mutant[m].extend(this_m2u)
            # print(method2mutant)


            # 得到每一个变异体的四种参数！因此每一个方法拥有着和ta对应的变异体数量相同的四参数组合
            mutant_total_dic = {}
            for k,v in mutation.items():
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
            for k, v in statement2mutant.items():
                print(k,v)
                this_save = []
                for vv in v:
                    this_save.append(mutant_total_dic[vv])
                save_dic[k] = this_save
            # print(save_dic)

        #     method2ftest = {}
        #     method2rtest = {}
        #
        #     for m_l in method2lines:
        #         m = m_l[0]
        #         l = m_l[1]
        #         this_ftest = []
        #         this_rtest = []
        #         for l_ft in lines2ftest:
        #             if l_ft[0] == l:
        #                 if l_ft[1] not in this_ftest:
        #                     this_ftest.append(l_ft[1])
        #         for l_rt in lines2rtest:
        #             if l_rt[0] == l:
        #                 if l_rt[1] not in this_rtest:
        #                     this_rtest.append(l_rt[1])
        #         method2ftest[m] = this_ftest
        #         method2rtest[m] = this_rtest
        #     # print(method2lines)
        #     # print(lines2ftest)
        #     # print(lines2rtest)
        #     # print(method2rtest)
        #     # print(method2ftest)
        #
            proj = data_name

            save_json[proj] = save_dic
        # print(save_json)
        save_path = f'''{Four_dic}_statement.json'''
        Save_json(save_json, save_path)

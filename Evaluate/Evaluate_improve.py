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


def get_top_n_rank(sus_dic, fault_list):
    top1 = 0
    top3 = 0
    top5 = 0
    top10 = 0
    for fault in fault_list:
        this_fault_rank = 0
        # print("fault:", fault, sus_dic)
        this_fault_sus = sus_dic[str(fault)]
        # print(sus_dic)
        for m_id, suspicious in sus_dic.items():
            if suspicious >= this_fault_sus:
                this_fault_rank += 1
        if this_fault_rank <= 1:    top1 += 1
        if this_fault_rank <= 3:    top3 += 1
        if this_fault_rank <= 5:    top5 += 1
        if this_fault_rank <= 10:    top10 += 1

    return top1, top3, top5, top10


def get_mar(sus_dic, fault_list):
    mar = 0
    for fault in fault_list:
        this_fault_rank = 0
        this_fault_sus = sus_dic[str(fault)]
        for m_id, suspicious in sus_dic.items():
            if suspicious >= this_fault_sus:
                this_fault_rank += 1
        mar = this_fault_rank + mar

    return mar / len(fault_list)


def get_mfr(sus_dic, fault_list):
    mfr = 0
    for fault in fault_list:
        this_fault_rank = 1
        this_fault_sus = sus_dic[str(fault)]
        for m_id, suspicious in sus_dic.items():
            if suspicious > this_fault_sus:
                this_fault_rank += 1
        mfr = this_fault_rank + mfr
    return mfr / len(fault_list)


def get_exam(sus_dic, fault_list, method_count):
    exam = 0
    for fault in fault_list:
        this_fault_rank = 0
        this_fault_sus = sus_dic[str(fault)]
        for m_id, suspicious in sus_dic.items():
            if suspicious >= this_fault_sus:
                this_fault_rank += 1
        exam = this_fault_rank / method_count + exam
    return exam / len(fault_list)


def MBFL_suspicious_method():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Result/Suspicious/{subject_name}/MBFL_m.json', 'r') as rf:
            datas = json.load(rf)
        print("GET JSON FILE FINISHED!", end='\n\n')
        this_version_dic = {}
        for version_id, methoods_msg in datas.items():
            this_method_suspicious_dic = {}
            for method_id, suspicious_msg in methoods_msg.items():
                # print(suspicious_msg) #suspicious_msg是一个列表
                this_method_suspicious_dic_msg = {}
                this_method_suspicious_max = {}
                this_method_suspicious_avg = {}
                for formula in formula_list:
                    this_formula_max_suspicious = 0
                    this_formula_avg_suspicious = 0
                    for suspicious_dic in suspicious_msg:
                        if suspicious_dic[formula] > this_formula_max_suspicious:
                            this_formula_max_suspicious = suspicious_dic[formula]
                        this_formula_avg_suspicious += suspicious_dic[formula]
                    if len(suspicious_msg) != 0:
                        this_formula_avg_suspicious = this_formula_avg_suspicious / len(suspicious_msg)
                    this_method_suspicious_avg[formula] = this_formula_avg_suspicious
                    this_method_suspicious_max[formula] = this_formula_max_suspicious
                this_method_suspicious_dic_msg["max"] = this_method_suspicious_max
                this_method_suspicious_dic_msg["avg"] = this_method_suspicious_avg
                this_method_suspicious_dic[method_id] = this_method_suspicious_dic_msg
            this_version_dic[version_id] = this_method_suspicious_dic
            # print(this_version_dic)

        path = f'../Result/Suspicious/{subject_name}/MBFL_clear_method.json'
        Save_json(this_version_dic, path)


def MBFL_suspicious_statement():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Result/Suspicious/{subject_name}/MBFL_s.json', 'r') as rf:
            datas = json.load(rf)
        print("GET JSON FILE FINISHED!", end='\n\n')
        this_version_dic = {}
        for version_id, methoods_msg in datas.items():
            this_method_suspicious_dic = {}
            for method_id, suspicious_msg in methoods_msg.items():
                this_method_suspicious_dic_msg = {}
                # print(suspicious_msg) #suspicious_msg是一个列表
                this_method_suspicious_max = {}
                this_method_suspicious_avg = {}
                for formula in formula_list:
                    this_formula_max_suspicious = 0
                    this_formula_avg_suspicious = 0
                    for suspicious_dic in suspicious_msg:
                        if suspicious_dic[formula] > this_formula_max_suspicious:
                            this_formula_max_suspicious = suspicious_dic[formula]
                        this_formula_avg_suspicious += suspicious_dic[formula]
                    if len(suspicious_msg) != 0:
                        this_formula_avg_suspicious = this_formula_avg_suspicious / len(suspicious_msg)
                    this_method_suspicious_avg[formula] = this_formula_avg_suspicious
                    this_method_suspicious_max[formula] = this_formula_max_suspicious
                this_method_suspicious_dic_msg["max"] = this_method_suspicious_max
                this_method_suspicious_dic_msg["avg"] = this_method_suspicious_avg
                this_method_suspicious_dic[method_id] = this_method_suspicious_dic_msg
                # print(method_id, this_method_suspicious_max)
            # print(this_method_suspicious_dic)
            this_version_dic[version_id] = this_method_suspicious_dic
            # print(this_version_dic)
            # for k, v in this_version_dic.items():
            #     print(k, v)
            # break
        path = f'../Result/Suspicious/{subject_name}/MBFL_clear_statement.json'
        Save_json(this_version_dic, path)


def MBFL_Evaluate():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Data/{subject_name}.json', 'r') as rf:
            datas = json.load(rf)
        print("GET JSON FILE FINISHED!", end='\n\n')
        with open(f'../Result/Suspicious/{subject_name}/MBFL_clear_method.json', 'r') as rf:
            suspicious_datas = json.load(rf)

        MBFL_evaluate_dic = {}
        for data in datas:
            fault_location = data["ans"]
            version_name = data['proj']
            method_count = len(data['methods'])
            # print(version_name, fault_location)
            this_version_suspicious = suspicious_datas[version_name]
            evaluate_dic_formula = {}
            for formula in formula_list:
                this_formula_dic = {}
                this_formula_max_dic = {}
                this_formula_avg_dic = {}

                this_formula_max_suspicious = {}
                this_formula_avg_suspicious = {}

                for method_id, this_version_sus in this_version_suspicious.items():
                    # print(this_version_sus)
                    this_formula_max_suspicious[method_id] = this_version_sus["max"][formula]
                    this_formula_avg_suspicious[method_id] = this_version_sus["avg"][formula]

                this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5, this_formula_max_top_10 = get_top_n_rank(
                    this_formula_max_suspicious, fault_location)

                this_formula_avg_top_1, this_formula_avg_top_3, this_formula_avg_top_5, this_formula_avg_top_10 = get_top_n_rank(
                    this_formula_avg_suspicious, fault_location)

                this_formula_max_mar = get_mar(this_formula_max_suspicious, fault_location)
                this_formula_max_mfr = get_mfr(this_formula_max_suspicious, fault_location)
                this_formula_max_exam = get_exam(this_formula_max_suspicious, fault_location, method_count)

                this_formula_avg_mar = get_mar(this_formula_avg_suspicious, fault_location)
                this_formula_avg_mfr = get_mfr(this_formula_avg_suspicious, fault_location)
                this_formula_avg_exam = get_exam(this_formula_avg_suspicious, fault_location, method_count)
                # print(len(fault_location), this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5,
                #       this_formula_max_top_10, this_formula_max_mar, this_formula_max_mfr, this_formula_max_exam)

                this_formula_max_dic["top1"] = this_formula_max_top_1
                this_formula_max_dic["top3"] = this_formula_max_top_3
                this_formula_max_dic["top5"] = this_formula_max_top_5
                this_formula_max_dic["top10"] = this_formula_max_top_10
                this_formula_max_dic["mar"] = this_formula_max_mar
                this_formula_max_dic["mfr"] = this_formula_max_mfr
                this_formula_max_dic["exam"] = this_formula_max_exam

                this_formula_avg_dic["top1"] = this_formula_avg_top_1
                this_formula_avg_dic["top3"] = this_formula_avg_top_3
                this_formula_avg_dic["top5"] = this_formula_avg_top_5
                this_formula_avg_dic["top10"] = this_formula_avg_top_10
                this_formula_avg_dic["mar"] = this_formula_avg_mar
                this_formula_avg_dic["mfr"] = this_formula_avg_mfr
                this_formula_avg_dic["exam"] = this_formula_avg_exam
                this_formula_dic["avg"] = this_formula_avg_dic
                this_formula_dic["max"] = this_formula_max_dic
                evaluate_dic_formula[formula] = this_formula_dic
            MBFL_evaluate_dic[version_name] = evaluate_dic_formula
        path = f"F:\GB4FL\Result\Evaluation\{subject_name}_MBFL.json"
        ensure_directory_exists(path)
        Save_json(MBFL_evaluate_dic, path)
    return


def SBFL_Evaluate():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Data/{subject_name}.json', 'r') as rf:
            datas = json.load(rf)
        print("GET JSON FILE FINISHED!", end='\n\n')
        with open(f'../Result/Suspicious/{subject_name}/SBFL_m.json', 'r') as rf:
            suspicious_datas = json.load(rf)

        SBFL_evaluate_dic = {}
        for data in datas:
            fault_location = data["ans"]
            version_name = data['proj']
            method_count = len(data['methods'])
            # print(version_name, fault_location)
            this_version_suspicious = suspicious_datas[version_name]
            evaluate_dic_formula = {}
            for formula in formula_list:
                this_formula_dic = {}
                this_formula_max_dic = {}
                this_formula_avg_dic = {}

                this_formula_max_suspicious = {}

                for method_id, this_version_sus in this_version_suspicious.items():
                    # print(this_version_sus)
                    this_formula_max_suspicious[method_id] = this_version_sus[formula]

                this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5, this_formula_max_top_10 = get_top_n_rank(
                    this_formula_max_suspicious, fault_location)



                this_formula_max_mar = get_mar(this_formula_max_suspicious, fault_location)
                this_formula_max_mfr = get_mfr(this_formula_max_suspicious, fault_location)
                this_formula_max_exam = get_exam(this_formula_max_suspicious, fault_location, method_count)


                # print(len(fault_location), this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5,
                #       this_formula_max_top_10, this_formula_max_mar, this_formula_max_mfr, this_formula_max_exam)

                this_formula_max_dic["top1"] = this_formula_max_top_1
                this_formula_max_dic["top3"] = this_formula_max_top_3
                this_formula_max_dic["top5"] = this_formula_max_top_5
                this_formula_max_dic["top10"] = this_formula_max_top_10
                this_formula_max_dic["mar"] = this_formula_max_mar
                this_formula_max_dic["mfr"] = this_formula_max_mfr
                this_formula_max_dic["exam"] = this_formula_max_exam



                evaluate_dic_formula[formula] = this_formula_max_dic
            SBFL_evaluate_dic[version_name] = evaluate_dic_formula
        path = f"F:\GB4FL\Result\Evaluation\{subject_name}_SBFL.json"
        ensure_directory_exists(path)
        Save_json(SBFL_evaluate_dic, path)
    return
def GBSR_SBFL_Evaluate():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath']
    type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Subject_name = ['Lang']
    for type_ in type_list:

        for subject_name in Subject_name:
            with open(f'../Data/{subject_name}.json', 'r') as rf:
                datas = json.load(rf)
            print("GET JSON FILE FINISHED!", end='\n\n')
            with open(f'../Result/Suspicious_improve/{subject_name}/GBSR_FOR_SBFL_{type_}.json', 'r') as rf:
                suspicious_datas = json.load(rf)
            SBFL_evaluate_dic = {}
            for data in datas:
                fault_location = data["ans"]
                version_name = data['proj']
                method_count = len(data['methods'])
                # print(version_name, fault_location)
                this_version_suspicious = suspicious_datas[version_name]
                evaluate_dic_formula = {}
                for formula in formula_list:
                    this_formula_dic = {}
                    this_formula_max_dic = {}
                    this_formula_avg_dic = {}

                    this_formula_max_suspicious = {}

                    for method_id, this_version_sus in this_version_suspicious.items():
                        # print(this_version_sus)
                        this_formula_max_suspicious[method_id] = this_version_sus[formula]

                    this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5, this_formula_max_top_10 = get_top_n_rank(
                        this_formula_max_suspicious, fault_location)



                    this_formula_max_mar = get_mar(this_formula_max_suspicious, fault_location)
                    this_formula_max_mfr = get_mfr(this_formula_max_suspicious, fault_location)
                    this_formula_max_exam = get_exam(this_formula_max_suspicious, fault_location, method_count)


                    # print(len(fault_location), this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5,
                    #       this_formula_max_top_10, this_formula_max_mar, this_formula_max_mfr, this_formula_max_exam)

                    this_formula_max_dic["top1"] = this_formula_max_top_1
                    this_formula_max_dic["top3"] = this_formula_max_top_3
                    this_formula_max_dic["top5"] = this_formula_max_top_5
                    this_formula_max_dic["top10"] = this_formula_max_top_10
                    this_formula_max_dic["mar"] = this_formula_max_mar
                    this_formula_max_dic["mfr"] = this_formula_max_mfr
                    this_formula_max_dic["exam"] = this_formula_max_exam



                    evaluate_dic_formula[formula] = this_formula_max_dic
                SBFL_evaluate_dic[version_name] = evaluate_dic_formula
            path = f"F:\GB4FL\Result\Evaluation_improve\{subject_name}_GBSR_FOR_SBFL_{type_}.json"
            ensure_directory_exists(path)
            Save_json(SBFL_evaluate_dic, path)


def GBSR_MBFL_Evaluate():
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath']
    type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Subject_name = ['Lang']
    for type_ in type_list:

        for subject_name in Subject_name:
            with open(f'../Data/{subject_name}.json', 'r') as rf:
                datas = json.load(rf)
            print("GET JSON FILE FINISHED!", end='\n\n')
            with open(f'../Result/Suspicious_improve/{subject_name}/GBSR_FOR_MBFL_{type_}.json', 'r') as rf:
                suspicious_datas = json.load(rf)
            SBFL_evaluate_dic = {}
            for data in datas:
                fault_location = data["ans"]
                version_name = data['proj']
                method_count = len(data['methods'])
                # print(version_name, fault_location)
                this_version_suspicious = suspicious_datas[version_name]
                evaluate_dic_formula = {}
                for formula in formula_list:
                    this_formula_dic = {}
                    this_formula_max_dic = {}
                    this_formula_avg_dic = {}

                    this_formula_max_suspicious = {}

                    for method_id, this_version_sus in this_version_suspicious.items():
                        # print(this_version_sus)
                        this_formula_max_suspicious[method_id] = this_version_sus[formula]

                    this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5, this_formula_max_top_10 = get_top_n_rank(
                        this_formula_max_suspicious, fault_location)

                    this_formula_max_mar = get_mar(this_formula_max_suspicious, fault_location)
                    this_formula_max_mfr = get_mfr(this_formula_max_suspicious, fault_location)
                    this_formula_max_exam = get_exam(this_formula_max_suspicious, fault_location, method_count)

                    # print(len(fault_location), this_formula_max_top_1, this_formula_max_top_3, this_formula_max_top_5,
                    #       this_formula_max_top_10, this_formula_max_mar, this_formula_max_mfr, this_formula_max_exam)

                    this_formula_max_dic["top1"] = this_formula_max_top_1
                    this_formula_max_dic["top3"] = this_formula_max_top_3
                    this_formula_max_dic["top5"] = this_formula_max_top_5
                    this_formula_max_dic["top10"] = this_formula_max_top_10
                    this_formula_max_dic["mar"] = this_formula_max_mar
                    this_formula_max_dic["mfr"] = this_formula_max_mfr
                    this_formula_max_dic["exam"] = this_formula_max_exam

                    evaluate_dic_formula[formula] = this_formula_max_dic
                SBFL_evaluate_dic[version_name] = evaluate_dic_formula
            path = f"F:\GB4FL\Result\Evaluation_improve\{subject_name}_GBSR_FOR_MBFL_{type_}.json"
            ensure_directory_exists(path)
            Save_json(SBFL_evaluate_dic, path)


if __name__ == '__main__':
    # 处理MBFL有关语句和方法两个级别的怀疑度值
    # MBFL_suspicious_method()
    # MBFL_suspicious_statement()

    # MBFL_Evaluate()
    # SBFL_Evaluate()

    GBSR_SBFL_Evaluate()
    GBSR_MBFL_Evaluate()



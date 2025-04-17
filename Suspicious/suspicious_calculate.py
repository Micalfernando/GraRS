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
    # else:
    #     print(f"目录 '{directory}' 已存在。")


def Save_json(data, file_path):
    # 确保文件目录存在
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 将数据保存为 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON 文件已保存到: {file_path}")


def Tarantula(aef, aep, anf, anp):
    try:
        sus = (aef / (aef + aep)) / ((aef / (aef + anf)) + (aep / (aep + anp)))
    except:
        sus = 0
    return sus


def Jaccard(aef, aep, anf, anp):
    try:
        sus = aef / (aef + anf + aep)
    except:
        sus = 0
    return sus


def Dstar(aef, aep, anf, anp):
    try:
        sus = (aef ** 2) / (aep + anf)
    except:
        sus = 0
    return sus


def Wong1(aef, aep, anf, anp):
    sus = aef
    return sus


def Hamming(aef, aep, anf, anp):
    sus = aef + anp
    return sus


def Hamann(aef, aep, anf, anp):
    try:
        sus = (aef + anp - aep - anf) / (aef + anp + anf + aep)
    except:
        sus = 0
    return sus


def Op2(aef, aep, anf, anp):
    sus = aef - aep / (aep + anp + 1)
    return sus


def Ochiai(aef, aep, anf, anp):
    try:
        sus = aef / (((aef + anf) * (aef + aep)) ** 0.5)
    except:
        sus = 0
    return sus


def GP13(aef, aep, anf, anp):
    try:
        sus = aef * (1 + 1 / (2 * aep + aef))
    except:
        sus = 0
    return sus


def Dice(aef, aep, anf, anp):
    try:
        sus = 2 * aef / (aef + aep + anf)
    except:
        sus = 0
    return sus


def Calculate(aef, aep, anf, anp):
    this_dic = {'Tarantula': Tarantula(aef, aep, anf, anp), 'Jaccard': Jaccard(aef, aep, anf, anp),
                'Dstar': Dstar(aef, aep, anf, anp), 'Wong1': Wong1(aef, aep, anf, anp),
                'Hamming': Hamming(aef, aep, anf, anp), 'Hamann': Hamann(aef, aep, anf, anp),
                'Op2': Op2(aef, aep, anf, anp), 'Ochiai': Ochiai(aef, aep, anf, anp), 'GP13': GP13(aef, aep, anf, anp),
                'Dice': Dice(aef, aep, anf, anp)}
    return this_dic


def MBFL_m(subject_name):
    with open(f'../Four_canshu/MBFL/{subject_name}.json', 'r') as rf:
        datas = json.load(rf)
        MBFL_m_result = {}
        for dataname, datamsg in datas.items():
            # print(dataname, datamsg)
            this_method_list = {}
            for method_no, mutate_canshu_list in datamsg.items():
                this_method_list[method_no] = []
                for mutate_canshu in mutate_canshu_list:
                    this_calculate_result = Calculate(aef=mutate_canshu['akf'], anf=mutate_canshu['anf'],
                                                      anp=mutate_canshu['anp'], aep=mutate_canshu['akp'])
                    this_method_list[method_no].append(this_calculate_result)
            MBFL_m_result[dataname] = this_method_list
    return MBFL_m_result


def SBFL_m(subject_name):
    with open(f'../Four_canshu/SBFL/{subject_name}.json', 'r') as rf:
        datas = json.load(rf)
        SBFL_m_result = {}
        for dataname, datamsg in datas.items():
            # print(dataname, datamsg)
            this_method_list = {}
            for method_no, canshu in datamsg.items():
                this_method_list[method_no] = Calculate(aef=canshu['aef'], aep=canshu['aep'], anf=canshu['anf'],
                                                        anp=canshu['anp'])
            SBFL_m_result[dataname] = this_method_list
    return SBFL_m_result


def MBFL_s(subject_name):
    with open(f'../Four_canshu/MBFL/{subject_name}_statement.json', 'r') as rf:
        datas = json.load(rf)
        MBFL_s_result = {}
        for dataname, datamsg in datas.items():
            # print(dataname, datamsg)
            this_statemrnt_list = {}
            for statemrnt_no, mutate_canshu_list in datamsg.items():
                this_statemrnt_list[statemrnt_no] = []
                for mutate_canshu in mutate_canshu_list:
                    this_calculate_result = Calculate(aef=mutate_canshu['akf'], anf=mutate_canshu['anf'],
                                                      anp=mutate_canshu['anp'], aep=mutate_canshu['akp'])
                    this_statemrnt_list[statemrnt_no].append(this_calculate_result)
            MBFL_s_result[dataname] = this_statemrnt_list

    return MBFL_s_result


def SBFL_s(subject_name):
    with open(f'../Four_canshu/SBFL/{subject_name}_statement.json', 'r') as rf:
        datas = json.load(rf)
        SBFL_s_result = {}
        for dataname, datamsg in datas.items():
            # print(dataname, datamsg)
            this_statement_list = {}
            for statement_no, canshu in datamsg.items():
                this_statement_list[statement_no] = Calculate(aef=canshu['aef'], aep=canshu['aep'], anf=canshu['anf'],
                                                              anp=canshu['anp'])
            SBFL_s_result[dataname] = this_statement_list
    return SBFL_s_result


if __name__ == "__main__":

    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        MBFL_m_DIC = MBFL_m(subject_name)
        SBFL_m_DIC = SBFL_m(subject_name)
        MBFL_s_DIC = MBFL_s(subject_name)
        SBFL_s_DIC = SBFL_s(subject_name)
        # print(MBFL_m_DIC)
        # print(SBFL_m_DIC)
        # print(MBFL_s_DIC)
        # print(SBFL_s_DIC)

        Path = f"../Result/Suspicious/{subject_name}"
        ensure_directory_exists(Path)

        Save_json(MBFL_m_DIC, Path + '/MBFL_m.json')
        Save_json(MBFL_s_DIC, Path + '/MBFL_s.json')
        Save_json(SBFL_m_DIC, Path + '/SBFL_m.json')
        Save_json(SBFL_s_DIC, Path + '/SBFL_s.json')


        # with open(f'../Four_canshu/', 'r') as rf:
        #     datas = json.load(rf)
        #     print("GET JSON FILE FINISHED!", end='\n\n')

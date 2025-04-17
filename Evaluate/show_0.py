import pandas as pd
import json


def show(datas):
    # with open(f'../Result/Evaluation/save_.json', 'r') as rf:
    #     datas = json.load(rf)
    rows = []
    # for subject_name, s_datas in datas.items():

    for type_name, t_datas in datas.items():

        for gbsr_name, g_datas in t_datas.items():

            for formula_name, f_datas in g_datas.items():
                # for eval_name, e_datas in f_datas.items():
                rows.append({
                    # "Subject": subject_name,
                    "Type": type_name,
                    "GBSR": gbsr_name,
                    "Formula": formula_name,
                    "Top-1": f_datas["top1"],
                    "Top-3": f_datas["top3"],
                    "Top-5": f_datas["top5"],
                    "Top-10": f_datas["top10"],
                    "MAR": f_datas["mar"],
                    "MFR": f_datas["mfr"],
                    "EXAM": f_datas["exam"]
                })

    df = pd.DataFrame(rows)

    # 保存为 Excel 文件
    output_path = "../Result/Reduced_Evaluation/output2.xlsx"
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"JSON 数据已整理并导出为 Excel 文件：{output_path}")

def show0():
    with open(f'../Result/Reduced_Evaluation/save_0.json', 'r') as rf:
        datas = json.load(rf)
    rows = []
    for subject_name, s_datas in datas.items():
        print(subject_name, s_datas)
        for type_name, t_datas in s_datas.items():
            print(type_name, t_datas)
            for gbsr_name, g_datas in t_datas.items():
                print(gbsr_name, g_datas)
                for formula_name, f_datas in g_datas.items():
                    print(formula_name, f_datas)
                    # for eval_name, e_datas in f_datas.items():
                    rows.append({
                        "Subject": subject_name,
                        "Type": type_name,
                        "GBSR": gbsr_name,
                        "Formula": formula_name,
                        "Top-1": f_datas["top1"],
                        "Top-3": f_datas["top3"],
                        "Top-5": f_datas["top5"],
                        "Top-10": f_datas["top10"],
                        "MAR": f_datas["mar"],
                        "MFR": f_datas["mfr"],
                        "EXAM": f_datas["exam"]
                    })

    df = pd.DataFrame(rows)

    # 保存为 Excel 文件
    output_path = "../Result/Reduced_Evaluation/output1.xlsx"
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"JSON 数据已整理并导出为 Excel 文件：{output_path}")

def sum_intergrate():
    # SBFL_LIST = ["SBFL", "GBSR_FOR_SBFL_0_0", "GBSR_FOR_SBFL_1_0", "GBSR_FOR_SBFL_2_0", "GBSR_FOR_SBFL_3_0", "GBSR_FOR_SBFL_4_0",
    #              "GBSR_FOR_SBFL_5_0", "GBSR_FOR_SBFL_6_0", "GBSR_FOR_SBFL_7_0", "GBSR_FOR_SBFL_8_0"]
    MBFL_LIST = ["MBFL", "GBSR_FOR_MBFL_0_0", "GBSR_FOR_MBFL_1_0", "GBSR_FOR_MBFL_2_0", "GBSR_FOR_MBFL_3_0", "GBSR_FOR_MBFL_4_0",
                 "GBSR_FOR_MBFL_5_0", "GBSR_FOR_MBFL_6_0", "GBSR_FOR_MBFL_7_0", "GBSR_FOR_MBFL_8_0"]
    type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']

    with open(f'../Result/Reduced_Evaluation/save_0.json', 'r') as rf:
        datas = json.load(rf)
    print(datas)
    type_json = {}
    type_json["SBFL"] = {}
    type_json["MBFL"] = {}

    print(type_json)
    # for sbfl_ in SBFL_LIST:
    #     type_json['SBFL'][sbfl_] = {}
    #     for formula_ in formula_list:
    #         type_json['SBFL'][sbfl_][formula_] = {}
    #         type_json['SBFL'][sbfl_][formula_]['top1'] = 0
    #         type_json['SBFL'][sbfl_][formula_]['top3'] = 0
    #         type_json['SBFL'][sbfl_][formula_]['top5'] = 0
    #         type_json['SBFL'][sbfl_][formula_]['top10'] = 0
    #         type_json['SBFL'][sbfl_][formula_]['mar'] = 0
    #         type_json['SBFL'][sbfl_][formula_]['mfr'] = 0
    #         type_json['SBFL'][sbfl_][formula_]['exam'] = 0
    for mbfl_ in MBFL_LIST:
        type_json['MBFL'][mbfl_] = {}
        for formula_ in formula_list:
            type_json['MBFL'][mbfl_][formula_] = {}
            type_json['MBFL'][mbfl_][formula_]['top1'] = 0
            type_json['MBFL'][mbfl_][formula_]['top3'] = 0
            type_json['MBFL'][mbfl_][formula_]['top5'] = 0
            type_json['MBFL'][mbfl_][formula_]['top10'] = 0
            type_json['MBFL'][mbfl_][formula_]['mar'] = 0
            type_json['MBFL'][mbfl_][formula_]['mfr'] = 0
            type_json['MBFL'][mbfl_][formula_]['exam'] = 0

    # for sbfl_ in SBFL_LIST:
    #     for formula_ in formula_list:
    #         for subject_ in Subject_name:
    #             type_json['SBFL'][sbfl_][formula_]['top1'] += datas[subject_]['SBFL'][sbfl_][formula_]['top1']
    #             type_json['SBFL'][sbfl_][formula_]['top3'] += datas[subject_]['SBFL'][sbfl_][formula_]['top3']
    #             type_json['SBFL'][sbfl_][formula_]['top5'] += datas[subject_]['SBFL'][sbfl_][formula_]['top5']
    #             type_json['SBFL'][sbfl_][formula_]['top10'] += datas[subject_]['SBFL'][sbfl_][formula_]['top10']
    #             type_json['SBFL'][sbfl_][formula_]['mar'] += datas[subject_]['SBFL'][sbfl_][formula_]['mar']
    #             type_json['SBFL'][sbfl_][formula_]['mfr'] += datas[subject_]['SBFL'][sbfl_][formula_]['mfr']
    #             type_json['SBFL'][sbfl_][formula_]['exam'] += datas[subject_]['SBFL'][sbfl_][formula_]['exam']
    #         type_json['SBFL'][sbfl_][formula_]['mar'] = type_json['SBFL'][sbfl_][formula_]['mar'] / 5
    #         type_json['SBFL'][sbfl_][formula_]['mfr'] = type_json['SBFL'][sbfl_][formula_]['mfr'] / 5
    #         type_json['SBFL'][sbfl_][formula_]['exam'] = type_json['SBFL'][sbfl_][formula_]['exam'] / 5
    for mbfl_ in MBFL_LIST:
        for formula_ in formula_list:
            for subject_ in Subject_name:
                type_json['MBFL'][mbfl_][formula_]['top1'] += datas[subject_]['MBFL'][mbfl_][formula_]['top1']
                type_json['MBFL'][mbfl_][formula_]['top3'] += datas[subject_]['MBFL'][mbfl_][formula_]['top3']
                type_json['MBFL'][mbfl_][formula_]['top5'] += datas[subject_]['MBFL'][mbfl_][formula_]['top5']
                type_json['MBFL'][mbfl_][formula_]['top10'] += datas[subject_]['MBFL'][mbfl_][formula_]['top10']
                type_json['MBFL'][mbfl_][formula_]['mar'] += datas[subject_]['MBFL'][mbfl_][formula_]['mar']
                type_json['MBFL'][mbfl_][formula_]['mfr'] += datas[subject_]['MBFL'][mbfl_][formula_]['mfr']
                type_json['MBFL'][mbfl_][formula_]['exam'] += datas[subject_]['MBFL'][mbfl_][formula_]['exam']
            type_json['MBFL'][mbfl_][formula_]['mar'] = type_json['MBFL'][mbfl_][formula_]['mar'] / 5
            type_json['MBFL'][mbfl_][formula_]['mfr'] = type_json['MBFL'][mbfl_][formula_]['mfr'] / 5
            type_json['MBFL'][mbfl_][formula_]['exam'] = type_json['MBFL'][mbfl_][formula_]['exam'] / 5
    show(type_json)
    show0()


if __name__ == "__main__":
    sum_intergrate()
    # for subject_name, s_datas in datas.items():
    #     t_json = {}
    #     for type_name, t_datas in s_datas.items():
    #         g_json = {}
    #         for gbsr_name, g_datas in t_datas.items():
    #             f_json = {}
    #             for formula_name, f_datas in g_datas.items():
    #                 e_json = {}
    #                 for eval_name, e_datas in f_datas.items():
    #                     e_json["top1"] += e_datas[formula_name]["top1"]
    #                     e_json["top3"] += e_datas[formula_name]["top3"]
    #                     e_json["top5"] += e_datas[formula_name]["top5"]
    #                     e_json["top10"] += e_datas[formula_name]["top10"]
    #                     e_json["mar"] += e_datas[formula_name]["mar"]
    #                     e_json["mfr"] += e_datas[formula_name]["mfr"]
    #                     e_json["exam"] += e_datas[formula_name]["exam"]

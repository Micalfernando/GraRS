import json
import os
import pickle

import numpy as np

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

import json
import numpy as np
import pickle

np.set_printoptions(suppress=True)


def get_matrix(len1, len2, edges):
    matrix = np.zeros((len1, len2))
    for edge in edges:
        dot1 = int(edge[0])
        dot2 = int(edge[1])
        # print(dot1, dot2)
        matrix[dot1][dot2] = 1
    each_j = []
    for j in range(len1):
        sum = 0
        for i in range(len2):
            sum += matrix[j][i]
        each_j.append(sum)
    for j in range(len1):
        for i in range(len2):
            if each_j[j] != 0:
                matrix[j][i] = matrix[j][i] / each_j[j]
    return matrix



def integration(M1, M2, M3, M4, M4_1, M5, M5_1, L1, L2, L3, L4, L5):
    # M1 ~ M5 : method-method ; method - lines ; mutation - lines ; lines - r/f tests ; mutation - r/f tests ;
    # L1 ~ L5 : method ; lines ; mutations ; r tests; f tests

    len_total = L1 + L2 + L3
    P_len = len_total + L4
    F_len = len_total + L5

    matrix_P = np.zeros((P_len, P_len))
    matrix_F = np.zeros((F_len, F_len))

    # 方法-方法之间调用关系&被调用关系 获取
    for i in range(L1):
        for j in range(L1):
            node1 = i
            node2 = j
            matrix_P[node1][node2] = M1[i][j]

            matrix_F[node1][node2] = M1[i][j]

    # 方法-语句之间的结构关系
    for i in range(L1):
        for j in range(L2):
            node1 = i
            node2 = j + L1
            matrix_P[node1][node2] = M2[i][j]
            matrix_P[node2][node1] = M2[i][j]

            matrix_F[node1][node2] = M2[i][j]
            matrix_F[node2][node1] = M2[i][j]

    # 语句-变异体之间的生成关系（注意顺序）
    for i in range(L3):
        for j in range(L2):
            node1 = i + L1 + L2  # 变异体
            node2 = j + L1  # 语句
            matrix_P[node1][node2] = M3[i][j]
            matrix_P[node2][node1] = M3[i][j]

            matrix_F[node1][node2] = M3[i][j]
            matrix_F[node2][node1] = M3[i][j]

    # 语句-正确测试之间的覆盖关系
    for i in range(L2):
        for j in range(L4):
            node1 = i + L1
            node2 = j + L1 + L2 + L3

            matrix_P[node1][node2] = M4[i][j]
            matrix_P[node2][node1] = M4[i][j]

    # 变异体-正确测试之间的杀死关系
    for i in range(L3):
        for j in range(L4):
            node1 = i + L1 + L2
            node2 = j + L1 + L2 + L3

            matrix_P[node1][node2] = M5[i][j]
            matrix_P[node2][node1] = M5[i][j]

    # 语句-失败测试之间的覆盖关系
    for i in range(L2):
        for j in range(L5):
            node1 = i + L1
            node2 = j + L1 + L2 + L3

            matrix_F[node1][node2] = M4_1[i][j]
            matrix_F[node2][node1] = M4_1[i][j]

    # 变异体-失败测试之间的杀死关系
    for i in range(L3):
        for j in range(L5):
            node1 = i + L1 + L2
            node2 = j + L1 + L2 + L3

            matrix_F[node1][node2] = M5_1[i][j]
            matrix_F[node2][node1] = M5_1[i][j]

    return matrix_P, matrix_F


def m2m_matrix(length, data):
    matrix = np.zeros((length, length))
    for d in data:
        ll = len(d[1])
        if ll != 0:
            for j in d[1]:
                matrix[d[0]][j] = 1.0 / ll
                matrix[j][d[0]] = 1.0 / ll
    return matrix


if __name__ == '__main__':
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Data/{subject_name}.json', 'r') as rf:
            datas = json.load(rf)
            print("GET JSON FILE FINISHED!", end='\n\n')

        m2m_data = {}
        with open(f'../Data/{subject_name}_M2M.txt', 'r') as M_f:
            mf = M_f.readlines()
        for m2m in mf:
            name = m2m.split(' * ')[0]
            M2M = m2m.split(' * ')[1]
            M2M = eval(M2M)
            m2m_data[name] = M2M

        # print(m2m_data)
        # break
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

            method2method = {}
            method2lines = data['edge2']
            mutation2lines = data['edge12']
            lines2rtest = data['edge10']
            lines2ftest = data['edge']
            mutation2rtest = data['edge13']
            mutation2ftest = data['edge14']
            print("GET EDGES FINISHED!", end='\n\n')

            matrix = np.zeros((len_total, len_total))
            # print(len_total)
            # print(matrix.shape)

            try:
                this_m2m_data = m2m_data[data_name]
            except:
                print('err----')
                continue

            # methed-method 矩阵 建立
            method2method_matrix = m2m_matrix(len_method, this_m2m_data)
            # method-lines 矩阵 建立
            method2lines_matrix = get_matrix(len_method, len_lines, method2lines)
            # mutation-lines 矩阵 建立
            mutation2lines_matrix = get_matrix(len_mutation, len_lines, mutation2lines)
            # lines-rtest 矩阵 建立
            lines2rtest_matrix = get_matrix(len_lines, len_rtest, lines2rtest)
            # line-ftest 矩阵 建立
            lines2ftest_matrix = get_matrix(len_lines, len_ftest, lines2ftest)
            # mutation-rtest 矩阵 建立
            mutation2rtest_matrix = get_matrix(len_mutation, len_rtest, mutation2rtest)
            # mutation-ftest 矩阵 建立
            mutation2ftest_matrix = get_matrix(len_mutation, len_ftest, mutation2ftest)

            print('------正在获取通过测试/失败测试对应的图矩阵--------')
            P_matrix, F_matrix = integration(method2method_matrix, method2lines_matrix, mutation2lines_matrix,
                                             lines2rtest_matrix, lines2ftest_matrix, mutation2rtest_matrix,
                                             mutation2ftest_matrix, len_method, len_lines, len_mutation, len_rtest,
                                             len_ftest)
            print(f'------获取{data_name}图矩阵成功！--------')


            P_file_path = f'''../Matrix/{subject_name}/P_{data_name}_matrix.pkl'''
            F_file_path = f'''../Matrix/{subject_name}/F_{data_name}_matrix.pkl'''
            ensure_directory_exists(P_file_path)
            ensure_directory_exists(F_file_path)

            with open(P_file_path, 'wb') as wf:
                pickle.dump(P_matrix, wf)
            with open(F_file_path, 'wb') as wf:
                pickle.dump(F_matrix, wf)



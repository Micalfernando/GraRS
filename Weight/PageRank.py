import numpy as np
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


def pagerank_from_adjacency_matrix(adj_matrix, alpha=0.85, tol=1e-6, max_iter=100):
    """
    计算邻接矩阵形式图中每个节点的 PageRank 值。

    参数:
        adj_matrix (numpy.ndarray): 图的邻接矩阵，形状为 (n, n)。
        alpha (float): 阻尼因子，通常设置为 0.85。
        tol (float): 收敛的阈值，PageRank 值的变化小于该值时停止迭代。
        max_iter (int): 最大迭代次数。

    返回:
        numpy.ndarray: 每个节点的 PageRank 值。
    """
    n = adj_matrix.shape[0]

    # 处理出度为 0 的节点（dangling nodes）
    out_degree = adj_matrix.sum(axis=1)
    dangling_nodes = (out_degree == 0)

    # 构造转移概率矩阵
    transition_matrix = adj_matrix / np.maximum(out_degree[:, np.newaxis], 1)
    transition_matrix[dangling_nodes, :] = 1.0 / n  # 为悬挂节点分配均匀概率

    # 初始化 PageRank 值
    rank = np.ones(n) / n

    # Power iteration
    for i in range(max_iter):
        new_rank = alpha * transition_matrix.T @ rank + (1 - alpha) / n
        if np.linalg.norm(new_rank - rank, 1) < tol:
            break
        rank = new_rank

    return list(rank)


def load_pkl_to_matrix(file_path):
    """
    读取 pkl 文件并转换为矩阵。

    参数:
        file_path (str): pkl 文件路径。

    返回:
        numpy.ndarray: 转换后的矩阵。
    """
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    # 确保数据可以转换为矩阵
    try:
        matrix = np.array(data)
    except ValueError as e:
        raise ValueError("文件内容无法转换为矩阵: {}".format(e))

    return matrix


def count_statement_coverage_list(edges, num_statements, start_index=0):
    """
    统计每个语句被失败测试用例覆盖的次数，使用列表存储结果。

    参数:
        edges (list of lists): 每个子列表包含两个整数 [statement_num, failing_test_case_num]
        num_statements (int): 语句的总数量
        start_index (int): 语句编号的起始索引（默认0）

    返回:
        list: 一个列表，索引对应语句编号，值为覆盖次数
    """
    coverage_counts = [0] * num_statements

    for edge in edges:
        if len(edge) != 2:
            print(f"警告: 无效的边 {edge}，应包含两个元素。")
            continue
        statement_num, failing_test_case_num = edge
        if start_index <= statement_num < start_index + num_statements:
            coverage_counts[statement_num - start_index] += 1
        else:
            print(f"警告: 语句编号 {statement_num} 超出范围（{start_index} 到 {start_index + num_statements - 1}）。")

    return coverage_counts


if __name__ == "__main__":
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        with open(f'../Data/{subject_name}.json', 'r') as rf:
            datas = json.load(rf)
        print(f"GET {subject_name} JSON FILE FINISHED!", end='\n\n')
        msg_dic = {}
        for data in datas:
            this_version_msg_dic = {}
            version_name = data['proj']
            number_method = len(data['methods'])
            fault_list = data['ans']
            number_statement = len(data['lines'])
            number_mutation = len(data['mutation'])
            number_rtest = len(data['rtest'])
            number_ftest = len(data['ftest'])
            print(f"READY TO DEAL {version_name} DATA", end='\n\n')

            F_matrix_path = f'../Matrix/{subject_name}/F_{version_name}_matrix.pkl'
            P_matrix_path = f'../Matrix/{subject_name}/P_{version_name}_matrix.pkl'

            F_matrix = load_pkl_to_matrix(F_matrix_path)
            P_matrix = load_pkl_to_matrix(P_matrix_path)
            print(f"COMPUTE PAGERANK VALUE OF P-MATRIX", end='\n\n')


            P_pagerank_value = pagerank_from_adjacency_matrix(P_matrix)

            print(f"COMPUTE PAGERANK VALUE OF F-MATRIX", end='\n\n')

            F_pagerank_value = pagerank_from_adjacency_matrix(F_matrix)

            print(f"{version_name} FINISHED!", end='\n\n')

            this_version_msg_dic["number_method"] = number_method
            this_version_msg_dic["number_statement"] = number_statement
            this_version_msg_dic["number_mutation"] = number_mutation
            this_version_msg_dic["number_ftest"] = number_ftest
            this_version_msg_dic["number_rtest"] = number_rtest
            this_version_msg_dic["fault_list"] = fault_list

            this_version_msg_dic["P_value"] = P_pagerank_value
            this_version_msg_dic["F_value"] = F_pagerank_value

            msg_dic[version_name] = this_version_msg_dic
            # print(msg_dic)
            # break
        save_path = f"../Result/Weight/{subject_name}.json"
        ensure_directory_exists(save_path)
        Save_json(msg_dic, save_path)
        # print(P_pagerank_value)
        # print(version_name, len(F_matrix), number_ftest + number_method + number_mutation + number_statement)
        # with open(f'../Matrix/{subject_name}/SBFL_m.json', 'r') as rf:
        #     suspicious_datas = json.load(rf)

# # 示例：输入邻接矩阵
# adj_matrix = np.array([
#     [0, 1, 0.5, 0],
#     [0, 0, 0, 1],
#     [1, 0, 0, 1],
#     [0, 0, 0.5, 0]
# ])
#
# # 计算 PageRank
# pagerank_values = pagerank_from_adjacency_matrix(adj_matrix)
# print("PageRank 值:", pagerank_values)

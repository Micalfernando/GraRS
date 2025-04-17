import json
import pickle
import numpy as np


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
    mfr = 999
    for fault in fault_list:
        this_fault_rank = 1
        this_fault_sus = sus_dic[str(fault)]
        for m_id, suspicious in sus_dic.items():
            if suspicious >= this_fault_sus:
                this_fault_rank += 1
        if this_fault_rank <= mfr:
            mfr = this_fault_rank
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


def top_n(errlist, methods, n):
    top = 0
    lists = (sorted(methods.items(), key=lambda kv: (kv[1], kv[0])))
    # print(lists)
    # print(lists[-n:])
    for i in lists[-n:]:
        if i[0] in errlist:
            top += 1
    return top


def get_num(rank, err):
    if rank in err:
        return 1
    else:
        return 0


def Sum(lists):
    sum = 0
    for i in lists:
        sum += float(i)
    return sum


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


if __name__ == '__main__':

    # Math0 = ['1', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #          '21', '22', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
    #          '40', '41', '42', '43', '44', '45', '46', '51', '52', '53', '54', '55', '57', '58', '59', '60', '61', '62',
    #          '63', '64', '65']
    # Math = ['1', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #         '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38',
    #         '39', '40', '41', '42', '43', '44', '45', '46', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
    #         '61', '62', '63']
    # formula_list = ['Tarantula', 'Jaccard', 'Dstar', 'Wong1', 'Hamming', 'Hamann', 'Op2', 'Ochiai', 'GP13', 'Dice']
    Subject_name = ['Lang', 'Chart', 'Cli', 'JxPath', 'Math']
    # Subject_name = ['Lang']
    for subject_name in Subject_name:
        print(subject_name)
        Pr_Grace = {}
        this_subject_top1 = 0
        this_subject_top3 = 0
        this_subject_top5 = 0
        this_subject_top10 = 0
        this_subject_mar = 0
        this_subject_mfr = 0
        this_subject_exam = 0

        this_improved_subject_top1 = 0
        this_improved_subject_top3 = 0
        this_improved_subject_top5 = 0
        this_improved_subject_top10 = 0
        this_improved_subject_mar = 0
        this_improved_subject_mfr = 0
        this_improved_subject_exam = 0

        with open(f"../Result/Weight/{subject_name}.json") as weight_f:
            weight_json = json.load(weight_f)
        this_count = 0

        for k, v in weight_json.items():
            # print(k)
            this_fault_list = v["fault_list"]
            this_p_value = v["P_value"]
            this_f_value = v["F_value"]
            number_method = v["number_method"]
            # print(this_fault_list)
            # with open('../Grace_data/Math0/Math.pkl', 'rb') as G_rf:
            try:
                with open(f'../Grace/{subject_name}/{k}_epoch_method.json', 'r') as js_f:
                    epoch = json.load(js_f)[9]
                    this_count += 1
                    # print(epoch)
                    this_version_top1, this_version_top3, this_version_top5, this_version_top10 = get_top_n_rank(epoch,
                                                                                                                 this_fault_list)
                    this_version_mfr = get_mfr(epoch, this_fault_list)
                    this_version_mar = get_mar(epoch, this_fault_list)
                    this_version_exam = get_exam(epoch, this_fault_list, number_method)
                    # print(this_version_top1, this_version_top3, this_version_top5, this_version_top10)

                    this_subject_top1 += this_version_top1
                    this_subject_top3 += this_version_top3
                    this_subject_top5 += this_version_top5
                    this_subject_top10 += this_version_top10
                    this_subject_mar += this_version_mar
                    this_subject_mfr += this_version_mfr
                    this_subject_exam += this_version_exam

                    improve_dic = {}

                    for method_id, Grace_sus in epoch.items():
                        w = this_f_value[int(method_id)] - 0.5 * this_p_value[int(method_id)]
                        s = Grace_sus
                        improve_dic[method_id] = (1 + w) * s

                    # print(improve_dic)
                    this_improved_version_top1, this_improved_version_top3, this_improved_version_top5, this_improved_version_top10 = get_top_n_rank(
                        improve_dic,
                        this_fault_list)
                    this_improved_version_mfr = get_mfr(improve_dic, this_fault_list)
                    this_improved_version_mar = get_mar(improve_dic, this_fault_list)
                    this_improved_version_exam = get_exam(improve_dic, this_fault_list, number_method)
                    # print(this_improved_version_top1, this_improved_version_top3, this_improved_version_top5,
                    #       this_improved_version_top10)

                    this_improved_subject_top1 += this_improved_version_top1
                    this_improved_subject_top3 += this_improved_version_top3
                    this_improved_subject_top5 += this_improved_version_top5
                    this_improved_subject_top10 += this_improved_version_top10
                    this_improved_subject_mar += this_improved_version_mar
                    this_improved_subject_mfr += this_improved_version_mfr
                    this_improved_subject_exam += this_improved_version_exam
            except:
                continue
        print(this_count)
        this_subject_mar /= this_count
        this_subject_mfr /= this_count
        this_subject_exam /= this_count
        this_improved_subject_mar /= this_count
        this_improved_subject_mfr /= this_count
        this_improved_subject_exam /= this_count

        # print(this_subject_top1, this_subject_top3, this_subject_top5, this_subject_top10, this_subject_mar/len(weight_json),
        #       this_subject_mfr/len(weight_json), this_subject_exam/len(weight_json))
        # print(this_improved_subject_top1, this_improved_subject_top3, this_improved_subject_top5,
        #       this_improved_subject_top10, this_improved_subject_mar/len(weight_json), this_improved_subject_mar/len(weight_json),
        #       this_improved_subject_exam/len(weight_json))
        print(this_subject_top1, this_subject_top3, this_subject_top5, this_subject_top10,
              this_subject_mar,
              this_subject_mfr, this_subject_exam)
        print(this_improved_subject_top1, this_improved_subject_top3, this_improved_subject_top5,
              this_improved_subject_top10, this_improved_subject_mar,
              this_improved_subject_mfr,
              this_improved_subject_exam)
        # with open(f'../Grace/{subject_name}/{dataname}_epoch_method.json', 'r') as rf:
        #     datas = json.load(rf)
        #     # print("GET JSON FILE FINISHED!", end='\n\n')
        # with open('../data/Math.pkl', 'rb') as G_rf:
        #
        #     G_datas = pickle.load(G_rf)
        #     # print
        # Grace_data = {}
        # na = []
        # na2 = []
        # for D in G_datas:
        #     Grace_data[D['proj']] = [D['ans'], D['methods']]
        #     na.append(str(D['proj']).replace('Math', ''))
        # print(na)
        # Tra_data = {}
        # for D in datas:
        #     Tra_data[D['proj']] = [D['ans'], D['methods']]
        #     na2.append(str(D['proj']).replace('Math', ''))
        # print(na2)
        # G = {}
        # T = {}
        #
        # for k, v in Grace_data.items():
        #     G = {}
        #     T = {}
        #     dataname = k
        #     print(k)
        #     ans = v[0]
        #     # Mathno = str(dataname).replace('Math','')
        #     # p = Math.index(Mathno)
        #     # dn = "Math"+Math0[p]
        #     # print(dn)
        #     try:
        #         with open(f'Grace/Math/{dataname}_epoch_method.json', 'r') as js_f:
        #             epoch = json.load(js_f)[9]
        #     except:
        #         continue
        #     # print(epoch)
        #     # print(Tra_data[dataname])
        #     Grace_methods = dict(v[1])
        #     # print(dataname,Grace_methods)
        #     M_Pr = {}
        #     try:
        #         for method, no in Tra_data[dataname][1].items():
        #             T_method = method.split('@')[0].replace('.java', '')
        #             M = method.split('@')[1].split('.')[0]
        #             # print(T_method, M, no, '       ', method)
        #             T[T_method + M] = [no]
        #         Pr_canshu = []
        #         with open(f'../else/FIN_PR/Math/{dataname}_PR_a={a}_d={b}.txt') as pr_f:
        #             msg = pr_f.readlines()
        #             method_num = eval(msg[0].split(' ')[0])
        #             method_pr = msg[1].split(' ')[0:method_num]
        #             for i in range(0, int(method_num)):
        #                 Pr_canshu.append(1 + eval(method_pr[i]) / Sum(method_pr))
        #         # print(method_num, method_pr)
        #         # print(Pr_canshu)
        #         #
        #         # for G_num, G_sus in dict(epoch).items():
        #         #     print(G_num, G_sus)
        #
        #     except:
        #         print(f" ", end=' ')
        #
        #     for method, no in Grace_methods.items():
        #         G_method = method.split('@')[0].replace('.java', '')
        #         M = method.split('@')[1].split('.')[0]
        #         # print(G_method, M, no, '       ', method)
        #         G[G_method + M] = [no]
        #     PG_sus = {}
        #     for k, v in G.items():
        #         print(v, k)
        #
        #         G_metname = get_keys(G, v)
        #         # print(G_metname[0])
        #         # print(T[G_metname[0]])
        #         pr = 1
        #         try:
        #             num = int(T[G_metname[0]][0])
        #             pr = Pr_canshu[num]
        #         except:
        #             pr = 1
        #         # print(dataname,epoch,G)
        #         sus = epoch[str(v[0])] * pr
        #         # print(epoch[str(v[0])], sus)
        #         PG_sus[v[0]] = sus
        #     Pr_Grace[dataname] = [ans, PG_sus]
        #
        # for dataName, dataMsg in Pr_Grace.items():
        #     an = dataMsg[0]
        #     sus_list = dataMsg[1]
        #     max_Sus = 0
        #     max_p = -1
        #     for i, s in sus_list.items():
        #         if s > max_Sus:
        #             max_Sus = s
        #             max_p = i
        #         else:
        #             continue
        #     # if get_num(max_p,a) == 0:
        #     # print(dataName, a, max_p, sus_list)
        #
        #     top1 += top_n(an, sus_list, 1)
        #     top3 += top_n(an, sus_list, 3)
        #     top5 += top_n(an, sus_list, 5)
        # # if top1 - 40 + top3 - 57 + top5 - 59 > 0:
        # print('\n', top1, top3, top5, a, b)

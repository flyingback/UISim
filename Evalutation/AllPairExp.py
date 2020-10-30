__author__ = 'Mao'
import csv
import math
import sys
import scipy.stats as sp
# topk_list = [100, 50, 25]
topK = 3000

# Precision:
# foreach p in topKEstNP{
#     if p in topKTrueNP
#         count ++
# }
# Return count/k;

def Precision(topKEstNP, topKTrueNP, exact_ranking):
    count = 0.0
    for larger_n in topKEstNP:
        for smaller_n in topKEstNP[larger_n]:
            if larger_n in topKTrueNP:
                if smaller_n in topKTrueNP[larger_n]:
                    count += 1.0
    return count/len(exact_ranking)


# L1-diff:
# foreach nodePair  p in topKTrueNP{
#     if p in topKEstNP
#         L1_incre = |p.estScore - p.extScore|
#     else
#         L1_incre = p.extScore
#
#     L1+= L1_incre
# }
#
# Return L1;

def L1(topKEstNP, topKTrueNP):
    L1 = 0.0
    for larger_n in topKTrueNP:
        for smaller_n in topKTrueNP[larger_n]:
            L1_incre = topKTrueNP[larger_n][smaller_n] # L1_incre = p.extScore
            if larger_n in topKEstNP:
                if smaller_n in topKEstNP[larger_n]: # p in topKEstNP
                    L1_incre = abs(topKEstNP[larger_n][smaller_n] - topKTrueNP[larger_n][smaller_n])
            L1 += L1_incre
    return L1

# RAG:
# foreach nodePair p in topKEstNP{
#     if p in topKTrueNP
#         est_incre = p.extScore
#     else
#         est_incre = 0
#     sum_est += est_incre
# }
#
# sum_ext = summation of topk scores in ext_list
#
# Return sum_est/sum_ext;

def RAG(topKEstNP, topKTrueNP):
    sum_ext = 0.0
    sum_est = 0.0
    for larger_n in topKEstNP:
        for smaller_n in topKEstNP[larger_n]:
            est_incre = 0
            if larger_n in topKTrueNP:
                if smaller_n in topKTrueNP[larger_n]:
                    est_incre = topKTrueNP[larger_n][smaller_n]
            sum_est += est_incre
    for larger_n in topKTrueNP:
        for smaller_n in topKTrueNP[larger_n]:
            sum_ext += topKTrueNP[larger_n][smaller_n]
    return sum_est/sum_ext

# Kendall's tau
# allNodes <-- union of all the distinct nodes in topKTrueNP and topKEstNP
#
# for (i=0; i<k; i++)
#     for (j=i+1; j<k; j++){
#         np1 = allNodes[i]
#         np2 = allNodes[j]
#
#         if np1 in topKTrueNP
#             extp1 = np1.extScore
#         else
#             extp1 = 0
#
#         if np2 in topKTrueNP
#             extp2 = np2.extScore
#         else
#             extp2 = 0
#
#         if np1 in topKEstNP
#             estp1 = np1.estScore
#         else
#             estp1 = 0
#
#         if np2 in topKEstNP
#             estp2 = np2.estScore
#         else
#             estp2 = 0
#
#
#         if (extp1 == extp2) e++;
#         if (estp1 == estp2) a++;
#         if (extp1-extp2)*(estp1-estp2) > 0  c++;
#         elseif (extp1-extp2)*(estp1-estp2) < 0  d++;
#
#     }
#
# m = allNodes.size() * (allNodes.size() - 1) / 2.0;
# Return (c-d)/Math.sqrt((m - e) * (m - a));

def Tau(topKEstNP, topKTrueNP, est_ranking, exact_ranking):
    dict_all = dict()
    allNodes = []
    a = 0.0
    c = 0.0
    d = 0.0
    e = 0.0
    for np in est_ranking:
        if np[0] not in dict_all:
            dict_all[np[0]] = dict()
            dict_all[np[0]][np[1]] = True
            allNodes.append(np)
        elif np[1] not in dict_all[np[0]]:
            dict_all[np[0]][np[1]] = True
            allNodes.append(np)
    for np in exact_ranking:
        if np[0] not in dict_all:
            dict_all[np[0]] = dict()
            dict_all[np[0]][np[1]] = True
            allNodes.append(np)
        elif np[1] not in dict_all[np[0]]:
            dict_all[np[0]][np[1]] = True
            allNodes.append(np)
    k = len(allNodes)
    for i in range(0, k):
        for j in range(i+1, k):
            np1 = allNodes[i]
            np2 = allNodes[j]

            extp1 = 0
            if np1[0] in topKTrueNP:
                if np1[1] in topKTrueNP[np1[0]]:
                    extp1 = topKTrueNP[np1[0]][np1[1]]

            extp2 = 0
            if np2[0] in topKTrueNP:
                if np2[1] in topKTrueNP[np2[0]]:
                    extp2 = topKTrueNP[np2[0]][np2[1]]

            estp1 = 0
            if np1[0] in topKEstNP:
                if np1[1] in topKEstNP[np1[0]]:
                    estp1 = topKEstNP[np1[0]][np1[1]]

            estp2 = 0
            if np2[0] in topKEstNP:
                if np2[1] in topKEstNP[np2[0]]:
                    estp2 = topKEstNP[np2[0]][np2[1]]



            if extp1 == extp2:
                e += 1
            if estp1 == estp2:
                a += 1
            if (extp1-extp2)*(estp1-estp2) > 0:
                c += 1
            elif (extp1-extp2)*(estp1-estp2) < 0:
                d += 1
    # m = len(allNodes) * (len(allNodes) - 1) / 2.0
    # return (c-d)/math.sqrt((m - e) * (m - a))
    return (c-d)/math.sqrt((c + d + e) * (c + d + a))

def Calculate_exact(filename):
    all_exact_scores = dict()
    est_scores = dict()
    exact_ranking = []
    est_ranking = []


    est_count_line = 0
    with open(filename, 'r') as csvfile:
        fastsim = csv.reader(csvfile, delimiter='\t')
        score = dict()
        sum_time = 0
        # exact_query = open("exact_query"+query_count, 'w')
        for row in fastsim:
            est_count_line += 1
            if (est_count_line > topK):
                 break
            if "ms" in row[0]:
                sum_time = int(float(row[0].split("ms")[0]))
                continue
            n1 = int(row[0])
            n2 = int(row[1])
            val = float(row[2])
            larger_n = -1
            smaller_n = -1
            if n1 > n2:
                larger_n = n1
                smaller_n = n2
            else:
                larger_n = n2
                smaller_n = n1
            est_ranking.append([larger_n, smaller_n])
            if larger_n not in est_scores:
                est_scores[larger_n] = dict()
            est_scores[larger_n][smaller_n] = val
            # if larger_n in all_exact_scores:
            #     if smaller_n in all_exact_scores[larger_n]:
            #         exactScore = all_exact_scores[larger_n][smaller_n]
            # L1 += abs(val - exactScore)
            # RAG += min(val,exactScore)/max(val,exactScore)
            # nodes_count += 1
            # ranking.append(larger_n*10000+smaller_n)
        # for topk in topk_list:
        #     tau_list.append(sp.stats.kendalltau(ranking[0:topk], exact_ranking[0:topk])[0])
        # tau = sp.stats.kendalltau(ranking[0:topK], exact_ranking[0:topK])[0]
        # for tau in tau_list:
        #     print str(tau)+"\t",
    ext_count_line = 0
   # with open("/Users/zhufanwei/Dropbox/Fast-Simrank/facebook/resultsAP/Exact-AP-_D10", 'r') as csvfile:
    with open(sys.argv[1], 'r') as csvfile:
        
   
        exactSim = csv.reader(csvfile, delimiter='\t')
        score = dict()
        # exact_query = open("exact_query"+query_count, 'w')
        for row in exactSim:
            ext_count_line += 1
            if ext_count_line > est_count_line:
                break
            if "ms" in row[0]:
                continue
            n1 = int(row[0])
            n2 = int(row[1])
            val = float(row[2])
            larger_n = -1
            smaller_n = -1
            if n1 > n2:
                larger_n = n1
                smaller_n = n2
            else:
                larger_n = n2
                smaller_n = n1
            exact_ranking.append([larger_n, smaller_n])
            if larger_n not in all_exact_scores:
                all_exact_scores[larger_n] = dict()
            all_exact_scores[larger_n][smaller_n] = val
            # exact_ranking.append(larger_n*10000+smaller_n)
        # RAG_divisor = 0
        # RAG_dividend = 0
        # for larger_n in all_exact_scores:
        #     larger_n_map = all_exact_scores[larger_n]
        #     for smaller_n in larger_n_map:
        #         ext_score = larger_n_map[smaller_n]
        #         RAG_divisor += ext_score
        #         if larger_n in est_scores:
        #             if smaller_n in est_scores[larger_n]:
        #                 L1 += abs(ext_score - est_scores[larger_n][smaller_n])
        # for larger_n in est_scores:
        #     larger_n_map = est_scores[larger_n]
        #     for smaller_n in larger_n_map:
        #         if larger_n in all_exact_scores:
        #             if smaller_n in all_exact_scores[larger_n]:
        #                 RAG_dividend += all_exact_scores[larger_n][smaller_n]
        tau = Tau(est_scores, all_exact_scores, est_ranking, exact_ranking)
        precision = Precision(est_scores, all_exact_scores, exact_ranking)
        rag = RAG(est_scores, all_exact_scores)
        l1 = L1(est_scores, all_exact_scores)

        print(str(tau)+"\t"+str(precision)+"\t"+str(rag)+"\t"+str(l1)+"\t"+str(sum_time))






Calculate_exact(sys.argv[2])



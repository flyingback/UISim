__author__ = 'Mao'
import csv
import math
import sys
import scipy.stats as sp
# topk_list = [100, 50, 25]


# Precision:
# foreach p in topKEstNP{
#     if p in topKTrueNP
#         count ++
# }
# Return count/k;



def L1(EstScores, TrueScores):
    sumL1 = 0.0
    for i in range(len(EstScores)):
        oneL1=abs(EstScores[i]-TrueScores[i])
        sumL1+=oneL1
        
  #  print "sum L1"
  #  print sumL1
    return sumL1



def RAG(EstScores, TrueScores):
    sumRag = 0.0
    for i in range(len(EstScores)):
        if (EstScores[i] == 0 and TrueScores[i]==0):
            oneRag=1.0
        elif (TrueScores[i]==0 or EstScores[i]==0):
            oneRag=0.0
        else:
            if EstScores[i] < TrueScores[i]:
                oneRag=EstScores[i]/TrueScores[i]
            else:
                oneRag=TrueScores[i]/EstScores[i]
      
        sumRag += oneRag
        
    return sumRag
        

def RAG1(EstScores, TrueScores):
    sumRag =0.0
    for i in range(len(EstScores)):
        if (EstScores[i] < TrueScores[i]):
            oneRag = (EstScores[i]+0.0001)/(TrueScores[i]+0.0001)
        else:
            oneRag = (TrueScores[i]+0.0001)/(EstScores[i]+0.0001)
        #print oneRag    
        sumRag += oneRag
    return sumRag


def Calculate_exact(filename):
    est_scores = []
    ext_scores = []
    
    with open(filename, 'r') as csvfile:
        fastsim = csv.reader(csvfile, delimiter=' ')
        sum_time = 0.0
        # exact_query = open("exact_query"+query_count, 'w')
        for row in fastsim:
            #print(row)
            if "ms" in row[0]:
                #sum_time += int(row[0].split("ms")[0])
                sum_time += float(row[0].split("ms")[0])
                
            #print(float(row[1]))
            est_scores.append(float(row[1]))
  #  print "sum Time"
   # print sum_time
  #       
    # with open("/Users/zhufanwei/Dropbox/Fast-Simrank/SIGMOD-expt/p2p/fastSingleP_NoOffline_NoCorindeg_H600_Depth5_theta1.0E-4_delta1.0E-4_eta0", 'r') as csvfile:
    with open(sys.argv[1], 'r') as csvfile:
        exactSim = csv.reader(csvfile, delimiter=' ')
        
        # exact_query = open("exact_query"+query_count, 'w')
        for row in exactSim:
            ext_scores.append(float(row[1]))
            
            
    l1=L1(est_scores,ext_scores)
    rag=RAG1(est_scores,ext_scores)
    print ("L1\t RAG\t Time")
    print(str(l1/len(est_scores))+"\t"+str(rag/len(est_scores))+"\t"+str(sum_time/len(est_scores)))
    



Calculate_exact(sys.argv[2])


#Calculate_exact("/Users/zhufanwei/Dropbox/Fast-Simrank/facebook.noAttr/SPresults/fastSingleP_NoOffline_NoCorindeg_H2000_Depth5_theta1.0E-4_delta1.0E-4_eta2")


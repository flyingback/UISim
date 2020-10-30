# UISim

Datasets:
1. Wiki
2. DBLP
3. CA(CondMat)

4. enwiki2013 http://law.di.unimi.it/webdata/enwiki-2013/
5. it2014 http://law.di.unimi.it/webdata/it-2004/
6. Friendster http://snap.stanford.edu/data/com-Friendster.html



Baselines:
Single-pair: BLPMC
Single-source: ProbeSim, PRSim[1]
All-pair:TreeWand, LocalPush[2]

[1] PRSim: Sublinear Time SimRank Computation on Large Power-Law Graphs. [slides] [poster] [code] https://github.com/wzskytop/PRSim-Code
[2] Y. Wang, L. Chen, Y. Che, and Q. Luo. Accelerating pairwise simrank estimation over static and dynamic graphs. PVLDB, 28(1):99–122, 2019. 
Y. Wang, X. Lian, and L. Chen. Efficient simrank tracking in dynamic graphs. In ICDE, pages 545–556, 2018.
https://github.com/RapidsAtHKUST/SimRank
All pair, static graph, non-parallel (https://github.com/RapidsAtHKUST/SimRank/blob/master/LPMC-Profile/yche_refactor/local_push_yche.cpp)


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# data from http://grouplens.org/datasets/movielens/


# In[1]:


import os
data_folder = os.path.join( "ml-100k")
ratings_filename = os.path.join(data_folder, "u.data")


# In[2]:


import pandas as pd


# In[3]:


#加载数据集时，把分隔符设置为制表符
#告诉pandas不要把第一行作为表头（header=None ），设置好各列的名称。
all_ratings = pd.read_csv(ratings_filename, delimiter="\t", header=None, names = ["UserID", "MovieID", "Rating", "Datetime"])
#解析时间数据
all_ratings["Datetime"] = pd.to_datetime(all_ratings['Datetime'],unit='s')
#稀疏矩阵（sparse matrix)
all_ratings[:10]


# In[4]:


# As you can see, there are no review for most movies, such as #213
all_ratings[all_ratings["UserID"] == 675].sort_values("MovieID")  


# In[5]:


#本次目标生成的规则：
#如果用户喜欢某些电影，他们也会喜欢这部电影

#首先确定用户是否喜欢某一部电影
all_ratings["Favorable"] = all_ratings["Rating"] > 3
all_ratings[0:10]


# In[6]:


all_ratings[all_ratings["UserID"] == 1][:10]


# In[7]:


# Sample the dataset. You can try increasing the size of the sample, but the run time will be considerably longer
ratings = all_ratings[all_ratings['UserID'].isin(range(200))]  # & ratings["UserID"].isin(range(100))]


# In[8]:


# 新建一个只包含用户喜欢某部电影的数据行
favorable_ratings = ratings[ratings["Favorable"]]
favorable_ratings[:10]


# In[9]:


# 只留下为超过一部电影打过喜欢分的用户
favorable_reviews_by_users = dict((k, frozenset(v.values)) for k, v in favorable_ratings.groupby("UserID")["MovieID"])
len(favorable_reviews_by_users)


# In[10]:


# 计算每部电影的喜欢数
num_favorable_by_movie = ratings[["MovieID", "Favorable"]].groupby("MovieID").sum()
num_favorable_by_movie.sort_values("Favorable", ascending=False)[:10]


# In[11]:


# Apriori算法是亲和性分析的一部分，专门用于查找数据集中的频繁项集。
# 基本流程是从前一步找到的频繁项集中找到新的备选集合，接着检测备选集合的频繁程度是否够高，然后算法像下面这样进行迭代。
# (1) 把各项目放到只包含自己的项集中，生成最初的频繁项集。只使用达到最小支持度的项目。
# (2) 查找现有频繁项集的超集，发现新的频繁项集，并用其生成新的备选项集。
# (3) 测试新生成的备选项集的频繁程度，如果不够频繁，则舍弃。如果没有新的频繁项集，就跳到最后一步。
# (4) 存储新发现的频繁项集，跳到步骤(2)。
# (5) 返回发现的所有频繁项集。
from collections import defaultdict

def find_frequent_itemsets(favorable_reviews_by_users, k_1_itemsets, min_support):
    counts = defaultdict(int)
    for user, reviews in favorable_reviews_by_users.items():
        for itemset in k_1_itemsets:
            if itemset.issubset(reviews):
                for other_reviewed_movie in reviews - itemset:
                    current_superset = itemset | frozenset((other_reviewed_movie,))
                    counts[current_superset] += 1
    return dict([(itemset, frequency) for itemset, frequency in counts.items() if frequency >= min_support])


# In[12]:


import sys
# Apriori算法第一次迭代时，新发现的项集长度为2，它们是步骤(1)中创建的项集的超集。第二次迭代（经过步骤(4)）中，新发现的项集长度为3。
# 我们把发现的频繁项集保存到以项集长度为键的字典中，便于根据长度查找，这样就可以找到最新发现的频繁项集。下面的代码初始化一个字典。

frequent_itemsets = {}  # itemsets are sorted by length
# 最小支持度
min_support = 50

# Apriori算法的第一步，为每一部电影生成只包含它自己的项集，检测它是否够频繁。
# 长度为1的不进入选择
frequent_itemsets[1] = dict((frozenset((movie_id,)), row["Favorable"])
                                for movie_id, row in num_favorable_by_movie.iterrows()
                                if row["Favorable"] > min_support)

print("有 {} 个电影有超过 {} 喜爱数".format(len(frequent_itemsets[1]), min_support))
sys.stdout.flush()
for k in range(2, 20):
    # Generate candidates of length k, using the frequent itemsets of length k-1
    # Only store the frequent itemsets
    cur_frequent_itemsets = find_frequent_itemsets(favorable_reviews_by_users, frequent_itemsets[k-1],
                                                   min_support)
    if len(cur_frequent_itemsets) == 0:
        print("没发现频繁项集 {}".format(k))
        sys.stdout.flush()
        break
    else:
        print("发现 {} 个频繁项集长度为 {}".format(len(cur_frequent_itemsets), k))
        #print(cur_frequent_itemsets)
        sys.stdout.flush()
        frequent_itemsets[k] = cur_frequent_itemsets
# 删除长度为1的项集
del frequent_itemsets[1]


# In[13]:


print("总共发现 {0} 个频繁项集".format(sum(len(itemsets) for itemsets in frequent_itemsets.values())))


# In[14]:


# 下面的代码通过遍历不同长度的频繁项集，为每个项集生成规则。
candidate_rules = []
for itemset_length, itemset_counts in frequent_itemsets.items():
    for itemset in itemset_counts.keys():
        # 遍历项集中的每一部电影，把它作为结论。项集中的其他电影作为前提，用前提和结论组成备选规则。
        for conclusion in itemset:
            premise = itemset - set((conclusion,))
            candidate_rules.append((premise, conclusion))
print("共有 {} 候选规则".format(len(candidate_rules)))


# In[15]:


# 遍历项集中的每一部电影，把它作为结论。项集中的其他电影作为前提，用前提和结论组成备选规则。
print(candidate_rules[0:3])


# In[16]:


# 我们需要先创建两个字典，用来存储规则应验（正例 ）和规则不适用（反例 ）的次数。
correct_counts = defaultdict(int)
incorrect_counts = defaultdict(int)
# 遍历所有用户及其喜欢的电影数据，在这个过程中遍历每条关联规则。
for user, reviews in favorable_reviews_by_users.items():
    for candidate_rule in candidate_rules:
        premise, conclusion = candidate_rule
        # 用户是否喜欢前提中的所有电影
        if premise.issubset(reviews):
            # 如果前提符合，看一下用户是否喜欢结论中的电影
            if conclusion in reviews:
                correct_counts[candidate_rule] += 1
            else:
                incorrect_counts[candidate_rule] += 1
# 用规则应验的次数除以前提条件出现的总次数，计算每条规则的置信度。
rule_confidence = {candidate_rule: correct_counts[candidate_rule] / float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule])
              for candidate_rule in candidate_rules}


# In[17]:


# 最小置信度
min_confidence = 0.95


# In[18]:


# 筛选出置信度>0.95的
rule_confidence = {rule: confidence for rule, confidence in rule_confidence.items() if confidence > min_confidence}
print(len(rule_confidence))


# In[19]:


from operator import itemgetter
sorted_confidence = sorted(rule_confidence.items(), key=itemgetter(1), reverse=True)


# In[20]:


for index in range(5):
    print("Rule #{0}".format(index + 1))
    # 对字典排序，输出前5
    (premise, conclusion) = sorted_confidence[index][0]
    print(sorted_confidence[index])
    print("Rule: If a person recommends {0} they will also recommend {1}".format(premise, conclusion))
    print(" - Confidence: {0:.3f}".format(rule_confidence[(premise, conclusion)]))
    print("")


# In[21]:


# 从电影名字表中获取电影名字
movie_name_filename = os.path.join(data_folder, "u.item")
movie_name_data = pd.read_csv(movie_name_filename, delimiter="|", header=None, encoding = "mac-roman")
movie_name_data.columns = ["MovieID", "Title", "Release Date", "Video Release", "IMDB", "<UNK>", "Action", "Adventure",
                           "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir",
                           "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]


# In[22]:


def get_movie_name(movie_id):
    title_object = movie_name_data[movie_name_data["MovieID"] == movie_id]["Title"]
    title = title_object.values[0]
    return title


# In[23]:


get_movie_name(4)


# In[24]:


for index in range(1):
    print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    premise_names = ", ".join(get_movie_name(idx) for idx in premise)
    conclusion_name = get_movie_name(conclusion)
    print("Rule: If a person recommends {0} they will also recommend {1}".format(premise_names, conclusion_name))
    print(" - Confidence: {0:.3f}".format(rule_confidence[(premise, conclusion)]))
    print("")


# In[25]:


# 测试集
test_dataset = all_ratings[~all_ratings['UserID'].isin(range(300))]
test_favorable = test_dataset[test_dataset["Favorable"]]
test_favorable_by_users = dict((k, frozenset(v.values)) for k, v in test_favorable.groupby("UserID")["MovieID"])

#test_not_favourable = test_dataset[~test_dataset["Favourable"]]
#test_not_favourable_by_users = dict((k, frozenset(v.values)) for k, v in test_not_favourable.groupby("UserID")["MovieID"])
#test_users = test_dataset["UserID"].unique()


# In[26]:


test_dataset[:5]


# In[27]:


correct_counts = defaultdict(int)
incorrect_counts = defaultdict(int)
for user, reviews in test_favorable_by_users.items():
    for candidate_rule in candidate_rules:
        premise, conclusion = candidate_rule
        if premise.issubset(reviews):
            if conclusion in reviews:
                correct_counts[candidate_rule] += 1
            else:
                incorrect_counts[candidate_rule] += 1


# In[28]:


test_confidence = {candidate_rule: correct_counts[candidate_rule] / float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule])
                   for candidate_rule in rule_confidence}
print(len(test_confidence))


# In[29]:


sorted_test_confidence = sorted(test_confidence.items(), key=itemgetter(1), reverse=True)
print(sorted_test_confidence[:5])


# In[30]:


json = []
for index in range(52116):
    (premise, conclusion) = sorted_confidence[index][0]
    premise_names = ", ".join(get_movie_name(idx) for idx in premise)
    conclusion_name = get_movie_name(conclusion)
    if test_confidence.get((premise, conclusion), -1) > 0.96:
        print("Rule #{0}".format(index + 1))
        dict = []
        for idx in premise:
            dict.append(get_movie_name(idx))
        item = {}
        item["favor"] = dict
        item["recomondation"] = get_movie_name(conclusion)
        json.append(item)
        # print("{0}".format(conclusion_name))
        print("规则，如果喜欢 {0} 会推荐 {1}".format(premise_names, conclusion_name))
        print(" - Train Confidence: {0:.3f}".format(rule_confidence.get((premise, conclusion), -1)))
        print(" - Test Confidence: {0:.3f}".format(test_confidence.get((premise, conclusion), -1)))
        print("")


# In[31]:


print(json)






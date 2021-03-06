
# coding: utf-8

# In[171]:

import pandas as pa
import numpy as np
import sklearn
from sklearn import preprocessing
import math
from itertools import izip


# In[172]:

training_data = pa.read_csv("../bytecup2016data/invited_info_train.txt", sep = "\t")
question_data =  pa.read_csv("../bytecup2016data/question_info.txt", sep="\t")
user_data =  pa.read_csv("../bytecup2016data/user_info.txt", sep = "\t")
validation_info = pa.read_csv("../bytecup2016data/validate_nolabel.txt", sep = ",")


# In[173]:

test_data = pa.read_csv("../bytecup2016data/test.csv", sep = ",")


# In[174]:

'''
u/q matrix 
'''
question_list = list(set(training_data.iloc[:,0]))
expert_list = list(set(training_data.iloc[:,1]))


# In[175]:

'''
{
u1: [0,1,2,3],
}
'''
prediction_dict = {}
#print validation_info
for row in range(validation_info.shape[0]):
    row_info = validation_info.iloc[row]
    curr_q , curr_u  =  row_info[0], row_info[1] 

    if curr_u not in expert_list:
        expert_list.append(curr_u)
    
    if curr_q not in question_list:
        question_list.append(curr_q)
        
    question_index = question_list.index(curr_q)  
    expert_index = expert_list.index(curr_u)    
    

    if expert_index not in prediction_dict:
        prediction_dict[expert_index]=[question_index]
    else:
        prediction_dict[expert_index].append(question_index)


# In[176]:

#dictionary for test data
'''
{
u1: [0,1,2,3],
}
'''
prediction_dict_test = {}
for row in range(test_data.shape[0]):
    row_info = test_data.iloc[row]
    curr_q , curr_u  =  row_info[0], row_info[1] 

    if curr_u not in expert_list:
        expert_list.append(curr_u)
    
    if curr_q not in question_list:
        question_list.append(curr_q)
        
    question_index = question_list.index(curr_q)  
    expert_index = expert_list.index(curr_u)    
    

    if expert_index not in prediction_dict_test:
        prediction_dict_test[expert_index]=[]
    
    prediction_dict_test[expert_index].append(question_index)


# In[73]:

#working on a small dictionary
'''
prediction_dict_small = {}
for row in range(10):
    row_info = validation_info.iloc[row]
    curr_q , curr_u  =  row_info[0], row_info[1] 

    #if curr_u not in expert_list:
    #    expert_list.append(curr_u)
    
    #if curr_q not in question_list:
    #    question_list.append(curr_q)
        
    question_index = question_list.index(curr_q)  
    expert_index = expert_list.index(curr_u)    
    
    if expert_index not in prediction_dict_small:
        prediction_dict_small[expert_index]=[question_index]
    else:
        prediction_dict_small[expert_index].append(question_index)
'''


# In[177]:

#row_train = training_data.shape[0]

eq_matrix = np.zeros((len(expert_list), len(question_list)))
eq_matrix.fill(np.nan) #----fill with nans


# In[178]:

lines = []
for row in range(training_data.shape[0]):
    
    row_info = training_data.iloc[row]
    curr_q , curr_u, label =  row_info[0], row_info[1], row_info[2] 
    question_index = question_list.index(curr_q)      
    expert_index = expert_list.index(curr_u)    
    eq_matrix[expert_index][question_index] =  label


# In[179]:

'''
r_bar = []
'''
#for row in range(eq_matrix.shape[0]):
#0: 0 0 0 0 0 1 1 nan nan
ru_bar  =  np.nanmean(eq_matrix , axis = 1)

rq_bar =  np.nanmean(eq_matrix , axis = 0)

u_avg = np.nanmean(ru_bar)
q_avg = np.nanmean(rq_bar)

print u_avg
ru_bar[np.isnan(ru_bar)] = u_avg
rq_bar[np.isnan(rq_bar)] = q_avg
# ru_bar = pa.DataFrame(ru_bar1).fillna(u_avg)
# rq_bar =  pa.DataFrame(rq_bar1).fillna(q_avg)
# print '@@@',type(ru_bar)
# print '!!!',ru_bar
prior_expert = ru_bar
prior_item = rq_bar


# In[130]:

print u_avg, type(ru_bar)
#fill nan with average of other values


# In[180]:

#ru_bar = ru_bar.values.T.tolist()
#rq_bar = rq_bar.values.T.tolist()
# ru_bar1 = ru_bar1[0]

#print list(ru_bar)
#print type(rq_bar)


# In[ ]:

#Q: -> should I init remaining vals to avg of matrix      ???????????


# In[181]:

'''
w_a_u = expert * expert
'''
num_experts = eq_matrix.shape[0]
wau = np.zeros((num_experts,num_experts))

rated_questions = []

for exp in range(num_experts):
    faced = np.argwhere(~np.isnan(eq_matrix[exp]))
    c=map(float, faced)
    rated_questions.append(c)


# In[182]:

for exp1 in range(num_experts):
    for exp2 in range(exp1+1):
        #print '.',
        #wau[exp1][exp2] = 0
        
        common_qs = set(rated_questions[exp1]).intersection(set(rated_questions[exp2]))
        nr = 0
        dr1 = 0
        dr2 = 0
        a_bar = ru_bar[exp1]
        u_bar = ru_bar[exp2]
        
#         print ru_bar
        for q in common_qs:
            pa = (eq_matrix[exp1][q] - a_bar )
            pu =  (eq_matrix[exp2][q] - u_bar)
#             print type(pa)
            nr +=  float(pa)* pu
            dr1 += (pa)**2
            dr2 += (pu)**2

        dr = math.sqrt(dr1 * dr2)
        '''if  (a_bar == 0.0 and u_bar == 1.0)  or  (a_bar == 1.0 and u_bar == 0.0) :#when all ratings are the same 
            wau[exp1][exp2] = 0
            wau[exp2][exp1] = 0


        elif  (a_bar == 0.0 and u_bar == 0.0) or  (a_bar == 1.0 and u_bar == 1.0)  :#when all ratings are the same 
            wau[exp1][exp2] = 1
            wau[exp2][exp1] = 1
        
        else: 
       '''     #print nr, dr , a_bar, u_bar
        if dr == 0: 
            wau[exp1][exp2] = 0  #??????????????
#             print 'wau',wau[exp1][exp2]
        else:        
            wau[exp1][exp2] = 1.0*nr/dr
            wau[exp2][exp1] = wau[exp1][exp2]
#             print 'wau',wau[exp1][exp2]


# In[183]:

#------ predict funtion
import heapq
import numpy
K = 50
def predict_rating(a,q):
    global K
    if not math.isnan(eq_matrix[a][q]):
        return eq_matrix[a][q]
    
    pred = 0
    
    a_bar = ru_bar[a]
    if math.isnan(a_bar):
        a_bar = 0

    part2 = 0
    p2num = 0
    p2den = 0
    
    usrs = wau[a] #all users with curr user comb
    topK = heapq.nlargest(K, range(len(usrs)), usrs.take)
    for u_idx in topK:
        if not math.isnan(eq_matrix[u_idx][q]):
            curr_wau = wau[a][u_idx]
            curr_dev = (eq_matrix[u_idx][q] - ru_bar[u_idx])
            p2num += curr_wau * curr_dev
            p2den += abs(wau[a][u_idx])
    if p2den!=0:    
        part2 = p2num/p2den
    else:
        part2 = 0
        
    if math.isnan(part2):
        part2 = 0 
    
    return abs(a_bar + part2)


# In[184]:

'''
Time to make predicitons
'''
# for u in prediction_dict_small:
#     for q in prediction_dict_small[u]:
#         print 'u',u
#         print 'q',q
# #         print 'eq_matrix',eq_matrix[u][q]
         
#         r = predict_rating(u,q)
#         eq_matrix[u][q] = r
#         print '$$$',r
#         print '$$$',eq_matrix[u][q]
#         #raw_input()



# In[194]:

#print list(eq_matrix[78])


# In[195]:

'''''
Time to make predicitons for validations
'''
for u in prediction_dict:
    for q in prediction_dict[u]:
        #print 'u',u
        #print 'q',q
        #  print 'eq_matrix',eq_matrix[u][q]
        r = predict_rating(u,q)
        eq_matrix[u][q] = r
        #print '$$$',r
        #print '$$$',eq_matrix[u][q]
        #raw_input()

#print eq_matrix[24]


# In[196]:

#--- time for test preds
for u in prediction_dict_test:
    for q in prediction_dict_test[u]:
        r = predict_rating(u,q)
        eq_matrix[u][q] = r


# In[24]:

#print list(eq_matrix[26297])


# In[197]:

avg_matrix = np.nanmean(eq_matrix)


# In[198]:

print avg_matrix


# In[199]:

def ReadPredictions(dataset):
    global question_list, expert_list
    #------can be repeated for training data
    val_r_count = dataset.shape[0]
    y_pred = []
    for vrow in range(val_r_count):
        qid, uid = dataset.ix[vrow][0] ,  dataset.ix[vrow][1]
        question_index = question_list.index(qid)  
        expert_index = expert_list.index(uid)    
        curr_prob = 0
        if expert_index < eq_matrix.shape[0]:
            if question_index < eq_matrix.shape[1]: 
                curr_prob = eq_matrix[expert_index][question_index]
            else: 
                #question prediction not found
                curr_prob = ru_bar[expert_index]
        else: 
            #expert not in our matrix
            if question_index < eq_matrix.shape[1]:
                curr_prob = prior_item[question_index]
            else:
                print 'neither user nor ques found'
                curr_prob = avg_matrix
        y_pred.append(curr_prob)
    return y_pred


# In[200]:

yPredValidation = ReadPredictions(validation_info)


# In[201]:

yPredTest =  ReadPredictions(test_data)


# In[202]:

yPredTrain = ReadPredictions(training_data)


# In[203]:

y_pred_valid_str = map(str, yPredValidation)
with open('CollFiltering_Validation3.csv','w') as f:
    f.write('\n'.join(y_pred_valid_str))


# In[204]:

y_pred_test_str = map(str, yPredTest)
with open('CollFiltering_Test3.csv','w') as f:
    f.write('\n'.join(y_pred_test_str))


# In[205]:

y_pred_train_str = map(str, yPredTrain)
with open('CollFiltering_Train3.csv','w') as f:
    f.write('\n'.join(y_pred_train_str))


# In[53]:

print yPred , yPredTrain


# In[161]:

def RMSE(y_true, y_pred):
    return np.sqrt(np.mean((y_pred - y_true)**2))


# In[154]:

with open('CF_NEW_Validation.csv','w') as f:
    f.write('\n'.join(lines))


# In[163]:

#y_preds = ReadPredictions(training_data)
y_true = training_data.iloc[:,2]
print RMSE(y_true, yPredTrain)


# In[164]:

#calculate test acc
test_data  = pa.read_csv("../bytecup2016data/test_nolabel.txt", sep = "\t")


# In[ ]:




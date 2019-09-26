import math,time
from copy import deepcopy

#Followings are variables to be declared before
#variables to store incentive share_plan of all models
Models={}
#variable to set the initial value for first model offered by ExtremeVision
Model_Init={'model_value':1000}
#module of hype-parameters calculate credit & impact of users
Fed_Module={'budget_model':{'a':10,'b':8},'decay_model':{'alpha':0.05,'unit_time':3600},\
            'score_model':{'best_metric':0.8}}
#DICT to store temp users' new submit haven't processed yet.



#todo entrance for server submit
#each time there is a new model generated by server, it

#server first must upload the initial training model (m0) it process. initial training model
# is set with train_model_name=new_model_name.


def add_model(train_model_name,new_model_name,new_model_metric):
    #1. check existence of train_model, not = (new model/starting point)
    #   insert new model into global DICT variable Models.
    if train_model_name not in Models:
        model={'metric':new_model_metric,'model_value':Model_Init['model_value'],\
               'train_model_name':'None','timestamp':time.time(),\
               'credit_share_plan':[{'name':'Admin','credit':Model_Init['model_value']}],\
               'impact_share_plan':[{'name':'Admin','impact':Model_Init['model_value']}]}
        Models[new_model_name]=model
        return
    Models[new_model_name]['metric']=new_model_metric
    Models[new_model_name]['train_model_name']=train_model_name

    #2. calculate new model's incremental value = Budget
    #the value of the model is an exp function with hyper-parameter set based on experience.
    B=Fed_Module['budget_model']
    budget=B['a']*math.exp(B['b']*new_model_metric)-\
           B['a']*math.exp(B['b']*Models[train_model_name]['metric'])
    Models[new_model_name]['model_value']=B['a']*math.exp(B['b']*new_model_metric)


    #2. calculate credit (budget shared only by participant in this round)
    #3. 'credit' means the real share of budget
    credit_share_plan=[]
    for user in Models[new_model_name]['submissions']:
        record={}
        record['name']=user['name']
        record['credit']=user['data']*user['score']
        credit_share_plan.append(record)
    budget_modify_ratio=budget/sum([record['credit'] for record in credit_share_plan])
    for record in credit_share_plan:
        record['credit']*=budget_modify_ratio
    Models[new_model_name]['credit_share_plan']=credit_share_plan

    #3. calculate impact (budget shared by users and models)
    Models[new_model_name]['timestamp']=time.time()
    decay_model=Fed_Module['decay_model']

    #the impact value of previous model is decayed when it participant as training model.
    #the decay function is linear and can be set at global parameter Fed_Moduel['decay_model']
    train_model_value_decay_ratio=\
        max(0,1.0-decay_model['alpha']*\
            (Models[new_model_name]['timestamp']-Models[train_model_name]['timestamp'])\
            /decay_model['unit_time'])

    #merge the decayed value of each user in training model and new participant user.
    #the 'impact' value means the value should be based on their contribution.
    #however the budget may not be enough to compensate the 'impact' value. So the 'credit' means
    #if distribute the new generated budget according to the ratio of 'impact'
    train_impact_share=Models[train_model_name]['impact_share_plan']
    train_name_impact_dict={record['name']:record['impact']*train_model_value_decay_ratio\
                            for record in train_impact_share}
    new_name_impact_dict={record['name']:record['credit'] for record in credit_share_plan}
    merged_dict = {name: train_name_impact_dict.get(name, 0) + new_name_impact_dict.get(name, 0) \
                   for name in train_name_impact_dict.keys() | new_name_impact_dict.keys()}
    impact_share_plan = [{'name': name, 'impact': merged_dict[name]} for name in merged_dict]
    budget_ratio = budget / sum(merged_dict.values())
    for record in impact_share_plan:
        record['credit'] = record['impact'] * budget_ratio
    Models[new_model_name]['impact_share_plan'] = impact_share_plan

    #4. insert the new model into global DICT variable Models.
    #todo logging here can be written as any database or write file
    log_model=Models[new_model_name]
    pass




#todo entrance for user submit
def add_user(user_name,data_quantity,data_metric_result,new_model_name):
    #1. calculate score of user submit data, from its testing metric result
    #the 'best metric' represents the new dataset offers new knowledge with most desire
    # differences from previous dataset.
    score = 1.0 - abs(data_metric_result - Fed_Module['score_model']['best_metric'])

    #2. user's submission this round
    submission={'name':user_name,'data':data_quantity,\
                                'metric':data_metric_result,'score':score}

    #3. insert user's submission into new_model.
    #   First, check if new model exist.
    if new_model_name not in Models:
        model = {'submissions':[submission]}
        Models[new_model_name] = model
    else:
        Models[new_model_name]['submissions'].append(submission)
    return
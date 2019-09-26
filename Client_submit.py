import Server_Incentive as SI
import json


#each user when participant in new round the federation training, after test its new
# prepared data with newest model and get the test result as 'data_metric_result',
# calls the submit_results function.

#Server_Incentive is the function as server end to receive the parameter. User only
# has to upload the parameters.

#todo but user must upload the new_model_name it is about to participating in.
# OR if there is no such new_model_name can be provided. then it can be give at
# 'add_user' function at the server end.


def submit_results(user_name,data_quantity,data_metric_result,new_model_name):
    j_string = json.dumps((user_name, data_quantity, data_metric_result, new_model_name))
    SI.add_user(j_string)
    pass
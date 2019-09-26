import Server_Incentive as SI
import Client_submit as CS


'''
this is a rundown for user and server end of the incentive mechanism interaction.

Followings are some things to be considered:
1.Function CS.submit_results needs parameter 'new_model_name' 
  when user submit their new data to server.
  This parameter can either be submitted by user or given by server
  after user's submission.
  User submission only pass the parameters to server.

2. The final result is in global dict variable FI.Model at server
  end.
  It can be changed to write into local file or insert into
  database. Just change the last line of function add_model.
'''

# first, server add the initial model in
SI.add_model('m0','m0',0.75)

# client start participant and submit their info round 1
CS.submit_results('u1',100,0.75,'m1')
CS.submit_results('u2',80,0.6,'m1')

# server finishes training model and add the new model in
SI.add_model('m0','m1',0.76)

# client start participant and submit their info round 2
CS.submit_results('u1',100,0.8,'m2')
CS.submit_results('u3',50,0.8,'m2')

# server finishes training model and add the new model in
SI.add_model('m1','m2',0.77)

# all models info and corresponding incentive plan/distribution are store
# in SI.Models
print(SI.Models)
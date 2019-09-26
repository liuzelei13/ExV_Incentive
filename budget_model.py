import math
import numpy as np

Budget={'a':10,'b':8}
base_value=1000

def model_value(metric):
    return Budget['a']*math.exp(Budget['b']*metric)



metrics=np.arange(0.7,0.85,0.01)

print('base price: %d'%base_value)


for i in range(len(metrics)-1):
    print('metrics improve from %.2f -> %.2f : Value=%.2f'%(metrics[i],metrics[i+1],model_value(metrics[i+1])-model_value(metrics[i])))

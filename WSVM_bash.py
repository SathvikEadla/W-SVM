import re
import subprocess
import pandas as pd
import os

path_wsvm = '/home/sathvik/Desktop/W-SVM/W-SVM/' #path to W-SVM directory
if os.getcwd() != path_wsvm:
    os.chdir(path_wsvm)

train_command = './svm-train -s 8 -t 0 train_svm model'
process = subprocess.Popen(train_command.split(), stdout = subprocess.PIPE)
output, error = process.communicate()

test_command = './svm-predict -P 0.05 test_svm model_one_wsvm output.csv'
process1 = subprocess.Popen(test_command.split(),stdout = subprocess.PIPE)
out, error1 = process1.communicate()
metrics_string = out.decode()


metrics = ['Recognition Accuracy', 'Precision', 'Recall','Fmeasure',
            'Total tests', 'True pos','True Neg','False Pos','False neg']
metrics_list = re.findall(r'[-+]?\d*\.\d+|\d+', metrics_string)
metrics_list = list(map(float, metrics_list))
metrics_dict = dict(zip(metrics,metrics_list))
print(metrics_dict)
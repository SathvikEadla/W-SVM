# Requirements:
	- Operating system - Linux
	- build-essential (For installation of build-essential use sudo apt-get install build-essential)
	- python > 3.5
	- pandas
	- numpy
	- sklearn
	- matplotlib
	- seaborn
	- hyperopt
	
# Installation:

### Install libMR 

```sh
$ tar -zxf libMR.tgz
$ cd libMR
$ mkdir build;  % or whereyou like to build it
$ cd build
$ cmake ..
or to get a different installation directory
$ cmake -DCMAKE_INSTALL_PREFIX=<YOUR_INSTALLATON_PATH> ..
$ make
```	
	
After Installation copy ***libMR.so*** file generated inside *build/libMR* to */lib* folder.

### Installing library for W-SVM
Once libMR is build, next step is to specify the absolute path of libMR directory in Makefile available in libsvm-openset.  
Paste the absolute path of libMR folder in variable "LIBMR_DIR" in Makefile (line 2 of Makefile).  
For example: LIBMR_DIR = /home/sathvik/Desktop/OpenSet/W-SVM/libMR  
Type ***make*** to build the '*svm-train*' and '*svm-predict*' programs. Run them without arguments to show the usages of them.
	
```sh
$ cd W-SVM
$ make
$ ./svm-train (for testing whether the installation was successfull or not. It should display options as shown below)
$ ./svm-predict
```


	***svm-train [options] training_set_file [model_file]***
	options:
	-s svm_type : set type of SVM (default 0)
		0 -- C-SVC
		1 -- nu-SVC
		2 -- one-class SVM
		3 -- epsilon-SVR
		4 -- nu-SVR
		5 -- open-set oneclass SVM (open_set_training_file required)
		6 -- open-set pair-wise SVM  (open_set_training_file required)
		7 -- open-set binary SVM  (open_set_training_file required)
		8 -- one-vs-rest WSVM (open_set_training_file required)
		9 -- One-class PI-OSVM (open_set_training_file required)
		10 -- one-vs-all PI-SVM (open_set_training_file required)
	-t kernel_type : set type of kernel function (default 2)
		0 -- linear: u'*v
		1 -- polynomial: (gamma*u'*v + coef0)^degree
		2 -- radial basis function: exp(-gamma*|u-v|^2)
		3 -- sigmoid: tanh(gamma*u'*v + coef0)
		4 -- precomputed kernel (kernel values in training_set_file)
	-d degree : set degree in kernel function (default 3)
	-g gamma : set gamma in kernel function (default 1/num_features)
	-r coef0 : set coef0 in kernel function (default 0)
	-c cost : set the parameter C of C-SVC, epsilon-SVR, and nu-SVR (default 1)
	-n nu : set the parameter nu of nu-SVC, one-class SVM, and nu-SVR (default 0.5)
	-p epsilon : set the epsilon in loss function of epsilon-SVR (default 0.1)
	-m cachesize : set cache memory size in MB (default 100)
	-e epsilon : set tolerance of termination criterion (default 0.001)
	-h shrinking : whether to use the shrinking heuristics, 0 or 1 (default 1)
	-b probability_estimates : whether to train a SVC or SVR model for probability estimates, 0 or 1 (default 0)
	-wi weight : set the parameter C of class i to weight*C, for C-SVC (default 1)
	-v n: n-fold cross validation mode
	-P threshold probability value to reject sample as unknowns for WSVM/One-class PI-OSVM (default 0.0) (only for cross validation)
	-C threshold probability value to reject sample as unknowns for CAP model in WSVM(default 0.0) (only for cross validation)
	-B beta   will set the beta for fmeasure used in openset training, default =1
	-V filename   will log data about the opeset optimization process to filename
	-G nearpreasure farpressure   will adjust the pressures for openset optimiation. <0 will specalize, >0 will generalize
	-N  we build models for negative classes (used for multiclass where labels might be negative.  default is only positive models 
	-E  do exaustive search for best openset (otherwise do the default greedy optimization) 
	-q : quiet mode (no outputs)
	-o cost : set the parameter C for CAP model in one-vs-rest WSVM 
	-a gamma : set gamma in kernel function for CAP model in one-vs-rest WSVM 

	***svm-predict [options] test_file model_file output_file***
	options:
	  -b probability_estimates: whether to predict probability estimates, 0 or 1 (default 0); for one-class SVM only 0 is supported
	  -o: this is an open set problem. this will look for model files with names of the form <model_file>.<class>
	  -V  for more verbose output
	  -s output scores in bin format(1-2, 1-3, 1-4, 2-3) to outputfile(cannot be combined with -v or -t) 
	  -t output totaled scores 1-2+1-3+1-4=1 ect to outputfile(cannot be combined with -s or -v) 
	  -v output votes to outputfile(cannot be combined with -s or -t) 
	  -P threshold probability value to reject sample as unknowns for WSVM(default 0.0) 
	  -C threshold probability value to reject sample as unknowns for CAP model in WSVM(default 0.0) 
	  
# Modifications:
The core file ***svm-predict*** from libsvm-openset is modified to produce output file in comma seperated value format containing both actual and predicted value. (Original output file contains only predicted labels of known class without any separator)  
Changes are made to produce output label of '99' for untrained or unknown class.
		  
# Usage:
	In svm-train:
		-s 8 for the WSVM based on 1-vs-rest binary svms
	In svm-predict:
		-P specify thresholded probability value to reject sample as unknowns for WSVM (default 0.0)
		-C specify thresholded probability value to reject sample as unknowns for CAP model in WSVM (default 0.0)
	 
	To use WSVM in W-SVM folder:
	************ Training
	./svm-train -s 8 -t 0 TrainingDataFile ModelFile
			where if TrainingDataFile is training file in libsvm format. Two file "ModelFile" and "ModelFile_one_wsvm" will be genrated using 1-vs-rest SVM and one-class SVM (CAP) respectively for WSVM.
	************ Predicing Using two model files ("ModelFile" and "ModelFile_one_wsvm")
	./svm-predict -P 0.1 -C 0.001 TestDataFile ModelFile outputfile.csv
			where TestDataFile is testing file in libsvm format. ModelFile is file generated during training. ./svm-predict by default looks for ModelFile_one_wsvm file generated for CAP model in WSVM training.
			*outputfile.csv* consists actual label and predicted label separated with comma.
			-P specify the threshold to consider for rejecting samples as unknown in WSVM.
			-C specify the minimum threshold to consider for any sample in CAP model.

	- 'sample_data_prep.py' contains code for modelling letter-recongition data to openset condition.
	- 'WSVM_dataprep.py' contains code for converting the data to libsvm format. (*Note: the data should not contain text labels*)
	- 'WSVM_bash.py' contains code for running bash scripts in python.
	- 'wsvm_metrics.py' is used to obtain metrics such as Confusion Matrix, F-measure, Recognition Accuracy, Precision, Recall. 
	- 'WSVM_hypertune.py' performs hyperparameter tuning for your dataset using Hyperopt library.

	
# Attribution:
This is an implementation of the Probability Models for Open Set Recognition by Lalith P Jain and Walter J. Scheirer et al., with minor changes from the original work.  
The link to the original repos is attached herewith:  
libsvm-openset: https://github.com/ljain2/libsvm-openset  
libMR: https://github.com/Vastlab/libMR  

The conversion of data from normal format to libsvm format is modified from phraug. The link of original repo is https://github.com/zygmuntz/phraug.  

@article{Scheirer_2011_TPAMI,
author = {Walter J. Scheirer and Anderson Rocha and Ross Michaels and Terrance E. Boult},
title = {Meta-Recognition: The Theory and Practice of Recognition Score Analysis},
journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence (PAMI)},
volume = {33},
issue = {8},
pages = {1689--1695},
year = {2011}
}    

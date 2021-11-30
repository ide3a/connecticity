#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:16:26 2021
Last modified on Fri Nov 26

@author: Marie-Philine Becker, Riccardo Taormina and Andrea Cominola
"""

##### Imports ###############################################

# numpy stack
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import random as rn
import os
from paths import *

# scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# other packages
import time
from ruamel.yaml import YAML
from tqdm.notebook import tqdm as tqdm
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN
import tensorflow as tf
from scipy import stats
import joblib
import warnings; warnings.simplefilter('ignore')

# ML methods
from lightgbm import LGBMClassifier


##### Function for reading the configuration file ############################
def read_config(filename):

    with open(filename) as f:
        yaml = YAML(typ='safe')
        cfg = yaml.load(f)

    return cfg

def initalize_random_generators(cfg, count=0):

    '''
    This function initialites the random seeds specified in the config file.
    count: used for multiple seed testing
    '''
    # initialize random seeds for reproducibility
    np_seed=cfg['np_seed'][count]
    rn_seed=cfg['rn_seed'][count]
    tf_seed=cfg['tf_seed'][count]

    # initialize random generators for numpy, np and tensorflow
    np.random.seed(np_seed)
    rn.seed(rn_seed)
    tf.random.set_seed(tf_seed)


##### Function to load dataset ###############################################
def load_data(file):
    dataset = pd.read_csv(os.path.join(DATA_DIR, file))
    return dataset

##### Function to compute the number of time steps with overlapping end uses ############
def overlapping_time_steps(allData, endUses):
    allDataCopy = allData.copy()
    allDataCopy[allData>0]=1
    numOverlapp = np.sum(allDataCopy[endUses],axis=1)
    percOverlapp = np.sum(numOverlapp > 1)/np.sum(numOverlapp > 0)*100
    return percOverlapp

##### Function to extract end use events and statistics from end use time series ############
def extractEvents(allData, endUses):
    # Create temp dataframe to be filled with features
    data = []
    allEndUses = pd.DataFrame(data, columns=['Duration','Volume','Peak','Mode','Hour','Label'])

    # Extracting events
    for eu in range(len(endUses)):
        currEU = allData[endUses[eu]]
        currEU_bin = currEU.copy()
        currEU_bin[currEU_bin>0] = 1
        diffCurrEU = np.hstack([0,np.diff(currEU_bin)])

        # Identifying start and end of each end use event
        startPos = np.where(diffCurrEU == 1)
        endPos = np.where(diffCurrEU == -1)

        # Calculating statistics for each event
        for event in range(len(startPos[0])):
            currStart = startPos[0][event]
            currEnd = endPos[0][event]
            # Duration [seconds]
            d = (currEnd-currStart)*10
            # Volume
            v = np.sum(currEU[currStart:currEnd])
            # Peak
            p = np.max(currEU[currStart:currEnd])
            # Mode
            m = stats.mode(currEU[currStart:currEnd])
            # Hour [0:23]
            h = np.remainder(np.floor((currStart*10)/3600), 24)
            # Add event to the output data set
            allEndUses.loc[len(allEndUses)]=[d,v,p,m.mode[0],h, endUses[eu]]


    # Shuffle rows of output data set
    allEndUses = allEndUses.sample(frac=1).reset_index(drop=True)
    return(allEndUses)

##### Function to extract end use events and statistics from aggregated TOTAL consumption time series ############
def extractEventsFromTotal(allData):
    # Create temp dataframe to be filled with features
    data = []
    allEndUsesFromTotal = pd.DataFrame(data, columns=['Duration','Volume','Peak','Mode','Hour','Label'])

    potentialEndUses = []

    # Extracting events
    totWU = allData['TOTAL']
    totWU_bin = totWU.copy()
    totWU_bin[totWU_bin>0] = 1
    diffTotWU = np.hstack([0,np.diff(totWU_bin)])
    # Identifying start and end of each end use event
    startPos = np.where(diffTotWU == 1)
    endPos = np.where(diffTotWU == -1)

    # Calculating statistics for each event
    for event in range(len(startPos[0])):
        currStart = startPos[0][event]
        currEnd = endPos[0][event]
        # Duration [seconds]
        d = (currEnd-currStart)*10
        # Volume
        v = np.sum(totWU[currStart:currEnd])
        # Peak
        p = np.max(totWU[currStart:currEnd])
        # Mode
        m = stats.mode(totWU[currStart:currEnd])
        # Hour [0:23]
        h = np.remainder(np.floor((currStart*10)/3600), 24)
        # Compute end use label
        potentialEndUses = allData[['StToilet','StShower','StFaucet','StClothesWasher', 'StDishwasher']][currStart:currEnd]
        currLabel = pd.Series.idxmax(np.sum(potentialEndUses))
        # Add event to the output data set
        allEndUsesFromTotal.loc[len(allEndUsesFromTotal)]=[d,v,p,m.mode[0],h, currLabel]
    # Shuffle rows of output data set
    allEndUsesFromTotal = allEndUsesFromTotal.sample(frac=1).reset_index(drop=True)
    return(allEndUsesFromTotal)


##### Function for preparing the dataset for further computations ############
def data_prep(data, featList, labelName, randomState, testSize, trainSize=-1):

    '''
    This function defines the label (target variable) and the feature list
    as well as splitting the dataset into test and training set.
    Default values are set to the presented paper.
    '''
    X = data[featList]
    y = data[labelName]

    # Train - test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size= testSize,random_state= randomState)

    if trainSize > -1:
        X_train = X_train[:trainSize]
        y_train = y_train[:trainSize]

    return  X_train, X_test, y_train, y_test


# create stratified kfolds (done once to for faster implementation, especially if SMOTE is used)
def create_folds_with_SMOTE(X_cv, y_cv, n_splits, smoter=None):
    skfold = StratifiedKFold(n_splits)
    folds = [] # dictionary with folds
    for fold_, (tra_, val_) in enumerate(skfold.split(X_cv, y_cv)):
        # split dataset
        X_train, X_valid = X_cv.values[tra_], X_cv.values[val_]
        y_train, y_valid = y_cv.values[tra_], y_cv.values[val_]
        # standardize data based on training folds (needed for ANNs)
        scaler = MinMaxScaler()
        X_train = scaler.fit_transform(X_train)
        X_valid = scaler.transform(X_valid)
        # oversample only the data in the training section with SMOTE
        if smoter != None:
            X_train, y_train = smoter.fit_resample(X_train,y_train)
        # store folds
        folds.append({'train':(X_train,y_train,tra_), 'valid':(X_valid,y_valid,val_), 'scaler': scaler})
    return folds

def single_model_cv(folds, algorithm, params, n_valid, X_test=None, disable_tdqm=False):
    ## initiate object with out-of-fold predictions for computational efficiency
    oof_preds = np.zeros((n_valid,1)).astype(object)
    # oof_preds = pd.Series(index=np.arange(0,n_valid))
    # initiate array/dataframe with predictions on test dataset
    if X_test is not None:
        # tst_preds = pd.DataFrame(index=np.arange(0,len(X_test)))
        tst_preds = np.zeros((len(X_test),len(folds))).astype(object)
    else:
        tst_preds = None

    # initialize f1 scores list
    f1scores = []

    # iterate k-fold
    for i, fold in enumerate(tqdm(folds, disable = disable_tdqm)):
        # get data
        X_train, y_train, _    = fold['train']
        X_valid, y_valid, val_ = fold['valid'] # retrieve also validation indexes for oof_preds
        # build model
        model = algorithm(**params)
        # fit model to train data
        model.fit(X_train, y_train)
        # predict on validation fold
        preds = model.predict(X_valid)
        Fscore = f1_score(y_valid, preds, average='micro')
        # store score
        f1scores.append(Fscore)
        # store out of fold predictions
        oof_preds[val_,:]=preds.reshape(-1,1)
        # oof_preds[val_]=preds
        if X_test is not None:
            tst_preds[:,i] = model.predict(fold['scaler'].transform(X_test))

    return f1scores, oof_preds.reshape(1,-1)[0], tst_preds, model



##### Function for running the CV on all selected models #####################
def cv_model_selection(folds, configfile, seed):

    # get total length of validation dataset
    n_valid = 0
    for fold in folds:
        n_valid += fold['valid'][0].shape[0]

    # initialize matrix with cv performances and out of fold predictions
    results = pd.DataFrame(columns=['algorithm','seed','params','f1scores','avg_f1score','time','oof_preds'])

    # cv all model combinations
    k = 0 # row counter
    for alg_name in configfile['algorithm']:
        # get class from string
        algorithm = getattr(sys.modules[__name__], alg_name)
        # create parameter grid for algorithm
        grid = ParameterGrid(configfile['hyperParams'][alg_name])
        # progress update for model
        print('Start cross-validation for ' + str(alg_name))
        num_params = str(len(list(grid)))
        for count, params in  enumerate(grid):
            # progress update for parameter combinations
            print('Parameter combination '+str(count+1) +'/' + num_params )
            # track time
            start_time = time.time()
            # launch cv for single model
            f1scores, oof_preds, _, _ = single_model_cv(folds, algorithm, params,n_valid)
            train_time = time.time()-start_time
            # store results
            results.loc[k] = (alg_name,seed,params,f1scores,np.mean(f1scores),train_time,oof_preds)
            k += 1
    return results

def best_model_selection(configfile, num_seed):
    # initialize matrix for all results
    performance_distribution = pd.DataFrame()
    # load results for each seed from cv files
    for j in range(num_seed):
        results = pd.read_pickle(os.path.join(RESULT_DIR, 'cv_results/cv_results_seed{}'.format(j)))
        performance_distribution = performance_distribution.append(results)
    # final selection of best params combination
    final_models = pd.DataFrame(columns=['algorithm','params', 'median_f1score'])
    algo = performance_distribution.groupby('algorithm')
    for k,(name, group) in enumerate(algo):
        # extract and reshape f1 score for each parameter combination across all seeds
        f1_matrix = np.array(group.avg_f1score).reshape((num_seed, -1))
        # compute median and get index and parameters for best median performance model
        median_best = np.median(f1_matrix, axis=0).max()
        idx_best = median_best.argmax()
        params_best = group.params.iloc[idx_best]
        final_models.loc[k] = (name, params_best, median_best)
    return final_models, performance_distribution

def single_model_cv_and_test(folds,alg_name,params,X_test,y_test,maj_vote='hard'):
    # only hard majority vote implemented; to implement: 'soft' (e.g., with predict proba)
    if maj_vote != 'hard':
        error('Only hard majority vote implemented!')
    # get algorithm
    algorithm = getattr(sys.modules[__name__], alg_name)
    # get total length of validation dataset
    n_valid = 0
    for fold in folds:
        n_valid += fold['valid'][0].shape[0]
    f1scores, oof_preds, fold_tst_preds, model = single_model_cv(folds, algorithm, params,n_valid, X_test, True)
    # majority vote
    tst_preds = fold_tst_preds.max(axis=1)
    return tst_preds, fold_tst_preds, model

def get_confusion_matrix(y_test, y_hat, plot=True):

    # compute normalized confusion matrix
    cmNorm = confusion_matrix(y_test, y_hat, normalize = 'true')

    if plot:
        # Sorting fixturers in decreasing order of event counts
        fixtures,counts = np.unique(y_test, return_counts=True)
        count_sort_ind = np.argsort(-counts)

        # create figure
        fig, ax = plt.subplots(1,figsize=(8,7))
        # create  and plot confusion matrix

        heatmap = sns.heatmap(cmNorm[:, count_sort_ind][count_sort_ind], annot=True, fmt=".0%", cmap="Blues", ax=ax)
        heatmap.yaxis.set_ticklabels(fixtures[count_sort_ind], rotation=0, ha='right', fontsize=12)
        heatmap.xaxis.set_ticklabels(fixtures[count_sort_ind], rotation=45, ha='right', fontsize=12)
        ax.set_ylabel('True label', fontsize=14)
        ax.set_xlabel('Predicted label', fontsize=14)
        b, t = ax.set_ylim() # discover the values for bottom and top
        b += 0.5 # Add 0.5 to the bottom
        t -= 0.5 # Subtract 0.5 from the top
        ax.set_ylim(b, t) # update the ylim(bottom, top) values

    return cmNorm, ax

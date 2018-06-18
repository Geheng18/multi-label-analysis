from graphcnn.helper import *
import scipy.io
import numpy as np
import datetime
import graphcnn.setup.helper
import graphcnn.setup as setup
from skmultilearn.problem_transform import LabelPowerset # to help determine class_weights


def load_ucmerced_dataset():

    dataset = scipy.io.loadmat('dataset/new_dataset.mat')
    dataset = dataset['new_dataset']
    # nodes = np.squeeze(dataset['nodes'])
    edges = np.squeeze(dataset['edges'])
    index = np.squeeze(dataset['index']) 
    classes = np.squeeze(dataset['class']) # try class or classes
    # features = np.squeeze(dataset['features'])
    # print np.size(features)
    #loading features in which NaN have been replaced
    features = scipy.io.loadmat('dataset/features.mat')
    features = features['features']
    features = features['val']
    features = features[0]
    for i in range(0,len(features)):
        if np.isnan(features[i]).any() == True:
            print('features %d have NaN:'% i,np.isnan(features[i]).any())

    labels = scipy.io.loadmat('dataset/UCMERCED/multilabels/LandUse_multilabels.mat')
    labels = labels['labels']
    labels = np.transpose(labels,(1,0))
    
    # Calculating class weights
    lp = LabelPowerset()
    trans_labels = lp.transform(labels)
    unique, counts = np.unique(trans_labels, return_counts=True)
    class_freq = 1.0 / counts
    weight_mat = np.zeros((np.shape(trans_labels)))
    for i in range(len(weight_mat)):
        weight_mat[i] = class_freq[np.where(trans_labels[i]==unique)]
        
    # Calculating label weights
    sum_labels = np.sum(labels, axis=0, dtype=np.float32)
    sum_tot = np.sum(sum_labels, dtype=np.float32)
    label_freq = np.true_divide(sum_labels, sum_tot)
    
    return features, edges, labels, weight_mat, label_freq, index, classes

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 17:51:46 2018

@author: maggie
"""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

  
def create_user_vector(interests, dict_num2urlkey, df_sparse):
    """
    Creates vector of user entered interests.
    
    Input:
    """
    dict_urlkeys = {y:x for x,y in dict_num2urlkey.items()}
    interests_keyed = pd.Series(interests).apply(lambda x:dict_urlkeys[x])
    user_vector = np.zeros((1, df_sparse.shape[1]))
    user_vector[0, interests_keyed.values.astype(int)] = 1
    
    return csr_matrix(user_vector[0])


def calculate_user_similarity_cos_distance(df_sparse, user):
    # returns compressed user-similarity scores calculated by cosine distance
    # df_sparse is a compressed matrix
    sim = df_sparse.dot(user.T)
    user_norm = np.sqrt(user.sum())
    df_sparse_norm = np.sqrt(df_sparse.sum(axis=1))
    user_sim = sim / user_norm / df_sparse_norm
    return csr_matrix(user_sim)


def calculate_hobbies_weighted_average(user_sim, df_sparse):
    """
    Takes in
    user_sim: array of user-similarity scores
    df_sparse: user-item matrix
    
    Computes weighted average for each hobby.
    
    Returns 2 arrays for hobbies:
    hobby_scores_sorted_indices: sorted indices of hobbies
    hobby_scores_sorted: sorted scores of hobby
    Non-zero scores 
    """
    # returns weighted average for each hobby. Nonzero scores only Should be a compressed matrix
    hobby_scores =  user_sim.T.dot(df_sparse) / df_sparse.sum(axis=0)
    hobby_scores = hobby_scores[hobby_scores>0]
    
    # goes into recs function to output names
    hobby_scores_sorted_indices = np.asarray(np.argsort(hobby_scores))[0][::-1]

    # goes into plot to plot scores of each hobby
    hobby_scores_sorted = np.asarray(np.sort(hobby_scores))[0][::-1]
    
    return hobby_scores_sorted_indices, hobby_scores_sorted
    
def return_activities(hobby_scores_sorted_indices, dict_num2urlkey):
    """
    Input:
    hobby_scores_sorted_indices = array of indices of sorted scores
    dict_num2urlkey = dictionary of numeric code to hobby
    
    Returns:
    list of hobby names
    """
    recs = pd.Series(hobby_scores_sorted_indices).apply(lambda x: dict_num2urlkey[str(x)])
    return recs
    
def create_recs(interests, dict_num2urlkey, df_sparse):
    """
    Main function creating recommendations.
    
    Input:
        Interests: list of user interest (from model.py)
        dict_num2urlkey: dictionary of numeric code to hobby
        df_sparse: member database stored as compressed matrix
    Returns:
        recs: Full ranked list of hobbies
        hobby_scores: corresponding scores of hobbies
    """
    user_vector = create_user_vector(interests, dict_num2urlkey, df_sparse)
    user_sim = calculate_user_similarity_cos_distance(df_sparse, user_vector)
    hobby_indices, hobby_scores = calculate_hobbies_weighted_average(user_sim, df_sparse)
    recs = return_activities(hobby_indices, dict_num2urlkey)
    
    return recs, hobby_scores
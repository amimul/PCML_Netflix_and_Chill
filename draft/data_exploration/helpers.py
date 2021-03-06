#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Joachim Muth <joachim.henri.muth@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
import pandas as pd



def load_csv(filename='../data/data_train.csv'):
    df = pd.read_csv(filename)
    df['UserID'] = df['Id'].apply(lambda x: int(x.split('_')[0][1:]))
    df['MovieID'] = df['Id'].apply(lambda x: int(x.split('_')[1][1:]))
    df['Rating'] = df['Prediction']
    df = df.drop(['Id', 'Prediction'], axis=1)
    return df



def recover_original_table(original_df, col_userID, col_movie, col_rate):
    def id(row):
        return 'r' + str(int(row[col_userID])) + '_c' + str(int(row[col_movie]))

    def pred(row):
        return row[col_rate]

    df = pd.DataFrame.copy(original_df)
    df['Id'] = df.apply(id, axis=1)
    df['Prediction'] = df.apply(pred, axis=1)

    return df[['Id', 'Prediction']]


def extract_from_original_table(original_df):
    df = pd.DataFrame.copy(original_df)
    df['UserID'] = df['Id'].apply(lambda x: int(x.split('_')[0][1:]))
    df['MovieID'] = df['Id'].apply(lambda x: int(x.split('_')[1][1:]))
    df['Rating'] = df['Prediction']
    df = df.drop(['Id', 'Prediction'], axis=1)
    return df

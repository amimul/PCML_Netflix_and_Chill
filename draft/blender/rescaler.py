#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Joachim Muth <joachim.henri.muth@gmail.com>
#
# Distributed under terms of the MIT license.
"""
Allow a rescale of the data regarding the user mean, variation and deviation.

BEST: deviation

USE:
    rescaler = Rescaler(df)
    rescaled_train_set = rescaler.normalize_deviation()
    ...
    ... do the ML training which return `predicted_set`...
    ...
    rescaled_test_set = rescaler.recover_deviation(predicted_set)
"""

import numpy as np
import pandas as pd


def dict_mean_user(df):
    return dict(df.groupby('User').mean().Rating)


def dict_var_user(df):
    return dict(df.groupby('User').var().Rating)


def dict_dev_user(df):
    global_mean = df.groupby('User').mean().Rating.mean()
    return dict(df.groupby('User').mean().Rating - global_mean)
    np.mean(list(dict_mean.values()))


class Rescaler:
    def __init__(self, df):
        self.df = df
        self.variances = dict_var_user(df)
        self.means = dict_mean_user(df)
        self.deviation = dict_dev_user(df)

    def normalize(self):
        norm_df = pd.DataFrame.copy(self.df)
        norm_df['Rating'] = self.df.apply(
            lambda x: (x['Rating'] - self.means[x['User']]) / self.variances[x['User']],
            axis=1)

        return norm_df

    def recover(self, df):
        recovered_df = pd.DataFrame.copy(df)
        recovered_df['Rating'] = df.apply(
            lambda x: (x['Rating'] * self.variances[x['User']]) + self.means[x['User']],
            axis=1)

        return recovered_df

    def normalize_only_mean(self):
        norm_df = pd.DataFrame.copy(self.df)
        norm_df['Rating'] = self.df.apply(
            lambda x: x['Rating'] - self.means[x['User']],
            axis=1)

        return norm_df

    def recover_only_mean(self, df):
        recovered_df = pd.DataFrame.copy(df)
        recovered_df['Rating'] = df.apply(
            lambda x: x['Rating'] + self.means[x['User']],
            axis=1)

        return recovered_df

    def normalize_deviation(self):
        norm_df = pd.DataFrame.copy(self.df)
        norm_df['Rating'] = self.df.apply(
            lambda x: x['Rating'] - self.deviation[x['User']],
            axis=1)

        return norm_df

    def recover_deviation(self, df):
        recovered_df = pd.DataFrame.copy(df)
        recovered_df['Rating'] = df.apply(
            lambda x: x['Rating'] + self.deviation[x['User']],
            axis=1)

        return recovered_df
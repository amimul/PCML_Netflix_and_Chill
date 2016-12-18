import pandas as pd
import numpy as np

import random
from sklearn.linear_model import Ridge


def collaborative_filtering(train, test, **arg):
    # Rating of the train set
    rating = train.pivot(index='User', columns='Movie').Rating

    users, movies = rating.index, rating.columns
    Nu, Nm = len(users), len(movies)

    # Number of movie features
    nbr_movie_features = arg['movie_features']

    # Matrix of user preferences
    U = pd.DataFrame(np.random.rand(Nu, nbr_movie_features), index=users, columns=range(1, nbr_movie_features + 1))

    # Matrix of movie features
    M = pd.DataFrame(np.random.rand(Nm, nbr_movie_features), index=movies, columns=range(1, nbr_movie_features + 1))

    U0, M0 = U.copy(), M.copy()

    alpha = arg['alpha']

    bestFit = {'U': U0, 'M': M0, 'error': np.inf}
    fitUM(bestFit, alpha, U0, M0, train, rating, users, movies)

    U_opt, M_opt, error = bestFit['U'], bestFit['M'], bestFit['error']
    pred_mat = predict(U_opt, M_opt)

    pred = []

    df_return = test.copy()

    for i in range(len(test)):
        dd = test.iloc[i]
        val = pred_mat[dd.Movie][dd.User]
        if val > 5:
            val = 5
        elif val < 1:
            val = 1
        pred.append(val)

    df_return.Rating = pred

    return df_return


def rmse_cf(y, yhat):
    err = (y - yhat) ** 2
    return np.sqrt(np.mean(err.mean(skipna=True)))


def fitU(U, M, train, rating, error_history, bestFit, alpha, users):
    """ Fit the user preferences (U) """
    ## Join ratings and movie features
    Udata = train.set_index('Movie').join(M).sort_values('User').set_index('User')
    ## Function for fitting individual users
    model = Ridge(fit_intercept=False, alpha=alpha)

    def Ufit(i):
        df = Udata.ix[i]
        try:
            X = df.drop('Rating', axis=1)
            y = df.Rating
            model.fit(X, y)
            return model.coef_
        except:
            return df

    # Fit all users
    for i in users:
        U.ix[i] = Ufit(i)
    # Calculate the error
    pred = predict(U, M)
    error = rmse_cf(rating, pred)
    error_history.append(error)
    delta = bestFit['error'] - error
    if delta > 0:
        bestFit['U'] = U
        bestFit['M'] = M
        bestFit['error'] = error
    return U, delta


def fitM(U, M, train, rating, error_history, bestFit, alpha, movies):
    """ Fit the movie features (M) """
    # Join ratings and user preferences
    Mdata = train.set_index('User').join(U).sort_values('Movie').set_index('Movie')
    # Function for fitting individual movies
    model = Ridge(fit_intercept=False, alpha=alpha)

    def Mfit(j):
        df = Mdata.ix[j]
        X = df.drop('Rating', axis=1)
        y = df.Rating
        model.fit(X, y)
        return model.coef_

    # Fit all movies
    for j in movies:
        M.ix[j] = Mfit(j)
    # Calculate the error
    pred = predict(U, M)
    error = rmse_cf(rating, pred)
    error_history.append(error)
    delta = bestFit['error'] - error
    if delta > 0:
        bestFit['U'] = U
        bestFit['M'] = M
        bestFit['error'] = error
    return M, delta


def predict(U, M):
    """ Predict the ratings (U dot M) """
    pred = U.dot(M.T)
    pred[pred > 5] = 5
    pred[pred < 1] = 1
    return pred


def fitUM(bestFit, alpha, U0, M0, train, rating, users, movies, tol=0.05):
    """ Repeat the optimization until convergence """
    U, M = U0.copy(), M0.copy()
    error_history = []
    U, delta = fitU(U, M, train, rating, error_history, bestFit, alpha, users)
    tolerance = tol
    while delta > tolerance:
        M, delta = fitM(U, M, train, rating, error_history, bestFit, alpha, movies)
        if delta > tolerance:
            U, delta = fitU(U, M, train, rating, error_history, bestFit, alpha, users)
    return error_history
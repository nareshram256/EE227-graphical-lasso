import numpy as np
from numpy import linalg as LA 

class Lasso2(object):
    
    def __init__(self, alpha, max_iter = 1000, fit_intercept = True):
        self.alpha = alpha 
        self.n_iter_ = None 
        self.coef_ = None 
        self.fit_intercept = fit_intercept 
        self.intercept_ = None
        self.max_iter_ = max_iter
    
    def soft_tresh(self, x, alpha):
        if x < -alpha:
            return x + alpha 
        elif x > alpha: 
            return x - alpha 
        else:
            return 0
    
    def get_objective(self, X, y, beta):
        n = X.shape[0]
        obj = (1/2*n)*(LA.norm(y-np.dot(X,beta)))**2 + self.alpha*LA.norm(beta, ord=1)
        return obj
    
    def fit(self, X, y):
        p = X.shape[1]
        n = X.shape[0]
        
        if self.fit_intercept: 
            X = np.column_stack((np.ones(n), X))
            p = X.shape[1]

        convergence = False
        beta = np.zeros(p)
        
        if self.fit_intercept: 
            beta[0] = np.sum(y - np.dot(X[:, 1:], beta[1:]))/n

        for i in range (self.max_iter_):
            if self.fit_intercept: 
                index = 1
            else:
                index = 0
            
            for j in range(index, p):
                beta_prev = np.copy(beta)
                beta_bar = np.copy(beta)
                beta_bar[j] = 0
                r_j = y - np.dot(X, beta_bar)
                x_j = X[:,j]
                beta[j] = (1/LA.norm(x_j))**2 * self.soft_tresh(np.dot(r_j, x_j), n*self.alpha)
                if self.fit_intercept: 
                    beta[0] = np.sum(y - np.dot(X[:, 1:], beta[1:]))/n
           
            #if np.allclose(beta, beta_prev, rtol = 1e-10) and np.isclose(self.get_objective(X,y,beta), self.get_objective(X,y,beta_prev), rtol=1e-10):
                #break
         
        self.n_iter_ = i
        if self.fit_intercept:
            self.intercept_ = beta[0]
            self.coef_ = beta[1:]
        else:
            self.coef_ = beta    
#!/usr/bin/env python 3 
""" Module d'implémentation des tests statistiques"""

import numpy as np
import scipy.stats as st
import pandas as pd

def affichage_reponse(h0:float, intervalle:tuple, alpha:float)->bool:
    """Affichage et renvoi de la validation du test"""

    print(alpha)
    if intervalle[0] <= h0 <= intervalle[1]:
        res=True
        print(f"{h0:.4f} appartient à l'intervalle {intervalle}")
        print(f"Hypothèse 0 non rejetée avec une confiance de {(1-alpha)*100}%")
    else:
        res=False
        print(f"{h0:.4f} n'appartient pas à l'intervalle {intervalle}")
        print(f"Hypothèse 0 rejetée avec une confiance de {(1-alpha)*100}%")

    return res

def test_stat(x:np.array, n:int, h0:float, alpha=0.05, method='chi2')->bool:
    df = n-1
    if method == 'chi2':
        q2, q1 = st.chi2.ppf(1-alpha/2, df=df), st.chi2.ppf(alpha/2, df=df)
        intervalle = (df*np.std(x, ddof=1)**2/q2, df*np.std(x, ddof=1)**2/q1)
        res = affichage_reponse (np.std(x)**2, intervalle, alpha)

    elif method == 'fisher':
        # q = st.fisher_exact()
        pass
    elif method == 'student':
        q = st.t.ppf(1 - alpha/2, df=df)
        intervalle = (x.mean - np.std(x, ddof=1)*q/np.sqrt(n), \
                      x.mean + np.std(x, ddof=1)*q/np.sqrt(n))
        res = affichage_reponse (x.mean, intervalle, alpha)

    return res

if __name__ == "__main__":
    n = 10
    x1 = np.random.rand(n) + np.random.rand(n)
    x2 = np.random.rand(n)

    test_stat(x1, n, np.std(x2)**2, alpha=0.01)
    print(np.std(x1)**2, np.std(x2)**2)
    pass
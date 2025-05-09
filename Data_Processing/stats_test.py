#!/usr/bin/env python 3 
""" Module d'implémentation des tests statistiques"""

import numpy as np
import scipy.stats as st
# import pandas as pd

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"

def affichage_reponse(theta:float, h0:float, intervalle:list, alpha:float, ineq=None)->bool:
    """Affichage et renvoi de la validation du test"""

    if intervalle[0] <= theta <= intervalle[1]:
        res=True
        print(f"{theta:.4f} appartient à l'intervalle {intervalle}")
        print(f"{GREEN}Hypothèse 0 non rejetée{RESET} avec une confiance de {(1-alpha)*100}%")

    else:
        res=False
        print(f"{theta} est significativement différent de {h0}.")
        print(f"{theta:.4f} n'appartient pas à l'intervalle {intervalle}")
        print(f"{RED}Hypothèse 0 rejetée{RESET} avec une confiance de {(1-alpha)*100}%")

    return res

def test_bilateral_stat(x, n:int, h0:float, alpha=0.05, method='chi2')->bool:
    """Effectue un test statistique sur x avec H0 : var(x) = h0 ou moy(x) = h0"""
    df = n-1
    if method == 'chi2':
        A = st.chi2.ppf(1 - alpha/2, df=df)
        B = st.chi2.ppf(alpha/2, df=df)
        intervalle = [A, B]
        res = affichage_reponse (df/h0 * np.var(x, ddof=1), h0, intervalle, alpha)

    elif method == 'fisher':
        A = st.f.ppf(alpha/2, df, df)
        B = 1/A
        intervalle = [A, B]
        res = affichage_reponse(np.var(x, ddof=1), h0, intervalle, alpha)

    elif method == 'student':
        q = st.t.ppf(1 - alpha/2, df=df)
        intervalle = (x.mean - np.std(x, ddof=1)*q/np.sqrt(n), \
                      x.mean + np.std(x, ddof=1)*q/np.sqrt(n))
        res = affichage_reponse (np.mean(x), h0, intervalle, alpha)

    return res

if __name__ == "__main__":
    n = 10
    x1 = np.array([18.5, 24.5, 11, 2.5, 5.5, 3.5])
    x2 = np.array([10.5, 19.5, 7.5, 4, 4.5, 2])

    S1 = 1/n*2260-(1/n*150)**2
    S2 = 1/n*1974-(1/n*140)**2
    
    test_bilateral_stat(S1/S2, n, S2, alpha=0.05, method='fisher')
    print(S1, S2)
    print((n*S1+n*S2)/(2*n-2))
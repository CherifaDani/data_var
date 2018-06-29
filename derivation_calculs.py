# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd


def apply_operation(var_list, freq, operation, parameters):
    """
    Function used to derive dataframes
 
    Parameters
    ----------
    var_list : {Objects list type}
                A list of variables (objects)
 
    freq : {Char type}
            The frequecy of the Series,
            default: 'B'
 
    operation : {String type}
                The derivation to apply to the var_list
 
    parameters : {Dict type}
                 The parameters of the derivation

    Return
    ------
    fdf : {Dataframe type}
            full dataframes,
            Can be none if operation not found
    """
    fdf = pd.DataFrame()

    if operation == 'timeshift':
        mult = parameters['mult']
        # f = lambda x: (x.read_var(x.get_param('path')))
        # f = lambda x: read_df(x)
        # dfs = map(f, var_list)
        dfs = map(lambda x: read_df(x), var_list)
        fdf = []
        for _, df in enumerate(dfs):
            df_calc = apply_timeshift(df, freq, mult)
            fdf.append(df_calc)
 
        return fdf
 
    if operation == 'corr':
        # df_calc = apply_corr(df)
        dfs = map(lambda x: read_df(x), var_list)
        fdf = dfs[0] + dfs[1]
        #=======================================================================
        # fdf = []
        # for _, df in enumerate(dfs):
        #     df_calc = df * 55
        #     fdf.append(df_calc)
        #=======================================================================
        return fdf
        #===================================================================
            # f = lambda x, y: (x.read_var(x.get_param('path')) * )
            # dfs = map(f, var_list)
            # df_calc = map(lambda x, y: x*y, var_list)
            #===================================================================


def apply_timeshift(df, freq, mult, shift=0):
        """
        Renvoie une copie de l'objet courant, avec dates translatées
        d'un délai.
        Les noms de colonnes de l'objet courant ne sont pas modifiés.
        freq représente l''unité de compte du décalage
        ownfreq représente la fréquence finale(propre) de la série.
        refdate: date de calcul. si fournie, les décalages sont limités
        à cette date
        Exemple: décaler de 20j une série trimestrielle
        """
        # Shiffting with a given shift
        ndf = df.tshift(shift, freq)
        # Multiplication by mult
        ndf = ndf * mult
        return ndf


def read_df(x):
    return x.read_var(x.get_param('path'))


def apply_corr(df,  period=1, span=20, exponential=True, inpct=True, lag=0):
    '''Renvoie la série des corrélations entre deux colonnes d'un Dataset
           period: si 0, corrélation des valeurs, si > 0, corrélation des 
           variations sur period
           lag: retard sur la seconde colonne
           cols: spécifications de 1 ou 2 colonnes
        '''
    startval = period + lag * period
    cols = df.columns
    if len(cols) == 1:
        col1 = cols[0]
        col2 = col1
    else:
        col1 = cols[0]
        col2 = cols[1]

        if period == 0:
            data1 = df[col1]
            data2 = df[col2].shift(periods=lag)
        else:
            if inpct:
                data1 = df[col1].pct_change(period)[startval:]
                data2 = df[col2].pct_change(period).shift(
                    periods=lag * period)[startval:]
            else:
                data1 = df[col1].diff(period)[startval:]
                data2 = df[col2].diff(period).shift(
                    periods=lag * period)[startval:]

        if exponential:
            corrdata = pd.ewmcorr(data1[startval:],
                                  data2[startval:], span=span)
        else:
            corrdata = pd.rolling_corr(data1, data2, window=span)

        return corrdata









#===============================================================================
# 
# 
# 
# 
# path = '/home/cluster/git/data_v2/2 Data/1 Received/Market data/Base/FDFD_Index_LAST_PRICE.csv'
# var_name = 'FI_STR_USD_1D_LAST'
# df= data_utils.load_var(path=path, var_name=var_name)
# # print df.head(5)
#===============================================================================


































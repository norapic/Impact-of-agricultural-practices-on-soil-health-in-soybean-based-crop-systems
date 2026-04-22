import pandas as pd
import numpy as np
import scipy.stats as stats
import scikit_posthocs as sp

def global_test(df, trait, factor):
    """ Perform a global test (Anova or Kruskal-Wallis) test if the trait of interest
    is significantly different between the different groups of the factor of interest """
    ## Results to return
    res = {}
    ## Shapiro : Null hypothesis : The weights were drawn from a normal distribution
    shapiro_test = stats.shapiro(df[trait])

    ## Bartlett : Null hypothesis : All input samples are from populations with equal variances.
    list_inputs = [np.array(df.loc[df[factor] == val, trait]) for val in df[factor].unique()]

    barlett_test = stats.bartlett(*list_inputs) #En Python, * devant une liste signifie "déballer" cette liste en arguments séparés.

    ## Global test : Anova or Krukal-Wallis
    if (shapiro_test.pvalue <= 0.05) and (barlett_test.pvalue <= 0.05):
        # Kruskal-Wallis : Null hypothesis the population median of all of the groups are equal
        kruskal_test = stats.kruskal(*list_inputs)
        res['pvalue'] = kruskal_test.pvalue
    else:
        # Anova : Null hypothesis : The means of the groups are all equal
        anova_test = stats.f_oneway(*list_inputs)
        res['pvalue'] = anova_test.pvalue
    return res

def pval_interp(pval):
    """ Interpret the p-value of a test with conventions """
    if pval <= 0.05 and pval > 0.01:
        interp = "*"
    if pval <= 0.01 and pval > 0.001:
        interp = "**"
    if pval <= 0.001:
        interp = "***"
    else:
        interp = "ns"
    return interp

def post_hoc_test(df, trait, factor):
    """ Perform a post-hoc test (Tukey or Dunn) to compare the trait of interest between
    the different groups of the factor of interest """
    ## Results to return
    res = {}
    ## Shapiro : Null hypothesis : The weights were drawn from a normal distribution
    shapiro_test = stats.shapiro(df[trait])

    ## Bartlett : Null hypothesis : All input samples are from populations with equal variances.
    list_inputs = [np.array(df.loc[df[factor] == val, trait]) for val in df[factor].unique()]

    barlett_test = stats.bartlett(*list_inputs) #En Python, * devant une liste signifie "déballer" cette liste en arguments séparés.

    ## Global test : Anova or Krukal-Wallis
    if (shapiro_test.pvalue <= 0.05) and (barlett_test.pvalue <= 0.05):
        # Dunn test
        dunn_test = sp.posthoc_dunn(df, val_col=trait, group_col=factor, p_adjust='bonferroni')
        res = dunn_test
    else:
        # Tukey’s HSD test for equality of means over multiple treatments.
        tukey_test = sp.posthoc_tukey(df, val_col=trait, group_col=factor)
        res = tukey_test
    return res
    
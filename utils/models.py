import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

def fit_mixed_linear_model(df, trait, fixed_effects, random_effects, nested_random_effects=None):
    """ Fit a mixed effects model to the data and return the results of the model """
    # Create the formula for the fixed effects
    formula = f"{trait} ~ {fixed_effects}"
    
    # Fit the mixed effects model
    model = smf.mixedlm(formula, df, groups=df[random_effects])
    if (nested_random_effects is not None):
        model = smf.mixedlm(formula, df, groups=df[random_effects],
                            re_formula=f"~{nested_random_effects}")

    result = model.fit()
    
    return result

def fit_generalized_linear_model(df, trait, fixed_effects, random_effects, family, nested_random_effects=None):
    """ Fit a generalized linear model to the data and return the results of the model """
    # Create the formula for the fixed effects
    formula = f"{trait} ~ {fixed_effects}"
    
    # Fit the generalized linear model
    glm_model = sm.GLM.from_formula(formula, data=df, groups=df[random_effects],family=family)
    if (nested_random_effects is not None):
        glm_model = sm.GLM.from_formula(formula,
                                        data=df, groups=df[random_effects],
                                        re_formula=f"~{nested_random_effects}",
                                        family=family)
    results = glm_model.fit()
    
    return results

import plotly.express as px
import pandas as pd

def histogram_trait(df, trait):
    """ Plot an histogram of the trait if interest"""
    fig_hist = px.histogram(df, x=trait, title=f"Distribution of {trait}")
    return fig_hist

def boxplots_trait_factor(df, trait, factor):
    """ Make boxplots of the trait of interest depending on the groups of the factor of interest"""
    fig_box = px.box(df, y=trait, x=factor,
                      title=f"Boxplots of {trait} depending on {factor}",
                      color=factor)
    return fig_box

import pandas as pd
import json
import pickle
import numpy as np


def pickle_data(d):
    pickle_out = open("hops_data.pickle","wb")
    pickle.dump(d, pickle_out)
    pickle_out.close()

def get_data():
    pickle_in = open("/home/hops/mysite/hops_data.pickle","rb")
    df = pickle.load(pickle_in)
    #df = read_json()
    #df = add_avg_column(df)
    return df

def get_styles_data(sort_by="name", ascending=True):
    pickle_in = open("/home/hops/mysite/beer_styles_data.pickle","rb")
    df = pickle.load(pickle_in)
    df_sorted = get_style_sorted_data(df, sort_by, ascending)
    return df_sorted

def add_avg_column(df):
    df["AlphaAvg"] = round(((df["AlphaMin"] + df["AlphaMax"]) / 2),2)
    df["BetaAvg"] = round(((df["BetaMin"] + df["BetaMax"]) / 2), 2)
    return df

def add_bugu_column(df):
    df["bugu"] = round(df["ibu"]/((df["og"]-1)*1000), 2)
    return df

def calc_ibu(ounces, alpha, minutes):
    ibu = round((ounces * alpha * calc_percent_util(minutes) / 7.25),2)
    return ibu

def get_styles_values_only():
    df = get_styles_data()
    df.dropna(inplace=True)
    return df


def calc_percent_util(min):
    percent_util = 0
    if min <= 5:
        percent_util = 5
    elif min <= 10:
        percent_util = 6
    elif min <= 15:
        percent_util = 8
    elif min <= 20:
        percent_util = 10.1
    elif min <= 25:
        percent_util = 12.1
    elif min <= 30:
        percent_util = 15.3
    elif min <= 35:
        percent_util = 18.8
    elif min <= 40:
        percent_util = 22.8
    elif min <= 45:
        percent_util = 26.9
    elif min <= 50:
        percent_util = 28.1
    elif min <= 60:
        percent_util = 30
    elif min >= 60:
        percent_util = 31

    return percent_util

def calc_bugu(ibu, og):
    bugu = ibu / og
    return bugu

def make_styles_list(df):
    styles_list = []
    for row in df['Styles']:
        if row is None:
            row = []
        if row not in styles_list:
            styles_list.append(row)

    return styles_list

def process_styles_list(list):
    for item in list:
        str(item)
        item = item.strip("\n")
    return list

def get_hops_name_list(df):
    hop_names = df["Name"].to_list()
    return hop_names

def get_sort(arg, df):
    sorted_df = df
    if arg == "alpha_ascending":
        sorted_df = sort_data_by(df, "AlphaAvg", True)
    if arg == "alpha_descending":
        sorted_df = sort_data_by(df, "AlphaAvg", False)
    if arg == "beta_ascending":
        sorted_df = sort_data_by(df, "BetaAvg", True)
    if arg == "beta_descending":
        sorted_df = sort_data_by(df, "BetaAvg", False)
    if arg == "Name":
        sorted_df = sort_data_by(df, "Name", True)

    return sorted_df

def get_style_sorted_data(df, col, ascending):
    sorted_df = sort_data_by(df, col, ascending)
    return sorted_df

def sort_data_by(df, name, ascending):
    sorted_df = df.sort_values(by=[name], ascending=ascending)
    return sorted_df



def format_numbers():
    df = get_data()
    df.style.format("{:.2f}")
    pickle_data(df)

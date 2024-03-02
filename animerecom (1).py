# -*- coding: utf-8 -*-
"""AnimeRecom.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NDsfoUiaMehPLka5MkR6S6smbbiv9F3S
"""

# Commented out IPython magic to ensure Python compatibility.
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
# %matplotlib inline

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

anime = pd.read_csv("anime.csv")

anime.head(25)

anime[anime['episodes']=='Unknown'].head(3)

anime.loc[(anime["genre"]=="Hentai") & (anime["episodes"]=="Unknown"),"episodes"] = "1"
anime.loc[(anime["type"]=="OVA") & (anime["episodes"]=="Unknown"),"episodes"] = "1"

anime.loc[(anime["type"] == "Movie") & (anime["episodes"] == "Unknown")] = "1"
known_animes = {"Naruto Shippuuden":500, "One Piece":784,"Detective Conan":854, "Dragon Ball Super":86,
                "Crayon Shin chan":942, "Yu Gi Oh Arc V":148,"Shingeki no Kyojin Season 2":25,
                "Boku no Hero Academia 2nd Season":25,"Little Witch Academia TV":25}

for k,v in known_animes.items():
    anime.loc[anime["name"]==k,"episodes"] = v

anime["episodes"] = anime["episodes"].map(lambda x:np.nan if x=="Unknown" else x)

anime["episodes"].fillna(anime["episodes"].median(),inplace = True)

pd.get_dummies(anime[["type"]]).head()

anime["rating"] = anime["rating"].astype(float)
anime["rating"].fillna(anime["rating"].median(),inplace = True)
anime["members"] = anime["members"].astype(float)

anime_features = pd.concat([anime["genre"].str.get_dummies(sep=","),
                            pd.get_dummies(anime[["type"]]),
                            anime[["rating"]],anime[["members"]],anime["episodes"]],axis=1)
anime["name"] = anime["name"].map(lambda name:re.sub('[^A-Za-z0-9]+', " ", name))
anime_features.head()

anime_features.columns

from sklearn.preprocessing import MinMaxScaler

min_max_scaler = MinMaxScaler()
anime_features = min_max_scaler.fit_transform(anime_features)
np.round(anime_features,2)

from sklearn.neighbors import NearestNeighbors

nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(anime_features)

distances, indices = nbrs.kneighbors(anime_features)

def get_index_from_name(name):
    return anime[anime["name"]==name].index.tolist()[0]

all_anime_names = list(anime.name.values)

def get_id_from_partial_name(partial):
    for name in all_anime_names:
        if partial in name:
            print(name,all_anime_names.index(name))

def print_similar_animes(query):
  
  '''  if id == "":'''
  found_id = get_index_from_name(query)
  for id in indices[found_id][1:]:
        print(anime.loc[id]["name"])



print_similar_animes(query="Naruto")


print_similar_animes("Noragami")

print_similar_animes("Death Note")

print_similar_animes("Gintama")



'''pickle.dump(nbrs, open("model.pkl", "wb"))'''

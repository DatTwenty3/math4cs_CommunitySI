import random

import pandas as pd
import csv
import os
import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
import time

from networkx.algorithms.community import girvan_newman

RUN_STEP =1

# Read the Excel file into a DataFrame
#df = pd.read_csv('dataset/studentInfo.csv')
#df = pd.read_csv('dataset/studentInfo_20.csv')
#df = pd.read_csv('dataset/studentInfo_50.csv')
#df = pd.read_csv('dataset/studentInfo_80.csv')
df = pd.read_csv('dataset/studentInfo_100.csv')
#df = pd.read_csv('dataset/studentInfo_300.csv')
#df = pd.read_csv('dataset/studentInfo_500.csv')
#df = pd.read_csv('dataset/studentInfo_1000.csv')

print("==Begin build graph>>")

G = nx.Graph()
#G = nx.karate_club_graph()
# Display the contents of the DataFrame
#print(df.columns)
for index, row in df.iterrows():
    for index2, row2 in df.iterrows():
        # Access row data using column names or indices
        #print(f"Row[{index}] :", row.values)
        #print(f"Row[{index}] :", row['code_module'])
        #print(f"Row[{index}] ")
        if ((row['code_module'] == row2['code_module'])
                and (row['id_student'] != row2['id_student'])
                and (G.has_edge(row['id_student'], row2['id_student']) == False)):
            #print(f"id_student:{row['id_student']}", f"id_student2:{row2['id_student']}")
            G.add_edge(row['id_student'], row2['id_student'])




#nx.draw(G, with_labels=True, font_weight='bold')
print("==>Finished build graph>>")
print("==>Begin run girvan_newman>>")

# Apply Girvan-Newman algorithm to detect communities
comp = girvan_newman(G)

print("==>Finished run girvan_newman")
draw_community_step = 0
communitiesList = []

for communities_at_step in comp:
    if draw_community_step == RUN_STEP:
        communitiesList.append(tuple(c for c in communities_at_step))
        break
    print("==> process communities_at_step", draw_community_step, f", RUN_STEP: {RUN_STEP}")

    draw_community_step = draw_community_step + 1

# Get the first set of communities

print( f" ==>draw_community_step{RUN_STEP}")
print(f"==>length of community {len(communitiesList[0])}")

# Create a mapping of nodes to their community index
community_colors = ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(10000)]

default_color = 'black'
node_colors = {node: default_color for node in G.nodes()}
for  i, com1 in enumerate(communitiesList):
    for idx, com1 in enumerate(com1):
        for  node in com1:
            node_colors[node] = community_colors[idx]

# Draw the graph, coloring nodes based on communities
pos = nx.spring_layout(G, k=1)
nx.draw(G, pos, node_color=[node_colors[node] for node in G.nodes()], with_labels=True, cmap=plt.cm.jet)
plt.show()
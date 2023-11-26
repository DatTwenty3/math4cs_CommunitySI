import csv
import os
import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain

def browse_files():
    filename = filedialog.askopenfilename(initialdir="data_csv", title="Chọn file CSV",
                                          filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if filename:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames

            if fieldnames is None:
                raise ValueError("Không có trường có tên trong file CSV")

            G = nx.Graph()

            for row in reader:
                if all(row.get(field) for field in fieldnames):
                    for i in range(len(fieldnames) - 1):
                        if row[fieldnames[i]] and row[fieldnames[i + 1]]:
                            G.add_edge(row[fieldnames[i]], row[fieldnames[i + 1]])

            partition = community_louvain.best_partition(G)

            unique_clusters = set(partition.values())
            cluster_colors = plt.cm.tab10.colors[:len(unique_clusters)]

            cluster_color_mapping = {cluster: color for cluster, color in zip(unique_clusters, cluster_colors)}

            colors = [cluster_color_mapping[partition[n]] for n in G.nodes()]

            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(G)

            nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=500)
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
            nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

            graph_window = plt.get_current_fig_manager().window
            graph_window.title(f"Đồ thị mối liên hệ - {os.path.basename(filename)}")

            plt.title(f"Đồ thị thể hiện các mối liên hệ cho file {os.path.basename(filename)}")
            plt.tight_layout()
            plt.show()

root = tk.Tk()
root.title("Tạo đồ thị mối liên hệ")

root.geometry("300x100")

frame = tk.Frame(root)
frame.pack(expand=True)

button = tk.Button(frame, text="Chọn file CSV", command=browse_files)
button.pack(expand=True)

root.mainloop()
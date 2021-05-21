'''
# Instructions

To run the script follow these steps:
1. clone the repository: git clone https://github.com/JakubR12/cds-language.git
2. navigate to the newly created repository
3. create a virtual environment: bash create_network_venv.sh
4. activate the virtual environment: source network_venv/bin/activate
5. go to the src folder: cd src
6  run the script: python network_analysis.py

There are 6 arguments which can but do not have to be specified (the default option is the Trump tweet data):

flags: -i, --input_file,   default: ../data/raw/edges_df.csv,                              description: str, path to the input_file,
flags: -o, --output_file:  default: ../data/processed/measures_of_centrality.csv,            description: str, path to output_file
flags: -t, --threshold:    default: 500,                                                   description: int, the minimum weight threshold
flags: -l, --graph_labels: default: False,                                                 description: bool, whether to plot labels or not
flags: -p, --plot_network: default: False,                                                 description: bool, whether to plot  the network or not
flags: -pf, --plot_file:   default: ../report/figures/network_visualization.png,           description: str, path to plot_file



examples:
  python network_analysis.py -p -l -t 1500 -pf ../reports/figures/network_visualization_threshold_1500.png
  
  When using boolean flags, just leave them empty.

'''
# import libraries
import  os #for paths
import pandas as pd #for dataframes
import argparse #for getting arguments from terminal
import networkx as nx #for network stuff
import matplotlib.pyplot as plt #for plot stuff
import matplotlib
matplotlib.use("Agg")


# defining main function with 6 optional arguments with default options
## default optios are set twice to increase generalizability as argparse enables to set default when calling from a command line, while defining defaults again 
## withing the main funciton allows the function to have default values when using the script as a module in a python session.
def main(
  input_file = os.path.join("..", "data", "raw", "edges_df.csv"), 
         output_file = os.path.join("..", "data", "processed","measures_of_centrality.csv"),
         threshold = 500, 
         graph_labels = False,
         plot_network = False,
         plot_file= os.path.join("..", "reports", "figures", "network_visualization.png")):

  '''
  A function to load a weighted edgelist as a csv - wile with the columns "nodeA", "nodeB", and "weight".
  The function calculates measures of network centrality and and can optionally plot the network.
  
  Input:
    input_file,   default: ../data/raw/edges_df.csv,                              description: str, path to the input_file,
    output_file:  default: ../data/processed/measures_of_centrality.csv,            description: str, path to output_file
    threshold:    default: 500,                                                   description: int, the minimum weight threshold
    graph_labels: default: False,                                                 description: bool, whether to plot labels or not
    plot_network: default: False,                                                 description: bool, whether to plot  the network or not
    plot_file:    default: ../reports/figures/network_visualization.png,          description: str, path to plot_file
    
  Output:
    a saved image of the network plotted with networkx (optional)
    a csv-file of centrality measures for each node. columns: degree, betweenness, and eigenvector
    
  '''

  # reading the data 
  data = pd.read_csv(input_file)
  print(f"{input_file} has succesfully been read")
    
    
  # filtering based on the set threshold
  filtered_df= data[data["weight"] > threshold]
    
  # calculating G
  G = nx.from_pandas_edgelist(filtered_df, "nodeA", "nodeB", ["weight"])
  
  # plotting a network
  if plot_network == True:  
      
      pos = nx.nx_agraph.graphviz_layout(G, prog = "neato")
      # draw, use matplot lib draw...
      nx.draw(G, pos, with_labels = graph_labels, node_size = 20, font_size = 10)
      plt.savefig(plot_file, dpi=300, bbox_inches="tight")
      print(f"{plot_file} has succesfully been saved")
    
    

  # creating df for centrality measures
  centrality_df = pd.DataFrame()
  
  # calculating centrality measures
  
  ## degree centrality
  deg = nx.degree_centrality(G)
 
  ## eigenvector
  ev = nx.eigenvector_centrality(G)

  ## betweenness
  bc = nx.betweenness_centrality(G)
  
  # gathering measures into dictionary
  centrality_df= {"node":deg.keys(),"degree":deg.values(),"betweenness":bc.values(),"eigenvector":ev.values()}
  
  # forming a data frame out of the dictionary
  centrality_df= pd.DataFrame(data =centrality_df)
    
  # saving the data frame
  centrality_df.to_csv(output_file)
  print(f"{output_file} has succesfully been saved")
    
  # defining behavior for when the script is run from the terminal
if __name__ =="__main__":
    
    # We argparse to add possible inputs from terminal
    ap = argparse.ArgumentParser(description = "[INFO] Calculating network metrics and plotting network from an edgelist")
    
    ap.add_argument("-i", "--input_file", default = os.path.join("..", "data", "raw", "edges_df.csv"),
                    type = str, help = "str,path to input_file")
        
    ap.add_argument("-o", "--output_file",default = os.path.join("..", "data", "processed", "measures_of_centrality.csv"),
                    type = str, help = "str, path to output_file")
    
    ap.add_argument("-t", "--threshold", default = 500, type = int, help = "int, the minimum weight threshold")
    
    ap.add_argument("-l", "--graph_labels", default = False ,nargs = "?",const = True,
                    type = bool, help = "bool, whether to plot labels or not") #nargs and const are used for the boolean swithces to work
    
    ap.add_argument("-p", "--plot_network", type = bool, default = False, nargs = "?",
                    const = True, help = "bool, whether to plot  the network or not")
    
    ap.add_argument("-pf", "--plot_file", default = os.path.join("..", "reports", "figures","network_visualization.png"),
                    type = str, help = "str, path to plot_file")
    
    args = vars(ap.parse_args())

    main(
      args["input_file"],
      args["output_file"],
      args["threshold"],
      args["graph_labels"],
      args["plot_network"],
      args["plot_file"])
      

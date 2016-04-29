import matplotlib.pyplot as plt
import numpy as np

def map_step_to_index(Step):
    mapping_dict = {'C': 0, 'C#': 1, 'D':2 ,'D#':3 , 'E':4 ,'F':5 ,'F#':6 ,'G':7 , 'G#':8 , 'A':9 , 'A#':10 , 'B': 11}
    return mapping_dict[Step]




def pretty_scatter(values, legend, output):

    scatter_dict = {}

    fig = plt.figure()

    for i in range(len(legend)):
        if legend[i] in scatter_dict:
            scatter_dict[legend[i]].append(values[i])
        else: 
            scatter_dict[legend[i]] = [values[i]]

    text = iter(scatter_dict.keys())

    plot_list = []
    for key in scatter_dict.keys():
        
        X = [x[0] for x in scatter_dict[key]]
        y = [x[1] for x in scatter_dict[key]]

        plot_list.append(plt.scatter(X,y, color=np.random.rand(3) ))

    plt.legend(plot_list,scatter_dict.keys(),scatterpoints=1,
           loc='upper center',
           ncol=5,
           fontsize=5)

    plt.savefig(output)
        
        



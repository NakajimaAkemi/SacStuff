import matplotlib.pyplot as plt
import numpy as np
sumfile = lambda f: np.sum(np.loadtxt(f)[:, 1])
interfile = lambda f, n: np.loadtxt(f)[n, 0]
normalize = lambda f: 1.0 / (sumfile(f) * interfile(f, 2))


colors = ['C1', 'C2', 'C3', 'C4', 'C5']
labels = [r'Srv1', r'Srv2']


def make_plot(infiles, outfile):
    data_files=infiles
    normalized_data = []
    for f in data_files:
        data = np.loadtxt(f)
        sum_f = np.sum(data[:, 1])# sum of values
        inter = data[2, 0] # inter-bin itnerval
        norm_factor = 1.0 / (sum_f * inter)
        normalized_data.append((data, norm_factor))
    plt.figure(figsize=(10, 6))
    for i, (data, norm_factor) in enumerate(normalized_data):
        x = data[:, 0]
        y = data[:, 1] * norm_factor
        plt.plot(x, y, label=labels[i], color=colors[i % len(colors)])
    plt.xlabel('Response Time [s]', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend(loc='upper right')
    plt.savefig(outfile, dpi=300, bbox_inches='tight')



if __name__ == '__main__':
    make_plot(["results/MM1_LB_Unbalanced_Source_NOBAL1.data", 
              "results/MM1_LB_Unbalanced_Source_NOBAL2.data"],
              "MM1_LB_Unbalanced_SourceNOBAL.png")
    make_plot(["results/MM1_LB_Unbalanced_Source1.data", 
               "results/MM1_LB_Unbalanced_Source2.data"],
              "MM1_LB_Unbalanced_Source.png")
    make_plot(["results/MM1_LB_Unbalanced_Processing1.data", 
               "results/MM1_LB_Unbalanced_Processing2.data"],
              "MM1_LB_Unbalanced_Processing.png")
    make_plot(["results/MM1_LB_Unbalanced_Processing_Bal1.data", 
               "results/MM1_LB_Unbalanced_Processing_Bal2.data"],
              "MM1_LB_Unbalanced_Processing_Bal.png")
    make_plot(["results/MM1_LB_Unbalanced_Processing_BalSQ1.data", 
               "results/MM1_LB_Unbalanced_Processing_BalSQ2.data"],
              "MM1_LB_Unbalanced_Processing_BalSQ.png")
import matplotlib.pyplot as plt


def plot_graph(data):
    plt.bar(data.keys(), [int(x['total_time'].second()) for x in data.values()])
    plt.xticks(range(len(data.keys())), data.keys(), rotation=90, fontsize=3)
    plt.xlabel('Names')
    plt.ylabel('Total online time(hrs)')
    plt.title('Online status')
    plt.tight_layout()
    plt.savefig('temp.png')
    plt.clf()

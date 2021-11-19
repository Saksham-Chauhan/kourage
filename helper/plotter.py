import matplotlib.pyplot as plt


def plot_presence_graph(data):
    plt.bar(data.keys(), [int(x['total_time'].second()) for x in data.values()])
    plt.xticks(range(len(data.keys())), data.keys(), rotation=90, fontsize=3)
    plt.xlabel('Names')
    plt.ylabel('Total online time(hrs)')
    plt.title('Online status')
    plt.tight_layout()
    plt.savefig('presence_data.png')
    plt.clf()


def plot_sentiment_graph(data, score, analysis):
    data['compound'] = score.compound.apply(analysis)
    df = data.groupby(['author', 'compound']).size().unstack(fill_value=0)
    df1 = df.iloc[:, 0:].apply(lambda x: x.div(x.sum()).mul(100), axis=1).astype(int)
    df1.plot(kind='bar')
    plt.xticks(range(len(df1.index)), df1.index, rotation=90)
    plt.xlabel("Names")
    plt.ylabel("Percentage")
    plt.tight_layout()
    plt.savefig('sentiment_data.png')
    plt.clf()
    return

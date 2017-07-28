
import matplotlib.pyplot as plt

class Graph():
    def __init__(self, title):
        self.fig1 = plt.figure(figsize=(10, 4))
        plt.grid(b=True, which='both', color='0.65', linestyle='-')
        plt.style.use('seaborn-muted')
        plt.title(title)

        pass

    def addLine(self, df, col_name, color):
        plt.plot(df.index, df[col_name], color, markersize=4)
        #plt.plot_date(x=days, y=impressions)

    def show(self):
        plt.show()
        plt.close()




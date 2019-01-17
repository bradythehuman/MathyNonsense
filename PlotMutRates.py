import plotly.graph_objs as go
import plotly.io as pio
import plotly.plotly as py
import csv


class MrDataManager:
    def __init__(self):
        self.datas = {}

    def add(self, transformNum, label, mr, lower, upper):
        if transformNum not in self.datas.keys():
            self.datas[transformNum] = MrDataBlock()
        self.datas[transformNum].add(label, mr, lower, upper)

    def getKeys(self):
        return self.datas.keys()

    def getMrDataBlock(self, key):
        return self.datas[key]


class MrDataBlock:
    def __init__(self):
        self.label = []
        self.mr = []
        self.lower = []
        self.upper = []

    def add(self, label, mr, lower, upper):
        self.label.append(label)
        self.mr.append(float(mr))
        self.lower.append(float(lower))
        self.upper.append(float(upper))


def makePlot(mrDataBlock, strain):
    data = [go.Bar(
        x=mrDataBlock.label,
        y=mrDataBlock.mr,
        error_y = dict(
            type='data',
            symmetric=False,
            array=mrDataBlock.upper,
            arrayminus=mrDataBlock.lower
        )
    )]

    layout = go.Layout(yaxis=dict(type='log', autorange=True, exponentformat='e', showexponent='all'))
    fig = go.Figure(data=data, layout=layout)
    # pio.write_image(fig, "C:\\Users\\Brady Hearn\\Documents\\mutationrates" + strain + ".png")
    py.plot(fig, filename=strain)


mrData = MrDataManager()

file = "C:\\Users\\Brady Hearn\\Documents\\mutationrates\\l439vdata.csv"
with open(file, 'r') as fObj:
    fileData = csv.reader(fObj, delimiter=',')
    headerDict = {}  # Transformants, Replica, MR, Lower, Upper
    i = 0
    for row in fileData:
        if i == 0:
            for col in row:
                headerDict[col] = i
                i += 1
        elif row[headerDict["MR"]] != "" and row[headerDict["POL2_Geno"]] != "" and \
                        row[headerDict["Leu_Selection"]] == "y" and row[headerDict["Mixed"]] == "":
            mrData.add(row[headerDict["Transformants"]],
                    row[headerDict["Transformants"]] + "_" + row[headerDict["Replica"]] + " (" +
                                row[headerDict["POL2_Geno"]] + ")",
                    row[headerDict["MR"]],
                    row[headerDict["CI_Low"]],
                    row[headerDict["CI_High"]]
                    )

print(mrData.getKeys())
for key in mrData.getKeys():
    makePlot(mrData.getMrDataBlock(key), key)

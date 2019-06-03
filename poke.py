from random import randrange


def expr1():
    init_cell = Cell(mr=20)
    cul = Culture(init_cell, 100000, 1000, 1, 2000, 20, 1)
    cul.passage(20)
    cul.sort_burden(20)
    cul.analyze_nd_ratio()
    cul.print_analysis()


class Culture:
    def __init__(self, init_cell, max_density, dil_ratio, max_fit, gene_count, nd_ratio, nc_ratio):
        self.cells = [init_cell]
        self.max_density = max_density
        self.dil_ratio = dil_ratio
        self.max_fit = max_fit  # maximum logical fitness for this cell type/experiment
        self.gene_count = gene_count
        self.nd_ratio = nd_ratio # neutral to deluterious ratio
        self.nc_ratio = nc_ratio # noncoding ratio
        self.sort = []
        self.analysis = []

    def density(self):
        while len(self.cells) < self.max_density:
            print(len(self.cells))
            self.wt_gen()

    def dilute(self, ratio):
        transfer = []
        for i in range(0, len(self.cells), ratio):
            transfer.append(self.cells[i])
        self.cells = transfer

    def passage(self, count):
        for i in range(count - 1):
            self.density()
            self.dilute(self.dil_ratio)
        self.density()

    # sorts by increasing burden into x number of bins. does not gaurentee exactly equal member count in each bin but
    # does guarentee that each cell with the same mutational burden will be in the same bin
    def sort_burden(self, bins):
        max = 0
        burden_count = [0]
        for cell in self.cells:
            while cell.get_burden() > max:
                burden_count.append(0)
                max += 1
            burden_count[cell.get_burden()] += 1
        max_burden_by_bin = []
        curr_cells = 0
        curr_burden = -1
        self.sort = []
        for i in range(1, bins + 1):
            while curr_cells < int(len(self.cells) * i / bins):
                curr_burden += 1
                curr_cells += burden_count[curr_burden]
            max_burden_by_bin.append(curr_burden)
            self.sort.append([])
        print(max_burden_by_bin)
        for cell in self.cells:
            i = 0
            while cell.get_burden() > max_burden_by_bin[i]:
                i += 1
            self.sort[i].append(cell)

    # performs analysis blind to sorting. relies of applicable most recent sort
    def analyze_nd_ratio(self):
        self.analysis = []
        for i in range(len(self.sort)):
            n_count = 0
            d_count = 0
            for cell in self.sort[i]:
                n_count += cell.n_mut
                d_count += cell.d_mut
            # ratio adjusted to avoid dividing by 0
            self.analysis.append([n_count, d_count, float(n_count + 1) / (d_count + 1)])

    def print_analysis(self, header=""):
        print()
        if header:
            print(header)
        for i in range(len(self.analysis)):
            print("bin " + str(i) + ": " + str(self.analysis[i]))

    def wt_gen(self):
        for i in range(1, self.max_fit + 1):
            dots = []
            while self.cells:
                curr = self.cells.pop()
                if curr.fitness >= i:
                    for dot in curr.divide(self.gene_count, self.nc_ratio, self.nd_ratio):
                        dots.append(dot)
                else:
                    dots.append(curr)
            self.cells = dots


class Cell:
    def __init__(self, n_mut=0, d_mut=0, fit=1, mr=1):
        self.n_mut = n_mut  # assume no epistatic interactions
        self.d_mut = d_mut  # assumed reccessive lethal
        self.fitness = fit  # relative to WT
        self.mr = mr  # in mutations per division

    def mutate(self, mutations, gene_count, nc_ratio, nd_ratio):
        for i in range(0, mutations):
            if randrange(nc_ratio) == 0:
                if randrange(nd_ratio) == 0:
                    self.d_mut += 1
                    self.adj_fit(0, gene_count, self.d_mut)
                else:
                    self.n_mut += 1
                    # self.adj_fit(5, 250)

    def divide(self, gene_count, nc_ratio, nd_ratio):
        if self.fitness:
            dots = [Cell(), Cell()]  # dot ers
            for dot in dots:
                dot.n_mut = self.n_mut
                dot.d_mut = self.d_mut
                dot.fitness = self.fitness
                dot.mr = self.mr
                dot.mutate(self.mr, gene_count, nc_ratio, nd_ratio)
            return dots
        return []

    def adj_fit(self, fit, odds_n, odds_d=1, req_viab=True):
        if (self.fitness or not req_viab) and randrange(odds_n) + 1 <= odds_d:
            self.fitness = fit

    def get_burden(self):
        return self.d_mut + self.n_mut

if __name__ == "__main__":
    expr1()

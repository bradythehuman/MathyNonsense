from scipy.stats import binom, norm
from random import randrange as rr


def expr1():
    cul = Culture(CanMR(1, -3))
    for i in range(20):
        cul.ticks(20)
        cul.print_cul()


class Culture:
    def __init__(self, init_pop):
        self.pops = [init_pop]
        self.t = 0
        self.dmr_ratio = 2*0.00033  # chosen so half of the populations will develop a antimutator by t = 20
        self.eg_count = 1000  # essential gene count

    def ticks(self, ticks):
        for i in range(ticks):
            self.tick

    def tick(self):
        survivors = []
        for pop in self.pops:
            if pop.y(pop.t) > 0:
                survivors += pop.gen()
                survivors.append(pop)
        self.pops = survivors

    def print_cul(self):
        print("\nculture at t=" + str(self.t))
        for pop in self.pops:
            pop.print_pop()


class CanMR:
    def __init__(self, c, e):
        self.c = c
        self.e = e

    # mr at can1 locus
    def mr(self):
        return self.c * (10 ** (float(self.e)))

    def scale(self, scalar):
        n = self.mr() * scalar
        e = 0
        while int(n / (10 ** (e - 1))) <= 0:
            e -= 1
        return CanMR(int(n / (10 ** e)), e)


class Population4:
    def __init__(self, can1, l0=0):
        self.t = 0  # time in generations
        self.can1 = can1  # 10^-8 can1 mutation rate
        self.l0 = l0  # initial heterozygous recessive lethal mutations

    def gen(self):
        self.t += 1
        sub_pops = binom.rvs(self.y(self.t), self.can1.mr()*dmr_ratio)
        pops = []
        while sub_pops:
            pops.append(Population4(self.dmr_norm1(), l0=self.l()))
            sub_pops -= 1
        return pops

    # delta mutation rate from antimutator/mutator
    def dmr_norm1(self, s_min, variances):
        s = 0
        while abs(s) < s_min:
            s = norm.rvs(scale=variances[rr(len(variances))])  # choose random variance and use in dist for s
        if s > 0:
            return self.can1.scale(float(s))
        return self.can1.scale(1 / float(-s))

    # cell count
    def y(self, t):
        return (2**t)*((1-(1-(1-self.x())**t)**2)**n_eg)

    # mutation rate of random essential gene
    def x(self):
        return 0.73*self.can1.mr()

    # heterozygous recessive lethal mutations
    def l(self):
        return int((n_eg-self.l0)*(1-(1-self.x())**self.t)*(2*(1-self.x())**self.t-self.x()**(2*self.t))) + self.l0

    def print_pop(self):
        print("t=" + str(self.t) + ", mr=" + str(self.can1.mr()) + ", l0=" + str(self.l0))


if __name__ == "__main__":
    expr1()

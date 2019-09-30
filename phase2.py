import numpy as np


def f_equals(a, b):
    return True if np.abs(b - a) < 1e-10 else False


def simplex_method_phase2(c, AT, x, limitations, base):
    N = AT.shape[0]

    print(' A:\n{}'.format(AT.T))
    print(' base: {}'.format(base))
    print(' c: {}'.format(c))
    print(' x: {}'.format(x))
    print(' limitation: {}\n'.format(limitations))

    for i in range(1, 100000):
        mask = np.zeros(N, dtype=bool)
        mask[list(base)] = True
        J_b = np.arange(N)[mask]
        J_n = np.arange(N)[np.logical_not(mask)]
        A_b = AT[J_b]
        c_b = c[J_b]
        u = np.linalg.solve(A_b, c_b)
        delta = [c[i] - np.dot(u, AT[i]) for i in J_n]

        print('{} iteration'.format(i))
        print('\t A_base:')
        for string in A_b.T:
            print('\t\t {}'.format(string))
        print('\t c_base: {}'.format(c_b))
        print('\t index_base: {}'.format(J_b))
        print('\t index_nobase: {}'.format(J_n))
        print('\t potential: {}'.format(u))
        print('\t delta: {}'.format(delta))

        j_0 = None
        max_value = 0
        for index, value in enumerate(delta):
            if (value < 0 and not f_equals(x[J_n[index]], limitations[J_n[index]][0])) \
                    or (value > 0 and not f_equals(x[J_n[index]], limitations[J_n[index]][1])):
                if np.abs(value) > max_value:
                    max_value = np.abs(value)
                    j_0 = index

        if j_0 is None:
            print('\n optimality criterion is satisfied')
            break

        l = np.zeros(N)
        l[J_n[j_0]] = np.sign(delta[j_0])
        l[J_b] = np.linalg.solve(A_b.T, -AT[J_n[j_0]] * np.sign(delta[j_0]))

        print('\t direction vector: {}'.format(l))

        tetta = limitations[J_n[j_0]][1] - limitations[J_n[j_0]][0]
        print(' \t tetta[j_0]: {}'.format(tetta))
        j_new = None
        for index, value in enumerate(l):
            if index in base and abs(l[index]) > 1e-10:
                temp = None
                if l[index] > 0:
                    temp = limitations[index][1]
                else:
                    temp = limitations[index][0]
                temp = (temp - x[index]) / l[index]
                print('\t one of tetta[J_n]: {}'.format(temp))
                if temp < tetta:
                    j_new = index
                    tetta = temp

        x = x + tetta * l

        if j_new is not None:
            base -= {j_new}
            base.add(J_n[j_0])

        print('\t final tetta: {}'.format(tetta))
        print('\t j_0 and j_new: {}, {}'.format(J_n[j_0], j_new))
        print('\t base: {}'.format(base))
        print('\t x: {}\n'.format(x))

    print(' optimal plan: {}'.format(x))
    print(' target function: {}'.format(np.dot(x, c)))
    return x, base


'''
   ..normal..
80x1 + 70x2 -> max
8x1 + 25x2 < 800
8x1 + 5x2 < 640
x1 + 5x2 < 145

x1 [3, 78]
x2 [0, 28]

---------------
   ..canonical..
80x1 + 70x2 -> max
8x1 + 25x2 + x3 = 800
8x1 + 5x2 + x4 = 640
x1 + 5x2 + x5 = 145

x1 [3, 78]
x2 [0, 28]
x3 [0, 776]
x4 [0, 616]
x5 [0, 142]

'''
c = np.array([80, 70, 0, 0, 0])
x = [3, 0, 776, 616, 142]
base = {1, 2, 4}
AT = np.array([
    [8, 8, 1],
    [25, 5, 5],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])
limitations = [
    [3, 78],
    [0, 28],
    [0, 776],
    [0, 616],
    [0, 142]
]

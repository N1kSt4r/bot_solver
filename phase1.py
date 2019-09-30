import numpy as np
from phase2 import simplex_method_phase2

inf = 1e15


def string_to_int_list(str):
    return [int(num if num != 'inf' else inf) for num in str.split()]


def read_data():
    c = np.array(string_to_int_list(input()))

    rows, columns = string_to_int_list(input())
    A = []
    for row in range(rows):
        A.append(string_to_int_list(input()))
    AT = np.array(A).T

    b = string_to_int_list(input())

    limitations = []
    for _ in range(columns):
        limitations.append(string_to_int_list(input()))

    return c, AT, b, limitations


def get_diag_matrix_by_vector(v):
    matrix = np.identity(len(v))
    i, j = np.indices(matrix.shape)
    matrix[i == j] = v
    for index, value in enumerate(np.diag(matrix)):
        if value == 0:
            matrix[index][index] = 1e-15
    return np.array(matrix)


def change_bound(vector, limits):
    for i in range(len(vector)):
        if vector[i] == inf:
            vector[i] = limits[i][0]


c, AT, b, limitations = read_data()


print(' A:\n{}'.format(AT.T))
print(' b: {}'.format(b))
print(' c: {}'.format(c))
x = np.array(limitations).T[1]
change_bound(x, limitations)
n = AT.shape[1]
base = set(range(n))
discrepancy = b - np.dot(AT.T, x)

print(' x: {}'.format(x))
print(' limitation: {}'.format(limitations))
print(' discrepancy: {}'.format(discrepancy))

basis_plan_exist = False
if np.linalg.norm(discrepancy) > 1e-10:
    print('\n   --- Phase 1 --- \n')
    n = len(discrepancy)
    m = AT.size // n + n

    AT_extended = np.vstack((AT, get_diag_matrix_by_vector(np.sign(discrepancy))))

    
    lim_temp = limitations.copy()
    for bound in discrepancy:
        lim_temp.append([0, abs(bound)])

    c_temp = np.zeros(m)
    c_temp[-n:] = np.ones(n) * -1
    x_temp = np.array(lim_temp).T[1]
    change_bound(x_temp, lim_temp)

    print(' new A:\n{}'.format(AT_extended.T))
    print(' new limitation: {}'.format(lim_temp))
    print(' new c-vector: {}'.format(c_temp))
    print(' new x-vector: {}'.format(x_temp))
    print('\n\t\tvvvvvvvvvvvvv\n')
    x, base = simplex_method_phase2(c_temp, AT_extended, x_temp, lim_temp, set(range(m - n, m)))
    print('\n x-vector after phase 1: {}\n base after phase 1: {}'.format(x, base))
    print('\n --- Phase 1 end --- \n')

    if np.linalg.norm(x[len(x) - n:]) < 1e-10:
        basis_plan_exist = True

        if np.any([component in base for component in np.arange(5, 7)]):
            print("Buffer variables must be added")
            x_temp = np.copy(x)
            x = x[:len(x) - n]
            for_delete = set()
            for_add = set()
            rename_component_on = len(x)
            for component in range(len(x_temp) - n, len(x_temp)):
                if component in base:
                    for_delete.add(component)
                    for_add.add(rename_component_on)
                    rename_component_on += 1

                    x = np.append(x, x_temp[component])
                    limitations.append([0, 0])
                    AT = np.vstack((AT, AT_extended[component]))
                    c = np.append(c, [0])

            base -= for_delete
            base |= for_add
            print(' new A:\n{}'.format(AT.T))
            print(' new limitation: {}'.format(limitations))
            print(' new c-vector: {}'.format(c))
            print(' new x-vector: {}'.format(x))
        else:
            x = x[:len(x) - n]

if basis_plan_exist:
    print('basic plan is {}'.format(x))
    print('base: {}'.format(base))
    print('\n   --- Phase 2 --- \n')
    simplex_method_phase2(c, AT, x, limitations, base)
    print('\n --- Phase 2 end --- \n')
else:
    print('basic plan is not exist')


import sympy as sp
import numpy as np
import subprocess
import os


task_name = 'phase1'

buffer = ''
for string in open('./{}/{}.format'.format(task_name, task_name)):
    buffer += string
print(buffer)


def take_args():
    file = './{}/{}'.format(task_name, task_name)
    return 'python {}.py < {}.input > {}.output 2> {}.output'.format(task_name, file, file, file)


os.system(take_args())
#subprocess.run(take_args())


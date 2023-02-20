from pulp import *
from A_star import can_reach
import random

def gen_testcase(lim_jug = 5, lim_cap = 1000, lim_tar = 5000):
    jugs = [0] * random.randint(1, lim_jug)
    for i in range(len(jugs)):
        jugs[i] = random.randint(1, lim_cap)
    jugs = sorted(jugs)
    target = random.randint(1, lim_tar)
    return (jugs,target)
    if can_reach(jugs+[-1], target):
        return (jugs,target)
    else:
        return (jugs,target, -1)

def solve_int_linear_opt(jugs,target):

    if not can_reach(jugs+[-1], target):
        print((jugs,target, -1))
        return

    N = len(jugs)
    x_vars = LpVariable.dicts("x",range(N), cat='Integer')
    x_vars_abs = LpVariable.dicts("x_abs",range(N), cat='Integer')
    prob = LpProblem("min_sum_abs", LpMinimize)

    # OBJECTIVE
    prob += lpSum(x_vars_abs)

    # ABS CONSTRAINTS
    for i in range(N):
        prob += x_vars_abs[i] >= x_vars[i]
        prob += x_vars_abs[i] >= -x_vars[i]

    # OTHER MODEL CONSTRAINTS
    prob += lpSum(jugs[i] * x_vars[i] for i in range(N)) ==  target

    prob.solve()

    print ("Status: " + str(LpStatus[prob.status]))
    print ("Objective: " + str(value(prob.objective)))

    for v in prob.variables():
        print (v.name + " = " + str(v.varValue))
    print((jugs,target))

    if int(value(prob.objective)) < 50:
        # TBD write into file
        return

for i in range(10):
    jugs,target = gen_testcase()
    solve_int_linear_opt(jugs,target)
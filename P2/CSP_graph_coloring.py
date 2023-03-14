import sys

# Define a class for representing a CSP variable
class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.color = None

    def __str__(self):
        return f'name = {self.name}, domain = {self.domain}, color = {self.color}'

# Define a class for representing a CSP constraint
class Constraint:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    # Check if the constraint is satisfied
    def is_satisfied(self):
        if self.var1.color and self.var2.color:
            return self.var1.color != self.var2.color
        else:
            return True

    def __str__(self):
        return f'var1 = {self.var1}, var2 = {self.var2}'

# Define a function to read the graph from a file
def read_graph(filename):
    # store loaded data in a dict
    graph = {}
    with open(filename, 'r') as file:
        for line in file:
            # ignore comments and empty lines
            if not line.startswith('#') and not line.strip() == '':
                # get number of colors
                if line.startswith('Colors') or line.startswith('colors'):
                    num_colors = int(line.split('=')[1].strip())
                else:
                    # get constraints
                    v1, v2 = map(int, line.strip().split(','))
                    if v1 not in graph:
                        graph[v1] = []
                    if v2 not in graph:
                        graph[v2] = []
                    graph[v1].append(v2)
                    graph[v2].append(v1)
    # get all vertexs
    variables = []
    for v in graph.keys():
        variables.append(Variable(v, list(range(1, num_colors+1))))
    # build constraints
    constraints = []
    for v1 in graph.keys():
        for v2 in graph[v1]:
            if v1 < v2:
                constraints.append(Constraint(variables[v1-1], variables[v2-1]))
    return variables, constraints

# Define a function to perform AC3 constraint propagation
def ac3(constraints, queue=None):
    # init queue
    if queue is None:
        queue = list(constraints)
    while queue:
        c = queue.pop(0)
        #print(c)
        if len(c.var1.domain) == 0 or len(c.var2.domain) == 0:
                return False
        # check constraints
        if revise(c):
            if len(c.var1.domain) == 0 or len(c.var2.domain) == 0:
                return False
            for c2 in constraints:
                if c2.var2 == c.var1 and c2 != c:
                    queue.append(c2)
    return True

# Define a function to revise a single constraint
def revise(constraint):
    revised = False
    # revise after assign
    if constraint.var2.color and constraint.var2.color in constraint.var1.domain:
        revised = True
        constraint.var1.domain.remove(constraint.var2.color)
    # if len(constraint.var2.domain) >= 2, there is no conflict
    if len(constraint.var2.domain) >= 2:
        return revised
    # if there is conflict
    for x in constraint.var1.domain:
        if x == constraint.var2.domain[0]:
            constraint.var1.domain.remove(x)
            revised = True
    return revised

# Define a function to select the next variable to assign, MRV
def select_unassigned_variable(variables):
    return min([v for v in variables if v.color is None], key=lambda v: len(v.domain))

# Define a function to select the value to be assigned with LCV heuristic
def order_domain_values(var, variables, constraints):
    values = list(var.domain)
    # count how many constraints assigning this value will cause
    def constraining_value(value):
        var.color = value
        count = 0
        for c in constraints:
            if not c.is_satisfied():
                count += 1
        var.color = None
        return count
    values.sort(key=lambda value: constraining_value(value))
    return values

# Define the main function to solve the CSP problem
def solve_csp(variables, constraints):
    if not ac3(constraints):
        return None
    return backtrack(variables, constraints)

# Define the backtrack function
def backtrack(variables, constraints):
    if all([v.color != None for v in variables]):
        return variables
    # select the variable to be assigned using MRV
    var = select_unassigned_variable(variables)
    # determine the value to be asigned using LCV
    for value in order_domain_values(var, variables, constraints):
        # backup variables
        backup = []
        for v in variables:
            backup.append((v.name, v.domain, v.color))
        var.color = value
        #print(var,all([c.is_satisfied() for c in constraints]))
        if all([c.is_satisfied() for c in constraints]) and ac3(constraints):
            result = backtrack(variables, constraints)
            if result != None:
                return result
        # restore backup
        for i in range(len(variables)):
            variables[i].name, variables[i].domain, variables[i].color = backup[i]
    return None

# Define the main function to run the CSP algorithm
def main():
    if len(sys.argv) < 2:
        print('Usage: python CSP_graph_coloring.py <filename>')
        sys.exit(1)
    filename = sys.argv[1]
    variables, constraints = read_graph(filename)
    print(f'Loaded graph from: {filename}')
    result = solve_csp(variables, constraints)
    if result is None:
        print('No solution found.')
    else:
        for v in result:
            print('Vertex', v.name, 'is colored', v.color)

if __name__ == '__main__':
    main()






import numpy as np
import pandas as pd


class Depot:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Customer:
    def __init__(self, id, x, y, demand):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand

class Route:
    def __init__(self, depot_id):
        self.depot_id = depot_id
        self.customers = []

class Solution:
    def __init__(self):
        self.routes = []

depots = []
customers = []


def calculate_savings(depot, customers):
    savings = {}
    for customer in customers:
        savings[(depot.id, customer.id)] = distance(depot, customer)
    return savings

def distance(node1, node2):
    return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
# Read input data

def calculate_multidepot_savings(depots, customers):
    savings = {}
    for depot in depots:
        for customer in customers:
            savings[(depot.id, customer.id)] = distance(depot, customer)
    return savings


def construct_routes(savings, depots, customers, capacity):
    routes = []
    for depot in depots:
        route = Route(depot.id)
        for customer in customers:
            if route_capacity(route) + customer.demand <= capacity:
                route.customers.append(customer)
        routes.append(route)
    return routes

def route_capacity(route):
    return sum(customer.demand for customer in route.customers)


def two_phase_selection(savings, depots, customers, iterations):
    for i in range(iterations):
        # Phase 1: Generate savings list
        savings_list = calculate_multidepot_savings(depots, customers)
        # Phase 2: Select savings values based on probabilities
        selected_savings = select_savings_values(savings_list)
        # Phase 3: Merge selected savings into routes
        merged_routes = merge_savings_into_routes(selected_savings, depots, customers)
        # Phase 4: Route post-improvement
        improved_routes = post_improvement(merged_routes)
    return improved_routes

def select_savings_values(savings_list):
    selected_savings = []
    # Select savings values based on probabilities
    # Implement selection logic here
    return selected_savings

def merge_savings_into_routes(selected_savings, depots, customers):
    merged_routes = []
    # Merge selected savings into routes
    # Implement merging logic here
    return merged_routes

def post_improvement(routes):
    improved_routes = []
    # Implement route post-improvement logic here
    return improved_routes

def post_improvement(routes):
    improved_routes = []
    for route in routes:
        # Intraroute improvement
        intraroute_improved_route = intraroute_improvement(route)
        # Interroute improvement
        interroute_improved_route = interroute_improvement(intraroute_improved_route, routes)
        improved_routes.append(interroute_improved_route)
    return improved_routes

def intraroute_improvement(route):
    # Implement intraroute improvement logic here
    return route

def interroute_improvement(route, routes):
    # Implement interroute improvement logic here
    return route

def initialize_depots():
    # Implement logic to initialize depot locations
    depots = []  # Example depot locations
    return depots

def initialize_customers():
    # Implement logic to initialize customer locations and demands
    customers = []  # Example customer locations and demands
    return customers
# def calculate_saving(depot, customer):
#     # Implement logic to calculate savings between a depot and a customer
#     return saving

def calculate_savings(depots, customers):
    savings = []
    for depot in depots:
        for customer in customers:
            saving = calculate_multidepot_savings(depot, customer)
            savings.append(saving)
    return savings



def display_results(routes):
    for i, route in enumerate(routes):
        print(f"Route {i+1}: {route}")

def main():
    # Define parameter values
    depots = initialize_depots()  # Initialize depot locations
    customers = initialize_customers()  # Initialize customer locations and demands
    capacity = 100  # Define vehicle capacity
    iterations = 5000  # Define number of iterations for two-phase selection

    # Execute two-phase selection procedure
    improved_routes = two_phase_selection(savings, depots, customers, iterations)

    # Display results
    display_results(improved_routes)

# if __name__ == "__main__":
#     main()

# read node data in coordinate (x,y) format
nodes = pd.read_csv('input/demand.csv', index_col='node')
nodes.rename(columns={"distance to depot": 'd0'}, inplace=True)
node_number = len(nodes.index) - 1


# read pairwise distance
pw = pd.read_csv('input/pairwise.csv', index_col='Unnamed: 0')
pw.index.rename('', inplace=True)

# calculate savings for each link
# Parameter lambda
lambd = 0.5  # You can adjust this value as needed

# calculate savings for each link with lambda
savings = dict()
for r in pw.index:
    for c in pw.columns:
        if int(c) != int(r):
            a = max(int(r), int(c))
            b = min(int(r), int(c))
            key = '(' + str(a) + ',' + str(b) + ')'
            # Include lambda in the savings calculation
            savings[key] = lambd * nodes['d0'][int(r)] + lambd * nodes['d0'][int(c)] - pw[c][r]


# put savings in a pandas dataframe, and sort by descending
sv = pd.DataFrame.from_dict(savings, orient='index')
sv.rename(columns={0: 'saving'}, inplace=True)
sv.sort_values(by=['saving'], ascending=False, inplace=True)

# convert link string to link list to handle saving's key, i.e. str(10, 6) to (10, 6)
def get_node(link):
    link = link[1:]
    link = link[:-1]
    nodes = link.split(',')
    return [int(nodes[0]), int(nodes[1])]

# determine if a node is interior to a route
def interior(node, route):
    try:
        i = route.index(node)
        # adjacent to depot, not interior
        if i == 0 or i == (len(route) - 1):
            label = False
        else:
            label = True
    except:
        label = False

    return label

# merge two routes with a connection link
def merge(route0, route1, link):
    if route0.index(link[0]) != (len(route0) - 1):
        route0.reverse()

    if route1.index(link[1]) != 0:
        route1.reverse()

    return route0 + route1

# sum up to obtain the total passengers belonging to a route
def sum_cap(route):
    sum_cap = 0
    for node in route:
        sum_cap += nodes.demand[node]
    return sum_cap
# determine 4 things:
# 1. if the link in any route in routes -> determined by if count_in > 0
# 2. if yes, which node is in the route -> returned to node_sel
# 3. if yes, which route is the node belongs to -> returned to route id: i_route
# 4. are both of the nodes in the same route? -> overlap = 1, yes; otherwise, no
def which_route(link, routes):
    # assume nodes are not in any route
    node_sel = list()
    i_route = [-1, -1]
    count_in = 0
    
    for route in routes:
        for node in link:
            try:
                route.index(node)
                i_route[count_in] = routes.index(route)
                node_sel.append(node)
                count_in += 1
            except:
                pass
                
    if i_route[0] == i_route[1]:
        overlap = 1
    else:
        overlap = 0
        
    return node_sel, count_in, i_route, overlap
# determine if a link is already in any route
def link_in_route(link, routes):
    for route in routes:
        if link in route or link[::-1] in route:
            return True
    return False

# create empty routes
routes = list()

# if there is any remaining customer to be served
remaining = True

# define capacity of the vehicle
cap = 23

# record steps
step = 0

# get a list of nodes, excluding the depot
node_list = list(nodes.index)
node_list.remove(0)

# STEP 1: Calculate the savings
# STEP 2: Rank the savings and list them in descending order

# STEP 3: Process the savings list
while remaining and not sv.empty:
    step += 1
    print('step ', step, ':')

    # Take the topmost entry in the savings list
    link = get_node(sv.index[0])

    # Check if link is already in any route
    if not link_in_route(link, routes):
        node_sel, num_in, i_route, overlap = which_route(link, routes)

        # condition a. Include link in a new route if neither node is assigned to a route
        if num_in == 0:
            if sum_cap(link) <= cap:
                routes.append(link)
                node_list.remove(link[0])
                node_list.remove(link[1])
                print('\t', 'Link ', link, ' fulfills criteria a), so it is created as a new route')
            else:
                print('\t', 'Though Link ', link, ' fulfills criteria a), it exceeds maximum load, so skip this link.')

        # condition b. Include link in the existing route if one node is already assigned and not interior
        elif num_in == 1:
            n_sel = node_sel[0]
            i_rt = i_route[0]
            position = routes[i_rt].index(n_sel)
            link_temp = link.copy()
            link_temp.remove(n_sel)
            node = link_temp[0]

            cond1 = (not interior(n_sel, routes[i_rt]))
            cond2 = (sum_cap(routes[i_rt] + [node]) <= cap)

            if cond1:
                if cond2:
                    print('\t', 'Link ', link, ' fulfills criteria b), so a new node is added to route ', routes[i_rt], '.')
                    if position == 0:
                        routes[i_rt].insert(0, node)
                    else:
                        routes[i_rt].append(node)
                    node_list.remove(node)
                else:
                    print('\t', 'Though Link ', link, ' fulfills criteria b), it exceeds maximum load, so skip this link.')
                    sv.drop(sv.index[0], inplace=True)
                    continue
            else:
                print('\t', 'For Link ', link, ', node ', n_sel, ' is interior to route ', routes[i_rt], ', so skip this link')
                sv.drop(sv.index[0], inplace=True)
                continue

        # condition c. Merge routes if both nodes are in different existing routes and neither interior
        else:
            if overlap == 0:
                cond1 = (not interior(node_sel[0], routes[i_route[0]]))
                cond2 = (not interior(node_sel[1], routes[i_route[1]]))
                cond3 = (sum_cap(routes[i_route[0]] + routes[i_route[1]]) <= cap)

                if cond1 and cond2:
                    if cond3:
                        route_temp = merge(routes[i_route[0]], routes[i_route[1]], node_sel)
                        temp1 = routes[i_route[0]]
                        temp2 = routes[i_route[1]]
                        routes.remove(temp1)
                        routes.remove(temp2)
                        routes.append(route_temp)
                    else:
                        print('\t', 'Link ', link, ' fulfills criteria c), but merging exceeds maximum load, so skip this link.')
                        sv.drop(sv.index[0], inplace=True)
                        continue
            else:
                print('\t', 'Link ', link, ' fulfills criteria c), but both nodes are in the same route, so skip this link.')
                sv.drop(sv.index[0], inplace=True)
                continue

    # Remove the processed link from the savings list
    sv.drop(sv.index[0], inplace=True)

# STEP 4: Stop and output the routes
print("\nFinal routes:")
for route in routes:
    print(route)
# import numpy as np
# import pandas as pd
# # read node data in coordinate (x,y) format
# nodes = pd.read_csv('input/demand.csv', index_col = 'node')
# nodes.rename(columns={"distance to depot":'d0'}, inplace = True)
# node_number = len(nodes.index) - 1
# nodes.head() 
# # read pairwise distance
# pw = pd.read_csv('input/pairwise.csv', index_col = 'Unnamed: 0')
# pw.index.rename('',inplace = True)
# pw
# # calculate savings for each link
# savings = dict()
# for r in pw.index:
#     for c in pw.columns:
#         if int(c) != int(r):            
#             a = max(int(r), int(c))
#             b = min(int(r), int(c))
#             key = '(' + str(a) + ',' + str(b) + ')'
#             savings[key] = nodes['d0'][int(r)] + nodes['d0'][int(c)] - pw[c][r]

# # put savings in a pandas dataframe, and sort by descending
# sv = pd.DataFrame.from_dict(savings, orient = 'index')
# sv.rename(columns = {0:'saving'}, inplace = True)
# sv.sort_values(by = ['saving'], ascending = False, inplace = True)
# sv.head()
# # convert link string to link list to handle saving's key, i.e. str(10, 6) to (10, 6)
# def get_node(link):
#     link = link[1:]
#     link = link[:-1]
#     nodes = link.split(',')
#     return [int(nodes[0]), int(nodes[1])]
# # determine if a node is interior to a route
# def interior(node, route):
#     try:
#         i = route.index(node)
#         # adjacent to depot, not interior
#         if i == 0 or i == (len(route) - 1):
#             label = False
#         else:
#             label = True
#     except:
#         label = False
    
#     return label
# # merge two routes with a connection link
# def merge(route0, route1, link):
#     if route0.index(link[0]) != (len(route0) - 1):
#         route0.reverse()
    
#     if route1.index(link[1]) != 0:
#         route1.reverse()
        
#     return route0 + route1
# # sum up to obtain the total passengers belonging to a route
# def sum_cap(route):
#     sum_cap = 0
#     for node in route:
#         sum_cap += nodes.demand[node]
#     return sum_cap
# # determine 4 things:
# # 1. if the link in any route in routes -> determined by if count_in > 0
# # 2. if yes, which node is in the route -> returned to node_sel
# # 3. if yes, which route is the node belongs to -> returned to route id: i_route
# # 4. are both of the nodes in the same route? -> overlap = 1, yes; otherwise, no
# def which_route(link, routes):
#     # assume nodes are not in any route
#     node_sel = list()
#     i_route = [-1, -1]
#     count_in = 0
    
#     for route in routes:
#         for node in link:
#             try:
#                 route.index(node)
#                 i_route[count_in] = routes.index(route)
#                 node_sel.append(node)
#                 count_in += 1
#             except:
#                 pass
                
#     if i_route[0] == i_route[1]:
#         overlap = 1
#     else:
#         overlap = 0
        
#     return node_sel, count_in, i_route, overlap
# # create empty routes
# routes = list()

# # if there is any remaining customer to be served
# remaining = True

# # define capacity of the vehicle
# cap = 23

# # record steps
# step = 0

# # get a list of nodes, excluding the depot
# node_list = list(nodes.index)
# node_list.remove(0)

# # run through each link in the saving list
# for link in sv.index:
#     step += 1
#     if remaining:

#         print('step ', step, ':')

#         link = get_node(link)
#         node_sel, num_in, i_route, overlap = which_route(link, routes)

#         # condition a. Either, neither i nor j have already been assigned to a route, 
#         # ...in which case a new route is initiated including both i and j.
#         if num_in == 0:
#             if sum_cap(link) <= cap:
#                 routes.append(link)
#                 node_list.remove(link[0])
#                 node_list.remove(link[1])
#                 print('\t','Link ', link, ' fulfills criteria a), so it is created as a new route')
#             else:
#                 print('\t','Though Link ', link, ' fulfills criteria a), it exceeds maximum load, so skip this link.')

#         # condition b. Or, exactly one of the two nodes (i or j) has already been included 
#         # ...in an existing route and that point is not interior to that route 
#         # ...(a point is interior to a route if it is not adjacent to the depot D in the order of traversal of nodes), 
#         # ...in which case the link (i, j) is added to that same route.    
#         elif num_in == 1:
#             n_sel = node_sel[0]
#             i_rt = i_route[0]
#             position = routes[i_rt].index(n_sel)
#             link_temp = link.copy()
#             link_temp.remove(n_sel)
#             node = link_temp[0]

#             cond1 = (not interior(n_sel, routes[i_rt]))
#             cond2 = (sum_cap(routes[i_rt] + [node]) <= cap)

#             if cond1:
#                 if cond2:
#                     print('\t','Link ', link, ' fulfills criteria b), so a new node is added to route ', routes[i_rt], '.')
#                     if position == 0:
#                         routes[i_rt].insert(0, node)
#                     else:
#                         routes[i_rt].append(node)
#                     node_list.remove(node)
#                 else:
#                     print('\t','Though Link ', link, ' fulfills criteria b), it exceeds maximum load, so skip this link.')
#                     continue
#             else:
#                 print('\t','For Link ', link, ', node ', n_sel, ' is interior to route ', routes[i_rt], ', so skip this link')
#                 continue

#         # condition c. Or, both i and j have already been included in two different existing routes 
#         # ...and neither point is interior to its route, in which case the two routes are merged.        
#         else:
#             if overlap == 0:
#                 cond1 = (not interior(node_sel[0], routes[i_route[0]]))
#                 cond2 = (not interior(node_sel[1], routes[i_route[1]]))
#                 cond3 = (sum_cap(routes[i_route[0]] + routes[i_route[1]]) <= cap)

#                 if cond1 and cond2:
#                     if cond3:
#                         route_temp = merge(routes[i_route[0]], routes[i_route[1]], node_sel)
#                         temp1 = routes[i_route[0]]
#                         temp2 = routes[i_route[1]]
#                         routes.remove(temp1)
#                         routes.remove(temp2)
#                         routes.append(route_temp)
                       

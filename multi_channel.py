import numpy as np
from scipy.optimize import linprog
def optimize_channel_fulfillment(params):
    n = len(params["items"])
    costs = [p["cost"] for p in params["items"]]
    capacities = [p.get("capacity", 1000) for p in params["items"]]
    demand = params.get("demand", 500)
    A_eq = [[1]*n]; b_eq = [demand]
    A_ub = [[1 if j==i else 0 for j in range(n)] for i in range(n)]
    b_ub = capacities
    bounds = [(p.get("min",0), p.get("max",None)) for p in params["items"]]
    res = linprog(costs, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if res.success:
        alloc = {{params["items"][i]["name"]: round(res.x[i]) for i in range(n)}}
        return {{"allocation": alloc, "total_cost": round(res.fun, 2)}}
    return {{"error": "infeasible"}}
if __name__=="__main__":
    items = [{{"name": "S1", "cost": 5, "capacity": 500}},
             {{"name": "S2", "cost": 8, "capacity": 300}},
             {{"name": "S3", "cost": 12, "capacity": 200}}]
    print(optimize_channel_fulfillment({{"items": items, "demand": 800}}))

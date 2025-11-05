from rdflib import Graph

g = Graph()
g.parse("month_2022-01.n3", format="n3")

for subj, pred, obj in list(g)[:5]:
    print(subj, pred, obj)
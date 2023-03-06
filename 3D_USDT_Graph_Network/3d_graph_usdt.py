import pandas as pd
import json
from collections import defaultdict
from json import dumps
from random import random
from math import sqrt

df_addresses = pd.read_csv('addresses.csv')
addresses = df_addresses['address'].unique().tolist()

df_transactions = pd.read_csv('transactions.csv', sep=';')
links = defaultdict(float)
for i, row in df_transactions.iterrows():
    source = row['from']
    target = row['to']
    value = row['amount']
    links[(source, target)] += value

nodes = [{'id': addr, 'color': f'rgb({int(random()*255)}, {int(random()*255)}, {int(random()*255)})'} for addr in addresses]
links = [{'source': source, 'target': target, 'value': sqrt(value)} for (source, target), value in links.items()]
data = {'nodes': nodes, 'links': links}

with open('data.json', 'w') as f:
    json.dump(data, f)

with open('data.json', 'r') as f:
    json_data = f.read()

with open('graph.html', 'w') as f:
    f.write(f"""
    <html>
    <head>
        <script src="https://unpkg.com/3d-force-graph"></script>
        <style>
          #graph {{
            width: 100%;
            height: 800px;
            margin-top: 20px;
          }}
        </style>
    </head>
    <body>
        <div id="graph"></div>
        <script>
            const myGraph = ForceGraph3D()
            (document.getElementById('graph')) 
          myGraph.graphData({json_data})
          myGraph.nodeRelSize(5)
          myGraph.nodeResolution(10)
        </script>
    </body>
    </html>
    """)

import webbrowser
webbrowser.open('graph.html')

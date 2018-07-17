import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

con = sqlite3.connect("data.db")
c = con.cursor()

c.execute('SELECT temp, lux FROM data')
elems = c.fetchall()

temps = []
luxs = []
counts = []
count = 0

for row in elems:
    temps += [row[0]]
    luxs += [row[1]]
    count += 1
    counts += [count]

con.commit()
con.close()

TemperatureF = go.Scatter(
    x=counts,
    y=temps
)

Lux = go.Scatter(
    x=counts,
    y=luxs
)

graphs = [TemperatureF, Lux]

py.iplot(graphs, filename='testing')

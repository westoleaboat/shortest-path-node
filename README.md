# Shortest Path Node GUI
find the shortest path between two nodes in a network using python NetworkX.

## Description

A common problem where networks make an appearance is in the problem of finding the
shortest route between two nodes in a network. For instance, this could be the shortest distance between two cities, where the
nodes represent the cities and the edges are roads connecting pairs of cities. In this case, the
weights of the edges would be their lengths.

![shortest-path](screenshot.png)

## TODO
### Improve
- [ ] Validate spinbox input values (Int only)
- [ ] Make sure path-to-find is inside node range
- [x] Improve dynamic title for errors.
- [ ] Comment out old logic


### Completed
- [x] Organize layout with clases
- [x] Generate new plot with input values
- [x] Default plot

## Installation
1. Clone this repo into a project folder and create a virtual environment
```
cd project-folder/
git clone https://github.com/westoleaboat/shortest-path-node.git
cd shortest-path-node.git
python3 -m venv env_name
```
2. Install dependencies with pip
```
source env_name/bin/activate
pip install -r requirements.txt
```
3. run main.py
```
python3 shortest_path.py
```

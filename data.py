# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygraphviz as pgv

global graph
graph = pgv.AGraph()
global dotID
dotID=0
modules = []

global url_value
url_value= None

def add_modules( modulename):
    modules.append(modulename)

def get_modules():
    return modules
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import sys

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("datatable.html")

df = pd.read_csv(sys.argv[1],delimiter=";",nrows=1)  
cols = list(df)


print(template.render(cols=cols,filecsv=sys.argv[1]))


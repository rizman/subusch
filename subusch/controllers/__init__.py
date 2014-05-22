from jinja2 import Environment, FileSystemLoader

__author__ = 'Gilles'

env = Environment(loader=FileSystemLoader('views'))

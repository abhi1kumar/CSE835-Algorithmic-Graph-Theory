
import os, sys
sys.path.append(os.getcwd())

import numpy as np

def execute(command, print_flag= False):
    if print_flag:
        print(command)
    os.system(command)

nauty_path   = "~/course/CSE835_Graph_Theory/nauty27r1"
geng_binary  = "geng"
count_binary = "countg"
num_vertex_final = 10

output_dir   = "output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
output_file_path = os.path.join(os.getcwd(), output_dir, "graph.txt")

for n in range(1, num_vertex_final+1):
    command = os.path.join(nauty_path, geng_binary) + " " + str(n) + " -c > " + output_file_path
    execute(command)

    command = os.path.join(nauty_path, count_binary) + " " + output_file_path + " -E"
    execute(command)

    print("") 

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ast
import os
import sys
import glob
from pathlib import Path
from data import graph
from processingimport import ProcessingImport
import dot2png
from data import modules
import time
# import astpretty
# Press the green button in the gutter to run the script.
from memory_profiler import profile
@profile
def run():
    start = time.perf_counter()
    '''code ="""response = requests.get(url=random_host+"/random-list").json()"""
    tree = ast.parse(code)
    print(ast.dump(tree))'''
    # 读取第一个文件
    #current_dir = "C:\\Users\\admin\\Desktop\\call_graph\\istio-bookinfo"
    current_dir = "C:\\Users\\admin\\Desktop\\call_graph\\yowsup"
    #current_dir = "C:\\Users\\admin\\Desktop\\call_graph\\yowsup"
    pyfiles=[]
    for dirpath, dirnames, filenames in os.walk(current_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path=os.path.join(dirpath,filename)
                pyfiles.append(file_path)

    if not pyfiles:
        print("未找到python文件")
        sys.exit()

    for file in pyfiles:
        print("处理文件", file)
        py_file = Path(file)
        raw_tree = py_file.read_text(encoding='utf-8')
        root_node = ast.parse(raw_tree)
        # print(ast.dump(root_node))
        # astpretty.pprint(root_node)
        pb = ProcessingImport(root_node, file)  # 传入根节点
        pb.visit(root_node)

    graph.draw("StaticCG.png",prog="dot")
    graph.write("StaticCG.dot")
    dot2png.dot2png("StaticCG.dot","StaticCG.png")
    end = time.perf_counter()
    print("运行耗时: ", end - start)

if __name__ == '__main__':
    run()
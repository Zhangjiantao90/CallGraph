import ast
import data

class ProcessingPostOrder(ast.NodeVisitor):
    def __init__(self, targetnode):
        self.target = targetnode
        self.start_search = False
        data.url_value = None

    def generic_visit(self, node):
        if self.start_search == False and node == self.target:
            self.start_search = True
            print("找到原始节点",ast.dump(node))
        if self.start_search == True and isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call):
                print("使用函数的返回值赋值")
                return
            #print("某个赋值", ast.dump(node))

            if isinstance(self.target, ast.Name):
                if (isinstance(node.targets[0], ast.Name) and node.targets[0].id == self.target.id):
                    print("1找到赋值节点", ast.dump(node))
                    # print("ProcessingPostOrder:", ast.dump(node))
                    self.start_search=False
                    data.url_value = node
                    return
            elif isinstance(self.target, ast.Attribute):
                if (isinstance(node.targets[0], ast.Attribute) and node.targets[0].value.id == self.target.value.id and node.targets[0].attr == self.target.attr):
                    print("1找到赋值节点", ast.dump(node))
                    # print("ProcessingPostOrder:", ast.dump(node))
                    self.start_search=False
                    data.url_value = node
                    return

            if isinstance(node.targets[0], ast.Tuple):
                if hasattr(node.targets[0],"elts") and isinstance(node.targets[0].elts, list):
                    for x in node.targets[0].elts:
                        if self.target.id == x.id:
                            return

                elif self.target.id in node.targets[0].elts.id:
                    print("1找到赋值节点", ast.dump(node))
                    # print("ProcessingPostOrder:", ast.dump(node))
                    self.start_search=False
                    data.url_value = node
                    return

        for field, value in reversed(list(ast.iter_fields(node))):
            if isinstance(value, list):
                for item in reversed(value):
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
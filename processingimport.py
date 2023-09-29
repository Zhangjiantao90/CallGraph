import ast
import os
import data
from urllib.parse import urlparse

from processingpostorder import ProcessingPostOrder


class ProcessingImport(ast.NodeVisitor):
    def __init__(self, rootnode, nodename):
        self.parent = None
        self.root = rootnode
        data.dotID += 1
        self.dot_id = data.dotID
        self.client_node = None
        self.nodename = nodename

    def visit(self, node):
        # print("visit:", type(node).__name__)
        # set parent attribute for this node
        node.parent = self.parent
        # This node becomes the new parent
        self.parent = node
        # Do any work required by super class
        node = super().visit(node)
        # If we have a valid node (ie. node not being removed)
        if isinstance(node, ast.AST):
            # update the parent, since this may have been transformed
            # to a different node by super
            self.parent = node.parent
        return node

    def visit_Import(self, node):
        # print("Import a library:")
        for name in node.names:
            if name.name == "requests":
                print("Import: ", name.name)
            self.visit(name)
        # alias_nodes = node.names

    def visit_ImportFrom(self, node):  # 处理import
        if node.module == "urllib":
            print("ImportFrom:", node.module)
        for name in node.names:
            self.visit(name)

    def visit_alias(self, node):
        if node.name == "urllib.request":
            print("ImportAlias:", node.name)
            data.modules.append(node.name)

        if node.name == "request" and isinstance(node.parent, ast.ImportFrom) and node.parent.module == "urllib":
            print("ImportAlias:", node.name, "from", node.parent.module)
            data.modules.append(node.parent.module + "." + node.name)

    def visit_Call(self, node):
        if self.is_urllib(node) or self.is_requests(node):  # urllib.request
            # print("函数urllib.request的参数URL值为")
            # print(self.decode_node(node.args[0]))
            if self.client_node is None:
                data.graph.add_node(str(self.dot_id), labelloc="c")
                self.client_node = data.graph.get_node(str(self.dot_id))
                self.client_node.attr["label"] = os.path.basename(self.nodename)[:-3]

            print("调用函数request的节点", ast.dump(node))
            request_node = None
            if node.args:
                label = self.decode_node(node.args[0])
            elif node.keywords and node.keywords[0].arg=='url':
                label=self.decode_node(node.keywords[0].value)
            else:
                label = ""

            print("URL参数为", label)
            parsed_url = urlparse(label)
            print("parsed_url", parsed_url)
            host = parsed_url.netloc if parsed_url.netloc != '' else parsed_url.path
            print("host", host)

            nodes = data.graph.nodes()
            for item in nodes:
                if item.attr["label"] == host:
                    request_node = item

            if request_node is None:
                data.dotID += 1
                data.graph.add_node(str(data.dotID), labelloc="c")
                request_node = data.graph.get_node(str(data.dotID))
                request_node.attr["label"] = host

            if not data.graph.has_edge(self.client_node, request_node):
                print("路径",self.client_node.attr["label"],request_node.attr["label"])
                data.graph.add_edge(self.client_node, request_node, dir="forward")

    def is_requests(self, node):
        if isinstance(node.func, ast.Attribute):
            temp = node.func.value
            if isinstance(temp, ast.Name):
                if temp.id == "requests" and node.func.attr !='session':
                    return True
        return False

    def is_urllib(self, node):
        if isinstance(node.func, ast.Attribute):
            temp = node.func.value
            if isinstance(temp, ast.Attribute):
                if isinstance(temp.value, ast.Name) and temp.value.id == 'urllib' and temp.attr == 'request':
                    return True
        return False

    def decode_node(self, url_base):
        print("node类型",ast.dump(url_base))
        if isinstance(url_base, ast.Name):
            # print("ast.Name")
            return self.find_variable(url_base)
        elif isinstance(url_base, ast.Constant):
            # print("ast.Constant: ", url_base.value)
            return str(url_base.value)
        elif isinstance(url_base, ast.FormattedValue):
            # print("ast.FormattedValue")
            return self.decode_node(url_base.value)
        elif isinstance(url_base, ast.Subscript):
            # print("ast.Subscript")
            return self.decode_node(url_base.value) + "[" + self.decode_node(url_base.slice) + "]"
        elif isinstance(url_base, ast.Tuple):
            # print("ast.Tuple")
            url = ''
            for a in url_base.elts:
                url += self.decode_node(a)
            return url
        elif isinstance(url_base, ast.JoinedStr):
            # print("ast.JoinedStr")
            # An f-string, comprising a series of FormattedValue and Str nodes.
            url = ''
            for a in url_base.values:
                url += self.decode_node(a)
            return url
        elif isinstance(url_base, ast.BinOp):
            if isinstance(url_base.op, ast.Add):
                left = self.decode_node(url_base.left)
                print("左节点", left)
                right = self.decode_node(url_base.right)
                print("右节点", right)
                return left + right
        elif isinstance(url_base, ast.Attribute):
            return self.find_variable(url_base)
        else:
            return ""

    def find_variable(self, Name_node):
        if isinstance(Name_node, ast.Name):
            print("开始查找变量", Name_node.id)
            postorder = ProcessingPostOrder(Name_node)
            postorder.visit(self.root)
            if data.url_value is None:
                print("未找到赋值节点")
                return "$" + Name_node.id + "$"
            else:
                print("2找到赋值节点", ast.dump(data.url_value))
                temp = self.decode_node(data.url_value.value)
                if temp == "":
                    return "$" + Name_node.id + "$"
                else:
                    return temp
        elif isinstance(Name_node, ast.Attribute):
            print("开始查找变量", Name_node.value.id + Name_node.attr)
            postorder = ProcessingPostOrder(Name_node)
            postorder.visit(self.root)
            if data.url_value is None:
                print("未找到赋值节点")
                return "$" + Name_node.value.id + "." + Name_node.attr + "$"
            else:
                print("2找到赋值节点", ast.dump(data.url_value))
                temp = self.decode_node(data.url_value.value)
                if temp == "":
                    return "$" + Name_node.value.id + "." + Name_node.attr + "$"
                else:
                    return temp

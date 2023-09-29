import ast

class ProcessingBase(ast.NodeVisitor):
    def __init__(self):
        self.parent = None

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
            self.visit(name)
        # alias_nodes = node.names

    def visit_ImportFrom(self, node):
        if node.module=="urllib":
            print("ImportFrom:", node.module)
        for name in node.names:
            self.visit(name)

    def visit_alias(self, node):
        if node.name == "urllib.request":
            print("ImportAlias:",node.name)
        if node.name == "request" and node.parent.module=="urllib":
            print("ImportAlias:",node.name,"from",node.parent.module)


    def visit_Module(self, node):
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for stmt in ast.walk(node):
            print(stmt.__class__.__name__)

    def visit_Lambda(self, node, lambda_name=None):

        self.visit(node.body)

    def visit_For(self, node):
        for item in node.body:
            self.visit(item)

    def visit_Dict(self, node):
        for key, val in zip(node.keys, node.values):
            if key:
                self.visit(key)
            if val:
                self.visit(val)

    def visit_List(self, node):
        for elt in node.elts:
            self.visit(elt)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_ClassDef(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def visit_Tuple(self, node):
        for elt in node.elts:
            self.visit(elt)

    def _handle_assign(self, decoded):
        return

    def _visit_return(self, node):
        if not node or not node.value:
            return
        self.visit(node.value)
        self._handle_assign(self.decode_node(node.value))

    def _visit_assign(self, value, targets):
        self.visit(value)

    def decode_node(self, node):
        if isinstance(node, ast.Name):
            return
        elif isinstance(node, ast.Call):
            return
        elif isinstance(node, ast.Lambda):
            return
        elif isinstance(node, ast.Tuple):
            return
        elif isinstance(node, ast.BinOp):
            return
        elif isinstance(node, ast.Attribute):
            return
        elif isinstance(node, ast.Num):
            return [node.n]
        elif isinstance(node, ast.Str):
            return [node.s]
        elif self._is_literal(node):
            return [node]
        elif isinstance(node, ast.Dict):
            return
        elif isinstance(node, ast.List):
            return
        elif isinstance(node, ast.Subscript):
            return
        return []

    def _is_literal(self, item):
        return isinstance(item, int) or isinstance(item, str) or isinstance(item, float)

    def _retrieve_base_names(self, node):
        return

    def _retrieve_parent_names(self, node):
        return

    def _retrieve_attribute_names(self, node):
        return

    def iterate_call_args(self, defi, node):
        for pos, arg in enumerate(node.args):
            self.visit(arg)

    def retrieve_subscript_names(self, node):
        if not isinstance(node, ast.Subscript):
            raise Exception("The node is not an subcript")
        return

    def retrieve_call_names(self, node):
        names = set()
        if isinstance(node.func, ast.Name):
            return

    def analyze_submodules(self, cls, *args, **kwargs):
        return

    def analyze_submodule(self, cls, imp, *args, **kwargs):
        return

    def add_ext_mod_node(self, name):
        return

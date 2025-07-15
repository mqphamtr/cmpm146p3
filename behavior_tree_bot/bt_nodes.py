from copy import deepcopy
import logging

def log_execution(fn):
    def logged_fn(self, state):
        logging.debug('Executing:' + str(self))
        result = fn(self, state)
        logging.debug('Result: ' + str(self) + ' -> ' + ('Success' if result else 'Failure'))
        return result
    return logged_fn

############################### Base Classes ##################################
class Node:
    def __init__(self):
        raise NotImplementedError

    def execute(self, state):
        raise NotImplementedError

    def copy(self):
        return deepcopy(self)

############################### Composite Base Class ##################################
class Composite(Node):
    def __init__(self, child_nodes=[], name=None):
        self.child_nodes = child_nodes
        self.name = name

    def execute(self, state):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.name if self.name else self.__class__.__name__

    def tree_to_string(self, indent=0, visited=None):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return '| ' * indent + '[CYCLE DETECTED: ' + str(self) + ']\n'
        visited.add(id(self))

        string = '| ' * indent + str(self) + '\n'
        for child in self.child_nodes:
            if hasattr(child, 'tree_to_string'):
                string += child.tree_to_string(indent + 1, visited)
            else:
                string += '| ' * (indent + 1) + str(child) + '\n'
        return string

############################### Composite Nodes ##################################
class Selector(Composite):
    @log_execution
    def execute(self, state):
        for child_node in self.child_nodes:
            if child_node.execute(state):
                return True
        return False

class Sequence(Composite):
    @log_execution
    def execute(self, state):
        for child_node in self.child_nodes:
            if not child_node.execute(state):
                return False
        return True

############################### Leaf Nodes ##################################
class Check(Node):
    def __init__(self, check_function):
        self.check_function = check_function

    @log_execution
    def execute(self, state):
        return self.check_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.check_function.__name__

    def tree_to_string(self, indent=0, visited=None):
        return '| ' * indent + str(self) + '\n'

class Action(Node):
    def __init__(self, action_function):
        self.action_function = action_function

    @log_execution
    def execute(self, state):
        return self.action_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.action_function.__name__

    def tree_to_string(self, indent=0, visited=None):
        return '| ' * indent + str(self) + '\n'

############################### Decorators ##################################
class LoopUntilFail(Node):
    def __init__(self, child, max_iterations=10):
        self.child = child
        self.max_iterations = max_iterations

    @log_execution
    def execute(self, state):
        count = 0
        while count < self.max_iterations:
            if not self.child.execute(state):
                return True
            count += 1
        return True

    def __str__(self):
        return f'LoopUntilFail (max {self.max_iterations})'

    def tree_to_string(self, indent=0, visited=None):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return '| ' * indent + '[CYCLE DETECTED: ' + str(self) + ']\n'
        visited.add(id(self))

        string = '| ' * indent + str(self) + '\n'
        if hasattr(self.child, 'tree_to_string'):
            string += self.child.tree_to_string(indent + 1, visited)
        else:
            string += '| ' * (indent + 1) + str(self.child) + '\n'
        return string

class Inverter(Node):
    def __init__(self, child):
        self.child = child

    @log_execution
    def execute(self, state):
        return not self.child.execute(state)

    def __str__(self):
        return 'Inverter'

    def tree_to_string(self, indent=0, visited=None):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return '| ' * indent + '[CYCLE DETECTED: ' + str(self) + ']\n'
        visited.add(id(self))

        string = '| ' * indent + str(self) + '\n'
        if hasattr(self.child, 'tree_to_string'):
            string += self.child.tree_to_string(indent + 1, visited)
        else:
            string += '| ' * (indent + 1) + str(self.child) + '\n'
        return string

class AlwaysSucceed(Node):
    def __init__(self, child):
        self.child = child

    @log_execution
    def execute(self, state):
        self.child.execute(state)
        return True

    def __str__(self):
        return 'AlwaysSucceed'

    def tree_to_string(self, indent=0, visited=None):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return '| ' * indent + '[CYCLE DETECTED: ' + str(self) + ']\n'
        visited.add(id(self))

        string = '| ' * indent + str(self) + '\n'
        if hasattr(self.child, 'tree_to_string'):
            string += self.child.tree_to_string(indent + 1, visited)
        else:
            string += '| ' * (indent + 1) + str(self.child) + '\n'
        return string

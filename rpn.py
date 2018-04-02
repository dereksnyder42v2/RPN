#!/usr/local/Cellar/python/3.6.4_4/bin/python

class Stack:
    def __init__(self):
        self.contents = []
        self.index = 0
    def push(self, val):
        self.contents.append(val)
        self.index += 1
        return
    def pop(self):
        if self.index == 0:
            raise IndexError
            #
        else:
            self.index -= 1
            return self.contents.pop()
    def peek(self):
        if self.index == 0:  
            raise IndexError
        else:
            return self.contents[-1]
    '''# LOL, overcomplicated this a bit :D
    def __len__(self):
        if self.index != 0:
            self.index -= 1
            return 1 + len(self)
        else:
            return 0
    '''
    '''
    def __len__(self):
        from copy import deepcopy
        def l(s):
            if s.index != 0:
                s.index -= 1
                return 1 + l(s)
            else:
                return 0
        return l(deepcopy(self))
    '''
    def __len__(self):
        return self.index

class Node:
    def __init__(self, contents):
        self.left = None
        self.right = None
        self.contents = contents

    def eval(self):
        # TODO
        if Node.isOp(self.contents):
            return Node.ops()[self.contents](self.right.eval(), self.left.eval())
        elif self.isNumber(self.contents):
            return float(self.contents)
        else:
            raise Exception

    def clone(self, toNode):
        toNode.left = self.left
        toNode.right = self.right
        toNode.contents = self.contents
        return toNode
   
    @staticmethod
    def ops():
        return {
                '+': lambda x, y: x + y,
                '-': lambda x, y: x - y,
                '*': lambda x, y: x * y,
                '/': lambda x, y: x / y,
                '^': lambda x, y: x ** y
        }

    @staticmethod
    def isOp(val):
        if val in Node.ops():
            return True
        else:
            return False       

    @staticmethod
    def isNumber(val):
        try:
            float(val)
        except:
            return False
        else:
            return True

class Tree:
    def __init__(self):
        self.stack = Stack()
    
    def pushNumber(self, val):
        tempNode = Node(val)
        tempNode.left = None
        tempNode.right = None
        
        self.stack.push(tempNode)

    def pushOp(self, op):
        tempNode = Node(op)
        tempNode.left = self.stack.pop()
        tempNode.right = self.stack.pop()

        self.stack.push(tempNode)
    
    def evaluate(self):
        tempNode = Node(self.stack.peek().contents)
        tempNode.left = self.stack.peek().left
        tempNode.right = self.stack.peek().right

        return tempNode.eval()


if __name__ =='__main__':
    '''
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print('IF you take a peek, the top of the stack is', stack.peek())
    print('The size of the stack is', len(stack))
    while True:
        print(stack.pop())
    print('The size of the stack is now', len(stack))
    '''
    # --< Example >--
    # 1 2 + -1 * 2 ^
    #
    # equivalent to,
    # ((1 + 2) * -1) ^ 2 
    #                   --> 9
    '''
    tree = Tree()
    tree.pushNumber('1')
    tree.pushNumber('2')
    tree.pushOp('+')
    tree.pushNumber('-1')
    tree.pushOp('*')
    tree.pushNumber('2')
    tree.pushOp('^')
    print('Result is', tree.evaluate())
    '''

    # TODO Add support for reading an operand from pipe
    # TODO Write to stderr and quit(0) if error occurs

    import sys
    
    print('Evaluating \'%s\'' % ' '.join(sys.argv[1:]) )

    exprTree = Tree()
    for i in range(1, len(sys.argv)  ):
        if sys.argv[i] in ['+', '-', '*', '/', '^']:
            exprTree.pushOp( sys.argv[i] )
        else:
            try:
                float( sys.argv[i] )
            except:
                print('\'%s\' is not a valid number or operator.' % sys.argv[i] )
                quit(-1)
            else:
                exprTree.pushNumber( sys.argv[i] )
    print( exprTree.evaluate() )
    
    

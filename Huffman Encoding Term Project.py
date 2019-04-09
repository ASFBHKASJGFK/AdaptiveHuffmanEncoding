import numpy as np
from tkinter import *
import tkinter.messagebox
import queue
import copy

#node class used for building tree
class Node():
    def __init__(self, char, number, left=None, right=None, parent = None):
        self.char = char  # The node character
        self.number = number # number of times character occurs
        self.left = left    # Left child
        self.right = right  # Right child
        self.parent = parent #parent
        
    def size(self):
        sizenumber = 1
        if self.left is not None:
            i = self.left.size()
            sizenumber += i
        if self.right is not None:
            i = self.right.size()
            sizenumber += i
        return sizenumber

    def height(self):
        leftH = 0
        rightH = 0
        if self.left is not None:
            leftH += 1
            leftH += self.left.height()
        if self.right is not None:
            rightH += 1
            rightH += self.right.height()
        if leftH > rightH:
            return leftH
        else:
            return rightH
            
    
    def printNode(self):
        print(self.char + " X " + str(self.number) + ";")

#ADAPTIVE huffman tree Class
class AdaptiveTree:
    def __init__(self):
        self.zero_node = Node(char="zero", number = 0)   #node to be paired to every new character 
        self.root = self.zero_node    #root node
        self.nodes = [] #list of nodes in adaptive tree          
        
    def insert(self,char):
    
        #check the node already in list of current nodes
        new_node = None
        for node in self.nodes:
            if node.char == char:
                new_node = node
            
            
        #if char is new, insert in tree together with zero_node
        if new_node is None:
        
            #create new node
            new_node = Node(char=char, number=1)
            #parent of zero_node and new_node, its parent node will be the current parent of zero_node
            new_parent = Node(char=".../", number=1, left=self.zero_node, right=new_node, parent=self.zero_node.parent)
       
            new_node.parent = new_parent
            self.zero_node.parent = new_parent
            
            #if zero_node has no previous parent, it means it was previously the root
            #new_parent will be the new root
            if new_parent.parent is None:
                self.root = new_parent
            #if zero_node previous parent exist--means new_parent is now left child of previous parent of zero_node
            else:
                new_parent.parent.left = new_parent
                
            #insert new nodes into nodes list
            self.nodes.insert(0,new_parent)
            self.nodes.insert(0,new_node)         
                
            
            #inserted character, need to update the tree up to the root
            #start updating at the level of the new_parent
            new_node = new_parent.parent
        
        
        #if char is already seen, update the tree at current node
        
        #update tree 
        while new_node is not None:
        
            #find next node with equivalent_node number to new_node
            equivalent_node = self.find_equivalent_node_node(new_node.number)

            #if new_node is not currently the largest or new_node is not connected to equivalent_node, swap the nodes
            if (new_node is not equivalent_node and new_node is not equivalent_node.parent and equivalent_node is not new_node.parent):
                self.swap_nodes(new_node, equivalent_node)
            
         
            new_node.number = new_node.number + 1
            new_node = new_node.parent
       

       
       
    #find  node with similar weight in lsit of current nodes 
    #start searching nodes with equivalent numbers first    
    def find_equivalent_node_node(self, number):
        for node in reversed(self.nodes):
            if node.number == number:
                return node   
         

    
    #sawp two nodes from the AdaptiveTree
    def swap_nodes(self, node1, node2):
    
        #index of nodes
        index1 = self.nodes.index(node1)
        index2 = self.nodes.index(node2)
        
        #switch the nodes in the current list of nodes
        self.nodes[index1], self.nodes[index2] = self.nodes[index2], self.nodes[index1]
        
        #update the node parents
        node1_prev_parent = node1.parent
        node1.parent = node2.parent
        node2.parent = node1_prev_parent

        
        #update the node children of the updated parents
        #ex.if node1 was a left child--set node1 as left child of node1's new parent
        
        #if node1 was a left child
        if node1.parent.left is node2:
            node1.parent.left = node1
        #if node1 was a right child
        else:
            node1.parent.right = node1

            
        #if node2 was a left child
        if node2.parent.left is node1:
            node2.parent.left = node2
        #if node2 was a right child
        else:
            node2.parent.right = node2

#function used to build tree
def drawTree(root, x, y, nodeNumber, offset):
    if len(root.char) > 5:
        s = root.char[0:4] + "..." + " X " + str(root.number)
        msg = "Node " + str(nodeNumber) + "\n" + s
    else:
        msg = "Node " + str(nodeNumber) + "\n" + root.char + " X " + str(root.number)    
    drawNode(msg, x, y)
    nodeNumber += 1
    if root.left is not None:
        canvas.create_line(x-40, y, x-(200*offset), y+65)
        drawTree(root.left, x-(200*offset), y+100,nodeNumber,offset*1/2)
        nodeNumber += root.left.size()
    if root.right is not None:
        canvas.create_line(x+40, y, x+(200*offset), y+65)
        drawTree(root.right, x+(200*offset), y+100, nodeNumber, offset*1/2)
        nodeNumber += root.right.size()
    
#function to draw node
def drawNode(msg, x, y):
    circle = create_circle(x,y+5,40,canvas)
    canvas.create_text(x,y, text=msg)
    
#function to draw circle
def create_circle(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1)

#function to check if character is in the nodelist yet
def isCharInList(character,nodelist):
    i = 0
    while i < len(nodelist):
        if nodelist[i].char == character:
            return True
        i += 1
    return False

#put letters into the nodelist as nodes
def entryToList(string):
    nodelist = []
    for character in string:
        if isCharInList(character, nodelist) == False:
            newNode = Node(character, 1)
            nodelist.append(newNode)
        else:
            i = 0
            while i < len(nodelist):
                if nodelist[i].char == character:
                    break
                i += 1
            nodelist[i].number += 1
    return nodelist


#print the nodes in the nodelist
def printNodelist(nodelist):
    for x in nodelist:
        x.printNode()

#fuction to take nodelist and create a huffman tree
def createHuffmanTree(nodelist):
    while len(nodelist) > 1:
        #order the nodes ascendingly based on frequency/value
        nodelist.sort(key=lambda x: x.number, reverse=False)
        #printNodelist(nodelist)
        node_list_copy = copy.copy(nodelist)
        low_1_tuple = node_list_copy[0]
        low_2_tuple = node_list_copy[1]
        newNode = Node(low_1_tuple.char + "/"+ low_2_tuple.char,low_1_tuple.number + low_2_tuple.number,low_1_tuple, low_2_tuple)
        nodelist.pop(0)
        nodelist.pop(0)
        nodelist.append(newNode)
        #printNodelist(nodelist)

    return nodelist[0]



#explore tree iteratively, left first--DFS
def decodeHuffman(node, code, prefix = ""):

    
    #check if node has left children
    if (node.left != None):
        decodeHuffman(node.left, code, prefix + "0")
    #if no left child, means this is a leaf node
    else:
        code[node.char] = prefix
        return
        
     
    #check if node has right children
    if (node.right != None):
        decodeHuffman(node.right, code, prefix + "1")
    #if no right child, means this is a leaf node
    else:
        code[node.char] = prefix
        return
    
    return code

def createTable(codes):
    size = len(codes)
    codes_copy = codes
    width = 50
    length = 30
    i = 0
    canvas.create_text(width + 10, 25, text="Code Table")
    while i < size:
        y = i * length + 35
        j = 0
        string = codes_copy.popitem()
        while j < 2:
            x = j * width + 10
            canvas.create_rectangle(x, y, x + width, y + length)
            if(j == 0):
                canvas.create_text(x+ width/2, y + length/2, text=string[0])
            else:
                canvas.create_text(x + width/2, y + length/2, text=string[1:])
            j += 1
        i+=1

def buildTree():#testing button and stuff
    global PREV#global variable to save last input
    
    s = string.get()#get input

    #check to see if input is larger that 1 character
    if len(s) <= 1:
        tkinter.messagebox.showinfo("Invalid Input", "Tree must be larger than 1 Node. Please input at least 2 characters.")
        return -1
    
    nodelist = entryToList(s)#makes letters into nodes
    rootNode = createHuffmanTree(nodelist)#create huffman tree

    #check to see if tree exceeds height of 4
    if rootNode.height() > 4:
        tkinter.messagebox.showinfo("Invalid Input", "Sorry. The height of the tree exceeds 4, so tree cannot be built.")
        canvas.pack_forget()#delete tree
        return -1
    
    canvas.pack()#make canvas display

    #information for where to draw tree
    nodeNumber = 1
    offset = 2
    x = 950
    y = 50
    
    canvas.delete("all")#make sure canvas is clear
    drawTree(rootNode,x,y, nodeNumber, offset)#draw tree
    code = {}#where to store codes
    codes = decodeHuffman(rootNode, code)#get codes for each letter
    createTable(codes)#draw table
    PREV = s#save character list

def buildAdaptiveTree():#testing button and stuff
    global TREE#global variable to save last input
    
    s = string2.get()#get input

    #check to see if input is larger that 1 character
    if len(s) < 1:
        tkinter.messagebox.showinfo("Invalid Input", "Please input at least 1 character.")
        return -1

    #instance of adaptive tree, using FGK algorithm
    TREE = AdaptiveTree()
    #encode each character one by one
    for char in s:
        TREE.insert(char)

    #getting root node
    rootNode = TREE.nodes[-1]
    
    #check to see if tree exceeds height of 4
    if rootNode.height() > 4:
        tkinter.messagebox.showinfo("Invalid Input", "Sorry. The height of the tree exceeds 4, so tree cannot be built.")
        return -1
    
    canvas.pack()#make canvas display

    #information for where to draw tree
    nodeNumber = 1
    offset = 2
    x = 950
    y = 50
    
    canvas.delete("all")#make sure canvas is clear
    drawTree(rootNode,x,y, nodeNumber, offset)#draw tree
    code = {}#where to store codes
    codes = decodeHuffman(rootNode, code)#get codes for each letter
    createTable(codes)#draw table

def addNodeToTreeAdaptive():
    global TREE#global variable to save last input
    
    s = string2.get()#get input

    #check to see if input is  1 character
    if len(s) != 1:
        tkinter.messagebox.showinfo("Invalid Input", "Please input 1 and only 1 character.")
        return -1

    TREE.insert(s)#encode the character

    rootNode = TREE.nodes[-1]
    
    #check to see if tree exceeds height of 4
    if rootNode.height() > 4:
        tkinter.messagebox.showinfo("Invalid Input", "Sorry. The height of the tree exceeds 4, so tree cannot be built.")
        return -1
    
    canvas.pack()#make canvas display

    #information for where to draw tree
    nodeNumber = 1
    offset = 2
    x = 950
    y = 50
    
    canvas.delete("all")#make sure canvas is clear
    drawTree(rootNode,x,y, nodeNumber, offset)#draw tree
    code = {}#where to store codes
    codes = decodeHuffman(rootNode, code)#get codes for each letter
    createTable(codes)#draw table

def addNodeToTree():
    global PREV#global variable to save last input

    #check to see if a tree exists
    if len(PREV) <= 1 or PREV == None:
        tkinter.messagebox.showinfo("Invalid Input", "Cannot add node to an empty tree, Please build a tree first.")
        return -1
    
    s = string.get()#get input
    if len(s) < 1:
        tkinter.messagebox.showinfo("Invalid Input", "Please input at least 1 character.")
    prevString = PREV + s#add it to old list
    nodelist = entryToList(prevString)#makes letters into nodes
    rootNode = createHuffmanTree(nodelist)#create huffman tree

    #check to see if tree exceeds height of 4
    if rootNode.height() > 4:
        tkinter.messagebox.showinfo("Invalid Input", "Sorry. The height of the tree exceeds 4, so tree cannot be built.")
        return -1
    
    canvas.pack()#make canvas display

    #information for where to draw tree
    nodeNumber = 1
    offset = 2
    x = 950
    y = 50
    
    canvas.delete("all")#make sure its clear
    drawTree(rootNode,x,y, nodeNumber, offset)#draw tree
    code = {}#where to store codes
    codes = decodeHuffman(rootNode, code)#get codes for each letter
    createTable(codes)#draw table
    PREV = prevString#save character list

def clearCanvas():
    canvas.forget()

########
#START HERE
########

#global variables to hold the last entry
PREV = ""
#instance of adaptive tree, using FGK algorithm; also used as a global variable to save entries
TREE = AdaptiveTree()

#my window
root = Tk()

#my frames
titleFrame = Frame(root)
entryFrame = Frame(root)
buttonFrame = Frame(root)
entry2Frame = Frame(root)
button2Frame = Frame(root)

titleFrame.pack()
entryFrame.pack()
buttonFrame.pack()
entry2Frame.pack()
button2Frame.pack()
#my canvas
canvas = Canvas(root, width=1900, height=600)

#title of window
root.title("Huffman Encoding")
#title + entrybox + button
title = Label(titleFrame, text="Huffman Encoding", font=("",22))
label = Label(entryFrame, text="Please enter character(s) for Huffman Encoding: ")
string = StringVar()#entry saved in string
entry = Entry(entryFrame, textvariable=string)
label2 = Label(entry2Frame, text="Please enter character(s)for Adaptive Huffman Encoding: ")
string2 = StringVar()#entry saved in string
entry2 = Entry(entry2Frame, textvariable=string2)
#packing title + entry + button
title.pack(side=TOP,pady=5)
label.pack(side=LEFT,pady=5,padx=10)
entry.pack(side=LEFT,pady=5,padx=10)
label2.pack(side=LEFT,pady=5,padx=10)
entry2.pack(side=LEFT,pady=5,padx=10)
button1 = Button(buttonFrame, text="Build Huffman Tree",command= buildTree)
button1.pack(side=LEFT, pady=10,padx=7)
button2 = Button(button2Frame, text="Build Adaptive Huffman Tree",command= buildAdaptiveTree)
button2.pack(side=LEFT, pady=10, padx=7)
button3 = Button(buttonFrame, text="Add Character(s)",command=addNodeToTree)
button3.pack(side=LEFT, pady=10, padx=7)
button4 = Button(button2Frame, text="Add Character",command=addNodeToTreeAdaptive)
button4.pack(side=LEFT, pady=10, padx=7)
clearButton = Button(buttonFrame, text="Clear Canvas", command=clearCanvas)
clearButton.pack(side=LEFT, pady=10, padx=7)
clearButton2 = Button(button2Frame, text="Clear Canvas", command=clearCanvas)
clearButton2.pack(side=LEFT, pady=10, padx=7)

root.mainloop()#run window

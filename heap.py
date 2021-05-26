import sys
class myHeap:
    def __init__(self):
        self.Heap = [[sys.maxsize, 0]] # stores a list of [priority, ID] pairs
        self.root = 1
        self.current_size = 0
        self.tracker = {}

    def swapNode(self, node1, node2):
        self.Heap[node1][0], self.Heap[node2][0] = self.Heap[node2][0], self.Heap[node1][0] # swap priority
        self.Heap[node1][1], self.Heap[node2][1] = self.Heap[node2][1], self.Heap[node1][1] # swap ID

    def swapID(self, ID1, ID2):
        self.tracker[ID1],  self.tracker[ID2] = self.tracker[ID2],  self.tracker[ID1] #swap ID

    def keepHeap(self, nNode):
        parent = nNode // 2

        #if prioity of a node is higher than its parent, it needs to be swapped until it isn't
        if self.Heap[nNode][0] > self.Heap[parent][0]:
            tempChild  = nNode
            tempParent = tempChild // 2
            #as long as cureent node has larger priority than parent, swap it
            while self.Heap[tempChild][0] > self.Heap[tempParent][0]:
                child_ID = self.Heap[tempChild][1]
                parent_ID = self.Heap[tempParent][1]

                self.swapNode(tempChild, tempParent)
                self.swapID(self.Heap[tempChild][1], self.Heap[tempParent][1])
                tempChild  = tempParent
                tempParent = tempChild // 2

        else:
            #loop until node does not have children
            while nNode*2 <= self.current_size:
                
            # while not nNode > (self.current_size //2):
                current_node = nNode
                leftChild = current_node * 2
                rightChild = leftChild + 1

                

                #if we can swap left child with parent, do it
                if self.Heap[current_node][0] < self.Heap[leftChild][0]: #see if we have to swap with left child
                    self.swapNode(current_node, leftChild)
                    self.swapID(self.Heap[current_node][1], self.Heap[leftChild][1])
                    nNode *= 2

                #if we can swap children, do it
                if rightChild <= self.current_size: #see if we have to swap with right child
                    if self.Heap[leftChild][0] < self.Heap[rightChild][0] and self.Heap[current_node][0] < self.Heap[rightChild][0]:
                        self.swapNode(current_node, rightChild)
                        self.swapID(self.Heap[current_node][1], self.Heap[rightChild][1])
                        nNode = 2*nNode + 1
                else:
                    break


    def push(self, priority, uniqueID):
        if self.tracker.__contains__(uniqueID):
            print("Invalid entry", uniqueID, "already in heap")
            return

        self.current_size +=1
        self.Heap.append([priority, uniqueID]) #places it at the bottom of the tree
        current = self.current_size
        self.tracker[uniqueID] = self.current_size

        #swap node with parent if greater than parent
        while self.Heap[current][0] > self.Heap[current // 2][0]:
            current_ID = self.Heap[current][1]
            parent_ID = self.Heap[current // 2][1]

            self.swapNode(current, current//2)
            self.swapID(parent_ID, current_ID)
            current = current//2 #check node again

    def pop(self):
        
        output = self.Heap[self.root][1]     # Record the value at the root.
        del self.tracker[self.Heap[self.root][1]]    # Delete this value's entry in the logs.
            
        # If the value is not the last in the list, swap it with element at the end and check heap properties. In both cases, head size should be
        # decremented.
        if self.current_size != self.root:
            
            self.tracker[self.Heap[self.current_size][1]] = self.root   # Update the log of the value previously at the end of the list.
            self.swapNode(self.root, self.current_size)
            self.current_size -= 1
            self.keepHeap(self.root)
        else:
            self.current_size -= 1
        return output   # Return the output.
    
    def remove(self, uniqueID):
        if self.tracker.__contains__(uniqueID):
            index = self.tracker[uniqueID] #pull index from the tracker 
            del self.tracker[uniqueID] # delete removed entry

            if index != self.current_size: # if index it wasn't the last value in the heap reform the tracker and perform keepHeap
                self.tracker[self.Heap[self.current_size][1]] = index
                self.swapNode(index, self.current_size) 
                self.keepHeap(index)

            self.current_size -=1
        else:
            print(uniqueID, "not present!")
            return
    
    def isEmpty(self):
        return self.current_size == 0

heap = myHeap()
heap.push(7, 2)
heap.push(15, 3)
heap.push(9, 4)
heap.push(4, 5)
heap.push(13, 6)
for _ in range(5):
    print(heap.pop())

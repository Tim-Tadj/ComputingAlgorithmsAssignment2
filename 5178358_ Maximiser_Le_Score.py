import sys
import os
import time

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

                self.swapNode(tempChild, tempParent) #swap the actual node
                self.swapID(child_ID, parent_ID) #swap the ID
                tempChild  = tempParent # reapeat considreing the swapped node
                tempParent = tempChild // 2

        else:
            #loop until node does not have children
            
            while nNode*2 <= self.current_size:
                if ((2 * nNode) + 1) > self.current_size: #only consider left child if there is no right child
                    parent = self.Heap[nNode]
                    LeftChild = self.Heap[2 * nNode]
                    
                    # If the left child has greater priority than parent, swap them. Otherwise, break.
                    if LeftChild[0] > parent[0] :
                        self.swapID(parent[1], LeftChild[1]) # Swap the ID.
                        self.swapNode(nNode, 2*nNode) #swap actual node
                        nNode *= 2  # reapeat considreing the swapped node
                    
                    else:
                        break
                
                # Else if there is a left and right child.
                else:
                    parent = self.Heap[nNode]
                    LeftChild = self.Heap[2 * nNode]
                    RightChild = self.Heap[(2 * nNode) + 1]
                    
                    # check to see if a swap is nessesary
                    if parent[0] < LeftChild[0] or parent[0] < RightChild[0]:
                        
                        # Swap the largest child with the parent
                        if LeftChild[0] < RightChild[0]:
                            self.swapID(parent[1], RightChild[1]) # Swap the ID.       # Swap the logs.
                            self.swapNode(nNode, 2*nNode+1) #swap actual node
                            nNode = 2 * nNode + 1   # reapeat considreing the swapped node
                            
                        else:
                            self.swapID(parent[1], LeftChild[1]) # Swap the ID.
                            self.swapNode(nNode, 2*nNode) #swap actual node
                            nNode *= 2  # reapeat considreing the swapped node
                            
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
                self.current_size -=1
                self.keepHeap(index)
            else:
                self.current_size -=1
        else:
            print(uniqueID, "not present!")
            return
    
    def isEmpty(self):
        return self.current_size == 0


def sumDigits(num):
    result = 0
    while num >=10:
        result += num%10
        num = num // 10
    return result + num

def doProgram(nBalls, maxTurnsPerRound, balls, coinResult):
    rustyHeap = myHeap()
    scottHeap = myHeap()
    rustysBalls = []
    scottsBalls = []

    ballID = 0
    for ball in balls:
        scottHeap.push(ball, ballID)
        rustyHeap.push(sumDigits(ball), ballID)
        ballID += 1

    isRustyRound = False
    if coinResult == "TAILS":
        print("rusty starts")
        isRustyRound = True

    turnNum = 1
    for _ in range(nBalls):
        if isRustyRound:
            #do rustys turn
            poppedBallID = rustyHeap.pop()
            scottHeap.remove(poppedBallID)
            rustysBalls.append(balls[poppedBallID])
            print("rustys choice:", balls[poppedBallID])
        else:
            #do scotts turn
            poppedBallID = scottHeap.pop()
            rustyHeap.remove(poppedBallID)
            scottsBalls.append(balls[poppedBallID])
            print("scotts choice:", balls[poppedBallID])

        if turnNum % maxTurnsPerRound == 0:
            isRustyRound = not isRustyRound
        turnNum +=1
    
    return sum(scottsBalls), sum(rustysBalls)

with open(os.path.join(sys.path[0], "inputLeScore.txt"), "r") as openf: 
    with open(os.path.join(sys.path[0], "outputLeScore.txt"), "w") as ouputf:
        nTestCases = int(openf.readline().rstrip())

        for nCase in range(nTestCases):
            nBalls, maxTurnsPerRound = [int(b) for b in openf.readline().rstrip().split()]
            balls = [int(b) for b in openf.readline().rstrip().split()]
            coinResult = openf.readline().rstrip()

            print("Attempting case", nCase+1)

            start_time = time.perf_counter()
            result = doProgram(nBalls, maxTurnsPerRound, balls, coinResult)
            finish_time = time.perf_counter()
            print("Completed Case", nCase+1, "in", finish_time - start_time, "s")

            for score in result:
                print(score, end = " ", file= ouputf)
            print(file = ouputf)

            
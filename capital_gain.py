
# coding: utf-8

# In[24]:

'''Abhinav R. Pandey
   Project 1 (Part 2)
   capital_gain.py 
'''

class Empty(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class ArrayQueue:
    '''FIFO queue implementation using a Python list as underlying storage. Code source: Data Structures and Algorithms 
       in Python, pg. 243. 
    '''
    
    DEFAULT_CAPACITY = 10 #moderate capacity for all new queues. 
    
    def __init__(self):
        '''Create an empty sequence. 
        '''
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY   
        self._purchase_price = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._shares_bought = 0
        self._size = 0 
        self._front = 0 
        self._capgain = 0 
    
    def __len__(self):
        '''Return the number of elements in the queue. 
        '''
        return self._size
    
    def is_empty(self):
        '''Return True if the queue is empty. 
        '''
        return self._size == 0 
    
    def first(self):
        '''Return (but do not remove) the element at the front of the queue.
           Raise Empty exception if the queue is empty.
        '''
        if self.is_empty():
            raise Empty("queue is empty")
        return self._data[self._front]
    
    def dequeue(self):
        '''Remove and return the first element of the queue (i.e., FIFO).
           Raise Empty exception if the queue is empty.
        '''
        if self.is_empty():
            raise Empty("queue is empty")
        answer = self._data[self._front]
        self._data[self._front] = None #Help garbage collection. 
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1 
        return answer 
    
    def enqueue(self,e):
        '''Add element to the back of the queue. 
        '''
        if self._size == len(self._data):
            self._resize(2*len(self._data))   #Double the array size for the buy queue if needed. 
            self._resize(2*len(self._purchase_price))   #Double the array size for the purchase price queue if needed.    
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e[0]
        self._shares_bought = e[0] + self._shares_bought
        self._purchase_price[avail] = e[1]
        self._size += 1

    def _resize(self,cap):
        '''Resize to a new list of capacity >= len(self)
        '''
        old = self._data
        self._data = [None]*cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0
    
    def sell_shares(self, sell):
        '''Sell the shares when sell command is read in the input file. Update the overall capital gain as well.
        '''
        current_gain = 0      # Current gain/loss on this specific transaction. 
        sell_amount = sell[0]  # Amount of shares being sold, read from the input file. 
        sell_price_share = sell[1] #Price of shares being sold, read from the input file. 
        
        for i in range(len(self._data)):
            if type(self._data[i]) == int:  # Avoid considering elements of None type. 
                    if sell_amount > self._data[i]:
                        current_gain = self._data[i]*(sell_price_share - self._purchase_price[i]) #Find capital gain on the bought shares. 
                        sell_amount = sell_amount - self._data[i]  # Update the number of shares that still need to be sold. 
                        self._capgain += current_gain   # Update the overall capital gain/loss. 
                    else: 
                        current_gain = sell_amount*(sell_price_share - self._purchase_price[i])  #Sell the remaining number of shares needed to be sold.  
                        self._capgain += current_gain # Update overall capital gain/loss
                        sell_amount = 0   # Reset sell_amount for next sell_shares call. 
        return (self._capgain) # Return the capital gain. 
        
    
def capital_gain(file_name):
    '''Function that reads the input files, and either adds the bought shares with their respective prices to the queue
       or calls the sell_shares function. 
    '''
    
    myArray = ArrayQueue()
    with open(file_name,'r') as f:
        for line in f:      # Open file and read it line by line. 
            word_list = (line.split())
            if word_list[0] == "buy":  #When the first word encountered is 'buy', queue the order. 
                
                if myArray.__len__() % 10 == 0:      #If queue is full, resize it. 
                    myArray._resize(2*myArray.__len__())
                        
                num_shares_bought = int(word_list[1])   
                buy_price = int(word_list[4])
                buy = [num_shares_bought, buy_price]
                myArray.enqueue(buy)

            elif word_list[0] == "sell":    #When the first word encountered is "sell", call the sell_shares function. 
                num_shares_sold = int(word_list[1])
                sell_price = int(word_list[4])
                sell = [num_shares_sold, sell_price]
                myArray.sell_shares(sell)

            else:
                raise TypeError("File input error!")
                
    return myArray.sell_shares((0,0))      



if __name__ == "__main__":
    '''This is my test code, using the four files given in the project-1 PDF. 
    '''
    print ("Capital gain is: ", capital_gain("file1.dat"))
    print ("Capital gain is: ", capital_gain("file2.dat"))
    print ("Capital gain is: ", capital_gain("file3.dat"))
    print ("Capital gain is: ", capital_gain("file4.dat"))


# In[ ]:




# In[ ]:




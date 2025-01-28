from enum import Enum

class LRUCache(object):
    
    class DataIndex(Enum):
        Data = 0
        Age = 1
        Key = 2
    
    class Operation(Enum):
        Put = 0
        Get = 1
        Replace = 2
        
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self._dataFromKey:dict = {}
        self._dataFromAge:dict = {}
        # self._ages:list[int] = [0 for _ in range(capacity)]
        self._newestAge:int = 0
        self._oldestAge:int = -1
        self._capacity:int = capacity

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        
        if not key in self._dataFromKey: return -1
        
        dataItem:list = self._dataFromKey[key]
        
        oldAge:int = dataItem[self.DataIndex.Age.value]
        del self._dataFromAge[oldAge]
        
        newAge:int = self._updateNewestOldestAge(self.Operation.Get, dataItem[self.DataIndex.Age.value])
        dataItem[self.DataIndex.Age.value] = newAge
        self._dataFromAge[newAge] = dataItem
        
        return dataItem[self.DataIndex.Data.value]
        
    
    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self._dataFromKey:
            newAge:int = self._updateNewestOldestAge(self.Operation.Replace, self._dataFromKey[key][self.DataIndex.Age.value])
            
        else:
            newAge:int = self._updateNewestOldestAge(self.Operation.Put)
            
        self._dataFromAge[newAge] = self._dataFromKey[key] = [value, newAge, key]
        
    def _updateNewestOldestAge(self, operation:Operation, currentAge:int = -1) -> int:
        """
        Used to retrieve a new age.
        
        Keeps the self._newestAge and self._oldestAge up to date during the process.
        
        Note: Does NOT update the self._dataFromAge:dict's key

        Args:
            * operation (Operation): Specifies the type of operation (Put / Get / Replace) that called this method
            * currentAge (int, optional):
                * Defaults to -1 (for not used).
                * Provides context for what the currentAge is during a get operation.
                * Needed for edge case where oldest age is being called from Get operation or self._oldestAge is not yet initialized
                    * skips currentAge when looking for new self._oldestAge

        Returns:
            * int: self._newestAge
        """
        assert (currentAge != -1) if operation == self.Operation.Get else True, "Get operations MUST provide a currentAge value!"
        
        self._newestAge += 1
        
        if (len(self._dataFromKey) >= self._capacity and operation == self.Operation.Put) or operation == self.Operation.Replace:
            
            if not(len(self._dataFromAge) == 0) and self._oldestAge == -1: 
                while not self._oldestAge in self._dataFromAge: self._oldestAge += 1
                
            
            if operation == self.Operation.Replace:
                currentAgeKey = self._dataFromAge[currentAge][self.DataIndex.Key.value]
                del self._dataFromAge[currentAge], self._dataFromKey[currentAgeKey]
                
            else:
                oldestAgeKey = self._dataFromAge[self._oldestAge][self.DataIndex.Key.value]
                del self._dataFromAge[self._oldestAge], self._dataFromKey[oldestAgeKey]
            
            if len(self._dataFromAge) == 0: 
                self._oldestAge = -1
            else:
                while not self._oldestAge in self._dataFromAge: self._oldestAge += 1
        
        elif operation == self.Operation.Get and len(self._dataFromAge) == 0: self._oldestAge = -1
            
        elif operation == self.Operation.Get and (currentAge == self._oldestAge or self._oldestAge == -1):
            while (not self._oldestAge in self._dataFromAge) or currentAge == self._oldestAge: self._oldestAge += 1
        
        return self._newestAge
    
            
if __name__ == "__main__":
    # * TEST 1
    # cache = LRUCache(2)
    # cache.put(1, 1)         # cache is {1=1}
    # cache.put(2, 2)         # cache is {1=1, 2=2}
    # print(cache.get(1))     # return 1
    # cache.put(3, 3)         # LRU key was 2, evicts key 2, cache is {1=1, 3=3}
    # # print(cache.get(2))     # returns -1 (not found)
    # cache.put(4, 4)         # LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    # # print(cache.get(1))     # return -1 (not found)
    # print(cache.get(3))     # return 3
    # print(cache.get(4))     # return 4
    
    # * TEST 2
    # cache = LRUCache(2)
    # cache.put(1,0)
    # cache.put(2,2)
    # cache.get(1)
    # cache.put(3,3)
    # cache.get(2)
    # cache.put(4,4)
    # cache.get(1)
    # cache.get(3)
    # cache.get(4)
    
    # * TEST 3
    # cache = LRUCache(1)
    # cache.put(2,1)
    # cache.get(2)
    
    # * TEST 4
    # cache = LRUCache(1)
    # cache.put(2,1)
    # cache.get(2)
    # cache.put(3,2)
    # cache.get(2)
    # cache.get(3)
    
    # * TEST 5
    cache = LRUCache(2)
    cache.put(2,1)
    cache.put(1,1)
    cache.put(2,3)
    cache.put(4,1)
    print(cache.get(1))
    print(cache.get(2))
    
    # * TEST 6
    # cache = LRUCache(2)
    # cache.get(2)
    # cache.put(2,6)
    # cache.get(1)
    # cache.put(1,5)
    # cache.put(1,2)
    # cache.get(1)
    # cache.get(2)
    
    # * TEST 7
    # cache = LRUCache(10)
    
    # cache.put(10,13)
    # cache.put(3,17)
    # cache.put(6,11)
    # cache.put(10,5)
    # cache.put(9,10)
    # cache.get(13)
    # cache.put(2,19)
    # cache.get(2)
    # cache.get(3)
    # cache.put(5,25)
    # cache.get(8)
    # cache.put(9,22)
    # cache.put(5,5)
    # cache.put(1,30)
    # cache.get(11)
    # cache.put(9,12)
    # cache.get(7)
    # cache.get(5)
    # cache.get(8)
    # cache.get(9)
    # cache.put(4,30)
    # cache.put(9,3)
    # cache.get(9)
    # cache.get(10)
    # cache.get(10)
    # cache.put(6,14)
    # cache.put(3,1)
    # cache.get(3)
    # cache.put(10,11)
    # cache.get(8)
    # cache.put(2,14)
    # cache.get(1)
    # cache.get(5)
    # cache.get(4)
    # cache.put(11,4)
    # cache.put(12,24)
    # cache.put(5,18)
    # cache.get(13)
    # cache.put(7,23)
    # cache.get(8)
    # cache.get(12)
    # cache.put(3,27)
    # cache.put(2,12)
    # cache.get(5)
    # cache.put(2,9)
    # cache.put(13,4)
    # cache.put(8,18)
    # cache.put(1,7)
    # cache.get(6)
    # cache.put(9,29)
    # cache.put(8,21)
    # cache.get(5)
    # cache.put(6,30)
    # cache.put(1,12)
    # cache.get(10)
    # cache.put(4,15)
    # cache.put(7,22)
    # cache.put(11,26)
    # cache.put(8,17)
    # cache.put(9,29)
    # cache.get(5)
    # cache.put(3,4)
    # cache.put(11,30)
    # cache.get(12)
    # cache.put(4,29)
    # cache.get(3)
    # cache.get(9)
    # cache.get(6)
    # cache.put(3,4)
    # cache.get(1)
    # cache.get(10)
    # cache.put(3,29)
    # cache.put(10,28)
    # cache.put(1,20)
    # cache.put(11,13)
    # cache.get(3)
    # cache.put(3,12)
    # cache.put(3,8)
    # cache.put(10,9)
    # cache.put(3,26)
    # cache.get(8)
    # cache.get(7)
    # cache.get(5)
    # cache.put(13,17)
    # cache.put(2,27)
    # cache.put(11,15)
    # cache.get(12)
    # cache.put(9,19)
    # cache.put(2,15)
    # cache.put(3,16)
    # cache.get(1)
    # cache.put(12,17)
    # cache.put(9,1)
    # cache.put(6,19)
    # cache.get(4)
    # cache.get(5)
    # cache.get(5)
    # cache.put(8,1)
    # cache.put(11,7)
    # cache.put(5,2)
    # cache.put(9,28)
    # cache.get(1)
    # cache.put(2,2)
    # cache.put(7,4)
    # cache.put(4,22)
    # cache.put(7,24)
    # cache.put(9,26)
    # cache.put(13,28)
    # cache.put(11,26)
    
    print("DONE")

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

"""
class LRUCache(object):
    
    # class DataIndex(Enum):
        # Data = 0
        # Age = 1
        # Key = 2
    
    # class Operation(Enum):
        # Put = 0
        # Get = 1
        # Replace = 2
        
    def __init__(self, capacity):
        # :type capacity: int
        self._dataFromKey = {}
        self._dataFromAge = {}
        self._newestAge = 0
        self._oldestAge = -1
        self._capacity = capacity

    def get(self, key):
        # :type key: int
        # :rtype: int

        if not key in self._dataFromKey: return -1

        dataItem = self._dataFromKey[key]
        
        oldAge = dataItem[1]
        del self._dataFromAge[oldAge]
        
        newAge = self._updateNewestOldestAge(1, dataItem[1])
        dataItem[1] = newAge
        self._dataFromAge[newAge] = dataItem
        
        return dataItem[0]
        
    
    def put(self, key, value):
        # :type key: int
        # :type value: int
        # :rtype: None
        if key in self._dataFromKey:
            newAge = self._updateNewestOldestAge(2, self._dataFromKey[key][1])
        
        else:
            newAge = self._updateNewestOldestAge(0)
            
        self._dataFromAge[newAge] = self._dataFromKey[key] = [value, newAge, key]
        
            
    def _updateNewestOldestAge(self, operation, currentAge = -1):
        self._newestAge += 1
        
        if (len(self._dataFromKey) >= self._capacity and operation == 0) or operation == 2:
            
            if not(len(self._dataFromAge) == 0) and self._oldestAge == -1: 
                while not self._oldestAge in self._dataFromAge: self._oldestAge += 1
            if operation == 2:
                currentAgeKey = self._dataFromAge[currentAge][2]
                del self._dataFromAge[currentAge], self._dataFromKey[currentAgeKey]
                
            else:
                oldestAgeKey = self._dataFromAge[self._oldestAge][2]
                del self._dataFromAge[self._oldestAge], self._dataFromKey[oldestAgeKey]
            
            
            if len(self._dataFromAge) == 0: 
                self._oldestAge = -1
            else:
                while not self._oldestAge in self._dataFromAge: self._oldestAge += 1
            
        elif operation == 1 and len(self._dataFromAge) == 0: self._oldestAge = -1

        elif operation == 1 and (currentAge == self._oldestAge or self._oldestAge == -1):
            while (not self._oldestAge in self._dataFromAge) or currentAge == self._oldestAge: self._oldestAge += 1
        
        return self._newestAge 
"""
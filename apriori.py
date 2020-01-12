class Apriori():
    def __init__(self):
        self.__data = {}
        self.__distinct = []
        self.__table_count = {}
        self.__result = []

    def load_data(self, path):
        file = open(path, "r")
        data = []
        for line in file:
            data.append(line.rstrip().split(','))
        file.close()
        
        for i in data:
            for j in i:
                self.__distinct.append(j)
        self.__distinct = list(set(self.__distinct))
        
        for i,line in enumerate(data):
            self.__data[i] = [self.__distinct.index(x) for x in line]
        
    def get_dataset(self):
        return self.__data
    
    def __compare(self, list1, list2):
        eq = []
        for i in list1:
            for j in list2:
                if i == j:
                    eq.append(True)
                    if len(eq) == len(list2):
                        return True
        return False

    def __arrange(self,subset):
        arr = []
        for i in subset:
            sk = []
            for j in i:
                for k in j:
                    sk.append(k)
            if not list(set(sk)) in arr:
                mylist = list(set(sk))
               
                arr.append(mylist)
        return arr

    def __subset(self,set):
        if(len(set) == 1 or len(set) == 0):
            return set

        subset = []
        for i in range(int(len(set))):
            for j in range(len(set)):
                if j > i:
                    subset.append([set[i], set[j]])
        
        if type(subset[0][0]) == int:
            return subset
        else:
            return self.__arrange(subset)

    def get_result(self, support, confidence):
        support = int(support * len(self.__data.keys()))
        
        #Inıtialize
        for key, value in self.__data.items():
            for i in value:
                if i in self.__table_count.keys():
                    self.__table_count[i] = self.__table_count[i] + 1
                else:
                    self.__table_count[i] = 1

        for key, value in self.__table_count.copy().items():
            if value < support:
                self.__table_count.pop(key)

        self.__result = [0, 1]#initialize value 
        init_state = self.__table_count.copy()
        new_keys = list(init_state.keys())
    
        #Apriori algorithm
        while self.__result[-1] != self.__result[-2]:
            keys = new_keys
            subsets = self.__subset(keys)
            result_set = {}
            for key, value in self.__data.items():
                for sub in subsets:
                    if self.__compare(value, sub):
                        index = str(sub)
                        if index in result_set.keys():
                            result_set[index] = result_set[index] + 1 
                        else:
                            result_set[index] = 1
            new_keys = []
            for key, value in result_set.copy().items():
                if value < support:
                    result_set.pop(key)
                else:
                    #String to array
                    new_keys.append(self.__to_array(key.split(',')))

            self.__result.append(result_set)
            if result_set == {}:
                self.__result.append({})
            elif len(result_set.keys()) == 1:
                self.__result.append(result_set)
            
        if self.__result[-1] == {}:
            if self.__result[-3] == 1:
                print("No result")
                return -1
            return self.__analyze(self.__result[-3], confidence)
        else:
            return self.__analyze(self.__result[-1], confidence)

    def __to_array(self, arr):
        keys = []
        for i in arr:
            keys.append(int(str(i).replace('\'', '').replace('[', '').replace(']', '')))
        return keys

    def __count(self, x):
        if not type(x) == list:
            return self.__table_count.get(x)
        #pass 0-1 index
        for item in self.__result[2:]:
            for key in item.keys():
                keyArray = self.__to_array(key.split(','))
                if len(keyArray) == len(x) and self.__compare(keyArray, x):
                    return item.get(key)
        return 0

    def __confidence(self, x, y):
        countX = self.__count(x)
        X = []
        if not type(x) == list:
            X = [x]
        for item in y:
            X.append(item)
        return self.__count(X) / countX

    def __analyze(self, result, confidence):
        for key, value in result.items():
            key_array = self.__to_array(key.split(','))
            result_set = {}
            #first subset
            for i in key_array:
                tmp = key_array.copy()
                tmp.remove(i)
                index = str(self.__distinct[i]) + "->" + str([self.__distinct[x] for x in tmp])
                confidence_val = self.__confidence(i, tmp)
                if confidence_val >= confidence:
                    result_set[index] = confidence_val

            subsets = key_array
            for i in range(len(key_array) - 1):
                subsets = self.__subset(subsets)
                for subset in subsets:
                    tmp = key_array.copy()
                    for item in subset:
                        tmp.remove(item)
                    index = str([self.__distinct[x] for x in subset]) + "->" + str([self.__distinct[x] for x in tmp])
                    if not index in result_set.keys():
                        confidence_val = self.__confidence(subset, tmp)
                        if confidence_val >= confidence:
                            result_set[index] = 1 if confidence_val > 1 else confidence_val

            return result_set
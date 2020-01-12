class Apriori():
    def __init__(self):
        self.__data = {}
        self.__distinct = []

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
            # self.__data.append({i : [self.__distinct.index(x) for x in line]})
        
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
                arr.append(list(set(sk)))
        return arr

    def __subset(self,set):
        if(len(set) == 1):
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
        support = support * len(self.__data.keys())
        table_count = {}
        
        for key, value in self.__data.items():
            for i in value:
                if i in table_count.keys():
                    table_count[i] = table_count[i] + 1
                else:
                    table_count[i] = 1

        for key, value in table_count.copy().items():
            if value < support:
                table_count.pop(key)

        result = [0, 1]
        init_state = table_count.copy()
        # print("TABLE COUNT---")
        # for k,v in init_state.items():
            # print("{}:{}".format(self.__distinct[k], v))
        # print("----------")
        # keys = list(init_state.keys())
        new_keys = list(init_state.keys())

        while result[-1] != result[-2]:
            keys = new_keys
            subsets = self.__subset(keys)
            # print("SUBSET")
            # print([[self.__distinct[y] for y in x] for x in subsets])
            result_set = {}
            for key, value in self.__data.items():
                for sub in subsets:
                    if self.__compare(value, sub):
                        # print("{}--{}".format([self.__distinct[x] for x in value], [self.__distinct[x] for x in sub]))
                        # index = str([self.__distinct[x] for x in sub])
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
                    keys = []
                    for i in key.split(','):
                        keys.append(int(str(i).replace('\'', '').replace('[', '').replace(']', '')))
                    new_keys.append(keys)
            # print("NEW")
            # print(new_keys)
            result.append(result_set)
            # print(result_set)
        
        print(result[-1])
        self.__analyze(result[-1])

    def __analyze(self, result):
        pass
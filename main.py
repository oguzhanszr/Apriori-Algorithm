import os
import sys
from apriori import Apriori

if __name__ == "__main__":
    apriori = Apriori()
    apriori.load_data("sample_dataset.csv")
    # print(apriori.get_dataset())
    apriori.get_result(support=0.3, confidence=0.8)
    
    # a = {"a","b","c","c"}
    # ab = {str(a):"denem"}
    # b = set(str(a))
    # for i in a:
    #     print(i)
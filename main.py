from apriori import Apriori

if __name__ == "__main__":
    apriori = Apriori()
    apriori.load_data("sample_dataset.csv")
    result = apriori.get_result(support=0.2, confidence=0.5)

    for key, value in result.items():
        print("{}:{}".format(key, value))
    
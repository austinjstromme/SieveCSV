import SieveCSV

collection = SieveCSV.parse_csv("random.csv", [1, 2, 3], ["bab", "abba", "abacaba"])
print(collection)
# collection = SieveCSV.parse_csv("random.csv", [(1, "bab"), (2, "abba"), (3, "abacaba")])
# collecction = SieveCSV.parse_csv("random.csv", 1, "bab", 2, "abba", 3, "abacaba")
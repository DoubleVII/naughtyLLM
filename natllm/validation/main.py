from json_reader import JsonReader

if __name__ == "__main__":
    from tester import generater
    j = JsonReader(generater)
    j.read_json()
    print('Pass')

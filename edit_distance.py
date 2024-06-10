import random
import time
import matplotlib.pyplot as plt
import string

def edit_distance(source: str, target: str, first_call: bool = True) -> int:
    source_index: int = len(source)
    target_index: int = len(target) 

    if first_call and source_index < target_index:
            return -1
            
    if source_index == 0 or target_index == 0: 
        return source_index + target_index
    
    if  source[source_index - 1] == target[target_index - 1]:
        return edit_distance(source[:source_index - 1], target[:target_index - 1], first_call=False)
    
    else:
        delete = edit_distance(source[:source_index - 1], target, first_call=False)                                    
        replace = edit_distance(source[:source_index - 1], target[:target_index - 1], first_call=False)
        
        min_value = min(delete, replace) + 1
        return min_value 


def memo_edit_distance(source: str, target: str, first_call: bool = True, cache: list = []) -> int:
    source_index: int = len(source)
    target_index: int = len(target) 

    if first_call:
        if source_index < target_index:
            return -1
            
        cache = [[None for _ in range(target_index + 1)] for _ in range(source_index + 1)]
    
    if cache[source_index - 1][target_index - 1] is not None:
        return cache[source_index - 1][target_index - 1]
    
    if source_index == 0 or target_index == 0: 
        return source_index + target_index
    
    if  source[source_index - 1] == target[target_index - 1]:
        return memo_edit_distance(source[:source_index - 1], target[:target_index - 1], first_call=False, cache=cache)
    
    else:
        delete = memo_edit_distance(source[:source_index - 1], target, first_call=False, cache=cache)                                    
        replace = memo_edit_distance(source[:source_index - 1], target[:target_index - 1], first_call=False, cache=cache)
        
        min_value = min(delete, replace) + 1
        cache[source_index - 1][target_index - 1] = min_value
        return min_value 

def compare_test(source: str, target:str, iteration: int, actual_value: int, expected_value: int) -> None:
    print(f"Test {iteration}: {source} - {target}")
    if actual_value == expected_value:
        print(f"Correct, espected {expected_value} - get {actual_value}")
    else:
        print(f"Incorrect, espected {expected_value} - get {actual_value}")

def test() -> None:
    with open("input.txt", "r") as input, open("output.txt", "r") as output:
        line: str = input.readline()
        
        it: int = 0
        while line:
            it += 1

            source, target = line.strip().split("-")
            expected_value = int(output.readline())

            actual_value = memo_edit_distance(source, target)
            compare_test(source, target, it, actual_value, expected_value)

            line = input.readline()
        
def get_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k = length))

def experimentation(sentences: list[str], algorithm, iterations: int) -> list[float]:
    results = []   
    for source in sentences:
        for target in sentences:
            if source == target:
                continue
               
            delta = 0
            start = time.time()
            for _ in range(iterations):    
                algorithm(source, target)
            end = time.time() 
                
            delta = (end - start)*1000/iterations
            results.append(delta)
    return results

def main() -> None:
    iterations = 10
    with open("frases.txt", "r") as input:
        sentences = input.readlines()
        for i in range(len(sentences)):
            sentences[i] = sentences[i].rstrip()
            
        for source in sentences:
            for target in sentences:
                if source == target:
                    continue       
                print(f"{len(source)} - {len(target)}")

        no_memo_results = experimentation(sentences, edit_distance, iterations)
        memo_results = experimentation(sentences, memo_edit_distance, iterations)
        
        for i in range(len(no_memo_results)):
            print(f"no_memo: {no_memo_results[i]} - memo: {memo_results[i]}")
                
        
if __name__ == '__main__':
    #test()
    main()
    
    
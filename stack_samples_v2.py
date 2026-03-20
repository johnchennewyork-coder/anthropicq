
from typing import List, Tuple

'''

'''

from dataclasses import dataclass
from typing import List

@dataclass
class Sample:
    ts: float
    stack: List[str]

@dataclass
class Event:
    kind: str   # 'start' or 'end'
    ts: float
    name: str

def get_prefix_index(stack1: List[str], stack2: List[str]):
    '''
    Takes two lists and finds the longest prefix between them

    ['A', 'B', 'C']
    ['A', 'B', 'D'] -> 2

    ['A', 'B']
    ['A'] -> 1

    ['A'] 
    ['A'] -> 1 

    Returns the termination index of the prefix.
    '''
    for i, (s1,s2) in enumerate(zip(stack1,stack2)):
        print(i, s1, s2)
        if s1 != s2:
            return i 
     
    # print(f'prefix idx is {i}')
    return i + 1

     
'''
A function call starts when it appears in the current sample's stack but wasn't at that depth in the previous sample's stack.
A function call ends when it was in the previous sample's stack but is no longer present in the current sample's stack.
The resulting events should be ordered such that a nested function call's end event appears before the enclosing call's end event. (e.g., if multiple functions end at the same timestamp, they must be appended in reverse order because the inner functions terminate first).
Assume call frames in the very last sample haven't finished (do not generate end events for them).
Pay special attention to handling identical stacks back-to-back, and recursive calls where the same function name appears multiple times in the stack.
'''
def convert_stack_samples(samples: List[Tuple]):
    
    assert len(samples) > 0, "empty stack samples trace passed in"
    res = []
    prev_sample = samples[0].stack
    res.extend(["start " + fn for fn in prev_sample])

    for i in range(1, len(samples)):
        curr_sample = samples[i].stack
        prefix_idx = get_prefix_index(prev_sample, curr_sample)
        ended_fns = prev_sample[prefix_idx:]
        started_fns = curr_sample[prefix_idx:]
        print(f'prefix_idx {prefix_idx}, {started_fns}')
        if len(ended_fns) > 0:
            res.extend(["end " + fn for fn in reversed(ended_fns)])
        if len(started_fns) > 0:
            res.extend(["start " + fn for fn in started_fns])
        prev_sample = curr_sample

    return res 





    pass

if __name__ == "__main__":
    # Test Case 1: Standard
    samples1 = [
        Sample(1.0,["main"]),
        Sample(2.5, ["main", "func1"]),
        Sample(3.1, ["main"])
    ]

    res = convert_stack_samples(samples1)
    print('ex1,',res) # start main, start func1, end func1


    
    # Test Case 2: Identical Stacks (No state change)
    samples2 = [
        Sample(1.0, ["main", "f1"]),
        Sample(2.0, ["main", "f1"]),
        Sample(3.0,["main", "f1"])
    ]
    res = convert_stack_samples(samples2)
    print(res) # start main, start func1


    # Test Case 3: Recursive Calls
    samples3 =[
        Sample(1.0, ["main", "f1"]),
        Sample(2.0,["main", "f1", "f1"]),
        Sample(3.0,["main", "f1"])
    ]

    res = convert_stack_samples(samples3)
    print(res) # start main, start f1, start f1, end f1


    # Test Case 4: Multiple ends at the same time
    # Start order: f1, f2, f3. End order should be f3, f2, f1.
    samples4 =[
        Sample(1.0, ["main"]),
        Sample(2.0,["main", "f1", "f2", "f3"]),
        Sample(3.0, ["main"])
    ]

    res = convert_stack_samples(samples4)
    print(res) # start main, start f1, start f1, end f1
    

    # Test Case 5: Multiple ends at the same time
    # Start order: f1, f2, f3. End order should be f3, f2, f1.
    samples5 =[
        Sample(1.0, ["main"]),
        Sample(2.0,["main", "f1", "f2", "f3"]),
        Sample(3.0, ["main", "a1", "a2"])
    ]

    res = convert_stack_samples(samples5)
    print(res) # ['start main', 'start f1', 'start f2', 'start f3', 'end f3', 'end f2', 'end f1', "a1", "a2"]

    # Time complexity:
    # assume N samples, and K possible recursion depth
    # then, 2*O(K) to find the prefix and O(N) comparisons, then O(NK)

    # Space complexity:
    # prefix_idx is constant space, but O(NK) for the result array. otherwise, it could be yielded (constant space)


    # follow-up can 
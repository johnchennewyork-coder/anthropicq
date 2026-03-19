class Sample:
  '''
  Rules:
Initial State: For the very first sample, assume all functions in the stack just started, in order from outermost to innermost.
Transitions: When moving from one sample to the next, find the longest common prefix of the two stacks.
Ends: Functions in the previous stack that are not in the common prefix must have ended. Crucially, functions must end in reverse order (the innermost function finishes first).
Starts: Functions in the current stack that are not in the common prefix must have started. They start in standard order (outermost to innermost).
Final Cleanup: After processing the last sample, any functions that are still running must end (in reverse order).
  '''
    def __init__(self, timestamp: float, stack: list[str]):
        self.timestamp = timestamp
        self.stack = stack

def compare_prefix(stack1, stack2):
  '''
  compares the prefix
  '''
  prefix = []
  # find the smaller stack, and zip it 
  for i, (elt1, elt2) in enumerate(zip(stack1, stack2)):
    if elt1 == elt2:
      prefix.append(elt1)
    else:
      break
  return prefix
      '''

      Rules:
Initial State: For the very first sample, assume all functions in the stack just started, in order from outermost to innermost.
Transitions: When moving from one sample to the next, find the longest common prefix of the two stacks.
Ends: Functions in the previous stack that are not in the common prefix must have ended. Crucially, functions must end in reverse order (the innermost function finishes first).
Starts: Functions in the current stack that are not in the common prefix must have started. They start in standard order (outermost to innermost).
Final Cleanup: After processing the last sample, any functions that are still running must end (in reverse order).
      '''
def convert_stack_samples_to_trace(samples: List[Sample]):
  '''
  the first time we see a new function, we will output "start"
  currently_running_functions = set()
  '''
  assert len(samples) > 0, "no samples passed in"
  curr_running_stack = [samples[0].stack] #
  res = ['start ' + x for x in curr_running_stack]
  
  for i in range(1,len(samples)):
    prefix = compare_prefix(curr_running_stack, samples[i].stack)
    if curr_running_stack[len(prefix):]:
      ended_functions = set(samples[i].stack[len(prefix):])
      for i in range(len(ended_functions)-1, -1, -1):
        res.append(f'end {ended_functions[i]}')
    if samples[i].stack[len(prefix):]:
      new_functions = set(samples[i].stack[len(prefix):]) 
      for i in range(len(new_functions):
        res.append(f'start {new_functions[i]}')
    curr_running_stack = samples[i].stack

  return res
# --- TEST CASE 1: Basic nested calls ---
samples1 = [
    Sample(0.1,["main", "foo", "bar"]),
    Sample(0.2,["main", "foo", "baz"]),
    Sample(0.3, ["main"])
]

# Expected Output for Test Case 1:
# start main
# start foo
# start bar
# end bar -- note, we assume end before starts 
# start baz
# end baz
# end foo
# end main


# Test case 1a
samples1a = [
    Sample(0.1,["main", "foo", "bar"]),
    Sample(0.2,["main", "foo", ]),
    Sample(0.2,["main", "foo", "bin" ]),
    Sample(0.3, ["main"])
]

# Test case 1b
samples1a = [
    Sample(0.1,["main", "foo", "bar"]),
    Sample(0.2,["main", "foo", ]),
    Sample(0.2,["main", "foo", "bin" ]),
    Sample(0.3, ["main"])
]

# Expected Output for Test Case 1:
# start main
# start foo
# start bar
# end bar
# start bin
# end bin
# end foo
# end main

# --- TEST CASE 2: The Edge Case (Identical names, recursive/repeated calls) ---
samples2 = [
    Sample(0.0,["a", "b", "a", "c"]),
    Sample(1.0, ["a", "a", "b", "c"])
]

# Expected Output for Test Case 2:
# start a
# start b
# start a
# start c
# end c
# end a
# end b
# start a
# start b
# start c
# end c
# end b
# end a
# end a

#!/usr/bin/env python3
import sys
import csv
from collections import deque
import math

def trace_paths(tape, TM, max_depth):
    initial_config = ["", TM['start'], "".join(tape)]  
    tree = [[initial_config]]  
    nonleaves=0

    for depth in range(max_depth):
        current_level = tree[-1]  
        next_level = []  

        #Check all possible configurations
        for config in current_level:
            left_tape, state, right_tape = config

            # Accept state
            if state == TM['accept']:
                result = f"String accepted in {len(tree)-1} transitions\n"
                return tree, nonleaves, result

            # Reject state
            if state == TM['reject']:
                continue

            # Flag to track if no valid transitions were found
            transition_found = False

            # Explore all possible transitions
            for transition in TM["transitions"]:
                if state == transition[0] and (right_tape[0] if right_tape else "_") == transition[1]:
                    transition_found = True
                    # Apply the transition
                    new_left_tape = list(left_tape)
                    new_right_tape = list(right_tape)

                    if len(new_right_tape)>0: new_right_tape[0]=transition[3]
                        
                    # Determine the next state
                    new_state = transition[2]
                    if new_state!=TM['accept']:
                        if transition[4] == 'L':  # Move tape head left
                            if left_tape:  
                                new_right_tape.insert(0, new_left_tape[-1])
                                new_left_tape = new_left_tape[:-1]

                        elif transition[4] == 'R':  # Move tape head right
                            if right_tape:  
                                new_left_tape.append(new_right_tape[0])
                                new_right_tape = new_right_tape[1:]

                    # Add the new configuration to the next level
                    next_level.append(["".join(new_left_tape), new_state, "".join(new_right_tape)])
                    nonleaves+=1

            # If no valid transition was found, transition to the reject state
            if not transition_found:
                new_left_tape = left_tape
                new_right_tape = list(right_tape) 
                next_level.append([new_left_tape+new_right_tape[0] if new_right_tape else "", TM['reject'], "".join(new_right_tape[2:])])

        if not next_level:
            result = f"Rejected in {len(tree)-1} transitions\n"
            return tree, nonleaves, result
        
        tree.append(next_level)
    
    for transition in tree[-1]:
        if transition[1]==TM['accept']:
            result = f"String accepted in {len(tree)-1} transitions\n"
            return tree, nonleaves, result
    result = f"Maximum depth reached\n"
    return tree, nonleaves, result


def main():
    if len(sys.argv) < 4: 
        print("Error: Insufficient arguments\nUsage: python3 traceTM_djohan.py <Turing Machine csv> <Max Transitions> <string0> <string2> ... <stringx>")
        return
    csvFile = sys.argv[1]
    maxDepth = int(sys.argv[2])
    tapes = [list(tape) for tape in sys.argv[3:]]
    Turing = {}

    # Parse the Turing Machine csv file
    try:
        with open(csvFile, 'r') as file:
            csv_reader = list(csv.reader(file))[0]
            Turing['name'] = csv_reader[0]
            Turing['states'] = csv_reader[1].split()
            Turing['alphabet'] = csv_reader[2].split()
            Turing['tape'] = csv_reader[3].split()
            Turing['start'] = csv_reader[4].split()[0]
            Turing['accept'] = csv_reader[5].split()[0]
            Turing['reject'] = csv_reader[6].split()[0] 
            Turing['transitions'] = [transition.split('/') for transition in csv_reader[7].split()]
    except FileNotFoundError:
        print("File not found")
        return

    with open(f"{Turing['name']}_output.txt", "w") as f:
        f.write(f"Turing Machine: {Turing["name"]}\n")
        for tape in tapes:
            transitions=0
            f.write(f'Tape: {"".join(tape)}\n')
            tree, nonleaves, result = trace_paths(tape, Turing, maxDepth)
            f.write(result)
            for depth, level in enumerate(tree):
                #Format output
                level = [[l[0],l[1],l[2][0] if len(l[2]) else "_", l[2][1:]] for l in level] 
                f.write(f"Depth {depth:>{int(math.log(maxDepth,10))+1}}: {level}\n" if depth>0 else f"   Start: {level}\n")
                transitions+=len(level)
            f.write(f"Total Transitions: {transitions-1}\tNonleaves: {nonleaves}\nTotal Nondeterminism: {(transitions-1)/nonleaves}\n\n")


if __name__ == "__main__":
    main()

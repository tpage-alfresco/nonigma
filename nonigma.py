#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(prog='nonigma', description='Encrypt or decrypt messages using the nonigma algorithm. The message must either be supplied as an argument or a file.')
parser.add_argument('-w', '--wheelorder', required=True, help='comma separated list of wheels - e.g. lg,dg,bl,pu,re,or,pi,pe,gr')
parser.add_argument('-p', '--wheelpositions', required=True, help='comma separated list of wheel starting positions - e.g. 11,14,12,11,17,9,9,13,0')
parser.add_argument('-i', '--infile', required=False, help='path to an input file')
parser.add_argument('-o', '--outfile', required=False, help='path to an output file (or will output to stdout)')
parser.add_argument('-m', '--message', required=False, help='message to encrypt or decrypt')
parser.add_argument('-s', '--strip', action='store_true', help='filter out unsupported characters (rather than throw an error)')
args = parser.parse_args()

wheel_set = {
    'lg': [+8, +4, -7, -5, +5, -4, +6, +3, -8, -5, -3, +4, -6, +7, +3, -4, +5, -3], # Light green
    'dg': [-9, +6, -8, -5, +4, +5, +8, -6, -4, +9, -5, +6, +8, +2, -8, -2, +5, -6], # Dark green
    'bl': [-1, -5, +6, +9, -7, +5, +5, +2, -6, -2, -5, -5, -9, +3, +5, +7, -3, +1], # Blue
    'pu': [+2, -6, -2, -5, +6, +7, +9, +1, -1, +8, -6, +3, -7, +6, -3, -9, +5, -8], # Purple
    're': [-6, +2, +4, -2, +3, +8, -4, -3, -9, +11, +6, +11, +9, -8, +1, -1, -6, +2, +6, -2, -11, -9, -11, +9], # Red
    'or': [+6, -4, +2, +4, -2, +3, -6, -4, -3, +8, +3, +5, +2, -3, -2, +4, -5, -8], # Orange
    'pi': [-7, -2, +4, -7, +5, +3, -4, +3, -3, -5, -3, +7, +4, +2, +7, -2, -4, +2], # Pink
    'pe': [+4, +4, -6, -8, -4, -4, -8, +2, +4, -2, +5, +6, -4, +8, +6, -5, +8, -6], # Peach
    'gr': [+7, +8, -4, +9, -5, -8, +7, -7, +3, -8, +4, -3, -9, -7, -4, +8, +4, +5] # Grey
}

machine = [
    [(2, 6), (5, 4), (4, 0), (4, 22), (4, 21), (7, 14), (6, 17), (3, 15), 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', (1, 4)],
    [(4, 2), (4, 1), (6, 0), (3, 16), (0, 17), 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', (2, 5), (5, 5), (8, 14), (4, 3)],
    [(7, 3), (4, 7), (4, 5), (4, 6), (3, 17), (1, 14), (0, 0), 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', (8, 0), (5, 7)],
    [(4, 23), (4, 20), (8, 12), (4, 19), (7, 16), (6, 1), '1', '2', '3', '4', '5', '6', '7', '8', '9', (0, 7), (1, 3), (2, 4)],
    [(0, 2), (1, 1), (1, 0), (1, 17), (5, 3), (2, 2), (2, 3), (2, 1), (5, 2), (8, 16), (5, 1), (8, 13), (8, 15), (7, 1), (7, 0), (7, 17), (6, 6), (6, 3), (6, 2), (3, 3), (3, 1), (0, 4), (0, 3), (3, 0)],
    [(7, 2), (4, 10), (4, 8), (4, 4), (0, 1), (1, 15), (8, 17), (2, 17), 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', (6, 4)],
    [(1, 2), (3, 5), (4, 18), (4, 17), (5, 17), (7, 15), (4, 16), (8, 10), 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', (0, 6)],
    [(4, 14), (4, 13), (5, 0), (2, 0), (8, 11), '.', 'Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', (0, 5), (6, 5), (3, 4), (4, 15)],
    [(2, 16), '/', '🙁', '🙂', '-', '•', '?', "'", ',', '!', (6, 7), (7, 4), (3, 2), (4, 11), (1, 16), (4, 12), (4, 9), (5, 6)]
]

slot_sizes = list(map(len, machine))

def encode_letter(letter, state):
    wheel_order, wheel_positions = state
    wheels = [wheel_set[wheel_name] for wheel_name in wheel_order]
    terminal = None
    for slot_index, slot in enumerate(machine):
        if letter in slot:
            terminal = [slot_index, slot.index(letter)]
    if terminal == None:
        if args.strip:
            return ''
        raise Exception(f'Unsupported character: "{letter}"')
    start_slot_index = terminal[0]
    wheel = wheels[terminal[0]]
    slot_size = slot_sizes[terminal[0]]
    wheel_terminal = (terminal[1] + wheel_positions[terminal[0]]) % slot_size
    wheel_delta = wheel[wheel_terminal]
    terminal[1] = ((terminal[1] + wheel_delta) % slot_size + slot_size) % slot_size
    while type(machine[terminal[0]][terminal[1]]) == tuple:
        terminal = list(machine[terminal[0]][terminal[1]])
        wheel = wheels[terminal[0]]
        wheel_size = slot_sizes[terminal[0]]
        wheel_terminal = (terminal[1] + wheel_positions[terminal[0]]) % wheel_size
        wheel_delta = wheel[wheel_terminal]
        terminal[1] = ((terminal[1] + wheel_delta) % wheel_size + wheel_size) % wheel_size
    output = machine[terminal[0]][terminal[1]]
    end_slot_index = terminal[0]
    # Increment wheels
    wheel_positions[start_slot_index] = (wheel_positions[start_slot_index] + 1) % slot_sizes[start_slot_index]
    if end_slot_index == start_slot_index:
        end_slot_index = 4
    wheel_positions[end_slot_index] = (wheel_positions[end_slot_index] + 1) % slot_sizes[end_slot_index]
    return output

def encode_message(message, key):
    for slot_index, slot_size in enumerate(slot_sizes):
        wheel_name = key[0][slot_index]
        if len(wheel_set[wheel_name]) != slot_size:
            raise Exception(f'Wheel "{wheel_name}" does not fit in slot {slot_index}')
    wheel_state = (key[0], list(key[1]))
    out = ''
    for letter in message:
        out += encode_letter(letter, wheel_state)
    return out

# Run some tests that the program has the same connections as the cardboard version.

def test(wheel_order, wheel_positions, message, expected):
    key = (wheel_order, wheel_positions)
    out = encode_message(message, key)
    if out != expected:
        print('Failure, expected {} got {}'.format(expected, out))

wheel_order = ('lg', 'dg', 'bl', 'pu', 're', 'or', 'pi', 'pe', 'gr')
wheel_positions = (11, 14, 12, 11, 17, 9, 9, 13, 18)
test(wheel_order, wheel_positions, 'i', 'd')
test(wheel_order, wheel_positions, 'g', 'r')
test(wheel_order, wheel_positions, 'a', 'e')
test(wheel_order, wheel_positions, 'm', 'q')
test(wheel_order, wheel_positions, 'z', 't')
test(wheel_order, wheel_positions, 'D', 'F')
test(wheel_order, wheel_positions, 'O', 'K')
test(wheel_order, wheel_positions, 'Z', 'V')
test(wheel_order, wheel_positions, 'P', 'R')
test(wheel_order, wheel_positions, '!', '/')
test(wheel_order, wheel_positions, 'x', 'f')
test(wheel_order, wheel_positions, '2', '4')
test(wheel_order, wheel_positions, '3', '🙂')
test(wheel_order, wheel_positions, '9', 'h')
test(wheel_order, wheel_positions, 'A', 'N')
test(wheel_order, wheel_positions, 'N', 'A')
test(wheel_order, wheel_positions, '1', 'k')
# Test incrementing the wheels.
test(wheel_order, wheel_positions, 'HelloWorld!', 'BaMpk.-B1Ra')
test(wheel_order, wheel_positions, 'BaMpk.-B1Ra', 'HelloWorld!')
# Test that wheel position 0 gives the same result as 18.
wheel_positions = (11, 14, 12, 11, 17, 9, 9, 13, 0)
test(wheel_order, wheel_positions, 'HelloWorld!', 'BaMpk.-B1Ra')

wheel_order = [wheel_name.strip() for wheel_name in args.wheelorder.split(',')]
for wheel_name in wheel_order:
    if wheel_name not in wheel_set.keys():
        raise Exception(f'Wheel "{wheel_name}" not recognised')
wheel_positions = [int(wheel_position) for wheel_position in args.wheelpositions.split(',')]
key = (wheel_order, wheel_positions)
if args.message:
    message = args.message
elif args.infile:
    with open(args.infile) as input_file:
        message = input_file.read()
else:
    raise Exception('Either a message or input file must be specified')
out = encode_message(message, key)
if args.outfile:
    with open(args.outfile, 'w') as output_file:
        output_file.write(out)
else:
    print(out)

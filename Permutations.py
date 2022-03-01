"""Permutations.py
@author lmartin5

This file contains the functions create and store permuations 
of numbers 1 - n. These permuations are then used with GraphManager
to search for one-page book embeddings of graphs.
"""


def find_and_remove_flip(line, lines):
    reverse = line[::-1]
    try:
        del lines[reverse]
    except:
        return

def get_perms_from_file(num_elements, file_prefix="permutations_"):
    infile = open(file_prefix + str(num_elements) + ".txt", "r")
    lines = infile.readlines()
    infile.close()

    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

def remove_flip_elements(perms):
    perms_dict = store_perms_in_dict(perms)
    count = 0
    for perm_value in list(perms_dict):
        if perm_value in perms_dict:
            find_and_remove_flip(perm_value, perms_dict)
            count = count + 1        
    perms = list(perms_dict.values())
    return perms

# Python program to print all permutations with
# duplicates allowed
 
def toString(List):
    return ''.join(List)
 
# Function to print permutations of string
# This function takes three parameters:
# 1. String
# 2. Starting index of the string
# 3. Ending index of the string.
def permute(a, l, r, outfile):
    if l==r:
        outfile.write(toString(a) + "\n")
    else:
        for i in range(l,r+1):
            a[l], a[i] = a[i], a[l]
            permute(a, l+1, r, outfile)
            a[l], a[i] = a[i], a[l] # backtrack


# Driver program to test the above function
def generate_permutations_to_file(num_elements):
    outfile = open("permutations_" + str(num_elements) + ".txt", "w")
    string = ""
    for i in range(1, num_elements + 1):
        if i < 10:
            string += str(i)
        else:
            string += chr(i + 87)

    n = len(string)
    a = list(string)
    permute(a, 0, n-1, outfile)
    outfile.close()
# This code is contributed by Bhavya Jain

def store_permutations(perms, num_elements, file_prefix="permutations_"):
    outfile = open(file_prefix + str(num_elements) + ".txt", "w")
    for perm in perms:
        outfile.write(perm + "\n")
    outfile.close()

def strings_to_perms(perms):
    for i in range(len(perms)):
        perms[i] = string_to_perm(perms[i])
    return perms

def remove_identical_elements(a, b, perms):
    index = 0
    items_removed = 0
    while index < len(perms):
        items_removed += find_and_remove_identical_element(a, b, perms[index], perms)
        index = index + 1 
        print("Index: " + str(index) + " Items Removed: " + str(items_removed))

def find_and_remove_identical_element(a, b, line, lines):
    ident = string_to_perm(line)
    a_loc = ident.index(a)
    b_loc = ident.index(b)
    temp = ident[a_loc]
    ident[a_loc] = ident[b_loc]
    ident[b_loc] = temp
    ident = perm_to_string(ident)
    if ident in lines:
        lines.remove(ident)
        return 1
    return 0

def perm_to_string(perm):
    printed = ""
    for num in perm:
        if num < 10: 
            printed += str(num)
        else:
            printed += str(chr(num + 87))
    return printed

def string_to_perm(stri):
    perm = []
    for character in stri:
        if character.isnumeric():
            perm.append(int(character))
        else:
            perm.append(ord(character) - 87)
    return perm

def store_perms_in_dict(perms):
    new_perms = dict([])
    for perm in perms:
        new_perms[perm] = perm
    return new_perms

'''
perms = get_perms_from_file(10)
perms = remove_flip_elements(perms)
store_permutations(perms, 10, "flip_perms_")
'''
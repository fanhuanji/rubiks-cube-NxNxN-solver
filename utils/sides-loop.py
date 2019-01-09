#!/usr/bin/env python3

foo = [10, 23, 27, 14]
offset = 0
side_name = {
    0 : "Upper",
    1 : "Left",
    2 : "Front",
    3 : "Right",
    4 : "Back",
    5 : "Down",
}

#for side_index in range(1,5):
for side_index in range(6):
    #print("        %s: 0, # %s" % (': 0, '.join([str(x + offset) for x in foo]), side_name[side_index]))
    #offset += 36

    print("            %s, # %s" % (', '.join([str(x + offset) for x in foo]), side_name[side_index]))
    offset += 36

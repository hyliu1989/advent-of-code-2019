lines = []
with open('day22-input.txt', 'r') as f:
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.rstrip('\n')
        lines.append(line)

forward_str = ''
for line in lines:
    if line[:4] == 'cut ':
        forward_str += 'x_pos = cut_track1(x_pos, %d, mod)\n' % (int(line[4:]))
    elif line[:20] == 'deal with increment ':
        forward_str += 'x_pos = deal_with_inc(x_pos, %d, mod)\n' % (int(line[20:]))
    elif line == 'deal into new stack':
        forward_str += 'x_pos = deal_into_new_deck_track1(x_pos, mod)\n'
    else:
        print(line.__repr__())
        raise


rev_res_str = ''
for line in lines[::-1]:
    if line[:4] == 'cut ':
        rev_res_str += 'y_pos = inv_cut_track1(y_pos, %d, mod)\n' % (int(line[4:]))
    elif line[:20] == 'deal with increment ':
        rev_res_str += 'y_pos = inv_deal_with_inc(y_pos, %d, mod)\n' % (int(line[20:]))
    elif line == 'deal into new stack':
        rev_res_str += 'y_pos = inv_deal_into_new_deck_track1(y_pos, mod)\n'
    else:
        print(line.__repr__())
        raise
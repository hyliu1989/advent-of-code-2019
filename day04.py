
def range_valid_check(value, beg, end, n_digit_to_discard):
    denominator = 10**n_digit_to_discard
    q = value//denominator  # quotient
    if q < beg//denominator or q > end//denominator:
        return False
    else:
        return True

def check_double(seq):
    passed = False
    for i in range(0,len(seq)-1):
        if seq[i] == seq[i+1]:
            passed = True
            break
    return passed

def search(beg, end):
    allowed = []
    for i5 in range(beg//10**5,end//10**5+1):
        sum5 = i5*10**5
        if not range_valid_check(sum5, beg, end, 5):
            continue
        
        for i4 in range(i5,9+1):
            sum4 = i4*10**4 + sum5
            if not range_valid_check(sum4, beg, end, 4):
                continue
            
            for i3 in range(i4,9+1):
                sum3 = i3*10**3 + sum4
                if not range_valid_check(sum3, beg, end, 3):
                    continue
                
                for i2 in range(i3,9+1):
                    sum2 = i2*10**2 + sum3
                    if not range_valid_check(sum2, beg, end, 2):
                        continue
                    
                    for i1 in range(i2,9+1):
                        sum1 = i1*10**1 + sum2
                        if not range_valid_check(sum1, beg, end, 1):
                            continue
                        
                        for i0 in range(i1,9+1):
                            # check the double
                            if check_double([i5,i4,i3,i2,i1,i0]):
                                pass
                            else:
                                continue

                            sum0 = i0 + sum1
                            if not range_valid_check(sum0, beg, end, 0):
                                continue

                            allowed.append(sum0)

    print('part 1', len(allowed))

search(136818,685979)




def check_double2(seq):
    passed = False
    current_number = seq[0]
    appearance_cnt = 1
    for i in range(1,len(seq)):
        if seq[i] == current_number:
            appearance_cnt +=1
        else:
            if appearance_cnt == 2:
                passed = True
                break
            else:
                current_number = seq[i]
                appearance_cnt = 1
    if appearance_cnt == 2:
        passed = True
    return passed

def search2(beg, end):
    allowed = []
    for i5 in range(beg//10**5,end//10**5+1):
        sum5 = i5*10**5
        if not range_valid_check(sum5, beg, end, 5):
            continue
        
        for i4 in range(i5,9+1):
            sum4 = i4*10**4 + sum5
            if not range_valid_check(sum4, beg, end, 4):
                continue
            
            for i3 in range(i4,9+1):
                sum3 = i3*10**3 + sum4
                if not range_valid_check(sum3, beg, end, 3):
                    continue
                
                for i2 in range(i3,9+1):
                    sum2 = i2*10**2 + sum3
                    if not range_valid_check(sum2, beg, end, 2):
                        continue
                    
                    for i1 in range(i2,9+1):
                        sum1 = i1*10**1 + sum2
                        if not range_valid_check(sum1, beg, end, 1):
                            continue
                        
                        for i0 in range(i1,9+1):
                            sum0 = i0 + sum1
                            if not range_valid_check(sum0, beg, end, 0):
                                continue

                            # check the double
                            if check_double2([i5,i4,i3,i2,i1,i0]):
                                allowed.append(sum0)

    print('part 2', len(allowed))
    # print(allowed)

search2(136818,685979)

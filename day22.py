
def cut(x, N):
    return x[N:] + x[:N]

def deal_into_new_deck(x):
    return x[::-1]

def deal_with_inc(x,N):
    mod = len(x)
    new_deck = [None]*mod
    for i in range(mod):
        new_deck[(i*N)%mod] = x[i]
    return new_deck

deck = list(range(10007))
# deck = list(range(119315717514047))

with open('day22-input.txt', 'r') as f:
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.rstrip('\n')

        if line[:4] == 'cut ':
            deck = cut(deck, int(line[4:]))
        elif line[:20] == 'deal with increment ':
            deck = deal_with_inc(deck, int(line[20:]))
        elif line == 'deal into new stack':
            deck = deal_into_new_deck(deck)
        else:
            print(line.__repr__())
            raise
import numpy as np
print(np.where(np.array(deck) == 2019))









print('start part 2')
import numba

lines = []
with open('day22-input.txt', 'r') as f:
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.rstrip('\n')
        lines.append(line)
lines = lines[::-1]


###################################################################
@numba.jit('i8(i8,i8,i8)', nopython=True, nogil=True, fastmath=True)
def cut_track1(x_pos, N, mod):
    if N < 0:
        N = N + mod
    n1 = N
    n2 = mod-N

    if x_pos < n1:
        y_pos = x_pos + n2
    else:
        y_pos = x_pos - n1
    return y_pos

# @numba.jit('i8(i8,i8,i8)', nopython=True, nogil=True, fastmath=True)
# def inv_cut_track1(y_pos, N, mod):
#     if N < 0:
#         N = N + mod
#     n1 = N
#     n2 = mod-N

#     if y_pos < n2:
#         x_pos = y_pos + n1
#     else:
#         x_pos = y_pos - n2
#     return x_pos
###################################################################


###################################################################
@numba.jit('i8(i8,i8)', nopython=True, nogil=True, fastmath=True)
def deal_into_new_deck_track1(y_pos, mod):
    x_pos = mod - 1 - y_pos
    return x_pos

# inv_deal_into_new_deck_track1 = deal_into_new_deck_track1
###################################################################


###################################################################
@numba.jit('i8(i8,i8,i8)', nopython=True, nogil=True, fastmath=True)
def deal_with_inc(x_pos, N, mod):
    y_pos = (x_pos * N) % mod
    return y_pos

# @numba.jit('i8(i8,i8,i8)', nopython=True, nogil=True, fastmath=True)
# def inv_deal_with_inc(y_pos, N, mod):
#     r = mod % N
#     k = 0
#     while True:
#         if (y_pos + k*r) % N == 0:
#             break
#         k += 1
#     x_pos = (y_pos + k * mod) // N
#     return x_pos
###################################################################



@numba.jit('i8(i8,i8)', nopython=True, nogil=True, fastmath=True)
def single_pass_forward(x_pos, mod):
    # mod = 119315717514047
    # mod = 10007
    x_pos = cut_track1(x_pos, 9374, mod)
    x_pos = deal_with_inc(x_pos, 48, mod)
    x_pos = cut_track1(x_pos, -2354, mod)
    x_pos = deal_with_inc(x_pos, 12, mod)
    x_pos = cut_track1(x_pos, -7039, mod)
    x_pos = deal_with_inc(x_pos, 14, mod)
    x_pos = cut_track1(x_pos, -2325, mod)
    x_pos = deal_with_inc(x_pos, 40, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, 4219, mod)
    x_pos = deal_with_inc(x_pos, 15, mod)
    x_pos = cut_track1(x_pos, -3393, mod)
    x_pos = deal_with_inc(x_pos, 48, mod)
    x_pos = cut_track1(x_pos, 1221, mod)
    x_pos = deal_with_inc(x_pos, 66, mod)
    x_pos = cut_track1(x_pos, 1336, mod)
    x_pos = deal_with_inc(x_pos, 53, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, -5008, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 34, mod)
    x_pos = cut_track1(x_pos, 8509, mod)
    x_pos = deal_with_inc(x_pos, 24, mod)
    x_pos = cut_track1(x_pos, -1292, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, 8404, mod)
    x_pos = deal_with_inc(x_pos, 17, mod)
    x_pos = cut_track1(x_pos, -105, mod)
    x_pos = deal_with_inc(x_pos, 51, mod)
    x_pos = cut_track1(x_pos, 2974, mod)
    x_pos = deal_with_inc(x_pos, 5, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 53, mod)
    x_pos = cut_track1(x_pos, 155, mod)
    x_pos = deal_with_inc(x_pos, 31, mod)
    x_pos = cut_track1(x_pos, 2831, mod)
    x_pos = deal_with_inc(x_pos, 61, mod)
    x_pos = cut_track1(x_pos, -4193, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, 9942, mod)
    x_pos = deal_with_inc(x_pos, 13, mod)
    x_pos = cut_track1(x_pos, -532, mod)
    x_pos = deal_with_inc(x_pos, 41, mod)
    x_pos = cut_track1(x_pos, 2847, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, -2609, mod)
    x_pos = deal_with_inc(x_pos, 72, mod)
    x_pos = cut_track1(x_pos, 9098, mod)
    x_pos = deal_with_inc(x_pos, 64, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, 4292, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, -4427, mod)
    x_pos = deal_with_inc(x_pos, 24, mod)
    x_pos = cut_track1(x_pos, -4713, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, 5898, mod)
    x_pos = deal_with_inc(x_pos, 56, mod)
    x_pos = cut_track1(x_pos, -2515, mod)
    x_pos = deal_with_inc(x_pos, 2, mod)
    x_pos = cut_track1(x_pos, -5502, mod)
    x_pos = deal_with_inc(x_pos, 66, mod)
    x_pos = cut_track1(x_pos, 8414, mod)
    x_pos = deal_with_inc(x_pos, 7, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 35, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 29, mod)
    x_pos = cut_track1(x_pos, -2176, mod)
    x_pos = deal_with_inc(x_pos, 14, mod)
    x_pos = cut_track1(x_pos, 7773, mod)
    x_pos = deal_with_inc(x_pos, 36, mod)
    x_pos = cut_track1(x_pos, 2903, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 75, mod)
    x_pos = cut_track1(x_pos, 239, mod)
    x_pos = deal_with_inc(x_pos, 45, mod)
    x_pos = cut_track1(x_pos, 5450, mod)
    x_pos = deal_with_inc(x_pos, 10, mod)
    x_pos = cut_track1(x_pos, 6661, mod)
    x_pos = deal_with_inc(x_pos, 64, mod)
    x_pos = cut_track1(x_pos, -6842, mod)
    x_pos = deal_with_inc(x_pos, 40, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 31, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 46, mod)
    x_pos = cut_track1(x_pos, 6462, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = cut_track1(x_pos, -8752, mod)
    x_pos = deal_with_inc(x_pos, 28, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 43, mod)
    x_pos = deal_into_new_deck_track1(x_pos, mod)
    x_pos = deal_with_inc(x_pos, 54, mod)
    x_pos = cut_track1(x_pos, 9645, mod)
    x_pos = deal_with_inc(x_pos, 44, mod)
    x_pos = cut_track1(x_pos, 5342, mod)
    x_pos = deal_with_inc(x_pos, 66, mod)
    x_pos = cut_track1(x_pos, 3785, mod)

    return x_pos

# @numba.jit('i8(i8,i8)', nopython=True, nogil=True, fastmath=True)
# def single_pass_reverse(y_pos, mod):
#     y_pos = inv_cut_track1(y_pos, 3785, mod)
#     y_pos = inv_deal_with_inc(y_pos, 66, mod)
#     y_pos = inv_cut_track1(y_pos, 5342, mod)
#     y_pos = inv_deal_with_inc(y_pos, 44, mod)
#     y_pos = inv_cut_track1(y_pos, 9645, mod)
#     y_pos = inv_deal_with_inc(y_pos, 54, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 43, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 28, mod)
#     y_pos = inv_cut_track1(y_pos, -8752, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, 6462, mod)
#     y_pos = inv_deal_with_inc(y_pos, 46, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 31, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 40, mod)
#     y_pos = inv_cut_track1(y_pos, -6842, mod)
#     y_pos = inv_deal_with_inc(y_pos, 64, mod)
#     y_pos = inv_cut_track1(y_pos, 6661, mod)
#     y_pos = inv_deal_with_inc(y_pos, 10, mod)
#     y_pos = inv_cut_track1(y_pos, 5450, mod)
#     y_pos = inv_deal_with_inc(y_pos, 45, mod)
#     y_pos = inv_cut_track1(y_pos, 239, mod)
#     y_pos = inv_deal_with_inc(y_pos, 75, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, 2903, mod)
#     y_pos = inv_deal_with_inc(y_pos, 36, mod)
#     y_pos = inv_cut_track1(y_pos, 7773, mod)
#     y_pos = inv_deal_with_inc(y_pos, 14, mod)
#     y_pos = inv_cut_track1(y_pos, -2176, mod)
#     y_pos = inv_deal_with_inc(y_pos, 29, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 35, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 7, mod)
#     y_pos = inv_cut_track1(y_pos, 8414, mod)
#     y_pos = inv_deal_with_inc(y_pos, 66, mod)
#     y_pos = inv_cut_track1(y_pos, -5502, mod)
#     y_pos = inv_deal_with_inc(y_pos, 2, mod)
#     y_pos = inv_cut_track1(y_pos, -2515, mod)
#     y_pos = inv_deal_with_inc(y_pos, 56, mod)
#     y_pos = inv_cut_track1(y_pos, 5898, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, -4713, mod)
#     y_pos = inv_deal_with_inc(y_pos, 24, mod)
#     y_pos = inv_cut_track1(y_pos, -4427, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, 4292, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 64, mod)
#     y_pos = inv_cut_track1(y_pos, 9098, mod)
#     y_pos = inv_deal_with_inc(y_pos, 72, mod)
#     y_pos = inv_cut_track1(y_pos, -2609, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, 2847, mod)
#     y_pos = inv_deal_with_inc(y_pos, 41, mod)
#     y_pos = inv_cut_track1(y_pos, -532, mod)
#     y_pos = inv_deal_with_inc(y_pos, 13, mod)
#     y_pos = inv_cut_track1(y_pos, 9942, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, -4193, mod)
#     y_pos = inv_deal_with_inc(y_pos, 61, mod)
#     y_pos = inv_cut_track1(y_pos, 2831, mod)
#     y_pos = inv_deal_with_inc(y_pos, 31, mod)
#     y_pos = inv_cut_track1(y_pos, 155, mod)
#     y_pos = inv_deal_with_inc(y_pos, 53, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 5, mod)
#     y_pos = inv_cut_track1(y_pos, 2974, mod)
#     y_pos = inv_deal_with_inc(y_pos, 51, mod)
#     y_pos = inv_cut_track1(y_pos, -105, mod)
#     y_pos = inv_deal_with_inc(y_pos, 17, mod)
#     y_pos = inv_cut_track1(y_pos, 8404, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, -1292, mod)
#     y_pos = inv_deal_with_inc(y_pos, 24, mod)
#     y_pos = inv_cut_track1(y_pos, 8509, mod)
#     y_pos = inv_deal_with_inc(y_pos, 34, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_cut_track1(y_pos, -5008, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 53, mod)
#     y_pos = inv_cut_track1(y_pos, 1336, mod)
#     y_pos = inv_deal_with_inc(y_pos, 66, mod)
#     y_pos = inv_cut_track1(y_pos, 1221, mod)
#     y_pos = inv_deal_with_inc(y_pos, 48, mod)
#     y_pos = inv_cut_track1(y_pos, -3393, mod)
#     y_pos = inv_deal_with_inc(y_pos, 15, mod)
#     y_pos = inv_cut_track1(y_pos, 4219, mod)
#     y_pos = inv_deal_into_new_deck_track1(y_pos, mod)
#     y_pos = inv_deal_with_inc(y_pos, 40, mod)
#     y_pos = inv_cut_track1(y_pos, -2325, mod)
#     y_pos = inv_deal_with_inc(y_pos, 14, mod)
#     y_pos = inv_cut_track1(y_pos, -7039, mod)
#     y_pos = inv_deal_with_inc(y_pos, 12, mod)
#     y_pos = inv_cut_track1(y_pos, -2354, mod)
#     y_pos = inv_deal_with_inc(y_pos, 48, mod)
#     y_pos = inv_cut_track1(y_pos, 9374, mod)
#     return y_pos

mod = 119315717514047

y_pos = 2020
rep = 101741582076661

# @numba.jit('i8(i8)', nopython=True, nogil=True, fastmath=True)
# def run(y_pos):
#     mod = 119315717514047
#     for i in range(101741582076661):
#         y_pos = single_pass_reverse(y_pos, mod)
#     return y_pos

# # 17574135437386 = (119315717514047-101741582076661)
# @numba.jit('i8(i8)', nopython=True, nogil=True, fastmath=True)
# def run2(y_pos):
#     mod = 119315717514047
#     for i in range(17574135437386):
#         y_pos = single_pass_forward(y_pos, mod)
#     return y_pos

# @numba.jit('i8(i8)', nopython=True, nogil=True, fastmath=True)
# def find_rep(y_pos):
#     mod = 119315717514047
#     origin = y_pos
#     for i in range(101741582076661):
#         y_pos = single_pass_forward(y_pos, mod)
#         if y_pos == origin:
#             break
#     return i+1


# @numba.jit('i8(i8,i8)', nopython=True, nogil=True, fastmath=True)
# def find_rep_small(y_pos, mod):
#     origin = y_pos
#     for i in range(mod):
#         y_pos = single_pass_forward(y_pos, mod)
#         if y_pos == origin:
#             break
#     return i+1


# With the hint from https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbt5yuy/
def egcd(a, b):
    """returns x,y,g such that a*x + b*y = g = gcd(a,b)

    https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python

    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

b = single_pass_forward(0, mod)
a = (single_pass_forward(1, mod) - b) % mod
a_inv = modinv(a,mod)

def f(x):
    return (a*x+b) % mod

def f_inv(x):
    return (a_inv*(x-b)) % mod

# Checking that the new computation is correct
for i in np.random.randint(mod, size=100):
    i = int(i)
    assert f(i) == single_pass_forward(i, mod)

rep_curr = rep
c1 = a_inv
c0 = -b*a_inv
y = y_pos
while rep_curr != 0:
    if rep_curr % 2 == 1:
        y = (c1*y + c0) % mod

    rep_curr //= 2
    c0 = (c0*c1 + c0) % mod
    c1 = (c1*c1) % mod

print('Part 2', y)

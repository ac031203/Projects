import random
import math


def f_find(s, l, q):  # function to calculate hash value
    f = 0
    temp = 1 % q
    for i in range(l):
        f += (temp * ((ord(s[l - i - 1]) - 65) % q)) % q
        f %= q
        temp *= 26 % q
        temp %= q
    return f % q


def f_find2(s, l, q, ind):
    f = 0
    temp = 1
    for i in range(l):
        if l - i - 1 == ind:
            temp *= 26 % q
            temp %= q
        else:
            f += (temp * ((ord(s[l - i - 1]) - 65) % q)) % q
            f %= q
            temp *= 26 % q
            temp %= q
    return f % q


def fpw(n, r):  # fast power funtion
    if n == 0:
        return 1
    x = fpw(n // 2, r) % r
    x = (x * x) % r
    if n % 2 == 1:
        x = (x * 26) % r
    return x % r


# To generate random prime less than N
def randPrime(N):
    primes = []
    for q in range(2, N + 1):
        if (isPrime(q)):
            primes.append(q)
    return primes[random.randint(0, len(primes) - 1)]


# To check if a number is prime
def isPrime(q):
    if (q > 1):
        for i in range(2, int(math.sqrt(q)) + 1):
            if (q % i == 0):
                return False
        return True
    else:
        return False


# pattern matching
def randPatternMatch(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatch(q, p, x)


# pattern matching with wildcard
def randPatternMatchWildcard(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatchWildcard(q, p, x)


# return appropriate N that satisfies the error bounds
def findN(eps, m):  # If there is a false positive that is a mod q = b mod q , where a not equal to b , it means that
    # (a-b) mod q = 0 , since there are m bits so max value of mod(a-b) can be 26^m -1 , using claim 1 we get that
    # there can be total of log2(26^m-1) prime divisors , which is approx mlog2(26) , now these are the number of
    # primes which will cause collision, so we want the Pr(bad primes) < eps , so we get mlog2(26)/T < eps ,
    # where T is the total number of primes up to N, so T > mlog2(26)/eps = k/2(say) , also T >= N/2log2(N) [using
    # claim 2], for upper bound N/2log2(N) > k/2
    k = math.ceil((2 * m * math.log(26, 2)) / eps)
    '''lo = 2
    hi = 2
    # performing binary search to get the upper bound , where lo is 2 and hi is the number greater than k by
    # multiplying by 2
    hi = k**2
    mid = math.ceil((lo + hi)/ 2)
    while lo <= hi:
        mid = math.ceil((lo + hi)/2)
        if math.ceil(mid / math.log(mid, 2)) > k:
            hi = mid - 1
        else:
            lo = mid + 1'''
    # I have graphically calculated that when N = 1.2*k*log2(k), then N/logN > k
    return int(1.2 * k * math.log2(k))


# Return sorted list of starting indices where p matches x
def modPatternMatch(q, p, x):  # standard implementation of rolling hash functions as in Rabin Karp algorithm
    m = len(p)
    n = len(x)
    L = []
    pre = fpw(m - 1, q)
    h = f_find(x, m, q)
    fp = f_find(p, m, q)
    if h == fp:
        L.append(0)
    for i in range(1, n - m + 1):  # time complexity is 0(nlog2q) as we are traversing the text and performing
        # arithmetic operations in the order of O(log2q) because it is given in assignment that O(b) for b bit,
        # so for prime number q no of bits is log2(q)
        h -= pre * (ord(x[i - 1]) - 65) % q
        h %= q
        h *= (26 % q)
        h %= q
        h += (ord(x[i + m - 1]) - 65) % q
        h %= q
        if h == fp:
            L.append(i)
    return L


# space complexity of O(logn + logq) as mentioned logn is unavoidable and logq arises as we are storing pre,h,fp which are basically mod q so logq bits


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q, p, x):  # just skipping the '?' and ignoring the hash value at this index
    m = len(p)
    n = len(x)
    ind = -1
    for i in range(m):
        if p[i] == '?':
            ind = i
            break
    if ind == -1:
        return modPatternMatch(q, p, x)
    L = []
    pre = fpw(m - 1, q)
    pre2 = fpw(m - ind - 1, q)
    h = f_find(x, m, q)
    fp = f_find2(p, m, q, ind)
    if (h - (pre2 * (ord(x[ind]) - 65)) % q) % q == fp:
        L.append(0)

    for i in range(1, n - m + 1):
        h -= pre * (ord(x[i - 1]) - 65) % q
        h %= q
        h *= (26 % q)
        h %= q
        h += (ord(x[i + m - 1]) - 65) % q
        h %= q
        if (h - (pre2 * (ord(x[i + ind]) - 65)) % q) % q == fp:
            L.append(i)

    return L
# whole implementation same as modPatternMatch just skipping the index where there is a '?'

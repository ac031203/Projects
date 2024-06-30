def AssignmentTC():
    print("Assignment Test Cases:")
    q1 = listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0)
    if (q1 == []):
        print("TESTCASE 1 PASS HAI !")
    else:
        print("TESTCASE 1 FAILED ! ;(")
        print("YOUR ANS: ",q1)
        print("JURY'S ANS: []")
    print("-X-"*100)
    q2 = listCollisions([1.0, 1.0, 1.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5, 5.0)
    if (q2 == [(1.0, 0, -2.0), (1.0, 2, 2.0)]):
        print("TESTCASE 2 PASS HAI !")
    else:
        print("TESTCASE 2 FAILED ! ;(")
        print("YOUR ANS:",q2)
        print("JURY'S ANS: [(1.0, 0, -2.0), (1.0, 2, 2.0)]")
    print("-X-" * 100)
    q3 = listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0)
    party = True
    if (len(q3) != 6):
        party = False
    else:
        ans3 = [(1.0, 1, 1.0), (1.505, 0, 0.0), (1.6756, 1, 0.3377), (1.7626, 0, -0.0001), (1.8163, 1, 0.2080),(1.8533, 0, -0.0002)]

        for i in range(len(q3)):
            if (abs(q3[i][0] - ans3[i][0]) <= 0.0001 and abs(q3[i][2] - ans3[i][2]) <= 0.0001):
                continue
            else:
                party = False
                print("Found differing element from Jury:",q3[i][0],"!=",ans3[i][0])
                break
    if (party):
        print("TESTCASE 3 PASS HAI !")
    else:
        print("TESTCASE 3 FAILED '(")
        print("YOUR ANS: ",q3)
        print("JURY'S ANS: [(1.0, 1, 1.0), (1.505, 0, 0.0), (1.6756, 1, 0.3377), (1.7626, 0, -0.0001), (1.8163, 1, 0.2080),(1.8533, 0, -0.0002)]")
    print("-X-" * 100)
    q4 = listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5)
    if (q4 == [(1.0, 1, 1.0)]):
        print("TESTCASE 4 PASS HAI !")
    else:
        print("TESTCASE 4 FAILED '(")
        print("YOUR ANS:",q4)
        print("JURY'S ANS: [(1.0, 1, 1.0)]")


def Time(v1, v2, x):
    if ((v1 <= 0 and v2 >= 0) or (v1 <= 0 and v2 <= 0 and abs(v1) >= abs(v2)) or (v1 >= 0 and v2 > 0 and v2 >= v1) or v1 == v2):
        return float('inf')
    else:
        v12 = v1 - v2 
        return abs(x / (v12))


def POC(v1, v2, x1, x2):
    if Time(v1, v2, x2 - x1) == float('inf'):
        return -1
    return x1 + v1 * Time(v1, v2, (x2-x1))


def final_vel1(m1, m2, v1, v2):
    m12 = (m1-m2)*v1 + ((2*m2)*v2)
    return (m12)/(m1+m2)


def final_vel2(m1, m2, v1, v2):
    m12 = (2*m1)*v1-(m1-m2)*v2
    return (m12)/(m1+m2)

class MinHeap:
    class _item:
        __slots__ = '_key', '_value'

        def __init__(self, time, i):
            self._key = time
            self._value = i

        def __lt__(self, other):
            if type(self._key) == str:
                return False
            elif type(other._key)==str:
                return True
            elif self._key < other._key:
                return True
            elif self._key == other._key:
                if self._value < other._value:
                    return True
                else:
                    return False
            else:
                return False

        def change(self, next):
            self._key = next

        def val(self):
            return self._key

        def ind(self):
            return self._value

    def __init__(self, construct):
        self._data = [self._item(p, q) for p, q in construct]
        self._pos = [i for i in range(len(construct))]
        self._current_size = len(construct)
        if self._current_size > 1:
            self._Heapify()

    def HeapUp(self, i):
        """
        Moves the value up in the tree to maintain the heap property.
        """
        # While the element is not the root or the left element
        stop = False
        while ((i - 1) // 2 >= 0) and stop is False:
            # If the element is less than its parent swap the elements
            if self._data[i] < self._data[(i - 1) //  2]:
                self._data[i], self._data[(i - 1) //2] = self._data[(i - 1) // 2], self._data[i]
                self._pos[self._data[i].ind()], self._pos[self._data[(i-1)//2].ind()] = self._pos[self._data[(i-1)//2].ind()], self._pos[self._data[i].ind()]
            else:
                stop = True
            # Move the index to the parent to keep the properties
            i = (i - 1) // 2

    def Enqueue(self, t, i):
        """
        Inserts a value into the heap
        """
        # Append the element to the heap
        self._data.append((t, i))
        self._pos.append(len(self._data) - 1)
        # Increase the size of the heap.
        self._current_size += 1
        # Move the element to its position from bottom to the top
        self.HeapUp(self._current_size - 1)

    def _min_child(self, i):
        # If the current node has only one child, return the index of the unique child
        if self._current_size - 1 < (i * 2) + 2:
            return i * 2 + 1
        else:
            # Herein the current node has two children
            # Return the index of the min child according to their values
            if self._data[i * 2 + 1] < self._data[(i * 2) + 2]:
                return i * 2 + 1
            else:
                return (i * 2) + 2

    def HeapDown(self, i):
        # if the current node has at least one child
        while (i * 2 + 1) <= self._current_size - 1:
            # Get the index of the min child of the current node
            mc = self._min_child(i)
            # Swap the values of the current element is greater than its min child
            if self._data[mc] < self._data[i]:
                self._data[i], self._data[mc] = self._data[mc], self._data[i]
                self._pos[self._data[i].ind()],self._pos[self._data[mc].ind()] = self._pos[self._data[mc].ind()],self._pos[self._data[i].ind()]
            i = mc

    def _Heapify(self):
        for i in range(self._current_size - 2, -1, -1):
            self.HeapDown(i)

    def GetMin(self):
        if len(self._data) == 0:
            return ("Empty priority queue")
        item = self._data[0]
        return (item._key, item._value)

    def ExtractMin(self):
        # Equal to 1 since the heap list was initialized with a value
        if len(self._data) == 0:
            return 'Empty heap'

        # Move the last value of the heap to the root
        self._data[0] = self._data[self._current_size - 1]
        self._current_size -= 1
        item = self._data.pop();
        self._pos.pop()

        # Decrease the size of the heap

        # Move down the root (value at index 0) to keep the heap property
        self.HeapDown(0)

        # Return the min value of the heap
        return (item._key, item._value)

    def update(self, i, new):
        if new >= self._data[self._pos[i]].val():
            self._data[self._pos[i]].change(new)
            self.HeapDown(self._pos[i])
        else:
            self._data[self._pos[i]].change(new)
            self.HeapUp(self._pos[i])

    def printpos(self):
        print(*self._pos)
        return None

    def printdata(self):
        for i in self._data:
            print(i.val(), i.ind())
        return None


def listCollisions(M,x,v,m,T):
    n = len(M)
    Tl = []
    for i in range(n-1):
        Tl.append((Time(v[i],v[i+1],x[i+1]-x[i]),i))
    h = MinHeap(Tl)
    if (n == 1):
        return []
    if (n == 2):
        t = h.GetMin()[0]
        x = h.GetMin()[1]
        if (t == float('inf')):
            return []
        else:
            return [(t, 0, x)]
    #code starts
    else:
        t = 0
        no_of_collisions = 0
        ans = []
        last_updated = [0 for i in range(n)]
        while no_of_collisions < m and t <= T:
            (ans_t,i) = h.GetMin()
            t = ans_t
            if t > T:
                break






            if (i == 0):
                ans_x = POC(v[i], v[i + 1], x[i], x[i + 1])
                ans.append((t,i,ans_x))
                x[i] = ans_x;last_updated[i] = t
                x[i+1] = ans_x;last_updated[i+1] = t
                x[i+2] += v[i+2]*(t-last_updated[i+2]);last_updated[i+2] = t
                temp = v[i]
                vi = final_vel1(M[i], M[i + 1], v[i], v[i + 1])
                vii = final_vel2(M[i], M[i + 1], temp, v[i + 1])
                v[i] = vi
                v[i+1] = vii
                h.update(i, float("inf"))
                h.update(i + 1,t+Time(v[i + 1], v[i + 2], x[i + 2] - x[i + 1]))
            elif (i == n - 2):
                ans_x = POC(v[i], v[i + 1], x[i], x[i + 1])
                ans.append((t, i, ans_x))
                x[i] = ans_x
                last_updated[i] = t
                x[i-1] += v[i-1]*(t-last_updated[i-1]);last_updated[i-1] = t
                x[i+1] = ans_x;last_updated[i+1]=t
                temp = v[i]
                vi = final_vel1(M[i], M[i + 1], v[i], v[i + 1])
                vii = final_vel2(M[i], M[i + 1], temp, v[i + 1])
                v[i] = vi;v[i+1]=vii
                h.update(i, float('inf'))
                new_t = Time(v[i - 1], v[i], x[i] - x[i - 1])
                h.update(i - 1, t + new_t)

            else:
                ans_x = POC(v[i], v[i + 1], x[i], x[i + 1])
                ans.append((t, i, ans_x))
                x[i] = ans_x
                last_updated[i] = t
                x[i-1] += v[i-1]*(t-last_updated[i-1])
                last_updated[i - 1] = t
                x[i+1] = ans_x
                last_updated[i + 1] = t
                x[i+2] += v[i+2]*(t-last_updated[i+2])
                last_updated[i + 2] = t
                temp = v[i]
                vi = final_vel1(M[i], M[i + 1], v[i], v[i + 1])
                vii = final_vel2(M[i], M[i + 1], temp, v[i + 1])
                v[i] = vi
                v[i+1] = vii
                new_t = Time(v[i - 1], v[i], x[i] - (x[i - 1]))
                h.update(i - 1, t+new_t)
                h.update(i, float('inf'))
                h.update(i + 1, t+Time(v[i + 1], v[i + 2], x[i + 2] - x[i + 1]))

            no_of_collisions += 1
    final = []
    for i in ans:
        if i[0] <= T:
            final.append((round(i[0], 4), i[1], round(i[2], 4)))
    return final

'''print(listCollisions([1.0,1.0,1.0],[0.0,1.0,2.0],[-1.0,0.0,1.0],2,10.0))'''
'''AssignmentTC()'''
'''print(listCollisions([1.0, 1.0, 1.0,1.0,1.0,1.0],[0.0, 0.2,0.6,0.7,0.8, 1.0], [-8.0,0.0,-2.0,0.0,1.0, 0.0], 10.0, 10.0))
print(listCollisions([1.0,1.0,1.0,1.0],[0.0,1.0,2.0,3.0],[1.0,-1,0,1.0,3.0],2,100))'''
'''print(listCollisions([1.0,1.0,1.0,1.0],[0.0,1.0,2.0,3.0],[1.0,-1.0,1.0,-1.0],15,10.0))'''
'''print(listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0))'''

'''print(listCollisions([1.0,1.0,1.0,1.0],[0.0,1.0,2.0,3.0],[1.0,-1,0,1.0,3.0],2,100))
print(listCollisions([1.0,1.0,1.0,1.0,1.0,1.0],[0.0,1.0,2.0,3.0,4.0,5.0],[1.0,0.0,1.0,0.0,1.0,0.0],8,100.0))
print(listCollisions([1.0, 1.0, 1.0,1.0,1.0,1.0],[0.0, 0.2,0.6,0.7,0.8, 1.0], [-8.0,0.0,-2.0,0.0,1.0, 0.0], 10.0, 10.0))'''

'''t = [(1.0,2),(float('inf'),1),(1.0,0)]
h = MinHeap(t)
h.posi()
h.update(0,float('inf'))
h.data()
h.posi()'''

'''h.printdata()
h.printpos()
print(h.GetMin())'''

'''l = [(4,2), (4,1),(4,0)]
h = MinHeap(l)
print(h.GetMin())

h.printpos()
h.printdata()'''

'''print(Time(-1.0, -2.0, 3))
print(POC(-2, -3.56, 0, 2.5))
print(final_vel(1.0, 1.0, 0.0, -1.0))'''

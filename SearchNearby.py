class PointDatabase:
    class Node:
        def __init__(self, data):
            self.value = data
            self.left = None
            self.right = None
            self.assoc = []  # associated list in which we will be storing the coordinates in sorted order by y - coordinate

    def ConstructTree2d(self, lx, ly):
        # constructing a balanced BST out of the tuples in which node has a list associated with it which has all the
        # elements of the subtree rooted at that node sorted by y coordinate
        if not lx:
            return None
        if len(lx) == 1:
            node = self.Node(lx[0])
            node.assoc = [ly[0]]
        else:
            mid_val = len(lx) // 2
            node = self.Node(lx[mid_val])
            yl = []
            yr = []
            for i in range(len(ly)):
                if ly[i][0] < lx[mid_val][0]:
                    yl.append(ly[i])
                elif ly[i][0] > lx[mid_val][0]:
                    yr.append(ly[i])
            node.left = self.ConstructTree2d(lx[:mid_val], yl)
            node.right = self.ConstructTree2d(lx[mid_val + 1:], yr)
            node.assoc = ly
        return node

    def __init__(self, pointlist):
        lx = sorted(pointlist)  # sorted by x coord
        ly = sorted(pointlist, key=lambda x: x[1])  # sorted by y coord
        self.root = self.ConstructTree2d(lx, ly)

    @staticmethod
    def FindInRangeNode(root, p_min, p_max):
        # this function finds the first node which is in the x range
        rangenode = root
        # we start the root of the tree and compare its x node with the x range if it is greater we take left
        # otherwise right
        while rangenode is not None:
            val = rangenode.value[0]
            if p_max < val:
                rangenode = rangenode.left
            elif p_min > val:
                rangenode = rangenode.right
            elif p_min <= val <= p_max:
                break
        return rangenode

    def lower(self, l, lo, hi, el):
        # finding lower bound using binary search
        if hi < lo:
            return "None"
        elif lo == hi:

            if l[lo][1] >= el:
                return lo
            else:
                return "None"
        else:
            mid = (lo + hi) // 2
            if l[mid][1] < el:
                return self.lower(l, mid + 1, hi, el)
            elif l[mid][1] == el:
                return mid
            else:
                if l[mid - 1][1] < el:
                    return mid
                else:
                    return self.lower(l, lo, mid - 1, el)

    def upper(self, l, lo, hi, el):
        # finding upper bound using binary search
        if hi < lo:
            return "None"
        elif lo == hi:
            if l[lo][1] <= el:
                return lo
            else:
                return "None"
        else:
            mid = (lo + hi) // 2
            if l[mid][1] < el:
                if l[mid + 1][1] > el:
                    return mid
                return self.upper(l, mid + 1, hi, el)
            elif l[mid][1] == el:
                return mid
            else:
                return self.upper(l, lo, mid - 1, el)

    def SearchY(self, l, y1,
                y2):  # my idea is to simply find the least upper bound of y1(the least element of the range)
        # and greatest lower bound of y2(max element of the range)
        if y1 < l[0][1]:
            glb = 0
        else:
            glb = self.lower(l, 0, len(l) - 1, y1)
        lub = self.upper(l, 0, len(l) - 1, y2)
        if glb == "None" or lub == "None":
            return []
        ans = [l[i] for i in range(glb, lub + 1)]
        return ans

    def Search(self, x1, x2, y1, y2):  # logic is inspired from various university websites ,but it has been coded
        # entirely by myself the logic is that we will first search all the x-eligible points in our constructed tree
        # and then subsequently check their y by using our associated list attribute of the node
        results = []
        # finding first node in range (LCA)
        rangenode = self.FindInRangeNode(self.root, x1, x2)
        if rangenode is None:
            return results
        elif x1 <= rangenode.value[0] <= x2 and y1 <= rangenode.value[1] <= y2:
            results.append(rangenode.value)
            # Traverse the nodes in left child of LCA
        vl = rangenode.left

        while vl is not None:
            vv = vl.value
            # Check if the node is a valid node in range
            if x1 <= vv[0] <= x2 and y1 <= vv[1] <= y2:
                results.append(vv)

            # Search the associated y sorted list at the right child of current node in xtree
            if x1 <= vl.value[0]:
                if vl.right is not None:
                    for i in self.SearchY(vl.right.assoc, y1, y2):
                        results.append(i)
                vl = vl.left
            else:
                vl = vl.right

        # Traverse the nodes in right child of LCA
        vr = rangenode.right

        while vr is not None:
            vrv = vr.value
            # Check if the node is a valid node in range
            if x1 <= vrv[0] <= x2 and y1 <= vrv[1] <= y2:
                results.append(vr.value)
            # Search the associated y sorted list at the left child of current node in xtree
            if x2 >= vr.value[0]:
                if vr.left is not None:
                    for i in self.SearchY(vr.left.assoc, y1, y2):
                        results.append(i)
                vr = vr.right
            else:
                vr = vr.left

        return results

    def searchNearby(self, q, d):
        if self.Search(q[0] - d, q[0] + d, q[1] - d, q[1] + d) is None:
            return []
        # by the definition of the distance defined the coordinates which can be at d distance from given coordinates
        # is mod(x-q[0])<=d and mod(y-q[1])<=d
        return self.Search(q[0] - d, q[0] + d, q[1] - d, q[1] + d)

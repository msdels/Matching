from cython.operator import dereference as deref, predecrement, preincrement
from libcpp.vector cimport vector
from libcpp.map cimport map as cmap, pair
from libc.stdint cimport *
from libc.math cimport abs, INFINITY
import sys

ctypedef vector[int64_t]* pvector

cdef _test_find(double[:] a, int64_t[:] b, double[:] candidates, int64_t[:] indexes, double caliper):
    cdef:
        pvector YY
        cmap[double, pvector] X
        vector[pair[int64_t, int64_t]] Y
        cmap[double, pvector].iterator it, it2
        pair[double, pvector] compare, compare_pre
        int i
        double target
       
    for i in range(len(a)):
        it = X.find(a[i])
        if it != X.end():
            # append value
            deref(it).second.push_back(b[i])
        else:
            YY = new vector[int64_t]()
            YY.push_back(b[i])
            X.insert(pair[double, pvector](a[i], YY))
        
    
    for i in range(len(candidates)):
        if X.size() == 0:
            break
            
        target = candidates[i]
        it = X.lower_bound(target) # >= or next
        if it != X.end():
            compare = deref(it)
            delta_post = abs(target - compare.first)
        else:
            delta_post = INFINITY

        it2 = it
        if it != X.begin():
            it2 = predecrement(it2) # <

            compare_pre = deref(it2)
            delta_pre = abs(target - compare_pre.first)
        else:
            delta_pre = INFINITY
    
        # bail.
        if (delta_post > caliper) and (delta_pre > caliper):
            continue
            
        if delta_post < delta_pre:
            Y.push_back(pair[int64_t, int64_t](compare.second.back(), indexes[i]))
            
            compare.second.pop_back()
            if compare.second.size() == 0:
                X.erase(it)
        else:
            Y.push_back(pair[int64_t, int64_t](compare_pre.second.back(), indexes[i]))
            compare_pre.second.pop_back()
            if compare_pre.second.size() == 0:
                X.erase(it2)
                
    return Y


cpdef test_find(a, b, c, d, caliper):
    return _test_find(a, b, c, d, caliper)
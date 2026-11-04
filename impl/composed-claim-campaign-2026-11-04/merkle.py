"""Verifier paths: RFC9162 2.1.3.2 and 2.1.4.2; independent of builder."""
import hashlib

def leaf(entry):
    return hashlib.sha256(b"\0"+entry).digest()

def node(left,right):
    return hashlib.sha256(b"\1"+left+right).digest()

def _hashes(xs):
    return all(isinstance(x,bytes) and len(x)==32 for x in xs)

def inclusion(entry,index,size,path,root):
    if (type(index) is not int or type(size) is not int or not 0<=index<size
        or size>1024 or len(path)>64 or not _hashes([root]+path)):
        return False
    fn,sn=index,size-1
    r=leaf(entry)
    for p in path:
        if sn==0: return False
        if fn&1 or fn==sn:
            r=node(p,r)
            while fn and not fn&1:
                fn >>= 1;sn >>= 1
        else: r=node(r,p)
        fn >>= 1;sn >>= 1
    return sn==0 and r==root

def consistency(old_size,new_size,old_root,new_root,path):
    if (type(old_size) is not int or type(new_size) is not int
        or not 1<=old_size<=new_size<=1024 or len(path)>64
        or not _hashes([old_root,new_root]+path)): return False
    if old_size==new_size: return not path and old_root==new_root
    if not path: return False
    fn,sn=old_size-1,new_size-1
    while fn&1: fn >>= 1;sn >>= 1
    if fn==0: fr=sr=old_root;rest=path
    else: fr=sr=path[0];rest=path[1:]
    for p in rest:
        if sn==0: return False
        if fn&1 or fn==sn:
            fr=node(p,fr);sr=node(p,sr)
            while fn and not fn&1:
                fn >>= 1;sn >>= 1
        else: sr=node(sr,p)
        fn >>= 1;sn >>= 1
    return sn==0 and fr==old_root and sr==new_root

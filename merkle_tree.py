import hashlib

def hash_function(data):
  
    if isinstance(data, bytes):
        return hashlib.sha256(data).hexdigest()
    elif isinstance(data, str):
        return hashlib.sha256(data.encode()).hexdigest()


class MerkleTree:
    def __init__(self, data, hash_function=hashlib.sha256):
        self.hash_function = hash_function
        self.left = None
        self.right = None
        self.hash = hash_function(data).hexdigest()
        self.leaf = True # Add this line to set the leaf attribute to True
        if len(data) > 1:
            self.leaf = False # Set leaf attribute to False if node is not a leaf
            mid = len(data) // 2
            self.left = MerkleTree(data[:mid], hash_function=self.hash_function)
            self.right = MerkleTree(data[mid:], hash_function=self.hash_function)
        elif len(data) == 0:
            raise ValueError("MerkleTree() arg is an empty sequence")

    def get_root_hash(self):
        return self.hash if self.leaf else hash_function(self.left.get_root_hash() + self.right.get_root_hash())

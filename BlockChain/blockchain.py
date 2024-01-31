from block import Block


class Blockchain:
    """
      This is BlockChain.The list of blocks in the blockchain
    """
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # create genesis block
    """
这段代码是一个用于创建创世区块的函数。
它创建了一个新的区块对象，并设置了初始的索引、时间戳、数据和前一个哈希值。

具体来说，代码调用 `Block` 类创建了一个新的区块对象。
构造函数的参数依次为索引 `0`、当前时间戳 `datetime.now()`、数据字符串 `"Genesis Block"` 和前一个哈希值 `"0"`。这些参数分别表示创世区块的索引、创建时间、数据（通常是一些初始信息）以及前一个区块的哈希值。

然后，代码将创建的区块对象作为函数的返回值。

创世区块是区块链中的第一个区块，它没有前一个区块，
因此前一个哈希值通常被设置为一个特定的值，例如 `"0"`。

总之，这个函数的作用是创建并返回一个创世区块对象，
该区块作为区块链的起始点。创世区块在区块链中承担了重要的角色，
标志着链的开始，并提供了第一个有效的哈希值作为后续区块的前一个哈希值参考。
    """
    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    # get latest block
    """
这段代码是一个用于获取最新区块的函数。
它简单地返回区块链中最后一个区块，也就是链中的最新区块。

具体来说，代码使用索引 `-1` 从 `self.chain` 列表中获取最后一个元素，
即最新的区块。然后，将该区块作为函数的返回值。

这个函数的作用是方便获取当前区块链中的最新状态，
可以用于查看最新区块的信息、进行进一步的操作或提供给其他部分使用。
    """

    def get_latest_block(self):
        return self.chain[-1]
    
    # add block
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
    
    # verify block 验证块

    """
这段代码是一个用于验证区块链有效性的函数。它遍历整个区块链，
检查每个区块的哈希值和前一个区块的哈希值，以确保链条没有被篡改。

具体来说，代码通过循环遍历区块链中的每一个区块（除了创世区块），
并分别将当前区块 `current_block` 和前一个区块 `previous_block` 赋值为链中相邻的两个区块。

然后，代码分别检查当前区块的哈希值是否等于调用 `calculate_hash()` 方法计算得到的哈希值，
以及当前区块的前一个哈希值是否等于前一个区块的哈希值。如果有任何一个条件不满足，
则函数返回 False，表示区块链无效；否则，继续检查下一个区块。

最后，如果循环结束后没有发现任何不一致的情况，
即所有区块的哈希值和前一个哈希值都是有效的，
函数返回 True，表示区块链有效。

总之，这段代码的作用是验证区块链是否有效，
即确保区块链中的每个区块都没有被篡改，
并且各个区块之间的哈希值链接是正确的。
这是区块链技术中非常重要的一部分，用于确保数据的完整性和安全性。
    
    """
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

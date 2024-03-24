import hashlib
import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
        self.nonce = 0

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            (
                str(self.index)
                + str(self.timestamp)
                + str(self.data)
                + str(self.previous_hash)
                + str(self.nonce)
            ).encode("utf-8")
        )
        return sha.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print("Block mined:", self.hash,  self.nonce)


class Blockchain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.create_admin_block()
    
    difficulty = 4

    def create_genesis_block(self):

        return Block(1, datetime.datetime.now().date(), {"name": "Genesis Block", "password": "genesis123"}, "0"*64, "")

    def create_admin_block(self):
        # return Block(0, datetime.datetime.now().date(), {"name": "admin", "password": "admin","Admin":True}, "0")
        # nonce = Block.nonce
        data = {"name": "Admin Block", "username": "admin",
                "password": "admin", "Admin": True}
        new_blocks = Block((len(self.get_chain()) + 1),
                           datetime.datetime.now().date(), data, "", "")
        new_blocks.mine_block(4)
        self.add_block(new_blocks)

    def get_latest_block(self):
        return self.chain[-1]

    def get_chain(self):

        return self.chain

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        new_block.mine_block(4)

        previous_hash = self.get_latest_block().hash
        curr_hash = new_block.calculate_hash()

        # First verification with prev hash
        if previous_hash != new_block.previous_hash:
            return False

        # Second verification with Current hash difficulty level
        if not curr_hash.startswith('0' * Blockchain.difficulty):
            # and curr_hash == new_block.calculate_hash():
            return False

        self.chain.append(new_block)

    def getStudentData(self):
        new_chain = []
        for i in self.chain:
            if i.data.get("Student") == True:
                new_chain.append(i)
        return new_chain

    def getFacultyData(self):
        new_chain = []
        for i in self.chain:
            if i.data.get("Faculty") == True:
                new_chain.append(i)
        return new_chain

    def getAttendanceData(self):
        new_chain = []
        for i in self.chain:
            if i.data.get("Attendance") == True:
                new_chain.append(i)
        return new_chain

    def getAdminData(self):
        new_chain = []
        for i in self.chain:
            if i.data.get("Admin") == True:
                new_chain.append(i)
        return new_chain

    def getReviewsData(self):
        new_chain = []
        for i in self.chain:
            if i.data.get("Reviews") == True:
                new_chain.append(i)
        return new_chain

    def getJustificationData(self):
        new_chain = []
        for i in self.chain:
            if i.data.get("Justification") == True:
                new_chain.append(i)
        return new_chain

    def getAllData(self):
        new_chain = []
        for i in self.chain:
            new_chain.append(i)
        return new_chain


    def isValidchain(self):
        for i in range(1,len(self.chain)):
            previous = self.chain[i].previous_hash
            current = self.chain[i-1].hash
            if previous != current:
                print("The Blockchain is void and tempered!")
            elif current == previous:
                print("The Blockchain is valid and not tempered.")

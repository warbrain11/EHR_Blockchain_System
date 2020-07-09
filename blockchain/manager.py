from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Manager
from django.db.models import QuerySet
from django.db.models import signals
from django.db import connection
from datetime import datetime
import hashlib
import nacl, nacl.secret, nacl.utils, nacl.pwhash
import json

class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, date_of_birth, password = None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have a email')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last_name')
        if not date_of_birth:
            raise ValueError('Users must have a date of birth')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth,
            password = password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, date_of_birth, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class BlockchainQuerySet(QuerySet):
    def update(self, *args, **kwargs):
        raise Exception("Disabled for security reasons")

class Blockchain_Manager(Manager):
    def get_queryset(self):
        return BlockchainQuerySet(self.model, using = self._db)

    def add_block(self, block_data):
        with connection.cursor() as cursor:
            #Get count
            cursor.execute("""SELECT b.Hash, b.PreviousHash, b.TimeStamp, b.BlockData FROM Blockchain b""") # ORDER BY b.TimeStamp DESC""")
            results = cursor.fetchall()

            #If cursor is empty create genesis block then add new block
            if (len(results) == 0):
                #Create genesis hash
                g_h = hashlib.sha256()

                g_p_h = '0'                                                                                       #Genesis Previous Hash
                g_t = datetime.strftime(datetime.now().replace(microsecond = 0), "%Y-%m-%dT%H:%M:%S")             #Genesis Time
                g_b_d = '[]'                                                                                      #Genesis Block Data

                g_h.update(bytes(g_p_h.encode('utf-8')))
                g_h.update(bytes(g_t.encode('utf-8')))
                g_h.update(bytes(g_b_d.encode('utf-8')))

                g_hash = g_h.hexdigest()

                gen_block = self.model(Hash = g_hash, PreviousHash = g_p_h, TimeStamp = g_t, BlockData = g_b_d)
                gen_block.save(using = self._db)
                
                #Creating the new block consists of creating a time stamp, getting the previous block's hash, and creating
                #a new hash by processing the time stamp, previous hash, and block data through the hashlib sha256 algorithm
                h = hashlib.sha256()

                prev_hash = gen_block.Hash
                
                time_stamp = datetime.strftime(datetime.now(),  "%Y-%m-%dT%H:%M:%S")
                h.update(bytes(prev_hash.encode('utf-8')))
                h.update(bytes(time_stamp.encode('utf-8')))
                h.update(bytes(block_data.encode('utf-8')))

                my_hash = h.hexdigest()
                new_block = self.model(Hash = my_hash, PreviousHash = prev_hash, TimeStamp = time_stamp, BlockData = block_data)
                new_block.save(using = self._db)

                return new_block
            #If the blockchain is not empty, retrieve the most recent block and make a new block based on the previous block's data
            elif(len(results) > 0):
                prev_hash = results[-1][0]
                time_stamp = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")

                h = hashlib.sha256()

                h.update(bytes(prev_hash.encode('utf-8')))
                h.update(bytes(time_stamp.encode('utf-8')))
                h.update(bytes(block_data.encode('utf-8')))

                my_hash = h.hexdigest()
                new_block = self.model(Hash = my_hash, PreviousHash = prev_hash, TimeStamp = time_stamp, BlockData = block_data)
                new_block.save(using = self._db)

                return new_block

    def check_blockchain(self):
        data = {}
        blockchain_status = 'Untampered'

        with connection.cursor() as cursor:
            #Get count
            cursor.execute("""SELECT b.id, b.Hash, b.PreviousHash, b.TimeStamp, b.BlockData FROM Blockchain b""") # ORDER BY b.TimeStamp DESC""")
            bc = cursor.fetchall()
            
            count = len(bc) - 1

            while(count > 0):
                current = bc[count]
                prev = bc[count - 1]

                #If the current Hash's previous hash does not equal the hash of the previous hash, the block is tampered with 
                if(current[2] != prev[1]):
                    data[str(prev[0])] = 'Tampered'
                    blockchain_status = 'Tampered'
                else:
                    """
                    h = hashlib.new("sha256")

                    h.update(bytes(bc[count][2].encode('utf-8')))
                    h.update(bytes(bc[count][3].encode('utf-8')))
                    h.update(bytes(bc[count][4].encode('utf-8')))

                    f_hash = h.hexdigest()

                    if(bc[count][1] != f_hash):
                        data[str(current[0])] = 'Tampered'
                    """

                    data[str(prev[0])] = 'Untampered'


                

                count -= 1

            return (data, blockchain_status)

    def repair(self, bc_file):
        test_data = {}
        tampered = False

        cursor = connection.cursor()

        bc_file = bc_file #open("/var/www/html/blockchain_server/blockchain/Files/blockchain.bc", "rb")
        key_file = open("/var/www/html/blockchain_server/blockchain/Files/key_file.bin", "rb")

        bc = bc_file.read()
        key = key_file.read()

        box = nacl.secret.SecretBox(key)
        decrypted_msg = box.decrypt(bc)

        bc_file.close()
        key_file.close()

        blockchain = json.loads(decrypted_msg.decode('utf-8'))

        count = 0
        
        #Checks if the uploaded blockchain is valid
        for block in blockchain:
            new_h = hashlib.new("sha256")

            new_h.update(bytes(block['PreviousHash'].encode('utf-8')))
            new_h.update(bytes(block['TimeStamp'][:-1].encode('utf-8'))) #Remove the 'Z' character at the end of the datetime string to generate the correct Hash
            new_h.update(bytes(block['BlockData'].encode('utf-8')))

            f_hash = new_h.hexdigest()

            count += 1
            if(block['Hash'] != f_hash):
                tampered = True

            #If the uploaded blockchain is valid, use the check blockchain function to find any tampered blocks, and replace them with values from the untampered, uploaded 
            #blockchain
            count = 0

            if(tampered == False):
                checked_data = self.check_blockchain()

                #Repairs the blockchain The loop goes through each block and determines if it is tampered. Tampered blocks are then replaced by untampered blocks from the
                #uploaded file

                self.all().delete()
                for key in checked_data[0]:       
                    """
                    cursor.execute("INSERT INTO Blockchain (Hash, PreviousHash, TimeStamp, BlockData) VALUES (%s, %s, %s, %s)", 
                    [blockchain[count]['Hash'], blockchain[count]['PreviousHash'], blockchain[count]['TimeStamp'], blockchain[count]['BlockData']])
                    cursor.commit()
                    """
                    
                    new_block = self.model(Hash = blockchain[count]['Hash'], PreviousHash = blockchain[count]['PreviousHash'], TimeStamp = blockchain[count]['TimeStamp'], BlockData = blockchain[count]['BlockData'])
                    new_block.save(using = self._db)
                    

                    count += 1
            else:
                raise ValueError("Uploaded file is tampered with. Please upload an untampered valid file.")

        return (blockchain)



        





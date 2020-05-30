from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Manager
from django.db import connection
from datetime import datetime
import hashlib

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

class Blockchain_Manager(Manager):
    def add_block(self, block_data):
        with connection.cursor() as cursor:
            #Get count
            cursor.execute("""SELECT b.Hash, b.PreviousHash, b.TimeStamp, b.BlockData FROM Blockchain b""") # ORDER BY b.TimeStamp DESC""")
            results = cursor.fetchall()

            #If cursor is empty create genesis block then add new block
            if (len(results) == 0):
                gen_block = self.model(Hash = '0', PreviousHash = '0', TimeStamp = datetime.now().replace(microsecond = 0), BlockData = '[]')
                gen_block.save(using = self._db)
                
                #Creating the new block consists of creating a time stamp, getting the previous block's hash, and creating
                #a new hash by processing the time stamp, previous hash, and block data through the hashlib sha256 algorithm
                h = hashlib.sha256()

                prev_hash = gen_block.Hash
                
                time_stamp = datetime.strftime(datetime.now(),  "%Y-%m-%dT%H:%M:%S")
                h.update(bytes(prev_hash, encoding = 'utf-8'))
                h.update(bytes(time_stamp, encoding = 'utf-8'))
                h.update(bytes(block_data, encoding = 'utf-8'))

                my_hash = h.hexdigest()
                new_block = self.model(Hash = my_hash, PreviousHash = prev_hash, TimeStamp = time_stamp, BlockData = block_data)
                new_block.save(using = self._db)

                return new_block
            #If the blockchain is not empty, retrieve the most recent block and make a new block based on the previous block's data
            elif(len(results) > 0):
                prev_hash = results[-1][0]
                time_stamp = datetime.strftime(datetime.now(),  "%Y-%m-%dT%H:%M:%S")

                h = hashlib.sha256()

                h.update(bytes(prev_hash, encoding = 'utf-8'))
                h.update(bytes(time_stamp, encoding = 'utf-8'))
                h.update(bytes(block_data, encoding = 'utf-8'))

                my_hash = h.hexdigest()
                new_block = self.model(Hash = my_hash, PreviousHash = prev_hash, TimeStamp = time_stamp, BlockData = block_data)
                new_block.save(using = self._db)

                return new_block
        





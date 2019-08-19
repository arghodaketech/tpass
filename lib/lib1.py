#/bin/python3
"""Class file for Manager class"""
import hashlib
import secrets
import binascii
import SecureString
import getpass
from lib.lib2 import Group
import pickle
import os
import sys
from Crypto.Cipher import AES

class Manager:
	"""This class holds the information required to operate the application.
	   It only stores the hash of the master password and details of the groups created.
	   It has various methods to maipulate the objects of diffrent groups
	   Members :   Name            - String       - Name of the user 
				   master_password - tuple        - [0] : password hash
				   								    [1] : salt
				   No_of_Groups    - integer      - Number of groups created
				   Groups_List     - list         - List of name of groups
				   Current_Group   - Group object - Group object that is currently loaded 
	   """

	def __init__(self):                                    # construtor
		self.Name = input("Enter your name : ")
		print("Password creation :\n(Note - Please enter a secure Password as it will be used to encrypt your passwords for other accounts.If you loose it then you won't be able to recover your passwords.)")
		self.master_password = self.password_hasher()          # set master password
		print("Master Password set successfully ...")
		print("Creating 'default' group ...")
		self.No_of_Groups = 0
		self.Groups_List = []
		self.Current_Group = self.group_creator('default') 
		print("'default' group created successfully ...")
		print('Saving Current State ...')
		self.dumper(self,'manager')							  # saving current state to storage
		print('Current state saved successfully ...\nInitialisation complete.')

	def password_hasher(self):
		"""stores the master password"""
		password = getpass.getpass(prompt = "Enter password : ", stream = None)
		confirm_password = getpass.getpass(prompt = "Confirm Password : ", stream = None)
		if(confirm_password != password):
			print("Password did not match.\nExiting the process.")
			exit(0)
		if(len(password) % 32 != 0):
				password += " " * ( 32 - len(password) % 32)
		password = password.encode("utf-8")
		salt = hashlib.sha256(secrets.token_bytes(64)).hexdigest().encode('ascii')
		pass_hash = hashlib.pbkdf2_hmac('sha512',password,salt,100000)
		pass_hash = binascii.hexlify(pass_hash)	
		stored_pass = pass_hash.decode('ascii')
		salt = salt.decode('ascii')
		SecureString.clearmem(password)
		SecureString.clearmem(confirm_password)
		del(password)
		del(confirm_password)
		return (pass_hash,salt)

	def encryptor(self,message):
		"""accepts and ecnrypts the value using master password"""
		password_to_encrypt = getpass.getpass(prompt = message, stream=None)
		confirm_password = getpass.getpass(prompt = "Confirm : ",stream=None)
		if(password_to_encrypt != confirm_password):
			SecureString.clearmem(password_to_encrypt)
			SecureString.clearmem(confirm_password)
			del (password_to_encrypt)
			del (confirm_password)
			print("Did not match")
			return -1
		master_password = getpass.getpass(prompt = "Enter Master Password : ", stream=None)
		if(len(master_password) % 32 != 0):
				master_password += " " * ( 32 - len(master_password) % 32)
		master_password = master_password.encode('utf-8')
		password_hash = hashlib.pbkdf2_hmac('sha512',master_password,self.master_password[1].encode('ascii'),100000)
		hash_decode = binascii.hexlify(password_hash)
		authentication_status = "0"
		if(hash_decode == self.master_password[0]):
			authentication_status = "1"	
		if(authentication_status == "1"):
			if(len(password_to_encrypt) % 32 != 0):
				password_to_encrypt += " " * ( 32 - len(password_to_encrypt) % 32)
			salt = secrets.token_bytes(16)
			encryptor = AES.new(master_password,AES.MODE_CBC,salt)
			encrypted_password = encryptor.encrypt(password_to_encrypt)
			
			SecureString.clearmem(password_to_encrypt)
			SecureString.clearmem(confirm_password)
			SecureString.clearmem(master_password)
			SecureString.clearmem(password_hash)
			SecureString.clearmem(hash_decode)
			SecureString.clearmem(authentication_status)

			del(encryptor)
			del(password_to_encrypt)
			del(confirm_password)
			del(master_password)
			del(password_hash)
			del(hash_decode)
			del(authentication_status)
			return (encrypted_password,salt)
		else:
			print("Incorrect Master Password.")
			return -1

	def decryptor(self,encrypted_value):
		"""decrypts the encrypted text using master password"""
		try:
			master_password = getpass.getpass("Enter master Password : ")
			if(len(master_password) % 32 != 0):
				master_password += " " * ( 32 - len(master_password) % 32)
			decryptor = AES.new(master_password,AES.MODE_CBC,encrypted_value[1])
			decrypted_information = decryptor.decrypt(encrypted_value[0]).decode('utf-8') 
			print("Decrypted Value       : ",decrypted_information)
			SecureString.clearmem(master_password)
			SecureString.clearmem(decrypted_information)
			del(master_password)
			del(decrypted_information)
		except Exception as e:
			print("Invalid Details.")

	def authenticator(self):
		"""authenticates using master password and returns 'True' if authenticated"""
		master_password = getpass.getpass(prompt = "Enter Master Password : ", stream=None)
		if(len(master_password) % 32 != 0):
				master_password += " " * ( 32 - len(master_password) % 32)
		master_password = master_password.encode('utf-8')
		password_hash = hashlib.pbkdf2_hmac('sha512',master_password,self.master_password[1].encode('ascii'),100000)
		hash_decode = binascii.hexlify(password_hash)
		if(hash_decode == self.master_password[0]):
			authentication_status = True
		else:
			authentication_status = False
		SecureString.clearmem(master_password)
		SecureString.clearmem(password_hash)
		SecureString.clearmem(hash_decode)
		del(master_password)
		del(password_hash)
		del(hash_decode)
		return(authentication_status)

	def group_creator(self,group_name):
		"""Creates and initialises a group"""
		group_obj = Group(group_name)
		self.dumper(group_obj,group_name)
		self.__updater()
		self.No_of_Groups = self.No_of_Groups + 1
		self.Groups_List.append(group_name)
		return group_obj

	def group_changer(self,group_name):
		"""changes the loaded group"""
		self.dumper(self.Current_Group,self.Current_Group.Group_Name)
		self.Current_Group = self.loader(group_name)
		self.__updater()

	def credential_adder(self,credential_name,credential_password,details):
		self.Current_Group.credential_add(credential_name,credential_password)
		self.Current_Group.details_add(credential_name,details)
		self.dumper(self.Current_Group,self.Current_Group.Group_Name)
		self.__updater()

	def credential_updater(self,credential_to_update,status,group_name,credential_name,updated_information,detail_name="",encryption_status=""):
		"""updates a particular credential"""
		if(group_name != self.Current_Group.Group_Name):
			self.group_changer(group_name)
		if(credential_to_update == 'p'):
			self.Current_Group.credential_modifier(credential_name,updated_information)
		elif(credential_to_update == 'd'):
			if(status == 'u'):
				self.Current_Group.detail_modifier(credential_name,detail_name,encryption_status,updated_information)
			elif(status == 'a'):
				self.Current_Group.detail_modifier(credential_name,detail_name,encryption_status,updated_information)
			elif(status == 'r'):
				self.Current_Group.detail_deleter(credential_name,detail_name)
		elif(credential_to_update == "w"):
			self.Current_Group.credential_deleter(credential_name)
		self.dumper(self.Current_Group,group_name)
		self.__updater()
		return 0

	def credential_searcher(self,credential_name):
		"""searches for particular credential"""
		for group in self.Groups_List:
			group_object = self.loader(group)
			if(credential_name in list(group_object.get_credentials().keys())):
				credential_details = group_object.get_credentials()[credential_name]
				details_list = group_object.get_details()[credential_name]
				return(credential_name,credential_details,details_list,group_object.Group_Name)
				break
		else:
			return -1

	def dumper(self,object_to_dump,file_name):
		"""writes the object onto its pickle file"""
		object_file = open('data/'+file_name,'wb')
		pickle.dump(object_to_dump,object_file)
		object_file.close()
		return 0

	def loader(self,file_name):
		"""loads an object from its pickle file"""
		object_file = open('data/'+file_name,'rb')
		loaded_object = pickle.load(object_file)
		object_file.close()
		return loaded_object

	def __updater(self):
		"""writes itself onto the its pickle file"""
		self.dumper(self,"manager")

	def printer(self):
		"""prints details about itsel"""
		print("Global Settings : ")
		print("UserName : ",self.Name)
		print("No of Groups : ",self.No_of_Groups)
		print("Group List : ",end=" | ")
		for group in self.Groups_List:
			print(group,end=" | ")
		print("\nCurrent Group : ",self.Current_Group.Group_Name)

	def clear_screen(self):
		"""Overwrites the output of the terminal"""
		lines = os.get_terminal_size().lines
		i = 0 
		while i<lines:
			sys.stdout.write("\033[F") #back to previous line
			sys.stdout.write("\033[K")
			i = i + 1

		

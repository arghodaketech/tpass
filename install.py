#!/usr/bin/python3
# Required packages : 
# 1. AES
# 2. SecureString

import subprocess
import os

aes_flag = 0
securestring_flag = 0

# checking if aes is available
status = subprocess.Popen(["python",'-c','"from Crypto.Cipher import AES"'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
status = status.communicate()
if(status[0] != b"" and status[1] != b""):
	aes_flag = -1

# checking if SecureString is available
status = subprocess.Popen(["python",'-c','"import hashlib"'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
status = status.communicate()
if(status[0] != b"" and status[1] != b""):
	securestring_flag = -1

if(aes_flag == 0 and securestring_flag == 0):
	print("All requirments are fullfilled.")
else:
	if(aes_flag == -1):
		installer = subprocess.Popen(["pip3",'install','--user','pycrypto'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		installer = installer.communicate()
		if(installer[1] == b""):
			aes_flag = 0
		else:
			print("Unable to install pycrypto ... ")

	if(aes_flag == -1):
		installer = subprocess.Popen(["pip3",'install','--user','SecureString'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		installer = installer.communicate()
		if(installer[1] == b""):
			securestring_flag = 0
		else:
			print("Unable to install SecureString ... ")

if(aes_flag == 0 and securestring_flag == 0):
	print("Setting up alias ... ")
	path_to_directory = os.getcwd()+"/"
	path_to_tpass = path_to_directory+"tpass.py"
	home_path = os.path.expanduser("~")
	alias_file = open(home_path+"/.bashrc","a+")
	comment = "\n# alias created for tpass\n"
	alias = "alias tpass='cd "+path_to_directory+";"+path_to_tpass+"'"
	complete_alias = comment+alias
	alias_file.write(complete_alias)
	alias_file.close()
	print("Alias set ...")
	print("Start a new shell and run 'tpass' to access it from anywhere")
	exit(0)
else:
	print("Intall the required packages and then run the script again.")
	exit(-1)
#!/usr/bin/python3
"""term pass starter. Sets up new install if configuration files not found in 'data/'.
   If all configurations are ok then starts the application loop."""
import os
from lib.lib1 import Manager
import pickle
import getpass
from Crypto.Cipher import AES

app_manager = None     # global manager object
def main():
	global app_manager
	if(os.path.exists("data/manager")):            # checking if the object files exist
		object_file = open("data/manager","rb")
		app_manager = pickle.load(object_file)
	else:										   # fresh installation
		print("Welcome to Tpass !!!!")
		print("Seems like a fresh installation.",end=" ")
		while True:
			choice = input("Do you wish to import your files ? [y/n] ")     # importing files from another deployment
			if(choice == "y" or choice == "Y"):
				base_obj = import_object()
				if(base_obj == 0):												  
					return -1
				else:									
					app_manager = base_obj
					print("Inisitalisation complete. Press Enter to continue !")
					complete = input()
					break
			elif(choice == "n" or choice == "N"):									# initialising new objects
				print("Setting up fresh installation ...")
				app_manager = Manager()
				break
			else:
				print("Please enter valid choice.")
	workloop()																		# going into the application loop		

def import_object():
	"""imports an existing object files to the 'data/' """
	while True:
		path_to_object = str(input("Enter the path to the object directory : "))
		try:
			if(os.path.exists(path_to_object)):
				print("Importing Files ...")
				os.popen("cp -r "+path_to_object+"/* data/")
				pickle_file = open("data/manager","rb+")
				tmp_obj = pickle.load(pickle_file)
				print("Files Sucessfully imported ... ")
				return tmp_obj
			break
		except Exception as e:
			print(e)
			print("Inisitalisation failed.")
			return 0

def workloop():
	"""application working loop to accept commands and call respective functions"""
	app_manager .clear_screen()
	if( not app_manager.authenticator()):
		print("Authentication Error.")
		exit(0)
	while True:
		app_manager.clear_screen()
		print("Welcome "+app_manager.Name)
		print("( 'help' or 'h' to show list of available commands. )")
		command = input(" : ")
		if(command == "search" or command == "s" or command == "S"):
			status = search_function()
			if(status != 0):
				complete = input()
		elif(command == "add" or command == "a" or command == "A"):
			status = add_funtion()
			if(status != 0):
				complete = input()
		elif(command == "update" or command == "u"):
			status = update_function()
			if(status != 0):
				complete = input()
		elif(command == "group" or command == "g" or command == "G"):
			show_function()
			complete = input()
		elif(command == "help" or command == "h" or command == "H"):
			help_function()
			complete = input()
		elif(command == "quit" or command == "q" or command == "Q"):
			cleanup()
		else:
			print("Invalid Command")
			complete = input()

def search_function():
	"""takes the credential name to search and returns its details if found. 
	    It then prompts to decrypt the password or details if they want."""
	global app_manager
	app_manager.clear_screen()
	print("Enter credential name : ", end = "")
	credential_name = input()
	credential_details = app_manager.credential_searcher(credential_name)
	if(credential_details == -1):
		print("Credential not found.")
		return -1
	credential_display(credential_details)							# displays the credential details
	print("\n\nDo you want to decrypt the password or details ? \nP - Decrypt Password           D - Decrypt Detail")
	option = input(" # ")
	if(option == "p" or option == "P"):								# decrypts the password
		app_manager.decryptor(credential_details[1])
	elif(option == "d" or option == "D"):							# decrypts the detail
		print("Enter the detail name which you want to decrypt :")
		d_name = input(" # ")
		if(d_name in list(credential_details[2].keys())):
			app_manager.decryptor(credential_details[2][d_name][1])
		else:
			print("Invalid Detail name.\nAbort.")
			return -1
	elif(option == "" or option == " "):
		return 0
	else:
		print("Invalid Option.\nAbort.")
		return -1
	return 1

def add_funtion():
	"""adds a group or credential according to selection.
	   adds a group if it is not existing.
	   adds a credential and/or additional details if the credential does not exist."""
	global app_manager
	app_manager.clear_screen()
	print("Add Group or Credential ? [G/C] : ",end= "")
	choice = input()
	if(choice == "g" or choice == "G"):                  # adds a group
		print("Group List : ",end=" | ")
		for group in app_manager.Groups_List:
			print(group,end=" | ")
		group_name = input("\nNew Group Name : ")
		if(group_name == ""):
			print("Abort")
			return -1
		elif(group_name not in app_manager.Groups_List):
			app_manager.group_creator(group_name)
			print("Group Added.")
			return 0
		else:
			print("Group exists.\nAbort.")
			return -1
	elif(choice == "C" or choice == "c"):				# adds a credential
		print("Group List : ",end=" | ")
		for group in app_manager.Groups_List:
			print(group,end=" | ")
		print("\nSelect Group : ",end="")
		option = input()
		if(option not in app_manager.Groups_List):
			print("Invalid Group.\nAbort.")
			return -1
		app_manager.group_changer(option)
		app_manager.clear_screen()
		print("Adding Credential in : "+option)
		credential_name = input("Name of Credential : ")
		duplicate_credential = app_manager.credential_searcher(credential_name)
		if(duplicate_credential != -1):
			print("Duplicate credential name.\nAbort.")
			return -1
		credential_password =  app_manager.encryptor("Enter Password to encrypt :")
		if(credential_password == -1):
			return -1
		details = {}
		tmp_details = []
		while True:						               # adding details
			option = input("Do you want to add any more details : [y/n] ")
			if(option == "y"):
				detail_name = input("Detail Name : ")
				if(detail_name in list(app_manager.Current_Group.get_credentials().keys())):
					print("Dupliacte Detail name.\nAbort.")
					return -1
				if(detail_name in tmp_details):
					print("Dupliacte detail name.\nAbort.")
					return -1
				tmp_details.append(detail_name)
				encryption_status = input("Encrypt this detail ? :[y/n] ")
				if(encryption_status == "y" or encryption_status == "Y"):
					encryption_status = "y"
					detail_value = app_manager.encryptor("Enter Detail value to encrypt :")
					if(detail_value == -1):
						return -1
				else:
					encryption_status = "n"
					detail_value = input("Enter Detail value :")
				details[detail_name] = (encryption_status,detail_value)
			else:
				break
		app_manager.credential_adder(credential_name,credential_password,details)
		print("Credential added.")
	else:
		print("Invalid choice.\nAbort.")
		return -1
	
def update_function():
	"""updates the credential [update password,adds detail,updates detail,removes detail,delete the credential] if found"""
	global app_manager
	app_manager.clear_screen()
	credential_name = input("Enter name of credential which you want to update : ")
	credential_details = app_manager.credential_searcher(credential_name)
	if(credential_details == -1):
		print("Credential not found.\nAbort.")
		return -1
	credential_display(credential_details)
	print("\nP - Update password     D - Update Detail  A - Add detail  R - Remove Detail   \n\nDEL - Delete the complete credential\n\n")
	choice = input(" # ")
	if(choice == "p" or choice == "P"):							# update password
		updated_password = app_manager.encryptor("Enter updated password :")
		if(updated_password == -1):
			print("Invalid details\nAbort.")
			return -1
		app_manager.credential_updater("p","u",credential_details[3],credential_details[0],updated_password)
		print("Password Updated.")
		return 1
	elif(choice == "d" or choice == "D"):						# update detail
		detail_name = input("Enter the detail name to update :")
		if(detail_name not in list(credential_details[2].keys())):
			print("Invalid detail name.\nAbort.")
			return -1
		if(credential_details[2][detail_name][0] == "y"):
			encrypted_detail = app_manager.encryptor("Enter the encrypted detail value : ")
			app_manager.credential_updater("d","u",credential_details[3],credential_details[0],encrypted_detail,detail_name,"y")
		else:
			detail_value = input("Enter value : ")
			app_manager.credential_updater("d","u",credential_details[3],credential_details[0],detail_value,detail_name,"n")
		print("Detail Updated")
		return 1	
	elif(choice == "a" or choice == "A"):						# add detail
		authentication_status = app_manager.authenticator()
		if(authentication_status == False):
			print("Authentication Error.\nAbort.")
			return -1
		else:
			detail_to_add = input("Enter the name of detail to add :")
			if(detail_to_add in list(credential_details[2].keys())):
				print("Dupliacte Detail Name.\nAbort.")
				return -1
			else:
				encryption_status = input("Encrypt the detail : [y/n]")
				if(encryption_status == "y" or encryption_status == "Y"):
					encryption_status = "y"
					detail_value = app_manager.encryptor("Enter the encrypted detail value : ")
				elif(encryption_status == "n" or encryption_status == "N"):
					encryption_status = "n"
					detail_value = input("Enter the detail value :")
				else:
					print("Invalid option.\nAbort.")
					return -1
				app_manager.credential_updater("d","a",credential_details[3],credential_details[0],detail_value,detail_to_add,encryption_status)
				print("Detail Added.")
				return 1
	elif(choice == "r" or choice == "R"):						# remove detail
		authentication_status = app_manager.authenticator()
		if(authentication_status == False):
			print("Authentication Error.\nAbort.")
			return -1
		else:
			detail_to_delete = input("Enter the detail to delete :")
			if(detail_to_delete not in list(credential_details[2].keys())):
				print("Detail name not valid.\nAbort.")
				return -1 
			app_manager.credential_updater("d","r",credential_details[3],credential_details[0],"",detail_to_delete)
			print("Detail Removed.")
			return 1
	elif(choice == "DEL"):										# delete entire credential
		print("This action will permanently delete all the records for this credential.\nDo you wish to proceed ? [Type 'YES' to proceed] : ",end="")
		choice = input()
		if(choice == "YES"):
			authentication_status = app_manager.authenticator()
			if(authentication_status != True):
				print("Authentication Error.\nAbort.")
				return -1
			app_manager.credential_updater("w","",credential_details[3],credential_details[0],"","")
			print("Credential Removed.")
			return 1
		else:
			print("Abort.")
			return -1
	elif(choice == ""):
		return 0
	else:
		print("Invalid choice.\nAbort.")
		return -1
	
def show_function():
	"""shows the details of group like no of credenitals,list of credentials"""
	global app_manager
	app_manager.clear_screen()
	print("Group List : ",end=" | ")
	for group in app_manager.Groups_List:
			print(group,end=" | ")
	print("\nEnter group name : ",end="")
	choice = input()
	if(choice not in app_manager.Groups_List):
		print("Invalid group name.\nAbort.")
		return -1
	if(app_manager.Current_Group.Group_Name != choice):
		app_manager.group_changer(choice)
	app_manager.Current_Group.printer()
	return 0
	
def help_function():
	"""prints the list of commands. the help menu text is stored in help file"""
	global app_manager
	app_manager.clear_screen()
	help_file = open("lib/help","r")
	help_text = help_file.read()
	print(help_text)
	help_file.close()
	
def cleanup():
	"""exits the application"""
	global app_manager
	app_manager.clear_screen()
	exit(0)
	
def credential_display(credential_details):
	"""displays the credential details"""
	print("Group Name           : ",credential_details[3])
	print("Credential Name      : ",credential_details[0])
	print("Credential Password  : [Encrypted]")
	for detail_name in list(credential_details[2].keys()):
		print("Detail Name          : ",detail_name)
		if(credential_details[2][detail_name][0] == "y"):
			print("Detail Value         : [Encrypted]",)	
		else:
			print("Detail Value         : ",credential_details[2][detail_name][1])
pass

if __name__ == '__main__':
	main()
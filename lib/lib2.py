#/bin/python3
class Group:
	"""Object holds credential for a group.
	   Members :
	   			Group_Name           - String     - Name of the group
	   			No_of_Credentials    - Integer    - Number of credentials in the group
	   			__Credentials        - Dictionary - key - name of the credential
	   			                                    value - tuple containing passsword hash and salt
	   			__Details            - Dictionary - key - name of credential
	   											    value - dictionary - key - name of the detail
	   											   						value -  tuple containing encryption status
	   											   						         and value(value will be encrypted text and salt tuple if encryption status if 'y')
	"""
	def __init__(self,name):
		"""initialise the object"""
		self.Group_Name = name
		self.No_of_Credentials = 0
		self.__Credentials = {}
		self.__Details = {}

	def printer(self):
		"""Prints the details of the group"""
		print("Group Name : ",self.Group_Name)
		print("Number of credentials :",self.No_of_Credentials)
		if(self.No_of_Credentials):
			print("Credentials List : ",end=" | ")
			for credential_name in list(self.__Credentials.keys()):
				print(credential_name,end=" | ")
		pass

	def get_credentials(self):
		"""returns the __Credentials"""
		return self.__Credentials

	def get_details(self):
		"""returns __Details"""
		return self.__Details

	def credential_add(self,key,value):
		"""adds credential"""
		self.__Credentials[key] = value
		self.No_of_Credentials = self.No_of_Credentials + 1
		pass

	def details_add(self,key,value):
		"""adds a detail to a credential"""
		self.__Details[key] = value
		pass

	def credential_modifier(self,key,value):
		"""modifies a credential"""
		self.__Credentials[key] = value
		pass

	def detail_modifier(self,credential_name,detail_name,encryption_status,detail_value):
		"""modifies a detail"""
		self.__Details[credential_name][detail_name] = (encryption_status,detail_value)
		pass

	def credential_deleter(self,credential_name):
		"""deletes a credential"""
		del self.__Details[credential_name]
		del self.__Credentials[credential_name]
		self.No_of_Credentials = self.No_of_Credentials - 1
		pass
		
	def detail_deleter(self,credential_name,detail_name):
		"""deletes a detail"""
		del self.__Details[credential_name][detail_name]
		print(self.__Details)
		pass

	

	
		

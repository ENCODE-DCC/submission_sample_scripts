from ENCODETools import KeyENCODE

#if __name__ == "__main__":
'''
This script will be used to set certain identity variables to be used by the other tools.
'''
# FUTURE: Should allow user to set them at the prompt

# set user name
user_name = 'yourname@yourinstitute.com'

# set server name.
server_name = 'test'

# set output data file
data_file = 'update.json'

# set key file
key_file = 'keys.txt'

# state the variables
print(user_name + ' / ' + server_name + ' / ' + data_file)

# get ID, PW.  MODIFY TO USE USERNAME/PASS INSTEAD OF SERVER NAME TO GAIN ACCESS TO CREDENTIALS
keys = KeyENCODE(key_file,user_name,server_name)

#    return(server_name,user_name,data_file,keys)

# to convert the binary data taken from the /dev/urandom to ascii representation
import binascii

def generateSalt(size):
     """
     Generate a salt of the specified size that will be entered by the user
     
     Args:
         size (positive integer): specify the size of the salt
     
     Returns:
         the number of bytes from /dev/urandom
     """
     try:
          with open('/dev/urandom', 'rb') as file:
               return file.read(size)
     except Exception as e:
          print(f"Error accessing '/dev/urandom':{e}")
          exit(1)


def readPasswords(file_path):
     """
     Read passwords from the specified file
     
     Args:
         file_path (text format): a text file that contains all passwords with their index
     
     Returns:
         a dictionary of passwords
     """
     passwords = {} # initialize an empty dictionary to store passwords 
     try:
          with open(file_path, 'r') as rfile:
               next(rfile) # skip the header line of the file (index, password)
               for line in rfile:
                    parts = line.split() # split the line into two parts (first part is the index, the second part is the password itself)
                    if len(parts) == 2:
                         index = parts[0] # get the index of passwords 
                         password = parts[1] # get the password 
                         passwords[index] = password
                    
     except FileNotFoundError:
          print(f"Error: The file '{file_path}' was not found.")
          exit(1)
     
     except Exception as e:
          print(f"Error reading the file: {e}")
          exit(1)
     return passwords
# to convert the binary data taken from the /dev/urandom to ascii representation
import binascii
import sys

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
          print(f"\nError accessing '/dev/urandom':{e}")
          sys.exit(1)


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
                    parts = line.split(',') # split the line into two parts (first part is the index, the second part is the password itself)
                    if len(parts) == 2:
                         index = parts[0] # get the index of passwords 
                         password = parts[1] # get the password 
                         passwords[index] = password
                    
     except FileNotFoundError:
          print(f"Error: The file '{file_path}' was not found.")
          sys.exit(1)
     
     except Exception as e:
          print(f"\nError reading the file: {e}")
          sys.exit(1)
     return passwords


def saveSaltedPasswords(salted_passwords, output_file):
     """
     Save the salted passwords to the specified output file in hexadecimal format
     Args:
         salted_passwords (hexadecimal)
         output_file (text): contains all salted passwords with their index (based on the unsalted passwords file)
     """
     try:
          with open(output_file, 'w') as wfile:
               wfile.write("index, salted_password\n") # update the header 
               for index, sPassword in salted_passwords.items():
                    hexSaltedPassword = binascii.hexlify(sPassword).decode('utf-8') # convert the salted password to hexadecimal representation 
                    wfile.write(f"{index}, {hexSaltedPassword}\n")
     except Exception as e:
          print(f"\nError writing to the file: {e}")
          sys.exit(1)


def distributeSalt(password, salt):
     """
     Distribute the random salt across the password in three parts (beginning, middle, and end)
     Args:
         password: text password
         salt: random salt generated from the /dev/urandom
     Returns:
         distributed salted passwords 
     """
     if len(salt) < 3:
          return salt+password # not enough salt to distribute
     
     # Calculate the lengths for each part
     partLength = len(salt) // 3 # Length of each part based on salt size
     remaining = len(salt) % 3  # Check for remaining bytes to distribute
     
     firstPart = salt[:partLength + (1 if remaining > 0 else 0)] # first part takes extra byte if available
     secondPart = salt[partLength + (1 if remaining > 0 else 0): 2 * partLength + (1 if remaining > 1 else 0)]
     thirdPart = salt[2 * partLength + (1 if remaining > 1 else 0):] # third part takes the remaining bytes 
    
     midIndex = len(password) // 2 # find the middle index of the password to insert the second part 
     saltedPassword = firstPart + password[:midIndex] + secondPart + password[:midIndex] + thirdPart # combine the three parts with the password
     return saltedPassword


inputFile = 'unsalted_passwords.txt'
outputFile = 'salted_passwords.txt'

# get the salt size from the user
while True:
     try:
          saltSize = int(input("\nEnter the salt size in bytes: "))
          if saltSize <= 0:
               raise ValueError("Salt size must be a positive integer.")
          break
     except ValueError as e:
          print(f"\nInvalid input: {e}. Please enter a positive integer.")
     
rpasswords = readPasswords(inputFile)

saltedPasswords = {}
for index, password in rpasswords.items():
     salt = generateSalt(saltSize)
     sPass = distributeSalt(password.encode('utf-8'), salt)
     saltedPasswords[index] = sPass

saveSaltedPasswords(saltedPasswords, outputFile)
print(f"\nSalted passwords saved to '{outputFile}'.")



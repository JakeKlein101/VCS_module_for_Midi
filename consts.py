# consts:

HASH_ITERATIONS = 260000
HASH_SPLIT = '$'

# Socket consts:

IP = "127.0.0.1"
PORT = 10000
BUFFER_SIZE = 4096

# Codes:

FALSE_REQUEST = "-1"
AUTH_REQUEST = "authreq"
PUSH_REQUEST = "push"
CLONE_REQUEST = "clone"
FILE_NAME_REQUEST = "filenamerequest"
FILE_NOT_FOUND = "FNF"
FILE_NAME_RECIEVE_SUCCESS = "RFNS"  # Recieved file name success.
FILE_NAME_RECIEVE_FAIL = "RFNF"  # Recieved file name fail.
FILE_RECIEVE_SUCCESS = "RFS"  # Recived file succesfully.
FILE_RECIEVE_FAIL = "RFF"  # Recieving file failed.
OPCODE_RECIEVE_SUCCESS = "ROS"  # Recieved opcode successfully
OPCODE_RECIEVE_FAIL = "ROF"  # Recieving opcode failed.
AUTH_SUCCESS = "AS"  # Auth success
REPO_ID_RECIEVE_SUCCESS = "RRIS"  # Recieving repository ID success.
REPO_ID_FAIL = "RRIF"  # Recieving repository ID failed.
PASSWORD_RECIEVE_FAIL = "RPF"  # Recieving password failed.
PASSWORD_RECIEVE_SUCCESS = "RPS"  # Recieved password succesfully.
USERNAME_RECIEVE_SUCCESS = "URS"  # Username recieved succefully.
USERNAME_RECIEVE_FAIL = "URF"  # Username recieving failed.
SALT_REQUEST = "SR"
USER_NOT_FOUND = "UNF"
WRONG_PASSWORD = "WP"

PYTHON_DOCKER_IMAGE = "python:3"  # docker python image
CONTAINER_MEMORY_LIMIT = '4m'  # 4 megabytes container memory limit restriction
MAX_NUM_CONTAINERS = 3  # maximum allowed container at any given time
FUNCTIONS_FILE = "functions.py"  # hardcoded read-only file the container will share
CONSTS_FILE = "consts.py"  # consts file FUNCTIONS_FILE shares
ROOT_DIR = '/'

DEFAULT_REASON_EXCEPTION = "Error occurred"
FUNCTION_TIMEOUT = 5  # function timeout in seconds
MAX_RETURN_OBJECT_SIZE = 60  # function return size max size limit in bytes

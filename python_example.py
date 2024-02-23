from ctypes import *

# Ensure the chosen architecture matches the Python interpreter
dll_path = "C:\\ProgramData\\TradingAppStore\\x64\\TASlicense.dll"
dll = cdll.LoadLibrary(dll_path)

# Define customer and product information
customer_id = b"Python_App-MY_PLATFORM_USERNAME"
product_id = b"MY_PRODUCT_SKU"
debug_mode = True
tas_auth_enabled = True

# Perform user authentication using TAS machine authorization
error_machine_auth = dll.UserHasPermission(customer_id, product_id, debug_mode, tas_auth_enabled)
print(f"Error Code from Machine Authorization: {error_machine_auth}")

# If you prefer to use the username embedded into the license, set TASauth to False
tas_auth_enabled = False
error_username_auth = dll.UserHasPermission(customer_id, product_id, debug_mode, tas_auth_enabled)
print(f"Error Code from Username Authorization: {error_username_auth}")

# Process the returned errors accordingly
if error_machine_auth == 0 and error_username_auth == 0:
    print("Access Granted")
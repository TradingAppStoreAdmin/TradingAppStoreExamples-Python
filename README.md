# TradingAppStoreExamples-Python
## Description
TradingApp.Store offers a software suite that allows vendors to see if a particular user has permission to use their product(s). The suite includes multiple digitally signed Dynamic Link Libraries (DLLs) that contain functions which can be called by Python scripts included in your software.

## Setup
Go to vendors.tradingapp.store, create a vendor account, and click the "Create Listing" button at the top right. Fill out a product SKU (this will identify your testing product on our servers), target platform (Python_App), and an optional username that will be embedded into the license. This is useful if you'd like to offload machine authorization to a third party, like if you have your own username/password login system that you'd like to use. If no username, put "none". Click "Generate MSI", and then install the MSI once downloaded. You are now ready to integrate your app with our system.

## Implementation
Below is a python implementation that calls the UserHasPermission function of the TradingAppStore DLL:
```python
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
```

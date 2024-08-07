# TradingAppStoreExamples-Python
## Description
TradingApp.Store offers a comprehensive software suite enabling vendors to verify user permissions for their products. The suite comprises digitally signed Dynamic Link Libraries (DLLs) containing API functions accessible via Python scripts integrated into your software.

## Setup
Go to [vendors.tradingapp.store](https://vendors.tradingapp.store/app), create or sign into your vendor account.  Should you already be an end-user of products in the trading app store, then you should create a vendor login using the same email address as your existing app store's end-user login.  These are two seperate systems, so you will need to register for each individually.  By using the same email address for each, the store will know to link your vendor account to your end-user account so that you will only have to install one License Manager.  Once your License Manager is installed, you will see a choice of flipping from 'Vendor Test Mode', back to 'End-User Mode' within the License Manager software.  After you created a new Vendor account, or logged in, then click the gear at the top right and choose 'Settings', then on the left side click 'Vendor Page' and setup your Vendor Profile page.  This is where you insert your company logo or icon (500x500 pixels works best.)  Next, enter a company bio or description, and contact information.  Now click 'Send for Approval'. Once approved this enters you into the  [Vendor Directory](https://tradingapp.store/pages/vendor-directory).  Next create your first product listing by clicking 'Listings' at the top of the page, and then 'Create Listing' button at the top right. Proceed to fill out the Product Listing form.  Instructions below.

### Product Name:
Fill out a Product Name at the top left and a SKU will be automatically produced at the bottom of the page (this will identify your product on our servers). 

### Product Description:
Create a formated product description in an editor like Word or Google Docs and then paste it into the Product Description text-box. Read over it and do a final editing of the formatting to make sure it looks right. The product description should fully explain your product, its features, benefits, and how it works. Give as much detail as possible.

### Images:
Add images and/or videos one at a time. Most file common file types are accepted. You can also use online videos from YouTube via the URL link.

### Listing Types:
Check all that apply to this product.  Your product may fit into more than one Listing Type.  

### Subscription Options:
Choose the type of billing scheme to use. Available options are: Lifetime, Annual, Monthly, Free Trial + Monthly, Free Trial + Annual, Free Trial + Lifetime.

### Webhook Link:
If you have a real-time listening application that works with Webhooks, paste the link to it here to be notified when a purchase for this product is made.

### Purchase Email:
If you would like email notifications upon purchases, place the receiving address here.

### Target Platform:
Choose Python_App

### Platform Customer Data
If your software requires a username, you can put yours here. This value will be embedded into the license and can be checked at runtime. If no username, put "none".

### SKU:
Unique self-created product identifier that you will use in your script while accessing the DLL.

### Download MSI:
(NOTE: You must pick a 'Target Platform' and enter 'Platform Customer Data' in order for the 'Download MSI' button to appear.)  Press this to download a copy of the 'TradingApp.Store License Manager' that is master-keyed to this specific product and specifically to your platform customer number.  This provides you, the Vendor, the ability to test the integrations of your products with our DLLs.  After installing this MSI, launch the TradingApp.Store license manager application to see the generated license.  


![TradingApp.Store License Manager](licensemanager_screenshot.png)  

Your system is now ready for seamless integration with our platform.


## How it works
The DLL will automatically detect a license in the TradingAppStore/licenses folder and then will determine if the user has permission. If the license is expired, or a newer version of the license is required, then the DLL will automatically update the license to contain the new information. Consequently, users need only execute the installer once to access any trading apps or software included with their current or future purchases.
The TradingAppStore DLL also offers a hardware authorization option that only allows a certain number of devices to access one instance of your product. This adds an additional layer of security by preventing copies of a DLL / product from gaining permission.
You may download the installer for TradingAppStore from the vendor portal whenever you are in the process of creating a listing. All licenses created from the vendor portal are tagged with a “Debug” flag, so they will not have any functionality in release mode. Thus, BE SURE TO CHANGE THE DEBUG FLAG TO FALSE AFTER COMPLETION OF TESTING PHASES.

## DLL Inputs
The DLL must have 2 input values:
* string productID :    SKU of the product that was self generated above.
* bool debug :          set to True if you are testing to use Debug licenses distributed by the vendor portal. SET TO FALSE FOR RELEASE OR ELSE ANYONE WILL HAVE ACCESS TO YOUR PRODUCT!
  
## Implementation
Below is a Python implementation that calls the UserHasPermission function of the TradingAppStore DLL:
```python
from ctypes import *
import requests

"""Before you use the dlls, you should first make sure that they have not
   been tampered with."""
util_dll_path = "C:\\ProgramData\\TradingAppStore\\x64\\Utils.dll"
dll = cdll.LoadLibrary(util_dll_path)

#This gets a one-time-use magic number from a utility dll
dll.GetMagicNumber()
magic = ""
with open("C:\\ProgramData\\TradingAppStore\\temp\\magic.txt", "r") as infile:
   magic = infile.read()
json = {
   "magic_number" : magic
}

#Now, let's send that magic number to our server to be verified
dllValid = False
response = requests.post("https://tradingstoreapi.ngrok.app/verifyDLL", json=json)
if response.status_code == 200:
   dllValid = True
   print("DLL accepted")
elif response.status_code == 401:
   print("DLL has been tampered with.")
else:
   print(f"Error: {response.status_code}")

"""After verifying the DLLs, you can safely use them to authorize your customers."""
if dllValid:
    auth_dll_path = "C:\\ProgramData\\TradingAppStore\\x64\\TASlicense.dll"
    dll = cdll.LoadLibrary(auth_dll_path)
    
    # Define product information
    product_id = b"MY_PRODUCT_SKU"
    debug_mode = True
    
    # Perform user authentication using TAS machine authorization
    error_machine_auth = dll.UseMachineAuthorization(product_id, debug_mode)
    print(f"Error Code from Machine Authorization: {error_machine_auth}")
    
    # Process the returned errors accordingly
    if error_machine_auth == 0:
        print("Access Granted")
```

## DLL Return Values
The DLL will return various error values based on numerous factors. It is up to your application how to handle them.
```
0 - no error
1 - expired
2 - wrong customerId
3 - cannot use Debug license in Release Mode
4 - invalid productId
5 - Too many user instances. Only for TAS Authorization. Contact support@tradingapp.store
6 - billing attempt not found... likely expired
7 - internal error
8 - File Error
9 - other error
```

## Finishing Up
Go back to the Vendor Portal to complete your product setup.

### Upload Software Here:
Once your product is successfully integrated into our permissions system, take the product out of debug mode (see bool debug above), and export your project as a distribution package.  A great tutorial is here: https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications
If you have accompanying files, workspaces, symbol lists, etc, it is required that you zip everything into one file, and then upload it here.  This is what will be distributed to end-users at the time of purchase or free trial.

### Sales Information - Set Price:
This is the price per period for the subscription term of the product.  Revenue splits are explained in the Vendor Policy (https://tradingapp.store/pages/vendor-policy).

### Send for approval:
Click here to send this listing for approval by TAS site moderators.  You will be notified by email upon acceptance or rejection.


## Other Notes
The TradingApp.Store License Manager has the ability to switch between ‘End-User’ mode, and ‘Vendor Test Mode’ by-way of a checkbox at the top right of the TAS Lisence Manager labeled:  ‘Vendor Test Mode’.
When it's checked, only Vendor's products show in License Manager’s DataGrids, when unchecked, only End-User products show in DataGrids.
If a Vendor is also an End-User of other’s products, they must use the same email address during registrations of  each mode for this to work.  This enables one installation of this License Manager to handle both integration testing while in Vendor Mode, and alternatively using End-User mode for purchased products use.


## Further Help
If you need assistance in implementation, you may email support@tradingapp.store and we will respond as quickly as possible.

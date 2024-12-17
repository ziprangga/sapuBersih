![icon_128x128](https://github.com/user-attachments/assets/1e23120e-9b0b-4121-913c-073fc233b89d)

sapuBersih

sapuBersih is application cleaner for macOS. 
This app was built using open-source components and inspired by privacy guides from Sunknudsen (https://github.com/sunknudsen/privacy-guides/tree/master/how-to-clean-uninstall-macos-apps-using-appcleaner-open-source-alternative). Some of the scripts in this app adapt references from his guides, so I want to give him a big thank you!

The app’s interface is kept simple using Python, with the main goal of helping my beloved wife and friends who rarely use the terminal on macOS. On top of that, this project also serves as a way for me to dive deeper into Python.
If you're interested in using or even developing this app, feel free to download it.

"If you want to compile it yourself, don't forget to use PySide6."





Permissions and Privacy Notice for macOS

To perform its cleanup tasks effectively, sapuBersih requires specific permissions when running on macOS. Below is a detailed explanation of the permissions needed and their purposes:

1. Access to Finder (Automation Permission)
sapuBersih interacts with Finder to perform the following tasks:

Moving selected files or folders to the Trash.
⚠️ This permission is required.
Without access to Finder, sapuBersih cannot move files or folders to the Trash.
How to Grant Finder Access:

Go to System Preferences → Security & Privacy → Privacy → Automation.
Ensure sapuBersih is allowed to control Finder.
Restart the application after granting this permission.
2. Access to File Data (Optional Permission)
To identify and clean up files or folders associated with an application, sapuBersih may request access to the file system. This includes:

Reading directory paths of selected applications.
macOS may display a prompt like:

"sapuBersih.app would like to access data from other apps"
Note:

You can deny this permission without affecting core functionality.
If denied, sapuBersih can still open file locations, but its ability to scan for related files might be limited.
3. Why These Permissions Are Needed
The permissions are strictly used for the following purposes:

Locating and displaying file paths related to an application.
Allowing you to open file locations directly in Finder.
Moving files or folders to the Trash securely.
No files will be deleted automatically — all actions require user confirmation.

Troubleshooting Permissions
If you encounter issues, such as files not being moved to Trash, follow these steps:

Open System Preferences → Security & Privacy → Privacy.
Under Automation, ensure sapuBersih has permission to interact with Finder.
Restart sapuBersih after granting the required permissions.



How to Use sapuBersih

sapuBersih is an application designed to help you clean up application files or folders from your system, with the following features:
1. Selecting an Application
	•	Drag & Drop: Drag the application you want to clean directly into the sapuBersih window.
	•	Browse Button: Use the Browse button to manually select an application.
2. Displaying Related Files or Folders
Once an application is selected, sapuBersih will display a list of related files or folders.
	•	You can:
	◦	Delete All: Click the Move to Trash button to move all files/folders to the Trash.
	◦	Delete Selectively: Choose specific files or folders you want to delete, then click Move to Trash.
3. Verifying Deleted Files
Files or folders moved to the Trash can be reviewed. If needed, you can restore them to their original location.
4. Opening File/Folder Locations
To open the location of a file or folder, simply double-click on the item in the path list.
5. Searching for Log Files (BOM File Log)
sapuBersih can also search for log files (BOM file logs) to help with a more thorough cleanup.
	•	Default Location: Log files are automatically saved to the Desktop.


Screenshot:

<img width="500" alt="sapuBersih UI" src="https://github.com/user-attachments/assets/33125b09-27a3-4924-85a0-533ef3f48869" />


<img width="500" alt="list found file or folder" src="https://github.com/user-attachments/assets/e387cb57-5d99-41f5-a09e-d40768f6045a" /> <img width="500" alt="select or not" src="https://github.com/user-attachments/assets/f54c5c4c-c443-4908-8f26-b01309d7cd20" />






License:

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

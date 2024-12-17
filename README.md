# 🧹 sapuBersih

**sapuBersih** is a cleanup tool designed to safely remove applications and their associated files or folders from the macOS system.

This app was built using open-source components and inspired by privacy guides from Sunknudsen (https://github.com/sunknudsen/privacy-guides/tree/master/how-to-clean-uninstall-macos-apps-using-appcleaner-open-source-alternative). Some of the scripts in this app adapt references from his guides, so I want to give him a big thank you!

The app’s interface is kept simple using Python, with the main goal of helping my beloved wife and friends who rarely use the terminal on macOS. On top of that, this project also serves as a way for me to dive deeper into Python.
If you're interested in using or even developing this app, feel free to download it.

#### "If you want to compile it yourself, don't forget to use PySide6."

---

## ⚙️ Permissions and Privacy Notice for macOS

To perform cleanup tasks effectively, **sapuBersih** requires specific permissions when running on macOS. Below is a detailed explanation:

### 1️⃣ Access to Finder (Automation Permission)

sapuBersih interacts with Finder to:

- 🗑️ **Move selected files or folders to the Trash.**

⚠️ **This permission is required.**  
Without this permission, sapuBersih cannot move files or folders to the Trash.

**How to Grant Finder Access:**

1. Go to **System Preferences → Security & Privacy → Privacy → Automation**.
2. Ensure **sapuBersih** is allowed to control Finder.
3. Restart the application after granting this permission.

---

### 2️⃣ Access to File Data (Optional Permission)

To identify and clean up files or folders, sapuBersih may request access to the file system:

- 📁 Reading directory paths of selected applications.

macOS may display a prompt like:

> **"sapuBersih.app would like to access data from other apps"**

**Note:**

- You can **deny** this permission without affecting core functionality.
- If denied, sapuBersih can still open file locations, but its ability to **scan for related files** may be limited.

---

### ❓ Why These Permissions Are Needed

Permissions are strictly used for:

- 🔍 **Locating and displaying file paths** related to an application.
- 🗂️ Allowing you to **open file locations** directly in Finder.
- 🗑️ Securely **moving files or folders to the Trash**.

**No files will be deleted automatically** — all actions require user confirmation.

---

### 🛠️ Troubleshooting Permissions

If you encounter issues (e.g., files not moving to Trash), follow these steps:

1. Open **System Preferences → Security & Privacy → Privacy**.
2. Under **Automation**, ensure **sapuBersih** has permission to control Finder.
3. Restart sapuBersih after granting the required permissions.

---

## 🚀 How to Use sapuBersih

sapuBersih makes cleaning up applications simple and intuitive. Follow these steps:

### 1️⃣ Selecting an Application

- **Drag & Drop**: Drag the application you want to clean into the sapuBersih window.
- **Browse Button**: Use the **Browse** button to manually select an application.

---

### 2️⃣ Displaying Related Files or Folders

Once an application is selected, sapuBersih will display a list of related files or folders.

- 🗑️ **Delete All**: Click the **Move to Trash** button to move all files/folders to the Trash.
- ✂️ **Delete Selectively**: Choose specific files or folders you want to delete, then click **Move to Trash**.

---

### 3️⃣ Verifying Deleted Files

Files or folders moved to the **Trash** can be reviewed. If needed, you can restore them to their original location.

---

### 4️⃣ Opening File/Folder Locations

To open the location of a file or folder:

- 🖱️ **Double-click** on the item in the path list.

---

### 5️⃣ Searching for Log Files (BOM File Log)

sapuBersih can also search for log files to help with more thorough cleanup.

- **Default Location**: Log files are automatically saved to the **Desktop**.

---

## 📸 Screenshot

<img width="500" alt="sapuBersih UI" src="https://github.com/user-attachments/assets/33125b09-27a3-4924-85a0-533ef3f48869" />

<img width="500" alt="list found file or folder" src="https://github.com/user-attachments/assets/e387cb57-5d99-41f5-a09e-d40768f6045a" /> <img width="500" alt="select or not" src="https://github.com/user-attachments/assets/f54c5c4c-c443-4908-8f26-b01309d7cd20" />

---

## 📝 Permissions Summary

| Permission           | Required | Purpose                           | Notes                      |
| -------------------- | -------- | --------------------------------- | -------------------------- |
| **Finder Access**    | ✅ Yes   | Move files to Trash securely      | Grant via **Automation**.  |
| **File Data Access** | ❌ No    | Read directory paths for scanning | Optional, but recommended. |

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve sapuBersih or add new features, please open an issue or submit a pull request.

---

## ❓ Need Help?

If you experience issues or have questions, please check the **[Wiki](https://github.com/ziprangga/sapuBersih/wiki)** or open an issue.

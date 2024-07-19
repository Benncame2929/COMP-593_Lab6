import requests
import hashlib
import os
import subprocess

def main():
    # Start the installation process for VLC Media Player
    print("Starting the installation process for VLC Media Player...")
    # Retrieve the expected SHA-256 checksum from the VLC website
    expected_sha256 = get_expected_sha256()
    if expected_sha256 is None:
        print("Failed to retrieve the expected SHA-256 checksum. Please check your internet connection.")
        return

    # Download the VLC installer from the official site
    print("Downloading the VLC installer...")
    installer_data = download_installer()
    if installer_data is None:
        print("Failed to download the installer. Please check your network settings.")
        return

    # Verify the integrity of the downloaded VLC installer using SHA-256 checksum
    print("Verifying the integrity of the downloaded installer...")
    if installer_ok(installer_data, expected_sha256):
        print("Integrity check passed. Saving the installer...")
        # Save the installer to the disk
        installer_path = save_installer(installer_data)
        if installer_path:
            print("Installer saved successfully. Starting installation...")
            # Silently run the VLC installer
            if run_installer(installer_path):
                print("VLC Media Player has been successfully installed!")
            else:
                print("Installation failed. Please try running the installer manually.")
            # Clean up the installer from the disk
            clean_up(installer_path)
        else:
            print("Failed to save the installer on your system. Please check your storage space and permissions.")
    else:
        print("Installer verification failed. The downloaded file may be corrupted or tampered with.")




def get_expected_sha256():
    # Define the URL where the SHA-256 checksum can be found
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256"
    # Perform a GET request to fetch the checksum
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines:
            if 'vlc-3.0.17.4-win64.exe' in line:
                return line.split()[0]
    return None




def download_installer():
    # URL for downloading the VLC installer
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe"
    # Execute a GET request to download the installer
    response = requests.get(url)
    # Ensure the download was successful
    if response.status_code == 200:
        return response.content
    return None



def installer_ok(installer_data, expected_sha256):
    # Compute the SHA-256 hash of the installer data
    hash_value = hashlib.sha256(installer_data).hexdigest()
    # Compare the computed hash with the expected hash
    return hash_value == expected_sha256



def save_installer(installer_data):
    # Define the path where the installer will be saved, using the system's temp directory
    file_path = os.getenv('TEMP') + "\\vlc-3.0.17.4-win64.exe"
    try:
        # Attempt to save the installer to the disk
        with open(file_path, 'wb') as file:
            file.write(installer_data)
        return file_path
    except:
        print("Failed to save the installer. Please check the permissions and disk space.")
        return None



def run_installer(installer_path):
    # Execute the installer silently without user interaction
    try:
        subprocess.run([installer_path, '/L=1033', '/S'], check=True)
        return True
    except:
        print("The installer failed to execute. This might be due to system restrictions.")
        return False



def clean_up(installer_path):
    # Check if the installer file exists and then delete it
    if os.path.exists(installer_path):
        try:
            os.remove(installer_path)
            print("Clean-up completed. Installer file has been deleted.")
        except:
            print("Failed to delete the installer file. Please delete it manually.")
    else:
        print("No clean-up needed. The installer file does not exist.")

if __name__ == '__main__':
    main()

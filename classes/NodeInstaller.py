# Copyright 2024 Daxton Caylor
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import requests
import subprocess
import tempfile
from tqdm import tqdm
import shutil

class NodeInstaller:

    def __init__(self, installer_url):
        self.installer_url = installer_url
        self.installer_path = None

    def check_for_node_js(self):
        return (shutil.which('node') is not None)

    def download_nodejs(self):
        temp_dir = tempfile.gettempdir()
        self.installer_path = os.path.join(temp_dir, "nodejs_installer.msi")
        response = requests.get(self.installer_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        with open(self.installer_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
        if total_size != 0 and progress_bar.n != total_size:
            print("An error occurred during the download.")
        else:
            print("Node.js installer downloaded successfully.")

    def install_nodejs(self):
        if self.installer_path is None:
            print("Node.js installer has not been downloaded yet.")
            return
        process = subprocess.Popen([self.installer_path], shell=True)
        process.wait()
        
    def install_all_packages(self, package_list):
        for package_name in package_list:
            self.install_npm_package(package_name)

    def install_npm_package(self, package_name):
        install_command = f"npm install {package_name}"
        
        try:
            print("")
            process = subprocess.Popen(install_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in tqdm(iter(process.stdout.readline, b''), desc=f"Installing {package_name}", unit='B', unit_scale=True, leave=False):
                pass
            process.stdout.close()
            process.wait()
            print(f"\nnpm package '{package_name}' installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")


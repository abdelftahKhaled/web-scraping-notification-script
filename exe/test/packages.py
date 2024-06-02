import sys
import os
import subprocess
print(sys.executable)
venv_name = 'venv'
packages=['beautifulsoup4', 'requests', 'winotify']
dir_file=os.getcwd()
path_file=__file__
name_file=os.path.basename(path_file)
path_venv=os.path.join(dir_file,venv_name)
list_file_in_dir=os.listdir(dir_file)
file_python_in_venv=os.path.join(path_venv,'Scripts','python')
file_pip_in_venv=os.path.join(path_venv,'Scripts','pip')
name_of_file_packages_pythone='packages.py'
def install_dependencies():
    """
    Function to install dependencies using pip
    """
    global venv_name
    global packages
    # global file_pip_in_venv
    # global  file_python_in_venv
    def is_package_installed(package_name):
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
    for package in packages:
        if not is_package_installed(package):
            print(is_package_installed(package))
            # subprocess.call(['pip', 'install', package])
            combined_cmd = f'{file_pip_in_venv} install {package}'
            subprocess.call(combined_cmd, shell=True)          
install_dependencies()
# subprocess.run( os.path.join(dir_file,'program.py'), check=True , shell=True)
combined_cmd = f'{file_python_in_venv} {os.path.join(dir_file,'program.py')}'
subprocess.call(combined_cmd, shell=True)


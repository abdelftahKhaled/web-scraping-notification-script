from Run import *
def install_dependencies():
    """
    Function to install dependencies using pip
    """
    global venv_name
    global packages
    global file_pip_in_venv
    global  file_python_in_venv
    def is_package_installed(package_name):
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
  
    for package in packages:
        if not is_package_installed(package):
            subprocess.call(['pip', 'install', package])
            print(is_package_installed(package))
            
            
install_dependencies()
combined_cmd = f'{file_python_in_venv} {os.path.join(dir_file,'crping.py')}'
subprocess.call(combined_cmd, shell=True)

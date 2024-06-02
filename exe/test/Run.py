import subprocess
import sys
import os
venv_name = 'venv'
packages=['beautifulsoup4', 'requests', 'winotify']
dir_file=os.getcwd()
path_file=__file__
name_file=os.path.basename(path_file)
path_venv=os.path.join(dir_file,venv_name)
list_file_in_dir=os.listdir(dir_file)
file_python_in_venv=os.path.join(path_venv,'Scripts','python')
file_pip_in_venv=os.path.join(path_venv,'pip')
name_of_file_packages_pythone='packages.py'
def create_and_activate_venv():
    global venv_name
    if not os.path.exists(path_venv):
    
            subprocess.check_call([sys.executable, '-m', 'venv', venv_name])
    else:
            print(f"Virtual environment '{venv_name}' already exists!")
    # Activate virtual environment
    if sys.platform == 'win32':
        activate_script = os.path.join(venv_name, 'Scripts', 'activate')
    else:
        activate_script = os.path.join(venv_name, 'bin', 'activate')
    
    subprocess.run([activate_script], shell=True, check=True)
#     subprocess.run(os.path.join(dir,name_of_file_packages_pythone), shell=True,)
# # Replace 'myenv' with the desired name of your virtual environment
    combined_cmd = f'{file_python_in_venv} {os.path.join(dir_file,name_of_file_packages_pythone)}'
    subprocess.call(combined_cmd, shell=True)

create_and_activate_venv()



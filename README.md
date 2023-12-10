>   # How to build the application for LabelPrinter?



- Please make sure your system has install pyinstaller. If not, Please install this using below command:

  - pip3 install --proxy=http://child-prc.intel.com:913 pyinstaller==5.7.0

  

- Pyinstaller installed complete,  Change to LabelPrinter workspace. And then execute below command to build:

  - pyinstaller --onefile main.py --name=LabelPrinter --icon=icon/icon.ico --noconsole
  - pyinstaller --onefile main.py --name=LabelPrinter --icon=icon/icon.ico 

  

- Built complete,  Will generate two directory under LabelPrinter workspace.   `dist` and `build`

  - The new application is under `dist`, Copy the exe to LabelPrinter workspace.

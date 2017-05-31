# fltcnvt
Convert Openflight linux files (paths) to windows

## What does it do

* Converts /home and /h to the source drive
* Converts texture paths
* Copies files to target drive preserving/creating directory hierarchy
* Converts old style 'uSim' type switches to Creator switches
* Converts XRefs
* Recursively converts XRef'd files

* Please report 'unknown code' output

## Install Instructions

* Download the latest Python 2.7.x for Windows from:
    
    https://www.python.org/downloads/

* Download the Presagis OpenFlight API 15 from:
    
    http://www.presagis.com/products_services/products/modeling-simulation/free_tools/openflight_api/

* Download the fltcnvt repository

    Click on the green button above and download the zip file
    Extract the archive someplace convienent.

* Open a Command Prompt window (cmd.exe) in Admin mode (right-click)
    
    Enter the following exactly at the command prompt:

    ```
    C:\Windows\system32>setx PYTHONPATH "%PRESAGIS_OPENFLIGHT_API%\bin_x64\release
    
    SUCCESS: Specified value was saved.
    C:\Windows\system32>setx PRESAGIS_OPENFLIGHT_SCRIPT %PRESAGIS_OPENFLIGHT_API%\bin_x64\release
        
    SUCCESS: Specified value was saved.
    ```

    Refresh environment variables

    ```
    C:\Windows|system32>refreshenv
    Refreshing environment variables from registry for cmd.exe. Please wait...Finished..
    ```

    Verify the environment variable was set properly:

    ```
    C:\Windows\system32>echo %PYTHONPATH%
    C:\Presagis\Suite15\OpenFlight_API\bin_x64\release
    
    C:\Windows\system32>echo %PRESAGIS_OPENFLIGHT_SCRIPT%
    C:\Presagis\Suite15\OpenFlight_API\bin_x64\release
    ```

    Close the Command Prompt Window

* Open a Command Prompt window (cmd.exe) normally in the folder you downloaded and extracted for fltcnvt.

    Shift|Right-click on the folder in Windows Explorer and you will see a menu entry titled "Open command window here"

    Confirm python is working correctly in your new Command Prompt window (your directory will be different)

    ```
    C:\Users\joesmith\fltcnvt>python -V
    Python 2.7.13
    ```

    Now try the fltcnvt script itself

    ```
    C:\Users\joesmith\fltcnvt>python fltcnvt.py
    usage: fltcnvt.py <openFlight.flt> sourceDrive targetDrive
    ```

* All done

## Example

```
C:\Users\joesmith\fltcnvt>python fltcnvt.py U:\ucla\ucla.flt U: P:
I: OpenFlight API version 15.0.0.
I: Loading plugin <OpenFlight Data Dictionary> from <C:/Presagis/Suite15/OpenFlight_API/bin_x64/release/fltdata.dll>...
I: Site <FLTDATA> registered for plugin <OpenFlight Data Dictionary>.
I: Plugin <OpenFlight Data Dictionary> loaded.
I: File written <P:/mg/trees/olive.flt>.
I: File written <P:/mg/trees/olive3.flt>.
I: File written <P:/mg/trees/sycamore2.flt>.
.
.
.
```

## Notes

* You must enter the full path to the `<openflight.flt>` source file

* The `sourceDrv` and `targetDrv` are simply the drive designators, i.e. C:

* Make sure you have enought disk space on the targetDrive

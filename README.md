# Welcome to SmartHome System!


This project is done by Marcus Kho, Jonathan Au and Daniel Mario Tablan for the module Internet of Things (IoT).



## Disclaimer

Please also download the files stated in the Required Files folder.
For more information on our project, please download the **report.docx** file.



## Overview


This application is a SmartHome System. The camera is used to detect suspicious intrusion or activity around a protected/personal area, and also a surveillence camera to view and monitor the surroundings. The DHT11 Humidity and Temperature sensor is to sense the temperature and humidity of the house and if the detected temperature is too high, the Air Conditions will be automatically turned on to cool down the house. Where as the RFID Reader and RFID Tags acts as a key to the house and each family member should be in possession of a single RFID tag.

For the Camera, once movement any movement is detected the application will alert the user, and the user can view the live stream via a web interface or an application. From the live stream, the user can choose to record the current live stream and save it.

From the web interface, the user can also download any recorded videos, so that he does not have to connect into the IoT device to download. Lastly, it also comes with a doorbell function. From there, the user can also view the temperature and humidity of the house and control the air conditions around the house.

The various telepots that are used to support the applications acts as a remote for the sensors, like the RFID Scanner, used in this single application.



## Applications


This IoT device can be integrated into any home so as to make everyday house appliances more automated and even in a sense, much smarter. The SmartHome System also provides a much higher level of security as the keys to the house are replaced with RFID Scanner and Tags and there is also a surveillance camera system installed into this IoT device. The surveillance camera was primarily created to detect any suspicious intrusion or monitor any suspicious activity while the RFID Scanner and Tags were created to provide a much higher level of security by replacing normal everyday locks and key. From the telepot that is connected to the RFID Scanner, users are also able to keep track of user activities and check who is at home as well.



## Hardware Requirements

The items listed in this section are the sensors and actuators that we have attached to our breadboard

 
- DHT11 Sensor x1
 
- Buzzer x1
 
- Buttons x4
 
- RFID Scanner x1
 
- RFID Tag x1
 
- LDR x1
 
- MCP3008 x1
 
- pir Motion Sensor x1
 
- LED (To mimic air con) x1
 
- LED (For real LED) x1
 
- Resistors
 
- Wires
 
- Camera x1



## Required Libraries

These are some of the following Libraries that needs to be installed, more of the required libraries will be documented down in our **report.docx**

 
- uv4l
 
- node-red
 
- telepot
 
- python-opencv


## Youtube Video
Our YouTube video can be found at
https://youtu.be/0yecuXM2T4I
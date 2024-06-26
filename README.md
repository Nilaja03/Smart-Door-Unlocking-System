# Overview:

This project presents an Internet of Things (IoT) solution for enhancing home security through a smart door locking system. The system employs ESP32 and a servo motor to control the locking mechanism, offering two distinct scenarios for door access. The first scenario allows the door to unlock when the correct RFID card is presented or the accurate passcode is entered from the outside, reverting to a locked state otherwise.

The second scenario focuses on environmental monitoring, utilizing a DHT11 sensor to detect high temperatures within the house. Upon detecting elevated temperatures, a buzzer is activated, and the door is automatically unlocked using the servo motor. Unlike the first scenario, the door remains unlocked to facilitate ventilation and cooling until the temperature returns to a safe range.

Furthermore, the system integrates with ThingSpeak, a cloud platform, to transmit real-time temperature data, enabling users to remotely monitor and analyze temperature trends within their living space. This two-fold approach not only enhances security through traditional access control methods but also addresses comfort and safety concerns by responding to environmental conditions. The proposed smart door locking system offers a versatile and intelligent solution for modern home automation.


# Block Diagram of How the System Works:

![image](https://github.com/Nilaja03/Smart-Door-Unlocking-System/assets/88586459/c4bbca4e-a281-4ccd-8d70-80ddf0cbea20)


# Video Demos:

https://github.com/Nilaja03/Smart-Door-Unlocking-System/assets/88586459/7dc138d0-2759-4a80-8c41-47830bce0386



https://github.com/Nilaja03/Smart-Door-Unlocking-System/assets/88586459/c9566c35-0a4d-4989-b692-409fa1b5e8e0

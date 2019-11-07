# eta_prime
Eta Prime code and circuit CAD

This repository contains all the work done for the electronics for our speedbike Eta Prime.

The main purpose of this system was to implement a video feed with a read out ceratin values imposed of it for the rider to see out of the vechicle. There are two 'versions' of the circuit in this repository: 
  Primary one - based on using a raspberry pi and RPi Camera
  Backup - uses a MINIM OSD Module that overlay an OSD to an analog camera feed and passes it on as analog
  
We only currently have the circuitry (designed in EAGLE) for this back system and it is all contained in the "EtaPrimeVisionAnalog" folder. The remaining files are for the primary system which was designed in KiCAD and programmed in python.

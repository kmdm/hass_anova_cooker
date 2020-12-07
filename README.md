# hass_anova_cooker

The aim of this custom component is to support the ANOVA Precision Cookers in Home Assistant (WIFI only). 

Currently it only supports the "old style" API which requires the cooker_id and cooker_secret. For example, the original ANOVA Precision Cooker BT/WIFI. 

## Installation

In future this repository will hopefully be added to HACS but for now only the manual installation method is available.

### Manual installation

Copy `custom_components/anova_cooker` into the `custom_components/` folder in your HASS config directory (the directory containing `configuration.yaml`).

### HACS (preferred)

_CURRENTLY NOT AVAILABLE_

## ANOVA Precision Cooker BT/WIFI

To use this cooker you need to determine your cooker_id and cooker_secret. 

### Getting your cooker_id and cooker_secret

The best/(only!) way to do this is to follow the instructions in the original Python API implementing the API on which this project is based:

  * https://github.com/bmedicke/anova.py/issues/1

Once you have the cooker_id and cooker_secret (it can take several goes) you can add the integration from the integrations page.

## ANOVA Precision Cooker / ANOVA Precision Cooker PRO

_CURRENTLY NOT SUPPORTED_

## ANOVA Precision Cooker Nano

_WILL NEVER BE SUPPORTED_

## Home Assistant entities

This integration will create a few entities for interacting with your device:
  
  * A `climate` entity for managing the temperature and turning the device on/off
  * A `binary_sensor` to show whether the cook has ended and the alarm is sounding
  * A `sensor` to show the current remaining cook time (__In seconds but decreases in chunks of 60s__)
  
 This integration will also create a couple of services :
 
  * `stop_alarm`: Silence the currently active/beeping alarm (__Does not change the alarm state in the `binary_sensor`__)
  *  `create_job`: Create a cook job by providing the time and temperature (_CURRENTLY NOT AVAILABLE_) 
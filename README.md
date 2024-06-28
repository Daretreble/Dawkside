# Dawkside
A multi daw, multi devices, accessible platform for the visually impaired musicians like myself.

Currently, Dawkside functions smoothly in conjunction with Reaper and Ableton Live 12 beta, which is now accessible to screen readers).

# What it does

- This tool helps you create customized settings for plugins. You can name and rearrange pages as you like.
- Each page allows you to add any plugin parameter onto 32 sliders or knobs.
- You can add 32 buttons on each page. These buttons can control plugin settings, send notes or MIDI messages, use sysex, OSC, and predefined mouse movements.
- Ssupports motorized controllers and adjusts to changes.
- Even non-motorized controllers can now use a pickup or direct mode, even if your controller doesn't support it naturally.
- It replicates the accessible version of Push's 64 scaled pads mode in Live, including its scales and a simple drum rack.
- It also supports musical keyboards, letting you create transposition zones, keyboard splits, chord modes, etc.
- Keyboard transposition and zones automatically adapts to the track's name. For example, violin 1 can be transposed in a way and saved. It'll transpose automatically the next time that track's name is encountered, for a particular plugin.
- All these features are accessible through simple questionnaires answered with numbers.
- Customizing an entire controller takes only a few minutes. The functionalities are shared among active DAWs (Digital Audio Workstations). For instance, the undo button is in the same place in Reaper and Live.
- You can modify all configurations using unencrypted JSON files (for advanced users).
- Each button can contain sequences of actions. For instance, you can configure a button to move the mouse pointer to a specific area and produce a sound or send a MIDI note.
- Fixed, momentary, and latch modes are available for each button. Pressed and released states can be configured independantly.

# Supported devices

- Ableton Push 1
- AKAI APC Mini
- AKAI Midi Mix
- Arturia Keylab Mk2
- Icon Platform X+
- Korg D1

# Dawkside Setup Guide

This guide will walk you through the process of setting up Dawkside with Reaper on Windows.

## Prerequisites

- Windows operating system (Tested on Windows 11, 64 bit)
- Administrative privileges
- Internet connection

## Reapy mode or OSC Only mode
Dawkside offers two modes for use with Reaper: Reapy mode and OSC Only mode. The OSC Only mode is simpler to install and more stable, but it is more limited in its functionality. The Reapy mode, on the other hand, requires a more complex installation process involving the Reapy python script, but it offers greater flexibility and advanced features.

## Step 1: Install LoopMidi and create new midi ports for Reaper. (OSC Mode and Reapy Mode)

1. Download and install LoopMidi from [LoopMidi's official website](https://www.tobias-erichsen.de/software/loopmidi.html).
2. In LoopMidi, create two virtual MIDI ports and name them 'reaper_in' and 'reaper_out'.



## Step 2: Install Python (Reapy Mode only)

1. Download and install Python 3.9.7 or any Python version supported by Reaper from the [Python website](https://www.python.org/downloads/).

## Step 3: Install python-reapy (Reapy Mode only)

1. Open a command prompt.
2. Run the following command to install the `python-reapy` package:

   ```shell
   pip install python-reapy


## Step 4: Copy Dawkside ReaperOSC File

1. Locate the setup folder of the Dawkside package.
2. Copy the file named 'Dawkside Reapy.ReaperOSC' (Reapy Mode) or 'Dawkside.ReaperOSC' (OSC Mode),  from the setup folder.
3. Paste it into the OSC folder of your Reaper's installation directory. Typically, this directory is located at C:\Users\[your name]\AppData\Roaming\REAPER\OSC.

## Step 5: Run Reaper 64-bit with the OSARA extension.

## Step 6: Load reapy_config.py Script (Reapy Mode only)

1. Open the actions dialog box in Reaper.
2. Load the script called 'reapy_config.py' from the setup folder of the Dawkside package.
3. Close the dialog box when it confirms that Reapy is successfully installed.

## Step 7: Restart Reaper

## Step 8: Configure OSC Control Surface in Reaper Preferences

1. In Reaper, go to Preferences.
2. Navigate to the Control/OSC/web section.
3. Add a new OSC control surface with the following details:
	- Device name: Dawkside
	- Pattern config file: Dawkside Reapy (Reapy Mode) or Dawkside (OSC Mode)
	- Mode: Configure IP + local port
	- Device port: 9000
	- Device IP: 127.0.0.1
	- Local listen port: 8000
	- Wait between packets: 0

## 					Step 9: Enable MIDI Devices

1. In Reaper, go to Preferences.
2. Navigate to the MIDI devices section.
3. Enable 'reaper_in' as an input MIDI device and 'reaper_out' as an output MIDI device.

## Step 10: Restart Reaper

## Step 11: Run 'Dawkside.exe' from the Dawkside package.

## Step 12: Explore Dawkside
Use the 'help' button on your device to obtain information about all the new device's actions.
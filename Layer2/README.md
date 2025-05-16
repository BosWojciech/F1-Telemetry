# Python Project Setup Guide

This README provides instructions for setting up and running this Python project using a virtual environment.

## Setting up the Virtual Environment

### 1. Installing virtualenv

If you don't have virtualenv installed, you can install it using pip:

```
pip install virtualenv
```

### 2. Creating a Virtual Environment

To create a virtual environment named "env", run the following command in your project directory:

```
python -m virtualenv env
```

## Activating the Virtual Environment

### On Linux/MacOS:

```
source env/bin/activate
```

### On Windows:

```
env\Scripts\activate
```

When activated successfully, you should see `(env)` at the beginning of your command prompt.

## Installing Dependencies

After activating the virtual environment, install the required packages from requirements.txt:

```
pip install -r requirements.txt
```

## Running the Application

### Running main.py

The main application can be run with one of two options:

```
python main.py --mode datacollection
```

or

```
python main.py --mode passthroughmode
```

### Running zmqMonitor.py

To run the ZMQ monitor:

```
python zmq/zmqMonitor.py
```

## Deactivating the Virtual Environment

When finished, deactivate the virtual environment by simply running:

```
deactivate
```

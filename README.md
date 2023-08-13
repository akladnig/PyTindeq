# Tindeq Progressor Strength Tester for macOS

A python and bokeh application that creates a user interface to run climbing strength tests that can store and visualise results.

This application is based on the following apps:

- https://github.com/StuartLittlefair/PyTindeq
- https://github.com/sebastianmenze/Tindeq-Progressor-climbing-strength-test-server

 I needed to tweak Stuart's app to get it working but really wanted to implement some of the features of Sebastian's app. Unfortunately I couldn't get Sebastian's app to run, so I basically decided that it was time time to learn a bit of Python so I re-wrote the application using a mix of Stuart's and Sebastian's code.

 Results are also saved as text files for later analysis in laptop/data
 
 This only works on macOS. 
 
 It is built with the following dependencies:
- Python - 3.11.4
- numpy - 1.25.2
- bleak - 0.20.2
- bokeh - 3.2.1
- playsound - 1.3.0

Also - needs to be run from the laptop directory.
  
I am currently in the process of re-writing this in Flutter as I'm not a huge fan of whole Python, Numpy and Bokeh thing. And, I probably need to clean up all the crap that's not required.
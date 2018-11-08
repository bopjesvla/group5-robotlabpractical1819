**Index:**

Latest FAQ 									
The Robotlab					
Handling the NAO				
NAO code					
Specific questions on the assignments		


**Latest FAQ**

-

**The Robotlab**

*What is the password for the Robotlab wifi?*

The password will be handed out by Gabi.

*Do I need to make a reservation?*

Yes, you need to make a reservation for the Robotlab and a robot.You need to make a reservation so you can ensure you are allowed to use a NAO during the time period you want to work on it. Further, for administration such as who has the keys to the robotlab, it is also necessary you reserve a time slot.

*Where are the NAOs stored?*

The NAOs are stored in the cabinets to the right (when coming in) from the door of the Robotlab. The one furthest away from the door will usually have the most NAOs: use one of the other keys of the Robotlab keyset to open the cabinet.

**Handling the NAO**

*Where can I find the documentation?*

The documentation can be found at: http://doc.aldebaran.com/2-5/index_dev_guide.html 

*How do I turn the NAO on?*

When the NAO is turned off, press the NAO once in the chest button. It will take a while for the NAO to activate once you do this: once the NAO makes a sound, you can activate it.

*How do I get the NAO’s IP address?*

Press the NAO’s chest button in shortly once when it is on. Keep in mind that while a NAO tends to have the same IP address as it ahd before shutdown, it can change. Always check if the IP address is still the same when starting a NAO up.

*How do I turn the NAO off?*

Press the NAO’s chest button when it is turned on and keep it till the NAO makes a long turning-off noise. The NAO will take a while before completely shutting off.

*The NAO is in an unstable position, but its limbs refuse to budge. How do I get it to sit down without using any code?*

Two short presses on the chest button should force the NAO to rest and relax its muscles. It will also take on a slightly more stable position while doing so: this pose is less stable than sitting, and a firm push will get it to fall over. Move the limbs so it sits down.

*Where are the touch sensors?*

The NAO has a bumper on each feet, which has a left and right to them ('left side of right foot, for example), a touch sensor through the lower parts of its arm (does not always activate) a touch sensor on the back of its hand, touch sensors on the left and right side of the hand, and one button on top of its head (which activates 'head', and either 'for, middle and rear head').

*Where is the camera of the NAO?*

The camera of the NAO is the small black gap on the NAO’s forehead, above the middle of the eyes.

*I started my code, and it seems to go over, but the NAO is not doing anything or seems to do another group’s code or the code I got it to do before. What do I do?*

During later assignments, you will use various modules of the NAO and use the pythonbroker to do so. If the modules are not properly turned off (for example, due a crash), only the main code is stopped, not the code of the modules. The modules will keep on going. 

To fix this, turn the NAO off and then turn it back on, or have everyone using that specific NAO reset their python console. To prevent this situation from happening, make sure that the main part of your code is surrounded with a ‘try and catch’, with in the try the robot behaviour. Your catch should catch any exception. If the catch is activated, it should put the NAO in a resting position and use the following line of code:

pythonBroker.shutdown() (replace pythonBroker with the variable name you used for the pythonBroker object).

This will force any module to shut down, properly ending the code in all modules.

*I cannot connect to the NAO. What do I do?*

Check if your laptop is connected to the Robotlab wifi. If so, check if the NAO you use for testing is connected (press the button once shortly: if it is connected, it should successfully state its IP address, else state it cannot connect). If the NAO is still connected, try another NAO, and ask another group if they can run on your NAO. If you can do the former but not the latter, the NAO might still be disconnected: try resetting it, and if that does not work, inform the instructors or the student assistants. If another group can run their code, but yours cannot work on any NAO, check your code: did you make a connection with the NAO, or is it crashing or doing something else?

*Can I keep the NAO on the table while I run my code?*

If you need to have the NAO do anything but head/gentle arm movements, place the NAO on the ground. We do not want the NAO to fall off the table.

**NAO Code**

*How do I know if I installed naoqi on python?*

Check if the following line of code works in the python console:

import naoqi

If this runs without an error, you have a working version of naoqi.

*When I am installing NAOQI (Windows), it says it can only find Python 3.7 in the registry, but I have downloaded Python 2.7. How do I fix this?*

This can happen when you downloaded the 64-bit python 2.7 version. Download Python 2.7 for 32 bit (there is no mention of it being 64 bit in the file name) and install it. Now try to run the installer again.

If the above does not solve it, add python 2.7 to your environment variables and check again. If it still fails to find Python 2.7, ask a student-assistent to help you through.

*Why should my code end by placing the robot in a sitting position and putting it to rest?*

The sitting position is the most stable position for the Nao to be in: it is unlikely to fall. You need to put it in rest to ensure all motor limbs are set back to 0 stiffness: it requires power to have stiffness, and the motors may overheat if kept too long at a higher stiffness!

*The code seems to be working, but the NAO is not moving. How do I solve this?*

Check if you changed the stiffness of the limbs you are using to higher to 0.0. If this is not the case, the robot will not have the strength to move itself. Also make sure you connected to the correct modules.

*What does the stiffness mean?*

The stiffness represents how much power the motors in the limb use to keep or move the limb to a position. At 0 stiffness, the robot will not have the power to move. At 0.1 stiffness, the robot can move its limb, but any push will still cause it to give.

*What is the function to place get the NAO to rest in my code?*

mst.rest()

mst is the variable name for the motion Proxy (Created by, for example: 'mst = ALProxy("ALMotion")'). Also make sure that the robot is in a stable position first! (stop walking, sit down).

*The touch sensors report that two sensors are touched, but I only touched one. What is going wrong?*

Some of the touch sensors will report twice that they were touched. The head, for example, will report having been touched on the head, ('head'), and where on the head (front, middle or rear). Make sure to filter one of the two out in your code depending on your needs.

*One or more of the demo files does not work on my computer. Did I do something wrong?*

The demo code was tested by the student assistants. If the demos do not work on your computer, it is likely something went wrong on your side. If you are convinced the problem is in the code, ask the student assistants for help (and ask them when you cannot find the problem by yourself.)

*The sonar sensors seem to not react or react very late to an obstacle. What is the problem?*

We have found a similar problem during initial testing where the sonar sensors had trouble detecting obstacles. While we not found a solution yet, we will take the problems into account, so do not worry. Do try to find alternative solution for any problem that seems to require its use if we do not specify that you need to use the sonar sensor.

**Specific questions on the assignments**

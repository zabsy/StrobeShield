# StrobeShield
![Logo](https://github.com/zabsy/StrobeShield/assets/118029339/4ef7d70b-d9f9-4374-b85a-f5e2c475bc20)
![StrobeShield Image](https://github.com/zabsy/StrobeShield/assets/118029339/0414a460-40d2-497d-88e2-152297a199c1)

## Eureka Hacks Project

[Devpost](https://devpost.com/software/strobeshield)
[Pitch Deck](https://www.canva.com/design/DAGEUyZ1Bl0/Mm0vCsuFKII6kFYziTLEaA/edit?utm_content=DAGEUyZ1Bl0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

### Inspiration
One of our team members has a parent who is a school teacher, facing challenges with students experiencing epileptic seizures. Teachers like our team member's parent can't constantly monitor and prevent seizures. We came up with the idea of creating something to prevent photosensitive seizures in classrooms: a pair of glasses utilizing polarized film properties. This design idea of polarized lenses was inspired by a workshop held by the Institute of Quantum Computing at the University of Waterloo.

### What it does
StrobeShield is a pair of glasses designed to prevent photosensitive seizures. It detects flashing lights and blocks them by rotating polarized lenses, effectively blacking out the light. In addition, StrobeShield includes a web app that logs previous epileptic incidents. Moreover, it features an automated SMS system that alerts parents when a seizure occurs.

### How we built it
After numerous frame iterations, a final design was created using SOLIDWORKS and 3D printed in silk PLA. The frame adopted a classic glasses framework with two gears surrounding each lens, and a central gear to synchronize the rotation of both lenses. The device featured four polarized lenses, with two fixed and two able to rotate with the gears for polarization. A DC motor was mounted on the side of the glasses to drive the gear mechanism when flashing light was detected.

The code for the Pico involved creating an algorithm to interpret the inputs of the photoresistor to determine whether there were flashing lights present at a high enough frequency to be dangerous. Alongside that, we integrated a web app that acts as a log for the the seizure history detected by the Pico. An automated SMS system was also created in order to inform parents about a seizure that happened to their child.

### Challenges we ran into
We encountered a challenge initially when gluing the pieces together, with the lenses misaligning. Additionally, we faced the issue of the device not working in the final hour, despite having tested it earlier and it working perfectly.

### Accomplishments that we're proud of
We were immensely proud of the mechanical mechanism of the device. The countless hours of 3D design and prototyping truly paid off when it functioned smoothly. Our algorithm for detecting flashing lights at a specific frequency was another source of pride. Additionally, we were proud of our circuit system and all the meticulous soldering work that went into it.

### What we learned
For most of us, this was our first experience with an in-person hackathon. We gained valuable insights into the format of hackathons and learned extensively about Raspberry Pi, circuitry, epilepsy, and various new skills from each of our teammates. Most importantly, we discovered the significance of teamwork; without each other, we couldn't have completed this project in just one day. Understanding how to integrate device solutions to health issues while using web-based publishing of data allowed us to see the impact that we can have on the safety and wellbeing of individuals who have to go through stressful or potentially harmful situations, such as having epilepsy and the risks associated.

### What's next for StrobeShield
Next with StrobeShield, we plan to develop a seizure prediction feature by creating a machine learning model using TensorFlow. This will involve utilizing a dataset on ECG (electrocardiogram) and epilepsy to train the model.

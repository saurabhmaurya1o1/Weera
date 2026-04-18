# Weera

## 🚀 About the Project
A smart autonomous system that uses AI to identify weeds in real time and deliver targeted herbicide spraying, improving efficiency while minimizing labor and chemical waste.

## 🔗 Important Links
* **Presentation Deck:** [https://1drv.ms/p/c/D0A1682B3241637B/IQDNzbnJ7zDbTb1Ad9LURQOkAZpsT3Q6sLZqpCfHKnORUgM?e=bnsp3m]
* **Dataset used for training the model: ** [https://www.kaggle.com/datasets/sayalis069/mh-weed16]

## 🛠️ Built With
* [Yolov8]


## Model
* modelv1 is the Yolo Model we are using to detect and pin point weeds.

## Code Explanation
* main.py is program, we used to train the model.
* withTurretControl.py is program, we are using to detect and sending the coordinated to arduino.
* turret.ino is program, we're using in arduino to receive coordinated from model, and using that coordinated arduino locks the turrent to that specfic
 coodinated and performs precise targeted spraying.
* moisture.ino is used to detect moisture in soil, and blink designated color according to moisture level in soil.

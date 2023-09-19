# PrecisionFarming

Smart Precision Farming is an IoT and ML-based project that helps farmers use fertilizer and water resources effectively. The goal of this project is to enable any farmer or user with remote access to monitor his or her farm. This project aims to increase the farmer's profits,
effectively use the resources and yield a better crop.The project is divided into three sub categories 1) Crop Recommendation 2) Fertilizer Prediction and 3) Pump Controller Automation 

The basic idea of this project is that we plug in different sensors like n,p,k,ph,ec,soil moisture, and humidity on the farm. These sensors have the ability to transmit the readings wirelessly to any gateway located in or around a 10-kilometer radius. These sensors have better
battery life, less latency, being unlicensed, and many other advantages over other conventional sensors. The readings are transmitted to a gateway called LoraWan, which has the ability to connect to 100 sensors located within 10 km radius. LoraWan Gateway takes the readings from the sensor and transmits
to the cloud. This data is processed by sending into machine learning application, which uses different algorithms like XgBoost,Random Forest,SVM,Decision Tree. The best performing algorithm is automatically triggered as per the given inputs. The processed output is sent continuosly through mail and sms to the farmers in their desired language with the help of a cron job. 

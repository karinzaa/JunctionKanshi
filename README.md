<br>
<img align="right" src="https://github.com/karinzaa/JunctionKanshi/blob/main/JunctionKanshiLogoOriginal.png" width="350"></img>
<p align="center">
</br>	

# JunctionKanshi
## ICT720-software-2024
## Our Members
1. Purit Jessadakannasoon (6614552619)
2. Rosi Indah Agustin (6614552562)
3. Karin Vitoonkijvanit (6614552589)

# Overview     
## Domain: Traffic Control

## Objective
To develop a system that detects traffic congestion at junctions, enabling efficient traffic management and timely intervention.

## Core Components
1. **Sensors and Cameras:** Deployed at junctions to monitor traffic flow and density.
2. **Data Processing Unit:** Analyzes data from sensors and cameras, detecting congestion patterns.
3. **User Interface:** Displays real-time traffic data for public use and traffic management teams.

## Technology Stack
- **IoT Devices:** For real-time data collection.
- **Machine Learning Algorithms:** To analyze traffic patterns and predict jams.
- **Cloud Computing:** For data storage and processing.

## Stakeholders

1. **Traffic controller**
2. **Urban Planners**
3. **Law Enforcement**
4. **Tech Providers and Developers**

## User Stories

1. **US1:** as a traffic controller, I want to monitor real-time data on traffic volume
   - **acceptance criteria #1** I can see the number of vehicles passing through the junction over specific periods
   - **acceptance criteria #2** I can see the number of pedestrians crossing the junction over specific periods
   - **acceptance criteria #3** I can identify the peak hours and patterns of traffic congestion
2. **US1:** as a traffic controller, I want to be notified when there is a traffic jam at the junction
   - **acceptance criteria #1** I get no notification if there is no a traffic jam at the junction
3. **US2:** as an urban planner, I need comprehensive traffic data so that I can analyze traffic patterns and plan better road networks
   - **acceptance criteria #1** I get the data that contains the number of vehicles passing through the junction over specific periods
   - **acceptance criteria #2** I get the data that contains the number of pedestrians passing through the junction over specific periods
   - **acceptance criteria #3** I get the data that present the peak hours and patterns of traffic congestion
4. **US3:** as a law enforcement, I want to be notified when there is a traffic jam at the junction, as they might indicate accidents or illegal activities
   - **acceptance criteria #1** I get no notification if there is no a traffic jam at the junction
5. **US4:** as a tech provider/developer, I want to be notified when there is an error in the system
   - **acceptance criteria #1** I get a notification if the system can't display the real-time traffic junction
   - **acceptance criteria #2** I get a notification if the system detects an object with the accuracy below 50% of the object

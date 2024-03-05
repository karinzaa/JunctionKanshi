<br>
<img src="https://github.com/karinzaa/JunctionKanshi/blob/main/images/JunctionKanshiLogoLandscape.png" style="display: block; margin-left: auto; margin-right: auto; width: auto;" alt="JunctionKansh Logo">
</br>

# JunctionKanshi
## ICT720-software-2024
## Our Members
1. Purit Jessadakannasoon (661XXXX619)
2. Rosi Indah Agustin (661XXXX562)
3. Karin Vitoonkijvanit (661XXXX589)

# Overview     
## Domain: Traffic Control

## Objective
To develop a system that detects traffic congestion by artificial intelligence, enabling efficient traffic management and timely intervention.

## Stakeholders
1. **Traffic controller**
2. **Tech Providers and Developers**

## User Stories
1. **US1:** as a traffic controller, I want to monitor real-time data on traffic volume, so I know whether there is a traffic jam or not
   - **acceptance criteria #1** I can see the number of vehicles passing through the junction over specific periods
   - **acceptance criteria #2** I can identify the peak hours and patterns of traffic congestion
2. **US2:** as a traffic controller, I want to be notified when there is a traffic jam at the junction, so I can check and control the traffic
   - **acceptance criteria #1** I get no notification if there is no a traffic jam at the junction
3. **US3:** as a tech provider/developer, I want to monitor the status of devices
   - **acceptance criteria #1** I can see the status of all devices (online/activated/offline).
   - **acceptance criteria #2** I can see a map of installed devices

## Threat Categorization and Mitigation Technique
1. **Spoofing**
   - **Use Strong Authentication Methods:** Implement robust authentication mechanisms to verify the identity of users and systems.
   - **Implement Multi-Factor Authentication (MFA):** Require more than one method of authentication to increase security against unauthorized access.

2. **Tampering**
   - **Encrypt Sensitive Data:** Protect data integrity and confidentiality by encrypting data at rest and in transit.
   - **Use Integrity Checks:** Implement mechanisms like checksums and cryptographic hashes to detect unauthorized changes to data.

3. **Repudiation**
   - **Implement Non-Repudiation Mechanisms:** Use technologies that ensure an individual or entity cannot deny the authenticity of their actions.
   - **Use Digital Signatures:** Apply digital signatures to communications and transactions to provide proof of origin and integrity.

4. **Information Disclosure**
   - **Control Access to Sensitive Information:** Implement strict access controls to ensure only authorized individuals can access sensitive data.
   - **Use Data Leakage Prevention Tools:** Deploy tools designed to detect and prevent unauthorized access or disclosure of sensitive information.

5. **Denial of Service (DoS)**
   - **Implement Rate Limiting:** Use rate limiting to control the amount of traffic to a service, preventing overload and ensuring availability.
   - **Use Distributed Denial of Service (DDoS) Protection:** Employ DDoS protection services to mitigate the impact of large-scale denial-of-service attacks.

6. **Elevation of Privilege**
   - **Enforce Least Privilege Principle:** Ensure users and systems have only the minimum levels of access or permissions they need to perform their functions.
   - **Conduct Regular Privilege Audits:** Regularly review and adjust permissions to prevent unauthorized elevation of privilege

## Summary Diagram
<img align="center" src="https://github.com/karinzaa/JunctionKanshi/blob/main/images/JunctionKanshiDiagram.png"></img>

## Sequence Diagram
<img align="center" src="https://github.com/karinzaa/JunctionKanshi/blob/main/images/sequence_diagram.png"></img>

## State Diagram
<img align="center" src="https://github.com/karinzaa/JunctionKanshi/blob/main/images/state_diagram.JPG"></img>

## UML Class Diagram
<img align="center" src="https://github.com/karinzaa/JunctionKanshi/blob/be81252f911fbaf2ff1e75362cdb24baaa0ed5e8/images/UMLClassDiagram.png"></img>

## Threat Categorization and Mitigation Flowchart
<img align="center" src="https://github.com/karinzaa/JunctionKanshi/blob/main/images/Detailed%20Threat%20Categorization%20and%20Mitigation%20Flowchart.png"></img>

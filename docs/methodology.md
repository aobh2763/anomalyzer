# CRISP-DM Methodology

The project aims to explore the use of machine learning techniques to detect *anomalous* or *potentially malicious* behavior in *Windows Event Logs*. The system analyzes event data from Windows Server environments and aims to automatically detect suspicious patterns such as failed authentication attempts, privilege escalation, unauthorized account creation, abnormal service execution, and off-hours activity.

The **CRISP-DM methodology** is an appropriate framework for this project, as it is one of the most widely used methodologies for data mining and machine learning workflows.

## 1. Business Understanding
*Status*: Done

### Problem Statement

Windows Server environments generate large volumes of event logs across multiple channels (Security, System, and Application logs). Manually inspecting these logs is inefficient and impractical, particularly for detecting subtle or repetitive malicious behavior.

### Project Objective

The objective of this project is to detect suspicious activities in Windows Server logs using machine learning techniques.

The system aims to automatically detect the following types of behavior:

- Failed and repeated login attempts
- Privilege escalation events
- Suspicious account creation activities
- Unusual service execution events
- Activities occurring outside normal working hours

These represent common indicators of potential security incidents in Windows environments.

### Data Sources

The data used in this project is extracted from Windows servers, including:

- Application logs
- System logs
- Security logs

An example of a security log file is available [here](/data/raw/93_securitelog.evtx).

### Scope of the Project

**In Scope:**
- Analysis of Windows Event Logs (.evtx)
- Focus on Application, System, and Security logs
- Offline analysis of historical log data
- Unsupervised machine learning for anomaly detection
- Development of a simple interface to visualize results

**Out of Scope:**
- Real-time monitoring of systems
- Integration with enterprise SIEM tools
- Automated incident response
- Correlation across multiple machines or servers

## 2. Data Understanding
*Status*: In progress

The data understanding phase focuses on exploring Windows Event Log data (.evtx) to identify structure, patterns, and basic statistical properties before moving into feature engineering and modeling.

Initial work uses a single security log file containing 31,465 events, parsed using `PyEvtxParser` and converted into a structured tabular format. One invalid sentinel timestamp was removed during preprocessing.

### Focus of Exploration

The first step of analysis concentrates on temporal behavior, using timestamp-derived features such as event time, minute, and hour. This allows for an initial understanding of how events are distributed over time.

### Initial Findings

Early exploration shows that events are not uniformly distributed. Instead, the data exhibits clear periodic patterns and recurring spikes at consistent time intervals. Event frequency remains stable at a high level overall, suggesting a continuous and automated event generation process.

### Current Status

Analysis is ongoing. Further work will expand beyond timestamps to include additional log attributes in order to better understand event types and identify meaningful patterns for anomaly detection.

## 3. Data Preparation
*Status*: Not done

## 4. Modeling
*Status*: Not done

## 5. Evaluation
*Status*: Not done

## 6. Deployment
*Status*: Not done
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
*Status*: Done

The data understanding phase explored three Windows Event Log files (.evtx), Security, System, and Application, to identify structure, patterns, and attribute-level properties before moving into feature engineering and modeling.

A custom ETL pipeline (`extract.py`, `transform.py`, `load.py`) was built to parse `.evtx` files via `PyEvtxParser` and produce structured, analysis-ready DataFrames. The pipeline handles three components of each event record: **timestamps**, the **System block** (event metadata: EventID, Provider, Level, Correlation, Execution, etc.), and **EventData/UserData** (the event-specific payload). Because payload schema differs per EventID, and even per provider for the same EventID, the ETL normalizes several real-world edge cases: EventIDs wrapped with Qualifiers, unnamed `<Data>` elements (common in legacy providers), and providers using `UserData` instead of `EventData`.

### Timestamp Analysis

All three logs were profiled for temporal behavior (event rate, minute-of-hour and hour-of-day distribution, inter-event gaps):

- **Security log** (31,465 events, ~9.5-hour window): highly periodic, with major/secondary/tertiary peaks aligned to 60/15/5-minute marks, consistent with scheduled task activity rather than user-driven behavior.
- **System log** (59,779 events, ~3-month window): flatter hour-of-day distribution, but uneven minute-of-hour spikes and a recurring daily quiet-then-burst pattern in the `:45`–`:48` window, flagged for manual Event Viewer verification.
- **Application log**: similar automated/scheduled signature, dominated by a single high-frequency source (see below).

### System Block Analysis

Each log's System-block attributes (EventID, Provider, Level, Task, Opcode, Correlation, Execution, etc.) were profiled for constants, near-constants, and dependency on EventID. Genuinely constant fields (e.g. `Channel`, `Computer`, `Level` in Security log) were identified and excluded from later modeling; fields that appeared constant only due to profiling artifacts (e.g. NaN-inflation from combining EventIDs, or `astype(str)` conflating true constants with entirely-missing fields) were re-verified per EventID rather than dropped prematurely.

### EventData Analysis

Because EventData/UserData schema varies per EventID, a dedicated profiling utility was built to compute, per EventID, field-level null rate, cardinality, and a constant/high-null/variable classification, avoiding the pitfalls of profiling a single combined table. All EventIDs across all three logs were reviewed: common EventIDs via aggregate profiling, rare EventIDs (≤50 records) via direct row inspection, since aggregate statistics are not meaningful at very low sample counts.

Findings per log:

- **Security log**: 10 EventIDs identified as directly relevant to the project's five target behaviors (`4624`, `4634`, `4648`, `4662`, `4672`, `4697`, `4702`, `4776`, `4799`, `5379`), each with a distinct schema (5–22+ fields).
- **System log**: highest schema diversity (68 distinct EventIDs). Dominated by Service Control Manager events (`7036`/`7040`, 98.4% of volume), with a long tail of rare but target-relevant EventIDs (service installation, Terminal Services sessions, system time changes, security policy changes) promoted for extraction despite low sample counts.
- **Application log**: minimal structure, 96.5% of records are a single repeated PHP runtime warning (`EventID 4`), and no EventID exposes named/structured fields beyond free-text messages. Assessed as low-value for the project's targets; not planned as a primary feature source.

To reconcile the heterogeneous per-EventID schemas into a form usable by a single model per log type, a shared target schema (`entity`, `actor`, `entity_state`, `source_ip`, `source_host`, `logon_method`, `session_id`, `linked_session_id`, `elevated`, `restricted_admin`) was defined, populated per EventID via a declarative field-mapping registry rather than one-off extraction code. High-cardinality raw identifiers (e.g. `LogonGuid`, `SubjectUserSid`) were deliberately excluded from this schema, since including unique-per-row identifiers would cause trivial isolation of every record in the downstream Isolation Forest model rather than surfacing genuine anomalies.

### Outcome

Data understanding is considered complete for all three log types. Security and System logs are confirmed as the primary modeling sources. Application log was initially deprioritized as a primary feature source, given its low structural diversity (96.5% of records consisting of a single repeated warning). This assessment was later revisited during Modeling: a model was ultimately trained for Application log as well, to ensure complete coverage across all three log types within the final tool, despite an expected weaker signal relative to Security and System logs. The project proceeds with one Isolation Forest model per log type, covering all three logs (Security, System, Application), with anomaly scores combined at the webapp layer, given the differing time windows, schemas, and target relevance across logs.

## 3. Data Preparation
*Status*: Done

Building on the shared target schema defined during Data Understanding, this phase produced a unified, model-ready feature table for each of the three log types (Security, System, Application).

### Schema Unification

A three-layer schema (`timestamp`, `profile`, `data`) was defined, shared in structure across all three log types but with log-specific content for the `data` layer, reflecting the schema divergence observed during Data Understanding:

- **`timestamp`**: cyclic (sine/cosine) encodings of second, minute, hour, day, and month, plus `deltatime` between consecutive events, cyclic encoding avoids the artificial discontinuity of raw numeric time values (e.g. hour 23 and hour 0 appearing maximally distant despite being adjacent).
- **`profile`**: envelope-level attributes shared structurally across all three logs (`event_id`, `event_id_frequency`, `previous_event_id`, `version`, `correlation_activity_id`, `execution_thread_id`, `event_record_id`).
- **`data`**: log-specific payload attributes (e.g. `entity`, `actor`, `context`, `permission`, `ip` for Security; `old_value`/`new_value`, `session_id` for System), extracted via a per-EventID field-mapping registry.

### Field Selection

Given the schema heterogeneity across EventIDs (documented during Data Understanding), a selection rule was applied: EventIDs with at least 10 occurrences receive a full field-mapping entry, extracting their structured payload into the shared schema. EventIDs below this threshold are not individually mapped, but still contribute to modeling through `event_id`, `previous_event_id`, and `event_id_frequency`, ensuring no event is excluded from detection, while bounding the manual mapping effort to a manageable set of EventIDs.

### Feature Engineering

- `deltatime` and `event_id_frequency`/`previous_event_id` are computed across the full, chronologically sorted event sequence per log, so the model can learn both timing irregularities and sequence-level anomalies (an unusual EventID following an unusual predecessor).
- The first event's `deltatime` is set to the mean deltatime of the file rather than left undefined, and its `previous_event_id` defaults to its own `event_id`, avoiding null-handling edge cases at the start of each sequence.

### Encoding

Categorical fields were encoded according to cardinality and semantic type, using custom scikit-learn-compatible transformers where the field's structure required it:

- **Low-cardinality fields** (e.g. `actor`, `status`): one-hot encoding.
- **High-cardinality fields** (e.g. `entity`, `context`, `process_name`): frequency encoding, so rare values are preserved as signal rather than exploding into a sparse one-hot matrix.
- **IP addresses**: a custom `IPAddressEncoder`, decomposing each address into its octets plus a presence flag.
- **Mixed-type fields** (e.g. `old_value`/`new_value`, which hold timestamps, counts, or sizes depending on the source EventID): a custom `MixedValueEncoder`, inferring type (integer, timestamp, text, presence) per value rather than assuming a fixed type.
- **XML-bearing fields** (e.g. `value`, populated by scheduled-task EventIDs): a custom `PresenceXMLTransformer`, flagging presence and XML structure rather than encoding the raw content.
- **Free-text fields** (Application log's `context`): a sentence-embedding-based encoder, reduced via PCA, to capture semantic similarity between related but non-identical messages.
- Unique-per-row identifiers (e.g. `logon_id`, `correlation_activity_id` where near-unique, `event_record_id`) were excluded from the feature set entirely, since including them would cause Isolation Forest to trivially isolate every row, masking genuine anomalies rather than surfacing them.

All transformers were assembled into a single `ColumnTransformer` per log type, producing the final numeric feature table used for model training.

## 4. Modeling
*Status*: Done

Building on the encoded feature tables produced during Data Preparation, this phase assembled and trained the modeling pipeline for each log type (Security, System).

### Modeling Pipeline

Each log type has its own end-to-end pipeline, chaining together the components built in earlier phases: the parser (raw .evtx → nested {timestamp, profile, data} rows), the log-specific ColumnTransformer (encoding categorical/mixed/textual fields into a numeric matrix), and an IsolationForest estimator trained on the resulting feature table. All three log types, Security, System, and Application, ultimately received a trained model. Application log was initially deprioritized during Data Understanding due to its low structural diversity, but was included in modeling regardless, to ensure the deployed tool offers consistent, complete coverage across every log type an analyst might upload, rather than leaving one log type entirely unsupported.

### Why Isolation Forest

Isolation Forest was selected as the modeling algorithm for three reasons specific to this project. First, no labeled examples of malicious or anomalous activity are available in the source data, ruling out supervised classification. Second, the algorithm scales well to the volumes observed during Data Understanding (tens of thousands of events per log) without requiring distance computations across the full dataset, unlike density-based alternatives such as Local Outlier Factor. Third, its scoring mechanism, isolating points via random recursive partitioning and using average path length as an anomaly signal, aligns naturally with the project's feature design: rare categorical values (via frequency encoding) and rare EventID sequences (via `event_id_frequency`/`previous_event_id`) are, by construction, easier to isolate in fewer splits, which is exactly the behavior the model is built to detect.

## 5. Evaluation
*Status*: Done

### Decision Boundary

Isolation Forest does not produce a binary label directly; it produces a continuous anomaly score per event, and a `contamination` parameter determines where the boundary between "normal" and "anomalous" is drawn along that score distribution. In the absence of labeled data, this boundary cannot be tuned against ground truth in the conventional sense. Two considerations shaped the approach taken:

- A fixed, conservative `contamination` value was preferred over an automatically fitted one, reflecting the prior assumption that suspicious events represent a small minority of total activity, consistent with the periodic, largely automated nature of the traffic observed during Data Understanding.
- Synthetic anomalies, constructed to represent each of the five target behaviors (repeated failed logons, privilege escalation via session-linked events, rapid suspicious account creation, abnormal service installation, off-hours activity), were injected into the evaluation data. The position of these synthetic events within the anomaly score ranking, rather than a fixed threshold alone, served as the practical criterion for validating that the decision boundary separates meaningful behavior from routine activity.

### Finding the Correct Attributes

An early evaluation run surfaced a concrete case of this dependency: on the Application log, high-frequency, low-severity events (repeated PHP runtime warnings, routine SPP/RulesEngine events) were assigned disproportionately high anomaly scores. The cause traced back to feature construction rather than the model itself, specifically to free-text fields (`context`) containing volatile substrings, such as embedded GUIDs and temporary file paths, inside an otherwise repetitive message. Because these substrings differ on every occurrence, the embedding-based encoding treated each occurrence as semantically distinct, inflating the isolation difficulty of an event that was, in substance, routine.

This finding reinforced a broader principle applied throughout feature selection: an attribute's suitability for Isolation Forest depends not on whether it carries information in general, but on whether its *encoded* representation reflects genuine behavioral variation rather than incidental uniqueness. The same reasoning had already motivated the exclusion of raw identifiers (`logon_id`, near-unique `correlation_activity_id`, `event_record_id`) during Data Preparation, and this evaluation confirmed it extends to derived representations, such as embeddings of text containing volatile identifiers, not only to raw identifier fields themselves.

## 6. Deployment
*Status*: Done

The deployment phase exposes the trained models to an analyst through a web application, following the client-server architecture and package structure defined in the solution design.

### Web Application

The system is built as a FastAPI backend paired with a React frontend, communicating over a REST API. The analyst uploads a log file through the frontend; the backend runs the file through the corresponding log type's pipeline (parsing, encoding, scoring) and returns the resulting anomaly scores as JSON, which the frontend renders as a results table.

### Server-Side Model Hosting

Trained models and their associated fitted transformers are stored and loaded exclusively on the server; they are never downloaded to or executed on the client. This decision follows directly from three requirements established earlier in the project: encoder state fitted during training must be reused unchanged at inference time, which is only guaranteed if encoding happens in one controlled location; uploaded logs may contain sensitive organizational data (account names, internal IP addresses, file paths) that should not need to leave the server for analysis to occur; and the target user, an analyst without machine learning expertise, requires a working system rather than portable model artifacts.

In practice, both the `IsolationForest` models and their corresponding `ColumnTransformer` instances are loaded once at API startup and held in memory for the duration of the server process, rather than reloaded per request. The same applies to the sentence-embedding model used for Application log's free-text encoding, whose repeated per-request loading was identified as a performance bottleneck and addressed by loading it once at startup and deduplicating repeated text values before encoding.
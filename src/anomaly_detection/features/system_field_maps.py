SYSTEM_DATA_SCHEMA = {
    "context",
    "process_name",
    "session_id",
    "old_value",
    "new_value",
    "status",
    "entity",
    "actor",
}


SYSTEM_EVENT_FIELD_MAPS = {
    1: {  # System time changed
        "Reason": "context",
        "ProcessName": "process_name",
        "ProcessID": "session_id",
        "OldTime": "old_value",
        "NewTime": "new_value",
    },
    2: {  # NDIS/network driver version info
        "Version": "context",
        "Status": "status",
    },
    6: {  # Device status change
        "FinalStatus": "context",
        "DeviceName": "entity",
        "DeviceTime": "new_value",
    },
    12: {  # Network driver loaded
        "MiniportName": "entity",
        "BootMode": "context",
        "StartTime": "new_value",
    },
    14: {  # Network driver config
        "MiniportName": "entity",
        "Config": "context",
    },
    15: {  # Registry hive resized
        "HiveName": "entity",
        "OriginalSize": "old_value",
        "NewSize": "new_value",
    },
    16: {  # Registry hive flushed
        "HiveName": "entity",
        "KeysUpdated": "context",
    },
    20: {  # Boot status update
        "UpdateReason": "context",
        "CountOld": "old_value",
        "CountNew": "new_value",
    },
    35: {  # Time source (NTP)
        "TimeSource": "entity",
        "CurrentStratumNumber": "context",
    },
    55: {  # Processor power state
        "Number": "context",
    },
    98: {  # NTFS corruption detected
        "DriveName": "entity",
        "DeviceName": "actor",
    },
    1801: {  # WER bucket confidence
        "BucketConfidenceLevel": "context",
    },
    6013: {  # System uptime report
        "Data_text": "context",
    },
    6033: {  # Security policy refresh triggered by client
        "Client": "actor",
    },
    7001: {  # Terminal Services session logon
        "UserSid": "entity",
        "TSId": "session_id",
    },
    7002: {  # Terminal Services session logoff
        "UserSid": "entity",
        "TSId": "session_id",
    },
    7036: {  # Service state change
        "param1": "entity",
        "param2": "status",
    },
    7040: {  # Service start type changed
        "param1": "entity",
        "param2": "old_value",
        "param3": "new_value",
    },
}

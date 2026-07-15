APPLICATION_DATA_SCHEMA = {"context", "entity"}


APPLICATION_EVENT_FIELD_MAPS = {
    4: {  # Informational application event
        "Data_text": "context",
    },
    64: {  # COM+/Application object event
        "Context": "context",
        "ObjId": "entity",
    },
    1000: {  # Application Error (crash)
        "Data_text": "context",
    },
    1001: {  # Windows Error Reporting (WER)
        "Data_text": "context",
    },
    4098: {  # Group Policy Preferences
        "Data_text": "context",
    },
    16384: {  # Microsoft-Windows-Security-SPP (Software Protection Platform)
        "Data_text": "context",
    },
    16394: {  # Microsoft-Windows-Security-SPP (Software Protection Platform)
        "Data_text": "context",
    },
}

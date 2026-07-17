from pathlib import Path
from anomaly_detection.parser.data_parsers import parse_system

project_folder = Path.cwd()

evtx_path = project_folder / "data/raw/93_syslog.evtx"

print(evtx_path)
print(parse_system(evtx_path)[0])
print(len(parse_system(evtx_path)))

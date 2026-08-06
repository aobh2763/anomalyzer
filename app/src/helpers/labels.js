import i18next from "i18next";

export const SECURITY_LABELS = {
  4624: "securityids.4624",
  4672: "securityids.4672",
  4634: "securityids.4634",
  4648: "securityids.4648",
  4776: "securityids.4776",
  4799: "securityids.4799",
  4702: "securityids.4702",
  5379: "securityids.5379",
  4662: "securityids.4662",
  4697: "securityids.4697",
  4798: "securityids.4798",
  4611: "securityids.4611",
  5058: "securityids.5058",
  5061: "securityids.5061",
  5059: "securityids.5059",
  4699: "securityids.4699",
  4698: "securityids.4698",
};

export const APPLICATION_LABELS = {
  4: "applicationids.4",
  16394: "applicationids.16394",
  16384: "applicationids.16384",
  4098: "applicationids.4098",
  1001: "applicationids.1001",
  64: "applicationids.64",
  1000: "applicationids.1000",
  1704: "applicationids.1704",
  100: "applicationids.100",
  9027: "applicationids.9027",
};

export const SYSTEM_LABELS = {
  12: "systemids.12",
  19: "systemids.19",
  55: "systemids.55",
  98: "systemids.98",
  1074: "systemids.1074",
  6005: "systemids.6005",
  6006: "systemids.6006",
  6009: "systemids.6009",
  6013: "systemids.6013",
  7001: "systemids.7001",
  7002: "systemids.7002",
  7023: "systemids.7023",
  7024: "systemids.7024",
  7034: "systemids.7034",
  7036: "systemids.7036",
  7040: "systemids.7040",
  7042: "systemids.7042",
  7045: "systemids.7045",
};

const LABELS_BY_LOG_TYPE = {
  security: SECURITY_LABELS,
  application: APPLICATION_LABELS,
  system: SYSTEM_LABELS,
};

export function getEventLabel(eventId, logType) {
  const table = LABELS_BY_LOG_TYPE[logType];
  if (!table) return i18next.t("unknown");
  return table[eventId] ?? i18next.t("unknown");
}

export default LABELS_BY_LOG_TYPE;

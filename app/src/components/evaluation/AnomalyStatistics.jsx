import { Table, Progress, Text, Group, Paper, Stack } from "@mantine/core";
import { getEventLabel } from "../../helpers/labels";
import { useTranslation } from "react-i18next";

function computeStats(anomalies, logType) {
  const total = anomalies.length;
  const counts = {};

  anomalies.forEach((row) => {
    const id = row.event_id;
    counts[id] = (counts[id] ?? 0) + 1;
  });

  return Object.entries(counts)
    .map(([eventId, count]) => ({
      eventId,
      label: getEventLabel(Number(eventId), logType),
      count,
      percentage: total > 0 ? (count / total) * 100 : 0,
    }))
    .sort((a, b) => b.count - a.count);
}

function AnomalyStatistics({ anomalies, logType }) {
  const { t } = useTranslation();

  const stats = computeStats(anomalies, logType);
  const total = anomalies.length;

  if (total === 0) {
    return null;
  }

  return (
    <Paper withBorder radius="md" p="md" w="100%">
      <Stack gap="sm">
        <Group justify="space-between">
          <Text fw={600} size="lg">
            {t("eventIdDistribution")}
          </Text>
          <Text c="dimmed" size="sm">
            {t("lengthType", {
              length: stats.length,
            })}
            {stats.length > 1 ? "s" : ""}{" "}
            {t("eventTotalAnomaly", {
              total,
            })}
            {total > 1 ? "s" : ""}
          </Text>
        </Group>

        <Table verticalSpacing="xs">
          <Table.Thead>
            <Table.Tr>
              <Table.Th>{t("eventId")}</Table.Th>
              <Table.Th>{t("description")}</Table.Th>
              <Table.Th>{t("occurrences")}</Table.Th>
              <Table.Th>{t("anomalyShare")}</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {stats.map(({ eventId, label, count, percentage }) => (
              <Table.Tr key={eventId}>
                <Table.Td>{eventId}</Table.Td>
                <Table.Td c={label === t('unknown') ? "dimmed" : undefined}>
                  {t(`${label}`)}
                </Table.Td>
                <Table.Td>{count}</Table.Td>
                <Table.Td>
                  <Group gap="xs" wrap="nowrap">
                    <Progress
                      value={percentage}
                      color="gold"
                      size="lg"
                      style={{
                        flex: 1,
                      }}
                    />
                    <Text size="sm" w={50}>
                      {percentage.toFixed(1)}%
                    </Text>
                  </Group>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </Stack>
    </Paper>
  );
}

export default AnomalyStatistics;

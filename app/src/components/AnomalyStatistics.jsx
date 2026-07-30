import { Table, Progress, Text, Group, Paper, Stack } from "@mantine/core";
import { getEventLabel } from "../helpers/labels";

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
                        Répartition par Event ID
                    </Text>
                    <Text c="dimmed" size="sm">
                        {stats.length} type{stats.length > 1 ? "s" : ""}{" "}
                        d'événement · {total} anomalie{total > 1 ? "s" : ""}
                    </Text>
                </Group>

                <Table verticalSpacing="xs">
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>Event ID</Table.Th>
                            <Table.Th>Description</Table.Th>
                            <Table.Th>Occurrences</Table.Th>
                            <Table.Th>Part des anomalies</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {stats.map(({ eventId, label, count, percentage }) => (
                            <Table.Tr key={eventId}>
                                <Table.Td>{eventId}</Table.Td>
                                <Table.Td c={label === "Inconnu" ? "dimmed" : undefined}>
                                    {label}
                                </Table.Td>
                                <Table.Td>{count}</Table.Td>
                                <Table.Td>
                                    <Group gap="xs" wrap="nowrap">
                                        <Progress
                                            value={percentage}
                                            color="gold"
                                            size="lg"
                                            style={{ flex: 1 }}
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
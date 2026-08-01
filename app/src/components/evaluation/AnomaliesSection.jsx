import { Stack, Title, Text, Divider } from "@mantine/core";

import AnomalyStatistics from "./AnomalyStatistics";
import AnomaliesTable from "./AnomaliesTable";

function AnomaliesSection({ anomalies, logType }) {
    return (
        <Stack gap="md" align="center">
            <Title order={2} ta="center" fz={{ base: 28, sm: 32, md: 40 }}>
                Anomalies détectées ({anomalies.length})
            </Title>

            {anomalies.length === 0 ? (
                <Text c="dimmed" ta="center">
                    Aucune anomalie détectée avec cette frontière de décision.
                </Text>
            ) : (
                <>
                    <AnomalyStatistics anomalies={anomalies} logType={logType} />
                    <Divider mt="lg" />
                    <AnomaliesTable anomalies={anomalies} />
                </>
            )}
        </Stack>
    );
}

export default AnomaliesSection;

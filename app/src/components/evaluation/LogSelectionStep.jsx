import { Stack, Text, Select, Button } from "@mantine/core";

function LogSelectionStep({
    logOptions,
    selectedLog,
    setSelectedLog,
    loading,
    extracted,
    onExtract,
}) {
    return (
        <Stack gap="md" align="center">
            <Text c="dimmed" size="lg" ta="center">
                Choisir un log chargé pour extraire ses caractéristiques.
            </Text>

            <Select
                w={600}
                label="Logs disponibles"
                withAsterisk
                placeholder="Choisir un log"
                data={logOptions}
                value={selectedLog}
                onChange={setSelectedLog}
                loading={loading}
                disabled={extracted}
            />

            <Button
                w={400}
                color="gold"
                loading={loading}
                disabled={!selectedLog || extracted}
                onClick={onExtract}
            >
                Extraire les caractéristiques
            </Button>
        </Stack>
    );
}

export default LogSelectionStep;

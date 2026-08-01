import { Stack, Text, Select, Button } from "@mantine/core";

function ModelSelectionStep({
    modelOptions,
    selectedModel,
    setSelectedModel,
    loading,
    modelValidated,
    modelError,
    onSelectModel,
    onChangeModel,
}) {
    return (
        <Stack gap="md" align="center">
            <Text c="dimmed" size="lg" ta="center">
                Choisir un modèle compatible avec ce log.
            </Text>

            <Select
                w={600}
                label="Modèles disponibles"
                withAsterisk
                placeholder="Choisir un modèle"
                data={modelOptions}
                value={selectedModel}
                loading={loading}
                error={modelError}
                onChange={(value) => {
                    setSelectedModel(value);
                    onChangeModel();
                }}
            />

            <Button
                w={400}
                color="gold"
                loading={loading}
                disabled={!selectedModel || modelValidated}
                onClick={onSelectModel}
            >
                Sélectionner le modèle
            </Button>
        </Stack>
    );
}

export default ModelSelectionStep;

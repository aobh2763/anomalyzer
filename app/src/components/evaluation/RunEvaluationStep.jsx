import { Stack, Text, Button } from "@mantine/core";

function RunEvaluationStep({ loading, onEvaluate }) {
    return (
        <Stack gap="md" align="center">
            <Text c="green" size="lg">
                Modèle compatible
            </Text>

            <Text c="dimmed" ta="center">
                Une première évaluation peut prendre quelques instants.
            </Text>

            <Button w={400} color="gold" loading={loading} onClick={onEvaluate}>
                Lancer l'évaluation
            </Button>
        </Stack>
    );
}

export default RunEvaluationStep;

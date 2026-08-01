import { Stack, Title, Image, Text, NumberInput, Button } from "@mantine/core";

function EvaluationResultsStep({
    imageUrl,
    decisionBoundary,
    setDecisionBoundary,
    boundaryError,
    setBoundaryError,
    loading,
    onUpdateBoundary,
}) {
    return (
        <Stack gap="lg" align="center">
            <Title order={2} ta="center" fz={{ base: 28, sm: 32, md: 40 }}>
                Résultats
            </Title>

            <Image src={imageUrl} radius="md" w={1000} />

            <Text c="dimmed" ta="center">
                Modifier la frontière de décision afin de contrôler quelles
                observations sont considérées comme anormales.
            </Text>

            <NumberInput
                w={600}
                label="Frontière de décision"
                placeholder="-0.05"
                value={decisionBoundary}
                onChange={(value) => {
                    setDecisionBoundary(value);
                    setBoundaryError("");
                }}
                error={boundaryError}
                min={-1}
                max={1}
                step={0.01}
                decimalScale={3}
            />

            <Button
                w={400}
                color="gold"
                loading={loading}
                onClick={onUpdateBoundary}
            >
                Mettre à jour
            </Button>
        </Stack>
    );
}

export default EvaluationResultsStep;

import { Center, Title, Stack } from '@mantine/core';

function EvaluationPage() {
    return (
        <>
            <Center h="calc(100vh - 60px)">
                <Stack grow align="center">
                    <Title order={1} fz={{ base: 36, sm: 64 }}>Evaluation Page</Title>
                </Stack>
            </Center>
        </>
    );
}

export default EvaluationPage;
import { Center, Title, Stack } from '@mantine/core';

function ModelPage() {
    return (
        <>
            <Center h="100vh">
                <Stack grow align="center">
                    <Title order={1} fz={{ base: 36, sm: 64 }}>Model Page</Title>
                </Stack>
            </Center>
        </>
    );
}

export default ModelPage;
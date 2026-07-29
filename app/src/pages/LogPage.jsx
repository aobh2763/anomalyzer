import { Center, Title, Stack, Container, Divider, Text } from '@mantine/core';

function LogPage() {
    return (
        <>
            <Center h="100vh">
                <Container size="md" py="xl" pt={85}>
                    <Stack gap="xl">
                        <Title order={1} fz={{ base: 36, sm: 40, md: 48 }} ta="center">Logs</Title>
                        <Divider />
                    </Stack>
                </Container>
            </Center>
        </>
    );
}

export default LogPage;
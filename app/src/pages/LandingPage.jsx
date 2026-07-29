import { Center, Stack, Title, Box, Button, Text } from '@mantine/core';
import { Link } from 'react-router'

function LandingPage() {
    return (
        <>
            <Center h="calc(100vh - 60px)">
                <Stack align="center">
                    <Title order={1} fz={{ base: 36, sm: 64 }}>Détection des Anomalies</Title>
                    <Text c="dimmed" size="lg">Trouver les anomalies plus facilement dans le logs de Windows Server à l'aide de l'intelligence artificielle</Text>
                    <Link to="/logs">
                        <Box mt="lg">
                            <Button size="lg">Commencer</Button>
                        </Box>
                    </Link>
                </Stack>
            </Center>
        </>
    );
}

export default LandingPage;
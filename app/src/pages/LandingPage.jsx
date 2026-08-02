import {
    Button,
    Center,
    Container,
    Group,
    Paper,
    Stack,
    Text,
    ThemeIcon,
    Title,
} from "@mantine/core";
import { Link } from "react-router";
import { IconBrain, IconChartHistogram, IconShieldLock, IconSparkles } from "@tabler/icons-react";

function LandingPage() {
    return (
        <Center h="calc(100vh - 60px)">
            <Container size="md">
                <Stack align="center" gap="xl">
                    <Title order={1} ta="center" fz={{ base: 42, sm: 70 }}>
                        Anomalyseur
                    </Title>

                    <Text c="dimmed" size="xl" ta="center" maw={700}>
                        Détectez automatiquement les activités suspectes dans les
                        journaux Windows Server grâce au machine learning.
                        Analysez vos logs, visualisez les anomalies et ajustez la
                        frontière de décision en quelques clics.
                    </Text>

                    <Group mt="md">
                        <Link to="/logs">
                            <Button size="lg" color="gold">
                                Commencer
                            </Button>
                        </Link>
                        <Link to="/about">
                            <Button size="lg" variant="dark">
                                En savoir plus
                            </Button>
                        </Link>
                    </Group>

                    <Group mt={50} justify="center" gap="xl" w={1000}>
                        <Paper p="lg" radius="md" withBorder w={220}>
                            <Stack align="center" gap="sm">
                                <ThemeIcon size={50} radius="xl" color="pink">
                                    <IconBrain size={28} />
                                </ThemeIcon>

                                <Text fw={700}>
                                    Machine Learning
                                </Text>

                                <Text c="dimmed" size="sm" ta="center">
                                    Détection intelligente des comportements
                                    inhabituels dans le logs.
                                </Text>
                            </Stack>
                        </Paper>

                        <Paper p="lg" radius="md" withBorder w={220}>
                            <Stack align="center" gap="sm">
                                <ThemeIcon size={50} radius="xl" color="gold">
                                    <IconChartHistogram size={28} />
                                </ThemeIcon>

                                <Text fw={700}>
                                    Visualisation
                                </Text>

                                <Text c="dimmed" size="sm" ta="center">
                                    Histogrammes, scores d'anomalie et frontière de décision.
                                </Text>
                            </Stack>
                        </Paper>

                        <Paper p="lg" radius="md" withBorder w={220}>
                            <Stack align="center" gap="sm">
                                <ThemeIcon size={50} radius="xl" color="green">
                                    <IconShieldLock size={28} />
                                </ThemeIcon>

                                <Text fw={700}>
                                    Windows Server
                                </Text>

                                <Text c="dimmed" size="sm" ta="center">
                                    Compatible avec les journaux Security, System et Application.
                                </Text>
                            </Stack>
                        </Paper>

                        <Paper p="lg" radius="md" withBorder w={220}>
                            <Stack align="center" gap="sm">
                                <ThemeIcon size={50} radius="xl" color="violet">
                                    <IconSparkles size={28} />
                                </ThemeIcon>

                                <Text fw={700}>
                                    Explication par IA
                                </Text>

                                <Text c="dimmed" size="sm" ta="center">
                                    Obtenez une explication claire des anomalies, facilitant leur interprétation.
                                </Text>
                            </Stack>
                        </Paper>
                    </Group>
                </Stack>
            </Container>
        </Center>
    );
}

export default LandingPage;
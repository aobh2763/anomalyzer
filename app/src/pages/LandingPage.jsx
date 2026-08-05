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
import {
  IconBrain,
  IconChartHistogram,
  IconShieldLock,
  IconSparkles,
} from "@tabler/icons-react";
import { useTranslation } from "react-i18next";

function LandingPage() {
  const { t } = useTranslation();

  return (
    <Center h="calc(100vh - 60px)">
      <Container size="md">
        <Stack align="center" gap="xl">
          <Title
            order={1}
            ta="center"
            fz={{
              base: 42,
              sm: 70,
            }}
          >
            {t("anomalyzer")}
          </Title>

          <Text c="dimmed" size="xl" ta="center" maw={700}>
            {t("detectSuspiciousActivities")}
          </Text>

          <Group mt="md">
            <Link to="/logs">
              <Button size="lg" color="gold">
                {t("start")}
              </Button>
            </Link>
            <Link to="/about">
              <Button size="lg" variant="dark">
                {t("learnMore")}
              </Button>
            </Link>
          </Group>

          <Group mt={50} justify="center" gap="xl" w={1000}>
            <Paper p="lg" radius="md" withBorder w={220}>
              <Stack align="center" gap="sm">
                <ThemeIcon size={50} radius="xl" color="pink">
                  <IconBrain size={28} />
                </ThemeIcon>

                <Text fw={700}>{t("machineLearning")}</Text>

                <Text c="dimmed" size="sm" ta="center">
                  {t("intelligentDetection")}
                </Text>
              </Stack>
            </Paper>

            <Paper p="lg" radius="md" withBorder w={220}>
              <Stack align="center" gap="sm">
                <ThemeIcon size={50} radius="xl" color="gold">
                  <IconChartHistogram size={28} />
                </ThemeIcon>

                <Text fw={700}>{t("visualization")}</Text>

                <Text c="dimmed" size="sm" ta="center">
                  {t("histogramsAndScores")}
                </Text>
              </Stack>
            </Paper>

            <Paper p="lg" radius="md" withBorder w={220}>
              <Stack align="center" gap="sm">
                <ThemeIcon size={50} radius="xl" color="green">
                  <IconShieldLock size={28} />
                </ThemeIcon>

                <Text fw={700}>{t("windowsServer")}</Text>

                <Text c="dimmed" size="sm" ta="center">
                  {t("compatibleWithLogs")}
                </Text>
              </Stack>
            </Paper>

            <Paper p="lg" radius="md" withBorder w={220}>
              <Stack align="center" gap="sm">
                <ThemeIcon size={50} radius="xl" color="violet">
                  <IconSparkles size={28} />
                </ThemeIcon>

                <Text fw={700}>{t("aiExplanation")}</Text>

                <Text c="dimmed" size="sm" ta="center">
                  {t("clearExplanation")}
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

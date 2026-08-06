import { useEffect, useState } from "react";
import { Title, Stack, Container, Divider, Group } from "@mantine/core";
import LogPaper from "../components/logs/LogPaper";
import { logsApi } from "../api/logs";
import AddLogForm from "../components/logs/AddLogForm";
import { useTranslation } from "react-i18next";

function LogPage() {
  const { t } = useTranslation();
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    async function fetchLogs() {
      try {
        const data = await logsApi.getLogs();
        setLogs(data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchLogs();
  }, []);

  return (
    <>
      <Container size="xl" py="sm" pt={85}>
        <Stack gap="xl" justify="flex-start">
          <Title
            order={1}
            fz={{
              base: 36,
              sm: 40,
              md: 48,
            }}
            ta="center"
          >
            {t("logs")}
          </Title>

          <Divider color="gold" />

          <AddLogForm />

          <Divider color="gold" />

          <Group gap="md" justify="center" pt="md" pb="xl">
            {logs.map((log) => (
              <LogPaper key={log.log_id} log={log} />
            ))}
          </Group>
        </Stack>
      </Container>
    </>
  );
}

export default LogPage;

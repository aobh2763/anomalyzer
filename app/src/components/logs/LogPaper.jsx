import { Paper, Group, Text, Button, List, ThemeIcon, Divider } from "@mantine/core";
import LogTypeBadge from "./LogTypeBadge";
import { FaCaretRight } from "react-icons/fa";
import { logsApi } from '../../api/logs';
import { useNavigate } from "react-router";
import { useTranslation } from 'react-i18next';

function LogPaper({
  log
}) {
  const { t } = useTranslation();

  const navigate = useNavigate();
  const date = new Date(log.uploaded_at);

  const handleEvaluate = async () => {
    navigate("/evaluation");
  };

  const handleDelete = async () => {
    if (!confirm(t("confirmDelete", { name: log.name }))) return;

    try {
      await logsApi.deleteLog(log.log_id);
      window.location.reload();
    } catch (err) {
      console.error(err);
    }
  };

  return <>
    <Paper shadow="sm" withBorder p="lg" w={380}>
      <Group justify="space-between">
        <Text fw={700} size="xl">{log.name}</Text>
        <LogTypeBadge type={log.log_type} />
      </Group>

      <Divider mt="sm" mb="sm" />

      <List spacing="xs" size="sm" center icon={<ThemeIcon color="gold" size={24} radius="xl">
        <FaCaretRight size={16} />
      </ThemeIcon>}>
        <List.Item><b>{t('id')}</b> {log.log_id}</List.Item>
        <List.Item><b>{t('addedOn')}</b> {date.toLocaleString("fr-FR")}</List.Item>
        <List.Item>{t('containsRawEventCount', {
          raw_event_count: log.raw_event_count
        })}</List.Item>
      </List>

      <Divider mt="sm" mb="sm" />

      <Button color="gold" fullWidth mt="md" onClick={handleEvaluate}>
        {t('evaluateLog')}
      </Button>
      <Button color="pink" fullWidth mt="md" onClick={handleDelete}>
        {t('deleteLog')}
      </Button>
    </Paper>
  </>;
}

export default LogPaper;

import { Stack, Text, Select, Button } from "@mantine/core";
import { useTranslation } from "react-i18next";

function LogSelectionStep({
  logOptions,
  selectedLog,
  setSelectedLog,
  loading,
  extracted,
  onExtract,
}) {
  const { t } = useTranslation();

  return (
    <Stack gap="md" align="center">
      <Text c="dimmed" size="lg" ta="center">
        {t("chooseLoadedLog")}
      </Text>

      <Select
        w={600}
        label={t("availableLogs")}
        withAsterisk
        placeholder={t("chooseLog")}
        data={logOptions}
        value={selectedLog}
        onChange={setSelectedLog}
        loading={loading}
        disabled={extracted}
      />

      <Button
        w={400}
        color="gold"
        loading={loading}
        disabled={!selectedLog || extracted}
        onClick={onExtract}
      >
        {t("extractFeatures")}
      </Button>
    </Stack>
  );
}

export default LogSelectionStep;

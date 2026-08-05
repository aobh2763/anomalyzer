import { Stack, Text, Select, Button } from "@mantine/core";
import { useTranslation } from "react-i18next";

function ModelSelectionStep({
  modelOptions,
  selectedModel,
  setSelectedModel,
  loading,
  modelValidated,
  modelError,
  onSelectModel,
  onChangeModel,
}) {
  const { t } = useTranslation();

  return (
    <Stack gap="md" align="center">
      <Text c="dimmed" size="lg" ta="center">
        {t("chooseCompatibleModel")}
      </Text>

      <Select
        w={600}
        label={t("availableModels")}
        withAsterisk
        placeholder={t("chooseModel")}
        data={modelOptions}
        value={selectedModel}
        loading={loading}
        error={modelError}
        onChange={(value) => {
          setSelectedModel(value);
          onChangeModel();
        }}
      />

      <Button
        w={400}
        color="gold"
        loading={loading}
        disabled={!selectedModel || modelValidated}
        onClick={onSelectModel}
      >
        {t("selectModel")}
      </Button>
    </Stack>
  );
}

export default ModelSelectionStep;

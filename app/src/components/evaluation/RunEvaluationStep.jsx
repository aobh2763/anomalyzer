import { Stack, Text, Button } from "@mantine/core";
import { useTranslation } from "react-i18next";

function RunEvaluationStep({ loading, onEvaluate }) {
  const { t } = useTranslation();

  return (
    <Stack gap="md" align="center">
      <Text c="green" size="lg">
        {t("compatibleModel")}
      </Text>

      <Text c="dimmed" ta="center">
        {t("firstEvaluationTakesTime")}
      </Text>

      <Button w={400} color="gold" loading={loading} onClick={onEvaluate}>
        {t("startEvaluation")}
      </Button>
    </Stack>
  );
}

export default RunEvaluationStep;

import { Stack, Title, Text, Divider } from "@mantine/core";
import AnomalyStatistics from "./AnomalyStatistics";
import AnomaliesTable from "./AnomaliesTable";
import { useTranslation } from "react-i18next";

function AnomaliesSection({
  anomalies,
  evaluationId,
  logName,
  logType,
  modelName,
  decisionBoundary,
  imageUrl,
}) {
  const { t } = useTranslation();

  return (
    <Stack gap="md" align="center">
      <Title
        order={2}
        ta="center"
        fz={{
          base: 28,
          sm: 32,
          md: 40,
        }}
      >
        {t("detectedAnomaliesLength", {
          length: anomalies.length,
        })}
      </Title>

      {anomalies.length === 0 ? (
        <Text c="dimmed" ta="center">
          {t("noAnomalyDetected")}
        </Text>
      ) : (
        <>
          <AnomalyStatistics anomalies={anomalies} logType={logType} />
          <Divider mt="lg" />
          <AnomaliesTable
            anomalies={anomalies}
            logType={logType}
            evaluationId={evaluationId}
            logName={logName}
            modelName={modelName}
            decisionBoundary={decisionBoundary}
            imageUrl={imageUrl}
          />
        </>
      )}
    </Stack>
  );
}

export default AnomaliesSection;

import { useState } from "react";
import {
  Container,
  Stepper,
  Title,
  Stack,
  Group,
  Button,
  Paper,
  Divider
} from "@mantine/core";
import { useEvaluationFlow } from "../hooks/useEvaluationFlow";
import FeaturesTable from "../components/evaluation/FeaturesTable";
import LogSelectionStep from "../components/evaluation/LogSelectionStep";
import ModelSelectionStep from "../components/evaluation/ModelSelectionStep";
import RunEvaluationStep from "../components/evaluation/RunEvaluationStep";
import EvaluationResultsStep from "../components/evaluation/EvaluationResultsStep";
import AnomaliesSection from "../components/evaluation/AnomaliesSection";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";

function EvaluationPage() {
  const { t } = useTranslation();

  const location = useLocation();
  const incomingLogId = location.state?.logId ?? null;

  const flow = useEvaluationFlow(incomingLogId);

  const selectedLogObj = flow.logs.find(
    (log) => String(log.log_id) === flow.selectedLog,
  );

  const selectedModelObj = flow.models.find(
    (model) => String(model.model_id) === flow.selectedModel,
  );

  const logOptions = flow.logs.map((log) => ({
    value: String(log.log_id),
    label: t("nameLogType", {
      name: log.name,
      log_type: log.log_type,
    }),
  }));

  const modelOptions = flow.models
    .filter((model) => !model.deprecated)
    .map((model) => ({
      value: String(model.model_id),
      label: t("filenameLogType", {
        filename: model.filename,
        log_type: model.log_type,
      }),
    }));

  // Derive the current step from existing flow state — no new state needed.
  // 0: Log Selection · 1: Model Selection + Run Evaluation (merged) · 2: Results · 3: Anomalies
  const highestCompleted = flow.boundarySet
    ? 3
    : flow.evaluationRun
      ? 2
      : flow.extracted
        ? 1
        : 0;

  const [active, setActive] = useState(0);

  // Adjust state during render (React's recommended alternative to an Effect here):
  // if flow state was reset behind us (e.g. changing the model clears later steps),
  // pull the visible step back to whatever is still reachable. We never jump forward
  // automatically — moving to a newly-unlocked step is done via the Next button below,
  // so finishing a step doesn't whisk the user away before they can see its result.
  if (active > highestCompleted) {
    setActive(highestCompleted);
  }

  const handleStepClick = (step) => {
    // Only allow navigating to steps that have already been reached.
    if (step <= highestCompleted) {
      setActive(step);
    }
  };

  const goNext = () => setActive((step) => Math.min(step + 1, 3));

  return (
    <Container size="xl" py="sm" pt={85}>
      <Stack gap="xl">
        <Title
          order={1}
          ta="center"
          fz={{
            base: 36,
            sm: 40,
            md: 48,
          }}
        >
          {t("evaluation")}
        </Title>

        <Divider color="gold" />

        <Paper
          radius="lg"
          shadow="md"
          p="md"
          style={{ background: "var(--mantine-color-pink-light)" }}
        >
          <Stepper active={active} onStepClick={handleStepClick} color="gold">
            <Stepper.Step
              label={t("logSelection")}
              description={t("logSelectionDescription")}
            />
            <Stepper.Step
              label={t("modelSelection")}
              description={t("modelSelectionDescription")}
            />
            <Stepper.Step
              label={t("results")}
              description={t("resultsDescription")} />
            <Stepper.Step
              label={t("anomalies")}
              description={t("anomaliesDescription")} />
          </Stepper>
        </Paper>

        <Paper radius="lg" shadow="sm" p="xl" style={{
          background: "var(--mantine-color-default-hover)",
        }}>
          {active === 0 && (
            <Stack gap="lg">
              <LogSelectionStep
                logOptions={logOptions}
                selectedLog={flow.selectedLog}
                setSelectedLog={flow.setSelectedLog}
                loading={flow.loading}
                extracted={flow.extracted}
                onExtract={flow.handleFeature}
              />

              {flow.featuresData.length > 0 && (
                <FeaturesTable
                  featuresData={flow.featuresData}
                  logType={flow.selectedLogType}
                  logName={selectedLogObj?.name}
                />
              )}

              <Group justify="flex-end">
                <Button onClick={goNext} disabled={highestCompleted < 1}>
                  {t("nextStep")}
                </Button>
              </Group>
            </Stack>
          )}

          {active === 1 && (
            <Stack gap="lg">
              <ModelSelectionStep
                modelOptions={modelOptions}
                selectedModel={flow.selectedModel}
                setSelectedModel={flow.setSelectedModel}
                loading={flow.loading}
                modelValidated={flow.modelValidated}
                modelError={flow.modelError}
                onSelectModel={flow.handleModel}
                onChangeModel={() => {
                  flow.setModelValidated(false);
                  flow.setModelError("");
                  flow.setEvaluationRun(false);
                }}
              />

              {flow.modelValidated && (
                <>
                  <Divider color="gold" />

                  <RunEvaluationStep
                    loading={flow.loading}
                    onEvaluate={flow.handleEvaluate}
                  />
                </>
              )}

              <Group justify="flex-end">
                <Button onClick={goNext} disabled={highestCompleted < 2}>
                  {t("nextStep")}
                </Button>
              </Group>
            </Stack>
          )}

          {active === 2 && (
            <Stack gap="lg">
              <EvaluationResultsStep
                imageUrl={flow.imageUrl}
                decisionBoundary={flow.decisionBoundary}
                setDecisionBoundary={flow.setDecisionBoundary}
                boundaryError={flow.boundaryError}
                setBoundaryError={flow.setBoundaryError}
                loading={flow.loading}
                onUpdateBoundary={flow.handleDecisionBoundary}
              />

              <Group justify="flex-end">
                <Button onClick={goNext} disabled={highestCompleted < 3}>
                  {t("nextStep")}
                </Button>
              </Group>
            </Stack>
          )}

          {active === 3 && (
            <Stack gap="lg">
              <AnomaliesSection
                anomalies={flow.anomalies}
                logType={flow.selectedLogType}
                evaluationId={flow.selectedEvaluation}
                logName={selectedLogObj?.name}
                modelName={selectedModelObj?.filename}
                decisionBoundary={flow.decisionBoundary}
                imageUrl={flow.imageUrl}
              />
            </Stack>
          )}
        </Paper>
      </Stack>
    </Container>
  );
}

export default EvaluationPage;
import { Container, Divider, Title, Stack } from "@mantine/core";

import { useEvaluationFlow } from "../hooks/useEvaluationFlow";

import FeaturesTable from "../components/evaluation/FeaturesTable";
import LogSelectionStep from "../components/evaluation/LogSelectionStep";
import ModelSelectionStep from "../components/evaluation/ModelSelectionStep";
import RunEvaluationStep from "../components/evaluation/RunEvaluationStep";
import EvaluationResultsStep from "../components/evaluation/EvaluationResultsStep";
import AnomaliesSection from "../components/evaluation/AnomaliesSection";

function EvaluationPage() {
    const flow = useEvaluationFlow();

    const logOptions = flow.logs.map((log) => ({
        value: String(log.log_id),
        label: `${log.name} (${log.log_type})`,
    }));

    const modelOptions = flow.models
        .filter((model) => !model.deprecated)
        .map((model) => ({
            value: String(model.model_id),
            label: `${model.filename} (${model.log_type})`,
        }));

    return (
        <Container size="xl" py="sm" pt={85}>
            <Stack gap="xl">
                <Title order={1} ta="center" fz={{ base: 36, sm: 40, md: 48 }}>
                    Evaluation
                </Title>

                <Divider />

                <LogSelectionStep
                    logOptions={logOptions}
                    selectedLog={flow.selectedLog}
                    setSelectedLog={flow.setSelectedLog}
                    loading={flow.loading}
                    extracted={flow.extracted}
                    onExtract={flow.handleFeature}
                />

                {flow.featuresData.length > 0 && (
                    <>
                        <Divider />

                        <Title order={2} ta="center" fz={{ base: 28, sm: 32, md: 40 }}>
                            Caractéristiques
                        </Title>

                        <FeaturesTable featuresData={flow.featuresData} />
                    </>
                )}

                {flow.extracted && (
                    <>
                        <Divider />
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
                    </>
                )}

                {flow.modelValidated && (
                    <>
                        <Divider />
                        <RunEvaluationStep
                            loading={flow.loading}
                            onEvaluate={flow.handleEvaluate}
                        />
                    </>
                )}

                {flow.evaluationRun && (
                    <>
                        <Divider />
                        <EvaluationResultsStep
                            imageUrl={flow.imageUrl}
                            decisionBoundary={flow.decisionBoundary}
                            setDecisionBoundary={flow.setDecisionBoundary}
                            boundaryError={flow.boundaryError}
                            setBoundaryError={flow.setBoundaryError}
                            loading={flow.loading}
                            onUpdateBoundary={flow.handleDecisionBoundary}
                        />
                    </>
                )}

                {flow.boundarySet && (
                    <>
                        <Divider />
                        <AnomaliesSection
                            anomalies={flow.anomalies}
                            logType={flow.selectedLogType}
                        />
                    </>
                )}
            </Stack>
        </Container>
    );
}

export default EvaluationPage;
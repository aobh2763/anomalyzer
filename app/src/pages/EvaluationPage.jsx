import {
    Container,
    Divider,
    Title,
    Stack,
    Select,
    Button,
    Text,
    Image,
    NumberInput,
} from "@mantine/core";
import { useEffect, useState } from "react";
import Papa from "papaparse";

import { logsApi } from "../api/logs";
import { modelsApi } from "../api/models";
import { featuresApi } from "../api/features";
import { evaluationsApi } from "../api/evaluations";

import FeaturesTable from "../components/FeaturesTable";
import AnomaliesTable from "../components/AnomaliesTable";
import AnomalyStatistics from "../components/AnomalyStatistics";

function EvaluationPage() {
    const [logs, setLogs] = useState([]);
    const [models, setModels] = useState([]);

    const [loading, setLoading] = useState(false);

    const [selectedLog, setSelectedLog] = useState(null);
    const [selectedModel, setSelectedModel] = useState(null);
    const [selectedEvaluation, setSelectedEvaluation] = useState(null);

    const [featuresData, setFeaturesData] = useState([]);

    const [extracted, setExtracted] = useState(false);
    const [modelValidated, setModelValidated] = useState(false);

    const [modelError, setModelError] = useState("");
    const [boundaryError, setBoundaryError] = useState("");

    const [evaluationRun, setEvaluationRun] = useState(false);

    const [decisionBoundary, setDecisionBoundary] = useState(null);

    const [imageUrl, setImageUrl] = useState(null);

    const [anomalies, setAnomalies] = useState([]);
    const [boundarySet, setBoundarySet] = useState(false);

    const logOptions = logs.map((log) => ({
        value: String(log.log_id),
        label: `${log.name} (${log.log_type})`,
    }));

    const selectedLogType = logs.find(
        (log) => String(log.log_id) === selectedLog
    )?.log_type;

    const modelOptions = models
        .filter((model) => !model.deprecated)
        .map((model) => ({
            value: String(model.model_id),
            label: `${model.filename} (${model.log_type})`,
        }));

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

    useEffect(() => {
        async function fetchModels() {
            try {
                const data = await modelsApi.getModels();
                setModels(data);
            } catch (err) {
                console.error(err);
            }
        }

        fetchModels();
    }, []);

    useEffect(() => {
        return () => {
            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }
        };
    }, [imageUrl]);

    const transformFeatures = (data) => {
        const cyclicFeatures = [
            "minute",
            "hour",
            "day",
            "second",
            "month",
        ];

        return data.map((row) => {
            const transformed = { ...row };

            cyclicFeatures.forEach((feature) => {
                const sin = `${feature}_sin`;
                const cos = `${feature}_cos`;

                if (sin in row && cos in row) {
                    transformed[feature] = [
                        Number(row[sin].toFixed(4)),
                        Number(row[cos].toFixed(4)),
                    ];

                    delete transformed[sin];
                    delete transformed[cos];
                }
            });

            Object.keys(transformed).forEach((key) => {
                if (typeof transformed[key] === "number") {
                    transformed[key] = Number(
                        transformed[key].toFixed(3)
                    );
                }
            });

            return transformed;
        });
    };

    const handleFeature = async () => {
        if (!selectedLog) return;

        setLoading(true);

        try {
            const log = logs.find(
                (log) => String(log.log_id) === selectedLog
            );

            try {
                await featuresApi.getFeatures(log.log_id);
            } catch {
                await featuresApi.extractFeatures(log.log_id);
            }

            const blob = await featuresApi.downloadFeatures(
                selectedLog
            );

            const text = await blob.text();

            const { data } = Papa.parse(text, {
                header: true,
                skipEmptyLines: true,
                dynamicTyping: true,
            });

            const cleanedData = data.map(
                // eslint-disable-next-line no-unused-vars
                ({ "": _, ...row }) => row
            );

            setFeaturesData(
                transformFeatures(cleanedData)
            );

            setExtracted(true);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleModel = () => {
        if (!selectedModel) return;

        setLoading(true);

        const log = logs.find(
            (log) => String(log.log_id) === selectedLog
        );

        const model = models.find(
            (model) => String(model.model_id) === selectedModel
        );

        if (!log || !model) {
            setLoading(false);
            return;
        }

        if (log.log_type !== model.log_type) {
            setModelValidated(false);

            setModelError(
                `Modèle incompatible : le log est "${log.log_type}" mais le modèle attend "${model.log_type}".`
            );

            setLoading(false);
            return;
        }

        setModelError("");
        setModelValidated(true);

        setLoading(false);
    };

    const handleEvaluate = async () => {
        if (!selectedLog || !selectedModel) {
            return;
        }

        setLoading(true);

        try {
            let evaluation;

            try {
                evaluation =
                    await evaluationsApi.getEvaluationByLogAndModel(
                        selectedLog,
                        selectedModel
                    );
            } catch {
                evaluation =
                    await evaluationsApi.evaluateLog(
                        selectedLog,
                        selectedModel
                    );
            }

            const evaluationId = evaluation.evaluation_id;

            setSelectedEvaluation(evaluationId);

            const blob =
                await evaluationsApi.getEvaluationImage(
                    evaluationId
                );

            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }

            const url = URL.createObjectURL(blob);

            setImageUrl(url);

            setEvaluationRun(true);

            setAnomalies([]);
            setBoundarySet(false);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDecisionBoundary = async () => {
        if (!selectedEvaluation) {
            return;
        }

        if (
            decisionBoundary === null ||
            decisionBoundary === ""
        ) {
            setBoundaryError("Obligatoire");
            return;
        }

        setLoading(true);

        try {
            await evaluationsApi.setDecisionBoundary(
                selectedEvaluation,
                decisionBoundary
            );

            const blob =
                await evaluationsApi.getEvaluationImage(
                    selectedEvaluation
                );

            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }

            const url = URL.createObjectURL(blob);

            setImageUrl(url);

            const anomaliesData =
                await evaluationsApi.getAnomalies(
                    selectedEvaluation
                );

            setAnomalies(anomaliesData);
            setBoundarySet(true);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container size="xl" py="sm" pt={85}>
            <Stack gap="xl">

                <Title
                    order={1}
                    ta="center"
                    fz={{ base: 36, sm: 40, md: 48 }}
                >
                    Evaluation
                </Title>

                <Divider />

                {/* STEP 1 */}
                <Stack gap="md" align="center">

                    <Text
                        c="dimmed"
                        size="lg"
                        ta="center"
                    >
                        Choisir un log chargé pour extraire ses caractéristiques.
                    </Text>

                    <Select
                        w={600}
                        label="Logs disponibles"
                        withAsterisk
                        placeholder="Choisir un log"
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
                        onClick={handleFeature}
                    >
                        Extraire les caractéristiques
                    </Button>

                </Stack>

                {/* FEATURES */}
                {featuresData.length > 0 && (
                    <>
                        <Divider />

                        <Title
                            order={2}
                            ta="center"
                            fz={{ base: 28, sm: 32, md: 40 }}
                        >
                            Caractéristiques
                        </Title>

                        <FeaturesTable
                            featuresData={featuresData}
                        />
                    </>
                )}

                {/* STEP 2 */}
                {extracted && (
                    <>
                        <Divider />

                        <Stack gap="md" align="center">

                            <Text
                                c="dimmed"
                                size="lg"
                                ta="center"
                            >
                                Choisir un modèle compatible avec ce log.
                            </Text>

                            <Select
                                w={600}
                                label="Modèles disponibles"
                                withAsterisk
                                placeholder="Choisir un modèle"
                                data={modelOptions}
                                value={selectedModel}
                                loading={loading}
                                error={modelError}
                                onChange={(value) => {
                                    setSelectedModel(value);
                                    setModelValidated(false);
                                    setModelError("");
                                    setEvaluationRun(false);
                                }}
                            />

                            <Button
                                w={400}
                                color="gold"
                                loading={loading}
                                disabled={!selectedModel || modelValidated}
                                onClick={handleModel}
                            >
                                Sélectionner le modèle
                            </Button>

                        </Stack>
                    </>
                )}

                {/* STEP 3 */}
                {modelValidated && (
                    <>
                        <Divider />

                        <Stack gap="md" align="center">

                            <Text
                                c="green"
                                size="lg"
                            >
                                Modèle compatible
                            </Text>

                            <Text
                                c="dimmed"
                                ta="center"
                            >
                                Une première évaluation peut prendre quelques instants.
                            </Text>

                            <Button
                                w={400}
                                color="gold"
                                loading={loading}
                                onClick={handleEvaluate}
                            >
                                Lancer l'évaluation
                            </Button>

                        </Stack>
                    </>
                )}

                {/* STEP 4 */}
                {evaluationRun && (
                    <>
                        <Divider />

                        <Stack gap="lg" align="center">

                            <Title
                                order={2}
                                ta="center"
                                fz={{ base: 28, sm: 32, md: 40 }}
                            >
                                Résultats
                            </Title>

                            <Image
                                src={imageUrl}
                                radius="md"
                                w={1000}
                            />

                            <Text
                                c="dimmed"
                                ta="center"
                            >
                                Modifier la frontière de décision afin de contrôler
                                quelles observations sont considérées comme
                                anormales.
                            </Text>

                            <NumberInput
                                w={600}
                                label="Frontière de décision"
                                placeholder="-0.05"
                                value={decisionBoundary}
                                onChange={(value) => {
                                    setDecisionBoundary(value);
                                    setBoundaryError("");
                                }}
                                error={boundaryError}
                                min={-1}
                                max={1}
                                step={0.01}
                                decimalScale={3}
                            />

                            <Button
                                w={400}
                                color="gold"
                                loading={loading}
                                onClick={handleDecisionBoundary}
                            >
                                Mettre à jour
                            </Button>

                        </Stack>
                    </>
                )}

                {/* STEP 5: ANOMALIES */}
                {boundarySet && (
                    <>
                        <Divider />

                        <Stack gap="md" align="center">

                            <Title
                                order={2}
                                ta="center"
                                fz={{ base: 28, sm: 32, md: 40 }}
                            >
                                Anomalies détectées ({anomalies.length})
                            </Title>

                            {anomalies.length === 0 ? (
                                <Text c="dimmed" ta="center">
                                    Aucune anomalie détectée avec cette frontière de
                                    décision.
                                </Text>
                            ) : (
                                <>
                                    <AnomalyStatistics anomalies={anomalies} logType={selectedLogType} />

                                    <Divider mt="lg" />

                                    <AnomaliesTable anomalies={anomalies} />
                                </>
                            )}

                        </Stack>
                    </>
                )}

            </Stack>
        </Container>
    );
}

export default EvaluationPage;
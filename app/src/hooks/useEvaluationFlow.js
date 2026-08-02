import { useEffect, useState } from "react";
import Papa from "papaparse";

import { logsApi } from "../api/logs";
import { modelsApi } from "../api/models";
import { featuresApi } from "../api/features";
import { evaluationsApi } from "../api/evaluations";
import { anomaliesApi } from "../api/anomalies";
import { transformFeatures } from "../helpers/featuresTransform";



export function useEvaluationFlow() {
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

    const selectedLogType = logs.find(
        (log) => String(log.log_id) === selectedLog
    )?.log_type;

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

            const blob = await featuresApi.downloadFeatures(selectedLog);
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

            setFeaturesData(transformFeatures(cleanedData));
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

        const log = logs.find((log) => String(log.log_id) === selectedLog);
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
        if (!selectedLog || !selectedModel) return;

        setLoading(true);

        try {
            let evaluation;

            try {
                evaluation = await evaluationsApi.getEvaluationByLogAndModel(
                    selectedLog,
                    selectedModel
                );
            } catch {
                evaluation = await evaluationsApi.evaluateLog(
                    selectedLog,
                    selectedModel
                );
            }

            const evaluationId = evaluation.evaluation_id;
            setSelectedEvaluation(evaluationId);

            const blob = await evaluationsApi.getEvaluationImage(evaluationId);

            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }

            setImageUrl(URL.createObjectURL(blob));
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
        if (!selectedEvaluation) return;

        if (decisionBoundary === null || decisionBoundary === "") {
            setBoundaryError("Obligatoire");
            return;
        }

        setLoading(true);

        try {
            await evaluationsApi.setDecisionBoundary(
                selectedEvaluation,
                decisionBoundary
            );

            const blob = await evaluationsApi.getEvaluationImage(
                selectedEvaluation
            );

            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }

            setImageUrl(URL.createObjectURL(blob));

            const anomaliesData = await anomaliesApi.getAnomalies(
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

    return {
        // data
        logs,
        models,
        featuresData,
        anomalies,
        imageUrl,
        selectedLogType,
        selectedEvaluation,

        // selection state
        selectedLog,
        setSelectedLog,
        selectedModel,
        setSelectedModel,

        // flow state
        loading,
        extracted,
        modelValidated,
        evaluationRun,
        boundarySet,
        modelError,
        boundaryError,

        // decision boundary
        decisionBoundary,
        setDecisionBoundary,
        setBoundaryError,

        // handlers
        handleFeature,
        handleModel,
        handleEvaluate,
        handleDecisionBoundary,
        setModelValidated,
        setModelError,
        setEvaluationRun,
    };
}

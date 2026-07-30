import { useState } from 'react';
import { Text, Center, Stack, Select, TextInput, NumberInput, Button } from '@mantine/core';
import { modelsApi } from '../api/models';

const LOG_TYPES = [
    { value: 'security', label: 'Sécurité' },
    { value: 'system', label: 'Système' },
    { value: 'application', label: 'Application' },
];

function AddModelForm() {
    const [logType, setLogType] = useState(null);
    const [filename, setFilename] = useState('');
    const [nEstimators, setNEstimators] = useState('');
    const [maxSamples, setMaxSamples] = useState('');
    const [maxFeatures, setMaxFeatures] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAddModel = async () => {
        if (!logType) {
            setError("Veuillez sélectionner un type de log.");
            return;
        }

        if (!filename.trim()) {
            setError("Veuillez indiquer le nom du fichier du modèle.");
            return;
        }

        setError(null);
        setLoading(true);

        try {
            await modelsApi.addModel({
                logType,
                filename: filename.trim(),
                nEstimators: nEstimators === '' ? null : nEstimators,
                maxSamples: maxSamples === '' ? null : maxSamples,
                maxFeatures: maxFeatures === '' ? null : maxFeatures,
            });

            setLogType(null);
            setFilename('');
            setNEstimators('');
            setMaxSamples('');
            setMaxFeatures('');

            window.location.reload();
        } catch (err) {
            setError("Échec de l'ajout du modèle.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Stack gap="md" align="center">
            <Text c="dimmed" size="lg" ta="center">
                Enregistrer un modèle déjà entraîné pour un type de log donné. Le modèle doit se trouver déja côté serveur, sous l'extension .joblib.
            </Text>

            <Select
                w={600}
                label="Type de log"
                withAsterisk
                placeholder="Choisir un type de log"
                data={LOG_TYPES}
                value={logType}
                onChange={setLogType}
            />

            <TextInput
                w={600}
                label="Nom du fichier"
                withAsterisk
                description="Nom du fichier du modèle entraîné, stocké côté serveur."
                placeholder="ex: security_iforest_v1.joblib"
                value={filename}
                onChange={(event) => setFilename(event.currentTarget.value)}
            />

            <NumberInput
                w={600}
                label="n_estimators"
                description="Optionnel"
                placeholder="ex: 100"
                value={nEstimators}
                onChange={setNEstimators}
                min={1}
            />

            <NumberInput
                w={600}
                label="max_samples"
                description="Optionnel"
                placeholder="ex: 256"
                value={maxSamples}
                onChange={setMaxSamples}
                min={1}
            />

            <NumberInput
                w={600}
                label="max_features"
                description="Optionnel"
                placeholder="ex: 1"
                value={maxFeatures}
                onChange={setMaxFeatures}
                min={1}
            />

            {error && (
                <Text c="red" size="sm">{error}</Text>
            )}

            <Center>
                <Button color="gold" w={400} onClick={handleAddModel} disabled={loading}>
                    Ajouter Modèle
                </Button>
            </Center>
        </Stack>
    );
}

export default AddModelForm;
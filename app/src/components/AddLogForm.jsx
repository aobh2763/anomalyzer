import { Stack, Text, FileInput, Button } from "@mantine/core";
import { useState } from "react";
import { logsApi } from "../api/logs";

function AddLogForm() {
    const [file, setFile] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (selectedFile) => {
        setFile(selectedFile);
        setError(null);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Veuillez sélectionner un fichier.");
            return;
        }

        if (!file.name.toLowerCase().endsWith('.evtx')) {
            setError("Veuillez charger un fichier .evtx");
            return;
        }

        setError(null);

        setLoading(true);

        try {
            await logsApi.uploadLog(file);
            window.location.reload();
        } catch (err) {
            console.error(err);
        }

    };

    return (
        <Stack gap="md" align="center">
            <Text c="dimmed" size="lg" ta="center" mb="md">Charger un fichier .evtx et passer à l'onglet "Evaluation" pour l'évaluer.</Text>
            <FileInput
                w={600}
                label="Ajouter Log"
                withAsterisk
                description="Charger un fichier .evtx contenant des logs Système, Application ou Sécurité."
                error={error}
                placeholder="..."
                value={file}
                onChange={handleFileChange}
            />
            <Button color="gold" w={400} onClick={handleUpload} disabled={loading}>Charger Log</Button>
        </Stack>
    );
}

export default AddLogForm;
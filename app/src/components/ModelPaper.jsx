import { Paper, Group, Text, Button, List, ThemeIcon, Divider } from "@mantine/core";
import LogTypeBadge from "./LogTypeBadge";
import { FaCaretRight } from "react-icons/fa";
import { modelsApi } from '../api/models'

function ModelPaper({ model }) {
    const date = new Date(model.trained_at);

    const handleDelete = async () => {
        if (!confirm(`Êtes vous sûr de vouloir supprimer ${model.filename}? (Ceci ne peut pas être annulé!)`))
            return;

        try {
            await modelsApi.deleteModel(model.model_id)
            window.location.reload();
        } catch (err) {
            console.error(err);
        }
    };

    return <>
        <Paper shadow="sm" withBorder p="lg" w={380}>
            <Group justify="space-between">
                <Text fw={700} size="lg">{model.filename}</Text>
                {!model.deprecated ? <LogTypeBadge type={model.log_type} /> : <LogTypeBadge type="deprecated" />}
            </Group>

            <Divider mt="sm" mb="sm" />

            <List
                spacing="xs"
                size="sm"
                center
                icon={
                    <ThemeIcon color="gold" size={24} radius="xl">
                        <FaCaretRight size={16} />
                    </ThemeIcon>
                }
            >
                <List.Item><b>ID:</b> {model.model_id}</List.Item>
                <List.Item><b>Entrainé le:</b> {date.toLocaleString("fr-FR")}</List.Item>
                <List.Item><b>n_estimators =</b> {model.n_estimators ? model.n_estimators : '?'}</List.Item>
                <List.Item><b>max_samples =</b> {model.max_samples ? model.max_samples : '?'}</List.Item>
                <List.Item><b>max_features =</b> {model.max_features ? model.max_features : '?'}</List.Item>
            </List>

            <Divider mt="sm" mb="sm" />

            <Button color="pink" fullWidth mt="md" onClick={handleDelete} disabled={model.deprecated}>
                Supprimer Modèle
            </Button>
        </Paper>
    </>
}

export default ModelPaper;
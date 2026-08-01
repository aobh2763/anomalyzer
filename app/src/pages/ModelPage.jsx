import { useEffect, useState } from 'react';
import { Title, Stack, Container, Divider, Group } from '@mantine/core';
import { modelsApi } from '../api/models'
import ModelPaper from '../components/models/ModelPaper';
import AddModelForm from '../components/models/AddModelForm';

function ModelPage() {
    const [models, setModels] = useState([]);

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
    }, [])

    return (
        <>
            <Container size="xl" py="sm" pt={85}>
                <Stack gap="xl" justify="flex-start">
                    <Title order={1} fz={{ base: 36, sm: 40, md: 48 }} ta="center">Models</Title>

                    <Divider />

                    <AddModelForm />

                    <Divider />

                    <Group gap="md" justify="center" pt="md" pb="xl">
                        {models.map((model) => (
                            <ModelPaper key={model.model_id} model={model} />
                        ))}
                    </Group>
                </Stack>
            </Container >
        </>
    );
}

export default ModelPage;
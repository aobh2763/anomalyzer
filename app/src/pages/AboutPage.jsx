import { Container, Title, Text, Stack, Group, Divider, Box } from "@mantine/core"
import TechCard from "../components/TechCard";
import {
    IconBrandVite,
    IconBrandReact,
    IconBrandPython,
    IconApi,
    IconBrandMantine,
    IconRobot,
    IconTable,
    IconVectorTriangle,
    IconFileAnalytics,
    IconBinaryTree2,
    IconShieldCheck,
    IconRoute,
} from '@tabler/icons-react'

const techStack = {
    machineLearning: [
        { name: 'scikit-learn', icon: IconRobot, color: '#F7931E', description: 'Entraîne les modèles de forêt d\'isolation et assemble le pipeline d\'encodage (ColumnTransformer)', href: 'https://scikit-learn.org/' },
        { name: 'Isolation Forest', icon: IconBinaryTree2, color: '#2F9E44', description: 'Algorithme de détection d\'anomalies utilisé, isolant les événements rares par partitionnement aléatoire', href: 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html' },
        { name: 'pandas', icon: IconTable, color: '#150458', description: 'Manipule les données tabulaires tout au long du pipeline ETL et d\'extraction des caractéristiques', href: 'https://pandas.pydata.org/' },
        { name: 'Transformers', icon: IconVectorTriangle, color: '#FF6F00', description: 'Génère les plongements des champs de texte libre, réduits ensuite par PCA', href: 'https://www.sbert.net/' },
    ],
    backend: [
        { name: 'FastAPI', icon: IconApi, color: '#009688', description: 'Expose les modèles entraînés via une API REST', href: 'https://fastapi.tiangolo.com/' },
        { name: 'Python', icon: IconBrandPython, color: '#3776AB', description: 'Orchestre le pipeline d\'extraction, d\'encodage et d\'évaluation', href: 'https://www.python.org/' },
        { name: 'Pydantic', icon: IconShieldCheck, color: '#E92063', description: 'Définit et valide les modèles de données échangés par l\'API', href: 'https://docs.pydantic.dev/' },
        { name: 'python-evtx', icon: IconFileAnalytics, color: '#4B4B4B', description: 'Analyse les fichiers bruts de journaux d\'événements Windows (.evtx)', href: 'https://github.com/omerbenamram/evtx' },
    ],
    frontend: [
        { name: 'React', icon: IconBrandReact, color: '#61DAFB', description: 'Interface utilisateur pour le téléversement des journaux et la consultation des résultats', href: 'https://react.dev/' },
        { name: 'React Router', icon: IconRoute, color: '#CA4245', description: 'Gère la navigation entre les pages Logs, Modèles et Évaluation', href: 'https://reactrouter.com/' },
        { name: 'Mantine', icon: IconBrandMantine, color: '#339AF0', description: 'Bibliothèque de composants utilisée pour l\'ensemble de l\'interface', href: 'https://mantine.dev/' },
        { name: 'Vite', icon: IconBrandVite, color: '#646CFF', description: 'Serveur de développement et outil de build', href: 'https://vitejs.dev/' },
    ]
};

function AboutPage() {
    return (
        <Container size="md" py="xl" pt={85}>
            <Stack gap="xl">
                <Title order={1} fz={{ base: 36, sm: 40, md: 48 }} ta="center">À propos</Title>
                <Divider />
                <Box>
                    <Title order={2} mb="sm">Le projet</Title>
                    <Text>
                        Ce projet vise à détecter automatiquement les activités suspectes dans les
                        journaux d'événements Windows Server (Sécurité, Système, Application) à l'aide
                        de techniques de machine learning. Un modèle de forêt d'isolation est entraîné
                        pour chaque type de journal, permettant d'identifier les tentatives de connexion
                        échouées et répétées, les escalades de privilèges, la création suspecte de
                        comptes, l'exécution anormale de services, ainsi que les activités survenant en
                        dehors des horaires habituels. Cette application permet de téléverser un journal,
                        de l'évaluer, et de consulter les événements identifiés comme anormaux.
                    </Text>
                </Box>
                <Divider />
                <Box>
                    <Title order={2} mb="md">Stack technique</Title>
                    <Stack gap="sm">
                        <div>
                            <Text fw={600} mb="sm">Machine Learning</Text>
                            <Group grow gap="xs" align="stretch">
                                {techStack.machineLearning.map(tech => (
                                    <TechCard key={tech.name} tech={tech} />
                                ))}
                            </Group>
                        </div>
                        <div>
                            <Text fw={600} mb="sm">Backend</Text>
                            <Group grow gap="xs" align="stretch">
                                {techStack.backend.map(tech => (
                                    <TechCard key={tech.name} tech={tech} />
                                ))}
                            </Group>
                        </div>
                        <div>
                            <Text fw={600} mb="sm">Frontend</Text>
                            <Group grow gap="xs" align="stretch">
                                {techStack.frontend.map(tech => (
                                    <TechCard key={tech.name} tech={tech} />
                                ))}
                            </Group>
                        </div>
                    </Stack>
                </Box>
                <Divider />
                <Box>
                    <Title order={2} mb="sm">Liens</Title>
                    <Text>TBD</Text>
                </Box>
            </Stack>
        </Container>
    )
}

export default AboutPage;
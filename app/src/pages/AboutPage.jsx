import {
  Container,
  Title,
  Text,
  Stack,
  Group,
  Divider,
  Box,
} from "@mantine/core";
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
} from "@tabler/icons-react";
import { useTranslation } from "react-i18next";

const techStack = {
  machineLearning: [
    {
      name: "scikit-learn",
      icon: IconRobot,
      color: "#F7931E",
      descriptionKey: "descScikit",
      href: "https://scikit-learn.org/",
    },
    {
      name: "Isolation Forest",
      icon: IconBinaryTree2,
      color: "#2F9E44",
      descriptionKey: "descIsolationForest",
      href: "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html",
    },
    {
      name: "pandas",
      icon: IconTable,
      color: "#150458",
      descriptionKey: "descPandas",
      href: "https://pandas.pydata.org/",
    },
    {
      name: "Transformers",
      icon: IconVectorTriangle,
      color: "#FF6F00",
      descriptionKey: "descTransformers",
      href: "https://www.sbert.net/",
    },
  ],
  backend: [
    {
      name: "FastAPI",
      icon: IconApi,
      color: "#009688",
      descriptionKey: "descFastAPI",
      href: "https://fastapi.tiangolo.com/",
    },
    {
      name: "Python",
      icon: IconBrandPython,
      color: "#3776AB",
      descriptionKey: "descPython",
      href: "https://www.python.org/",
    },
    {
      name: "Pydantic",
      icon: IconShieldCheck,
      color: "#E92063",
      descriptionKey: "descPydantic",
      href: "https://docs.pydantic.dev/",
    },
    {
      name: "python-evtx",
      icon: IconFileAnalytics,
      color: "#4B4B4B",
      descriptionKey: "descPythonEvtx",
      href: "https://github.com/omerbenamram/evtx",
    },
  ],
  frontend: [
    {
      name: "React",
      icon: IconBrandReact,
      color: "#61DAFB",
      descriptionKey: "descReact",
      href: "https://react.dev/",
    },
    {
      name: "React Router",
      icon: IconRoute,
      color: "#CA4245",
      descriptionKey: "descReactRouter",
      href: "https://reactrouter.com/",
    },
    {
      name: "Mantine",
      icon: IconBrandMantine,
      color: "#339AF0",
      descriptionKey: "descMantine",
      href: "https://mantine.dev/",
    },
    {
      name: "Vite",
      icon: IconBrandVite,
      color: "#646CFF",
      descriptionKey: "descVite",
      href: "https://vitejs.dev/",
    },
  ],
};

function AboutPage() {
  const { t } = useTranslation();

  return (
    <Container size="lg" py="xl" pt={85}>
      <Stack gap="xl">
        <Title
          order={1}
          fz={{
            base: 36,
            sm: 40,
            md: 48,
          }}
          ta="center"
        >
          {t("about")}
        </Title>
        <Divider />
        <Box>
          <Title order={2} mb="sm">
            {t("theProject")}
          </Title>
          <Text>{t("projectDescription")}</Text>
        </Box>
        <Divider />
        <Box>
          <Title order={2} mb="md">
            {t("techStack")}
          </Title>
          <Stack gap="sm">
            <div>
              <Text fw={600} mb="sm">
                {t("machineLearning")}
              </Text>
              <Group grow gap="xs" align="stretch">
                {techStack.machineLearning.map((tech) => (
                  <TechCard
                    key={tech.name}
                    tech={{ ...tech, description: t(tech.descriptionKey) }}
                  />
                ))}
              </Group>
            </div>
            <div>
              <Text fw={600} mb="sm">
                {t("backend")}
              </Text>
              <Group grow gap="xs" align="stretch">
                {techStack.backend.map((tech) => (
                  <TechCard
                    key={tech.name}
                    tech={{ ...tech, description: t(tech.descriptionKey) }}
                  />
                ))}
              </Group>
            </div>
            <div>
              <Text fw={600} mb="sm">
                {t("frontend")}
              </Text>
              <Group grow gap="xs" align="stretch">
                {techStack.frontend.map((tech) => (
                  <TechCard
                    key={tech.name}
                    tech={{ ...tech, description: t(tech.descriptionKey) }}
                  />
                ))}
              </Group>
            </div>
          </Stack>
        </Box>
        <Divider />
        <Box>
          <Title order={2} mb="sm">
            {t("links")}
          </Title>
          <Text>TBD</Text>
        </Box>
      </Stack>
    </Container>
  );
}

export default AboutPage;

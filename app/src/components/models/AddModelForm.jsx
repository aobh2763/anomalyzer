import { useState } from "react";
import {
  Text,
  Center,
  Stack,
  Select,
  TextInput,
  NumberInput,
  Button,
} from "@mantine/core";
import { modelsApi } from "../../api/models";
import { useTranslation } from "react-i18next";

function AddModelForm() {
  const { t } = useTranslation();

  const LOG_TYPES = [
    { value: "security", label: t("security") },
    { value: "system", label: t("system") },
    { value: "application", label: t("application") },
  ];

  const [logType, setLogType] = useState(null);
  const [filename, setFilename] = useState("");

  const [nEstimators, setNEstimators] = useState("");
  const [maxSamples, setMaxSamples] = useState("");
  const [maxFeatures, setMaxFeatures] = useState("");

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddModel = async () => {
    if (!logType) {
      setError(t("pleaseSelectLogType"));
      return;
    }

    if (!filename.trim()) {
      setError(t("pleaseProvideModelFilename"));
      return;
    }

    setError(null);
    setLoading(true);

    try {
      await modelsApi.addModel({
        logType,
        filename: filename.trim(),
        nEstimators: nEstimators === "" ? null : nEstimators,
        maxSamples: maxSamples === "" ? null : maxSamples,
        maxFeatures: maxFeatures === "" ? null : maxFeatures,
      });

      setLogType(null);
      setFilename("");

      setNEstimators("");
      setMaxSamples("");
      setMaxFeatures("");

      window.location.reload();
    } catch (err) {
      setError(t("failedToAddModel"));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Stack gap="md" align="center">
      <Text c="dimmed" size="lg" ta="center">
        {t("registerPreTrainedModel")}
      </Text>

      <Select
        w={600}
        label={t("logType")}
        withAsterisk
        placeholder={t("chooseLogType")}
        data={LOG_TYPES}
        value={logType}
        onChange={setLogType}
      />

      <TextInput
        w={600}
        label={t("filename")}
        withAsterisk
        description={t("filenameOfTrainedModel")}
        placeholder={t("exSecurityIforestJoblib")}
        value={filename}
        onChange={(event) => setFilename(event.currentTarget.value)}
      />

      <NumberInput
        w={600}
        label="n_estimators"
        description={t("optional")}
        placeholder={t("ex100")}
        value={nEstimators}
        onChange={setNEstimators}
        min={1}
      />

      <NumberInput
        w={600}
        label="max_samples"
        description={t("optional")}
        placeholder={t("ex256")}
        value={maxSamples}
        onChange={setMaxSamples}
        min={1}
      />

      <NumberInput
        w={600}
        label="max_features"
        description={t("optional")}
        placeholder={t("ex1")}
        value={maxFeatures}
        onChange={setMaxFeatures}
        min={1}
      />

      {error && (
        <Text c="red" size="sm">
          {error}
        </Text>
      )}

      <Center>
        <Button
          color="gold"
          w={400}
          onClick={handleAddModel}
          disabled={loading}
        >
          {t("addModel")}
        </Button>
      </Center>
    </Stack>
  );
}

export default AddModelForm;

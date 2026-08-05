import { Stack, Text, FileInput, Button } from "@mantine/core";
import { useState } from "react";
import { logsApi } from "../../api/logs";
import { useTranslation } from 'react-i18next';

function AddLogForm() {
  const { t } = useTranslation();

  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = selectedFile => {
    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError(t("pleaseSelectFile"));
      return;
    }

    if (!file.name.toLowerCase().endsWith('.evtx')) {
      setError(t("pleaseUploadEvtx"));
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
      <Text c="dimmed" size="lg" ta="center" mb="md">{t('loadEvtxFileEvaluationInstruction')}</Text>
      <FileInput w={600} label={t('addLog')} withAsterisk description={t('loadEvtxFileDescription')} error={error} placeholder={t('key')} value={file} onChange={handleFileChange} />
      <Button color="gold" w={400} onClick={handleUpload} disabled={loading}>{t('loadLog')}</Button>
    </Stack>
  );
}

export default AddLogForm;

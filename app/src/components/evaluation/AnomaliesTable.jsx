import { useRef, useState } from "react";
import {
  Modal,
  Code,
  Button,
  Center,
  Divider,
  Text,
  Stack,
  Group,
} from "@mantine/core";
import { AgGridReact } from "ag-grid-react";
import {
  AllCommunityModule,
  ModuleRegistry,
  themeQuartz,
} from "ag-grid-community";
import { anomaliesApi } from "../../api/anomalies";
import ReactMarkdown from "react-markdown";
import { generateAnomaliesReport } from "../../helpers/pdfReport";
import { useTranslation } from "react-i18next";

ModuleRegistry.registerModules([AllCommunityModule]);

function resolveRawFields(row) {
  if (row.raw_fields && typeof row.raw_fields === "object") {
    return row.raw_fields;
  }

  if (row.raw_fields_json) {
    try {
      return JSON.parse(row.raw_fields_json);
    } catch {
      return {};
    }
  }

  return {};
}

function DetailsButtonRenderer(props) {
  const { t } = useTranslation();

  return (
    <Button
      size="xs"
      variant="light"
      color="gold"
      onClick={() => props.onDetailsClick(props.data)}
    >
      {t("details")}
    </Button>
  );
}

function AnomaliesTable({
  anomalies,
  evaluationId,
  logName,
  logType,
  modelName,
  decisionBoundary,
  imageUrl,
}) {
  const { t } = useTranslation();

  const [selectedRow, setSelectedRow] = useState(null);
  const [modalOpened, setModalOpened] = useState(false);
  const [explanation, setExplanation] = useState(null);

  const [explainOpened, setExplainOpened] = useState(false);
  const [explainLoading, setExplainLoading] = useState(false);

  const gridRef = useRef();

  const handleExport = () => {
    gridRef.current.api.exportDataAsCsv({
      fileName: "anomalies.csv",
    });
  };

  const defaultColDef = {
    sortable: true,
    filter: true,
    floatingFilter: true,
    resizable: true,
    flex: 1,
  };

  const openDetails = (row) => {
    setSelectedRow(row);
    setModalOpened(true);
  };

  const handleExplain = async () => {
    if (!selectedRow) return;

    setExplainLoading(true);
    setExplainOpened(true);

    try {
      const result = await anomaliesApi.explainAnomalyById(
        evaluationId,
        selectedRow.event_record_id,
      );

      setExplanation(result);
    } catch (err) {
      console.error(err);
      setExplanation("Erreur lors de la génération de l'explication.");
    } finally {
      setExplainLoading(false);
    }
  };

  const columnDefs = [
    {
      field: "event_record_id",
      headerName: t("eventRecordId"),
    },
    {
      field: "timestamp",
      headerName: t("timestamp"),
    },
    {
      field: "event_id",
      headerName: t("eventId"),
    },
    {
      field: "anomaly_score",
      headerName: t("anomalyScore"),
      valueFormatter: (params) =>
        typeof params.value === "number"
          ? params.value.toFixed(4)
          : params.value,
      cellStyle: {
        color: "#d4af37",
        fontWeight: 600,
      },
    },
    {
      headerName: "",
      field: "details",
      sortable: false,
      filter: false,
      floatingFilter: false,
      resizable: false,
      flex: 0,
      width: 120,
      cellRenderer: DetailsButtonRenderer,
      cellRendererParams: {
        onDetailsClick: openDetails,
      },
    },
  ];

  return (
    <>
      <div
        style={{
          height: 700,
          width: "100%",
        }}
      >
        <AgGridReact
          ref={gridRef}
          theme={themeQuartz.withParams({
            backgroundColor: "#1b1b1f",
            foregroundColor: "#f1f1f1",
            accentColor: "#d4af37",
            headerBackgroundColor: "#24242b",
          })}
          rowData={anomalies}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          pagination
          paginationPageSize={100}
          getRowId={(params) => params.data.event_record_id}
        />
      </div>

      <Modal
        opened={modalOpened}
        onClose={() => setModalOpened(false)}
        title={t("eventDetails")}
        size="lg"
        centered
      >
        <Code block>
          {selectedRow
            ? JSON.stringify(resolveRawFields(selectedRow), null, 2)
            : ""}
        </Code>

        <Divider my="sm" color="gold" />

        <Stack align="center">
          <Button color="gold" onClick={handleExplain}>
            {t("explainWithAi")}
          </Button>
        </Stack>
      </Modal>

      <Modal
        opened={explainOpened}
        onClose={() => setExplainOpened(false)}
        title={t("anomalyExplanation")}
        size="lg"
        centered
      >
        {explainLoading ? (
          <Text c="dimmed">{t("generating")}</Text>
        ) : (
          <div className="mantine-TypographyStylesProvider-root">
            <ReactMarkdown>{explanation}</ReactMarkdown>
          </div>
        )}
      </Modal>

      <Center>
        <Group>
          <Button color="gold" w={300} onClick={handleExport}>
            {t("downloadCsv")}
          </Button>

          <Button
            color="gold"
            w={300}
            onClick={() =>
              generateAnomaliesReport(anomalies, {
                logName,
                logType,
                modelName,
                decisionBoundary,
                imageUrl,
              })
            }
          >
            {t("downloadPdf")}
          </Button>
        </Group>
      </Center>
    </>
  );
}

export default AnomaliesTable;

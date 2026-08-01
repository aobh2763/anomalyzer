import { useRef, useState } from "react";
import { Modal, Code, Button, Center } from "@mantine/core";
import { AgGridReact } from "ag-grid-react";
import { AllCommunityModule, ModuleRegistry, themeQuartz } from "ag-grid-community";

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
    return (
        <Button
            size="xs"
            variant="light"
            color="gold"
            onClick={() => props.onDetailsClick(resolveRawFields(props.data))}
        >
            Détails
        </Button>
    );
}

function AnomaliesTable({ anomalies }) {
    const [selectedFields, setSelectedFields] = useState(null);
    const [modalOpened, setModalOpened] = useState(false);

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

    const openDetails = (fields) => {
        setSelectedFields(fields);
        setModalOpened(true);
    };

    const rowData = anomalies;

    const columnDefs = [
        { field: "event_record_id", headerName: "event record id" },
        { field: "timestamp", headerName: "timestamp" },
        { field: "event_id", headerName: "event id" },
        {
            field: "anomaly_score",
            headerName: "anomaly score",
            valueFormatter: (params) =>
                typeof params.value === "number"
                    ? params.value.toFixed(4)
                    : params.value,
            cellStyle: { color: "#d4af37", fontWeight: 600 },
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
            <div style={{ height: 700, width: "100%" }}>
                <AgGridReact
                    ref={gridRef}
                    theme={themeQuartz.withParams({
                        backgroundColor: "#1b1b1f",
                        foregroundColor: "#f1f1f1",
                        accentColor: "#d4af37",
                        headerBackgroundColor: "#24242b",
                    })}
                    rowData={rowData}
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
                title="Détails de l'événement"
                size="lg"
                centered
            >
                <Code block>
                    {selectedFields
                        ? JSON.stringify(selectedFields, null, 2)
                        : ""}
                </Code>
            </Modal>

            <Center>
                <Button color="gold" w={400} onClick={handleExport}>Télécharger CSV</Button>
            </Center>
        </>
    );
}

export default AnomaliesTable;
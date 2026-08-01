import { AgGridReact } from "ag-grid-react";
import { AllCommunityModule, ModuleRegistry, themeQuartz } from "ag-grid-community";
import { useRef } from "react";
import { Button, Center, Group } from "@mantine/core";
import { generateFeaturesReport } from "../../helpers/pdfReport";

ModuleRegistry.registerModules([AllCommunityModule]);

function FeaturesTable({ featuresData, logName, logType }) {
    const gridRef = useRef();

    const handleExport = () => {
        gridRef.current.api.exportDataAsCsv({
            fileName: "features.csv",
        });
    };

    const defaultColDef = {
        sortable: true,
        filter: true,
        floatingFilter: true,
        resizable: true,
    };

    const columnDefs =
        featuresData.length > 0
            ? Object.keys(featuresData[0]).map((key) => ({
                field: key,
                headerName: key.toLowerCase(),
                sortable: true,
                filter: true,
                resizable: true,
            }))
            : [];

    return (
        <>
            <div
                style={{ height: 700, width: "100%" }}
            >
                <AgGridReact
                    ref={gridRef}
                    theme={themeQuartz.withParams({
                        backgroundColor: "#1b1b1f",
                        foregroundColor: "#f1f1f1",
                        accentColor: "#d4af37",
                        headerBackgroundColor: "#24242b",
                    })}
                    rowData={featuresData}
                    columnDefs={columnDefs}
                    defaultColDef={defaultColDef}
                    pagination
                    paginationPageSize={100}
                />
            </div>

            <Center>
                <Group>
                    <Button color="gold" w={300} onClick={handleExport}>Télécharger CSV</Button>
                    <Button color="gold" w={300} onClick={() => generateFeaturesReport(featuresData, { logName: logName, logType: logType })}>
                        Télécharger PDF
                    </Button>
                </Group>
            </Center>
        </>
    );
}

export default FeaturesTable;
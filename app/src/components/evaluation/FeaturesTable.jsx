import { AgGridReact } from "ag-grid-react";
import {
  AllCommunityModule,
  ModuleRegistry,
  themeQuartz,
} from "ag-grid-community";
import { useRef } from "react";
import { Button, Center, Group, useComputedColorScheme } from "@mantine/core";
import { generateFeaturesReport } from "../../helpers/pdfReport";
import { useTranslation } from "react-i18next";

ModuleRegistry.registerModules([AllCommunityModule]);

function FeaturesTable({ featuresData, logName, logType }) {
  const { t } = useTranslation();

  const computedColorScheme = useComputedColorScheme("light")

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
        style={{
          height: 700,
          width: "100%",
        }}
      >
        <AgGridReact
          ref={gridRef}
          theme={
            computedColorScheme === "dark" ?
              themeQuartz.withParams({
                backgroundColor: "#1b1b1f",
                foregroundColor: "#f1f1f1",
                accentColor: "#d4af37",
                headerBackgroundColor: "#24242b",
              }) :
              themeQuartz.withParams({
                backgroundColor: "#FFE9F0",
                foregroundColor: "#442a12",
                accentColor: "#d6336c",
                headerBackgroundColor: "#FFEC99",
              })
          }
          rowData={featuresData}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          pagination
          paginationPageSize={100}
        />
      </div>

      <Center>
        <Group>
          <Button color="gold" w={300} onClick={handleExport}>
            {t("downloadCsv")}
          </Button>
          <Button
            color="gold"
            w={300}
            onClick={() =>
              generateFeaturesReport(featuresData, {
                logName: logName,
                logType: logType,
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

export default FeaturesTable;

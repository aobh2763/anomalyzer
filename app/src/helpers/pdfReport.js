import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import i18next from "i18next";

const BRAND_COLOR = [212, 175, 55];

function addReportHeader(doc, title, metadata = {}) {
    doc.setFontSize(18);
    doc.setTextColor(...BRAND_COLOR);
    doc.text(title, 14, 18);

    doc.setFontSize(10);
    doc.setTextColor(80, 80, 80);

    let y = 26;
    Object.entries(metadata).forEach(([label, value]) => {
        doc.text(`${label} : ${value}`, 14, y);
        y += 5;
    });

    doc.setDrawColor(...BRAND_COLOR);
    doc.setLineWidth(0.5);
    doc.line(14, y + 2, 196, y + 2);

    return y + 8;
}

function addFooter(doc) {
    const pageCount = doc.internal.getNumberOfPages();

    for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(
            i18next.t("pageGeneratedOn", { page: i, total: pageCount, date: new Date().toLocaleString() }),
            14,
            doc.internal.pageSize.height - 10,
        );
    }
}
async function blobUrlToDataUrl(blobUrl) {
    const response = await fetch(blobUrl);
    const blob = await response.blob();

    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

export function generateFeaturesReport(
    featuresData,
    { logName, logType } = {},
) {
    const doc = new jsPDF();

    const startY = addReportHeader(doc, i18next.t("featuresReport"), {
        Log: logName ?? "-",
        Type: logType ?? "-",
        [i18next.t("numberOfEvents")]: featuresData.length,
    });

    if (featuresData.length > 0) {
        const columns = Object.keys(featuresData[0]);
        const rows = featuresData.map((row) =>
            columns.map((col) => {
                const val = row[col];
                return Array.isArray(val) ? val.join(", ") : (val ?? "");
            }),
        );

        autoTable(doc, {
            startY,
            head: [columns],
            body: rows,
            styles: {
                fontSize: 6,
                cellPadding: 1.5,
            },
            headStyles: {
                fillColor: BRAND_COLOR,
                textColor: 20,
            },
            theme: "grid",
        });
    }

    addFooter(doc);
    doc.save("rapport_caracteristiques.pdf");
}

export async function generateAnomaliesReport(
    anomalies,
    { logName, logType, modelName, decisionBoundary, imageUrl } = {},
) {
    const doc = new jsPDF();

    const startY = addReportHeader(doc, i18next.t("anomaliesReport"), {
        Log: logName ?? "-",
        Type: logType ?? "-",
        Model: modelName ?? "-",
        [i18next.t("decisionBoundary")]: decisionBoundary ?? "-",
        [i18next.t("numberOfAnomalies")]: anomalies.length,
    });

    let currentY = startY;
    if (imageUrl) {
        try {
            const dataUrl = await blobUrlToDataUrl(imageUrl);
            const imgWidth = 180;
            const imgHeight = 90;
            doc.addImage(dataUrl, "PNG", 14, currentY, imgWidth, imgHeight);
            currentY += imgHeight + 10;
        } catch (err) {
            console.error("Failed to embed score plot:", err);
        }
    }

    if (anomalies.length > 0) {
        const columns = [
            i18next.t("eventRecordId"),
            i18next.t("timestamp"),
            i18next.t("eventId"),
            i18next.t("anomalyScore"),
        ];

        const rows = anomalies.map((row) => [
            row.event_record_id,
            row.timestamp,
            row.event_id,
            typeof row.anomaly_score === "number"
                ? row.anomaly_score.toFixed(4)
                : row.anomaly_score,
        ]);

        autoTable(doc, {
            startY: currentY,
            head: [columns],
            body: rows,
            styles: {
                fontSize: 8,
                cellPadding: 2,
            },
            headStyles: {
                fillColor: BRAND_COLOR,
                textColor: 20,
            },
            theme: "grid",
        });
    }

    addFooter(doc);
    doc.save("rapport_anomalies.pdf");
}

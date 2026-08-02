const CYCLIC_FEATURES = ["minute", "hour", "day", "second", "month"];

export function transformFeatures(data) {
    return data.map((row) => {
        const transformed = { ...row };

        CYCLIC_FEATURES.forEach((feature) => {
            const sin = `${feature}_sin`;
            const cos = `${feature}_cos`;

            if (sin in row && cos in row) {
                transformed[feature] = [
                    Number(row[sin].toFixed(4)),
                    Number(row[cos].toFixed(4)),
                ];

                delete transformed[sin];
                delete transformed[cos];
            }
        });

        Object.keys(transformed).forEach((key) => {
            if (typeof transformed[key] === "number") {
                transformed[key] = Number(transformed[key].toFixed(3));
            }
        });

        return transformed;
    });
}

import { createTheme } from "@mantine/core";

const theme = createTheme({
    primaryColor: "pink",
    defaultRadius: "md",

    colors: {
        pink: [
            "#fff0f6",
            "#ffdeeb",
            "#fcc2d7",
            "#faa2c1",
            "#f783ac",
            "#f06595",
            "#e64980",
            "#d6336c",
            "#c2255c",
            "#a61e4d",
        ],

        gold: [
            "#fff9db",
            "#fff3bf",
            "#ffec99",
            "#ffe066",
            "#ffd43b",
            "#fcc419",
            "#fab005",
            "#f08c00",
            "#e67700",
            "#d9480f",
        ],

        dark: [
            "#F8EDF3",
            "#EFD5E3",
            "#DDB3C8",
            "#C68FAE",
            "#A56E8E",
            "#725069",
            "#523847",
            "#382630",
            "#24181F",
            "#181015",
        ],
    },

    cssVariablesResolver: () => ({
        variables: {},

        light: {},

        dark: {
            /* Main backgrounds */
            "--mantine-color-body": "#181015",
            "--mantine-color-default": "#2E1F28",
            "--mantine-color-default-hover": "#392630",

            /* Borders */
            "--mantine-color-default-border": "#6B4A5B",

            /* Text */
            "--mantine-color-text": "#FFF4F8",
            "--mantine-color-dimmed": "#D8B8C9",

            /* Primary */
            "--mantine-primary-color-filled": "#d6336c",
            "--mantine-primary-color-filled-hover": "#e64980",

            /* Gold accents */
            "--mantine-color-anchor": "#ffd43b",
            "--mantine-color-placeholder": "#C8A96B",
        },
    }),
});

export default theme;
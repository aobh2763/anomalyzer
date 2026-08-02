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
            "#FCEEF5",
            "#F3D5E5",
            "#E2B4CD",
            "#CC8CAF",
            "#B16692",
            "#74345b",
            "#572442",
            "#441c34",
            "#2A1722",
            "#140A11",
        ],
    },

    cssVariablesResolver: () => ({
        variables: {},

        light: {},

        dark: {
            /* Main backgrounds */
            "--mantine-color-body": "#1E131A",
            "--mantine-color-default": "#34212B",
            "--mantine-color-default-hover": "#402834",

            /* Borders */
            "--mantine-color-default-border": "#7B5067",

            /* Text */
            "--mantine-color-text": "#FFF5F8",
            "--mantine-color-dimmed": "#E2BDD0",

            /* Primary */
            "--mantine-primary-color-filled": "#d6336c",
            "--mantine-primary-color-filled-hover": "#e64980",

            /* Gold accents */
            "--mantine-color-anchor": "#ffd43b",
            "--mantine-color-placeholder": "#D7B774",
        },
    }),
});

export default theme;
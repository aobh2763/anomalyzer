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
});

export const resolver = () => ({
  variables: {},

  light: {
    /* Main backgrounds — gold-dominant */
    "--mantine-color-body": "#FFF9DB",
    "--mantine-color-default": "#FFF3BF",
    "--mantine-color-default-hover": "#FFEC99",

    /* Borders — pink accent */
    "--mantine-color-default-border": "#f783ac",

    /* Text */
    "--mantine-color-text": "#442a12",
    "--mantine-color-dimmed": "#8a6a2a",

    /* Primary stays pink for buttons/interactive elements */
    "--mantine-primary-color-filled": "#d6336c",
    "--mantine-primary-color-filled-hover": "#e64980",

    /* Pink accents */
    "--mantine-color-anchor": "#d6336c",
    "--mantine-color-placeholder": "#e64980",
  },

  dark: {
    /* Main backgrounds */
    "--mantine-color-body": "#441c34",
    "--mantine-color-default": "#74345b",
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

    /* Lock down the raw dark-* scale so nothing falls back to the light-pink index 0 */
    "--mantine-color-dark-0": "#FFF5F8",
    "--mantine-color-dark-1": "#E2BDD0",
    "--mantine-color-dark-2": "#B16692",
    "--mantine-color-dark-3": "#7B5067",
    "--mantine-color-dark-4": "#572442",
    "--mantine-color-dark-5": "#441c34",
    "--mantine-color-dark-6": "#34212B",
    "--mantine-color-dark-7": "#2A1722",
    "--mantine-color-dark-8": "#1E131A",
    "--mantine-color-dark-9": "#140A11",
  },
});

export default theme;
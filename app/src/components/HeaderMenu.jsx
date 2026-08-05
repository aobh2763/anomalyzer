import { Burger, Container, Drawer, Group, Stack, Text } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link } from "react-router";
import { GiFruitTree } from "react-icons/gi";
import classes from "./HeaderMenu.module.css";
import { useTranslation } from "react-i18next";

export function HeaderMenu() {
  const { t } = useTranslation();

  const links = [
    { link: "/", label: t("home") },
    { link: "/logs", label: t("logs") },
    { link: "/models", label: t("models") },
    { link: "/evaluation", label: t("evaluation") },
    { link: "/about", label: t("about") },
  ];

  const [opened, { toggle, close }] = useDisclosure(false);

  const items = links.map((link) => (
    <Link key={link.link} to={link.link} className={classes.link}>
      {link.label}
    </Link>
  ));

  return (
    <>
      <header className={classes.header}>
        <Container size="lg">
          <div className={classes.inner}>
            <Group gap={15}>
              <GiFruitTree size={36} color="green" />
              <Link key="Home" to="/">
                <Text fz={30} fw={700} c="gold">
                  {t("anomalyzer")}
                </Text>
              </Link>
            </Group>
            <Group gap={5} visibleFrom="sm">
              {items}
            </Group>
            <Burger
              opened={opened}
              onClick={toggle}
              size="sm"
              hiddenFrom="sm"
              aria-label={t("toggleNavigation")}
            />
          </div>
        </Container>
      </header>

      <Drawer
        opened={opened}
        onClose={close}
        size="100%"
        padding="md"
        hiddenFrom="sm"
        zIndex={1000}
      >
        <Stack>
          {links.map((link) => (
            <Link
              key={link.label}
              to={link.link}
              className={classes.link}
              onClick={close}
            >
              {link.label}
            </Link>
          ))}
        </Stack>
      </Drawer>
    </>
  );
}

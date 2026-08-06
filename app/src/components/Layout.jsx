import { AppShell } from "@mantine/core";
import { Outlet } from "react-router";
import { HeaderMenu } from "./HeaderMenu";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";

function Layout() {
  const { t } = useTranslation();

  useEffect(() => {
    document.title = t("anomalyzer");
  }, [t]);

  return (
    <AppShell header={{ height: 60 }} padding={0}>
      <AppShell.Header>
        <HeaderMenu />
      </AppShell.Header>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}

export default Layout;

import { AppShell } from "@mantine/core";
import { Outlet } from "react-router";
import { HeaderMenu } from "./HeaderMenu";

function Layout() {
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

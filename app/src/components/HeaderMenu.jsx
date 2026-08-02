import { Burger, Container, Drawer, Group, Stack, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Link } from 'react-router'
import { GiFruitTree } from "react-icons/gi";
import classes from './HeaderMenu.module.css';

const links = [
  { link: '/', label: 'Home' },
  { link: '/logs', label: 'Logs' },
  { link: '/models', label: 'Models' },
  { link: '/evaluation', label: 'Evaluation' },
  { link: '/about', label: 'About' }
];

export function HeaderMenu() {
  const [opened, { toggle, close }] = useDisclosure(false);

  const items = links.map((link) => (
    <Link
      key={link.label}
      to={link.link}
      className={classes.link}
    >
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
              <Link
                key="Home"
                to="/"
              >
                <Text fz={30} fw={700} c='gold'>Anomalyseur</Text>
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
              aria-label="Toggle navigation"
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
          {links.map(link => (
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
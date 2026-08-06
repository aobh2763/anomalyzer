import { useState } from 'react';
import { IconChevronDown } from '@tabler/icons-react';
import { Group, Image, Menu, UnstyledButton } from '@mantine/core';
import classes from './LanguagePicker.module.css';
import { useTranslation } from 'react-i18next';

export function LanguagePicker() {
  const { i18n, t } = useTranslation();

  const data = [
    { value: "en", label: t("english"), image: "/langicons/english.png" },
    { value: "fr", label: t("french"), image: "/langicons/french.png" },
  ];

  const [opened, setOpened] = useState(false);

  const selected = data.find((item) =>
    i18n.language.startsWith(item.value)
  ) ?? data[0];

  const changeLanguage = (item) => {
    i18n.changeLanguage(item.value);
  };

  const items = data.map((item) => (
    <Menu.Item
      leftSection={
        <Image
          src={item.image}
          width={18}
          height={18}
          alt=""
        />
      }
      onClick={() => changeLanguage(item)}
      key={item.value}
    >
      {item.label}
    </Menu.Item>
  ));

  return (
    <Menu
      onOpen={() => setOpened(true)}
      onClose={() => setOpened(false)}
      radius="md"
      width="target"
      withinPortal
    >
      <Menu.Target>
        <UnstyledButton
          className={classes.control}
          data-expanded={opened || undefined}
        >
          <Group gap="xs">
            <Image
              src={selected.image}
              w={22}
              h={22}
              alt=""
            />

            <span className={classes.label}>
              {selected.label}
            </span>
          </Group>

          <IconChevronDown
            size={16}
            className={classes.icon}
            stroke={1.5}
          />
        </UnstyledButton>
      </Menu.Target>

      <Menu.Dropdown>
        {items}
      </Menu.Dropdown>
    </Menu>
  );
}
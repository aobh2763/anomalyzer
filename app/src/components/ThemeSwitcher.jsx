import { ActionIcon, useMantineColorScheme, useComputedColorScheme } from "@mantine/core";
import { LuSun, LuMoon } from "react-icons/lu";

export default function ThemeSwitcher() {
    const { setColorScheme } = useMantineColorScheme();
    const computedColorScheme = useComputedColorScheme("light");

    const toggleColorScheme = () => {
        setColorScheme(computedColorScheme === "light" ? "dark" : "light");
    };

    return (
        <ActionIcon
            onClick={toggleColorScheme}
            variant="subtle"
            size="lg"
            radius="md"
            aria-label="Toggle color scheme"
        >
            {computedColorScheme === "light" ? <LuMoon size={18} /> : <LuSun size={18} />}
        </ActionIcon>
    );
}
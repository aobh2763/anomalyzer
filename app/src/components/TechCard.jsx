import { Card, Group, Text, Button, Box } from "@mantine/core";

function TechCard({ tech }) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder style={{ display: 'flex', flexDirection: 'column' }}>
      <Group justify="space-between" mt="md" mb="xs">
        <Text fw={500} color={tech.color}>{tech.name}</Text>
        {tech.icon && <tech.icon size={24} color={tech.color} />}
      </Group>

      <Text size="md" c="dimmed">
        {tech.description}
      </Text>

      <Box mt="auto">
        <Button component="a" href={tech.href} color={tech.color} fullWidth mt="md" radius="md">
          Visit
        </Button>
      </Box>
    </Card>
  );
}

export default TechCard;
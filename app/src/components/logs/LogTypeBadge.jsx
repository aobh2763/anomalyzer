import { Badge } from "@mantine/core";

function LogTypeBadge({ type }) {
    let color = "gray";

    switch (type) {
        case "system":
            color = "yellow";
            break;
        case "application":
            color = "red";
            break;
        case "security":
            color = "blue";
            break;
    }


    return <>
        <Badge color={color}>{type}</Badge>
    </>
}

export default LogTypeBadge;

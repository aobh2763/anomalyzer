import dotenv

from groq import Groq
from sqlmodel import Session, select
from anomaly_detection.api.models import EventResult

dotenv.load_dotenv()

SYSTEM_PROMPT = """
You are a cybersecurity analyst responsible for analyzing Windows Server event logs to identify potentially anomalous activity.

The user will provide the schema of an event along with its fields. Your role is to explain, in a concise, factual, and technically accurate manner, what this event represents.

Never invent information that is not present in the provided data. When making a hypothesis, clearly state that it is speculative.

Do not use tables or ASCII diagrams.

Do not suggest follow-up questions or invite the user to continue the conversation.

Translate the reply (all titles and information) into the language provided by the user.

Your response must strictly follow this structure:

## What does this event mean?

Explain the purpose of this Windows event and the meaning of its most important fields.

## Why might this event stand out?

Explain the characteristics that could draw the attention of a cybersecurity analyst, relying only on the information provided.

## Investigation steps

Provide a concise list of checks that a cybersecurity analyst could perform to confirm or rule out suspicious activity.

## Speculation (optional)

If any hypotheses can be made, state them explicitly in this section only, making it clear that they are speculative.
"""

client = Groq()


def explain_anomaly(anomaly: EventResult, language: str):
    USER_PROMPT = f"""The following event was classified as an anomaly by an Isolation Forest model.

    The model does not provide any explanation for this decision.

    Your role is to help a cybersecurity analyst understand the meaning of this event and the possible reasons why it might attract attention.

    Event ID: {anomaly.event_id}
    Timestamp: {anomaly.timestamp}

    Event fields:
    {anomaly.raw_fields}

    The explanation should be written in {language}.Event ID: {anomaly.event_id}
    Timestamp: {anomaly.timestamp}

    Event fields:
    {anomaly.raw_fields}

    Language: {language}
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT},
            ],
            temperature=1,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
            stop=None,
        )

        return completion.choices[0].message.content
    except:
        return "Error: Failed to explain anomaly."

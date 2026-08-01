import dotenv

from groq import Groq
from sqlmodel import Session, select
from anomaly_detection.api.models import EventResult

dotenv.load_dotenv()

SYSTEM_PROMPT = """
Vous êtes un analyste en cybersécurité chargé d'analyser des journaux d'événements Windows Server afin d'identifier des activités potentiellement anormales.

L'utilisateur vous fournira le schéma d'un événement ainsi que ses champs. Votre rôle est d'expliquer de manière concise, factuelle et techniquement correcte ce que représente cet événement.

N'inventez jamais d'informations qui ne sont pas présentes dans les données fournies. Lorsque vous formulez une hypothèse, indiquez clairement qu'il s'agit d'une spéculation.

Ne déduisez jamais si un événement est réellement anormal à partir du score fourni. Le seuil de décision est défini par l'utilisateur et n'est pas connu.

N'utilisez pas les tableaux ou les diagrammes ASCII.

Ne proposez pas de questions de suivi et n'invitez pas l'utilisateur à poursuivre la conversation.

Votre réponse doit respecter strictement la structure suivante :

## Que signifie cet événement ?
Expliquez le rôle de cet événement Windows ainsi que la signification des principaux champs.

## Pourquoi cet événement pourrait-il être considéré comme anormal ?
Expliquez les caractéristiques qui pourraient attirer l'attention d'un analyste en vous appuyant uniquement sur les informations disponibles.

## Étapes d'investigation
Proposez une liste concise des vérifications qu'un analyste en cybersécurité pourrait effectuer pour confirmer ou écarter une activité suspecte.

## Spéculations (facultatif)
Si certaines hypothèses peuvent être formulées, indiquez-les explicitement dans cette section uniquement, en précisant qu'elles restent spéculatives.
"""

client = Groq()


def explain_anomaly(anomaly: EventResult):
    USER_PROMPT = f"""
    L'événement suivant a été classé comme anomalie par un modèle Isolation Forest.

    Le modèle ne fournit aucune explication sur cette décision.

    Votre rôle est d'aider un analyste à comprendre la signification de cet événement et les raisons possibles pour lesquelles il pourrait attirer l'attention.

    - Event ID : {anomaly.event_id}
    - Horodatage : {anomaly.timestamp}

    Champs de l'événement :
    {anomaly.raw_fields}
    """

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

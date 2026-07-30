export const SECURITY_LABELS = {
    4624: "Un compte s'est connecté avec succès",
    4672: "Des privilèges spéciaux ont été attribués à la nouvelle connexion",
    4634: "Un compte a été déconnecté",
    4648: "Une connexion a été tentée avec des informations d'identification explicites",
    4776: "L'ordinateur a tenté de valider les informations d'identification d'un compte",
    4799: "L'appartenance à un groupe local sécurisé a été énumérée",
    4702: "Une tâche planifiée a été mise à jour",
    5379: "Des informations d'identification du gestionnaire d'informations d'identification ont été lues",
    4662: "Une opération a été effectuée sur un objet",
    4697: "Un service a été installé dans le système",
    4798: "L'appartenance à un groupe local d'un utilisateur a été énumérée",
    4611: "Un processus d'ouverture de session approuvé a été enregistré auprès de l'autorité de sécurité locale",
    5058: "Opération sur un fichier de clé",
    5061: "Opération cryptographique",
    5059: "Opération de migration de clé",
    4699: "Une tâche planifiée a été supprimée",
    4698: "Une tâche planifiée a été créée",
};

export const APPLICATION_LABELS = {
    4: "Message de journal PHP, démarrage de l'interpréteur ou sortie d'exécution (avertissements, échecs de chargement d'extensions)",
    16394: "Statut de la plateforme de protection logicielle (licence ou activation)",
    16384: "Événement SPP, notification de sous-type ou moteur de règles distinct",
    4098: "Avertissement, échec de l'application d'un élément de préférence de registre GPO",
    1001: "Rapport WER enregistré après un plantage, en corrélation avec un événement 1000",
    64: "Avertissement, un certificat est sur le point d'expirer ou a expiré (renouvellement automatique échoué)",
    1000: "Enregistrement de plantage d'application, détails du processus ou module fautif",
    1704: "Informatif, les paramètres de sécurité de la stratégie de groupe ont été appliqués avec succès",
    100: "Message du service MariaDB, EventID non standardisé",
    9027: "Informatif, le gestionnaire de fenêtres du bureau a enregistré un nouveau port de session (des occurrences répétées peuvent indiquer une tentative de force brute RDP)",
};

export const SYSTEM_LABELS = {
    12: "Le système d'exploitation a démarré",
    19: "Mise à jour Windows installée avec succès",
    55: "Corruption détectée sur le système de fichiers du volume",
    98: "Vérification du volume NTFS terminée",
    1074: "Un processus a lancé le redémarrage ou l'arrêt de l'ordinateur",
    6005: "Le service de journal des événements a été démarré",
    6006: "Le service de journal des événements a été arrêté",
    6009: "Version de Microsoft Windows détectée au démarrage",
    6013: "Temps de fonctionnement du système",
    7001: "Un service n'a pas pu démarrer car un service dont il dépend n'a pas pu démarrer",
    7002: "Un service n'a pas pu démarrer car un pilote dont il dépend n'a pas pu démarrer",
    7036: "Le service a changé d'état (démarré ou arrêté)",
    7040: "Le type de démarrage du service a été modifié",
    7045: "Un nouveau service a été installé dans le système",
};

const LABELS_BY_LOG_TYPE = {
    security: SECURITY_LABELS,
    application: APPLICATION_LABELS,
    system: SYSTEM_LABELS,
};

export function getEventLabel(eventId, logType) {
    const table = LABELS_BY_LOG_TYPE[logType];
    if (!table) return "Inconnu";
    return table[eventId] ?? "Inconnu";
}

export default LABELS_BY_LOG_TYPE;
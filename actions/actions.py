from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop

class ActionProvideHelpLink(Action):
    def name(self) -> Text:
        return "action_provide_help_link"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Για περισσότερες πληροφορίες μπορείτε να απευθυνθείτε:\n* "
                "στην επίσημη ιστοσελίδα της [Ενιαίας Ψηφιακής Πύλης Δημόσιας Διοίκησης] (https://www.gov.gr/ipiresies/epikheirematike-drasterioteta/adeiodoteseis-kai-summorphose/karta-psephiakou-takhographou-odegou)\n* "
                "στην περιφερειακή διεύθυνση Μεταφορών και Επικοινωνιών της περιοχής σας\n* "
                "στα κατά τόπους Κέντρα Εξυπηρέτησης Πολιτών (ΚΕΠ)"
            ),
            markdown=True
        )
        return []
    
    
class ActionDynamicGreetMenu(Action):
    def name(self) -> Text:
        return "action_dynamic_greet_menu"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        last_user_intent = tracker.latest_message.get("intent", {}).get("name")

        # Define all initial menu options with their corresponding intents
        menu_options = [
            {"title": "Γενική Περιγραφή", "payload": "/ask_general_description", "intent": "ask_general_description"},
            {"title": "Δικαιολογητικά", "payload": "/ask_documents_required", "intent": "ask_documents_required"},
            {"title": "Κόστος", "payload": "/ask_card_cost", "intent": "ask_card_cost"},
            {"title": "Αρμόδια Αρχή", "payload": "/ask_competent_authority", "intent": "ask_competent_authority"},
            {"title": "Προϋποθέσεις", "payload": "/ask_requirements", "intent": "ask_requirements"},
            {"title": "Σημεία Eξυπηρέτησης", "payload": "/ask_contact_info", "intent": "ask_contact_info"},
        ]

        # Filter out the button that corresponds to the last user intent
        if last_user_intent and last_user_intent != "greet":
            available_buttons = [
                {"title": option["title"], "payload": option["payload"]}
                for option in menu_options
                if option["intent"] != last_user_intent
            ]
        else:
            # If it's the first greet or no specific intent, show all buttons
            available_buttons = [
                {"title": option["title"], "payload": option["payload"]}
                for option in menu_options
            ]

        dispatcher.utter_message(
            text="Παρακαλώ επιλέξτε ένα από τα παρακάτω σχετικά πεδία ή κάντε την δική σας ερώτηση.",
            buttons=available_buttons
        )

        return []


class ValidateDocumentApplicationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_document_application_form"

    def validate_application_method(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value in ["online", "in_person"]:
            documents_needed = []

            if slot_value == "online":
                documents_needed = [
                    "Φωτογραφία τύπου διαβατηρίου σε ψηφιακή μορφή (τύπος αρχείου: .jpg, .jpeg, .png, .gif, ελάχιστη ανάλυση: 800x1200 pixels)",
                    "Ψηφιακή εικόνα της φυσικής υπογραφής σας σε λευκό χαρτί (τύπος αρχείου: .jpg, .jpeg, .png, .gif, ελάχιστη ανάλυση: 1200x480 pixels)",
                ]
                intro_text="Για την αίτηση σας ηλεκτρονικά θα χρειαστείτε:"
            else:
                documents_needed = [
                    "Φωτοαντίγραφο της Αστυνομικής σας Ταυτότητας (ή του Διαβατηρίου)",
                    "Φωτογραφία τύπου διαβατηρίου",
                    "Άδεια Οδήγησης",
                    "Βεβαίωση Μόνιμης Κατοικίας"
                ]
                intro_text="Θα χρειαστεί να προσκομίσετε στο ΚΕΠ τα εξής δικαιολογητικά:"

            bullet_list = "\n".join([f"- {doc}" for doc in documents_needed])
            dispatcher.utter_message(text=f"{intro_text}\n{bullet_list}")

            return {"application_method": slot_value}
        else:
            dispatcher.utter_message(
                text="Παρακαλώ επιλέξτε έναν έγκυρο τρόπο υποβολής: 'Ηλεκτρονικά' ή 'Δια ζώσης'."
            )
            return {"application_method": None}


class ActionActivateDocumentForm(Action):
    def name(self) -> Text:
        return "action_activate_document_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("application_method", None), ActiveLoop("document_application_form")]

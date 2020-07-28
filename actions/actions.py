from typing import Dict, Text, Any, List, Union, Optional
import logging
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, EventType
from .database_connectivity import DataUpdate
from actions.parsing import (
    parse_duckling_time_as_interval,
    parse_duckling_time,
    get_entity_details,
    parse_duckling_currency,
)

logger = logging.getLogger(__name__)

class TransactSearchForm(FormAction):
    """Transaction search form"""
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "transact_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        book_type = tracker.get_slot("book_type")
        if book_type == "book" or book_type == "test":
            return ["PERSON", "time", "time2"]
        else:
            return ["PERSON"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {"PERSON": [self.from_entity(entity="PERSON")],
                "time": [self.from_entity(entity="time")],
                "time2": [self.from_entity(entity="time2")]
                }
    # def validate_PERSON(self,
    #     value: Text,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     """Validate PERSON value."""


    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate time value."""
        timeentity = get_entity_details(tracker, "time")
        parsedinterval = parse_duckling_time_as_interval(timeentity)
        if not parsedinterval:
            dispatcher.utter_message(template="utter_no_transactdate")
            return {"time": None}
        return parsedinterval

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        book_type = tracker.get_slot("book_type")
        start_time = tracker.get_slot("start_time")
        time2 = tracker.get_slot("time2")
        dispatcher.utter_message("date {}".format(start_time))
        if book_type == "book" or book_type == "test":
            DataUpdate("update", tracker.get_slot("PERSON"), start_time, time2)
            dispatcher.utter_message(template="utter_name_time_confirm",)
        else:
            DataUpdate("delete", tracker.get_slot("PERSON"), None, None)
            dispatcher.utter_message(template="utter_name__confirm")
        return []


# def custom_request_next_slot(
#     form,
#     dispatcher: "CollectingDispatcher",
#     tracker: "Tracker",
#     domain: Dict[Text, Any],
# ) -> Optional[List[EventType]]:
#     """Request the next slot and utter template if needed,
#         else return None"""
#
#     for slot in form.required_slots(tracker):
#         if form._should_request_slot(tracker, slot):
#             logger.debug(f"Request next slot '{slot}'")
#             dispatcher.utter_message(
#                 template=f"utter_ask_{form.name()}_{slot}", **tracker.slots
#             )
#             return [SlotSet(REQUESTED_SLOT, slot)]
#
#     return None
#
#
# class TransactSearchForm(FormAction):
#     """Transaction search form"""
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "transact_search_form"
#
#     def request_next_slot(
#         self,
#         dispatcher: "CollectingDispatcher",
#         tracker: "Tracker",
#         domain: Dict[Text, Any],
#     ) -> Optional[List[EventType]]:
#         return custom_request_next_slot(self, dispatcher, tracker, domain)
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["search_type", "time"]
#
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             # "vendor_name": self.from_entity(entity="vendor_name"),
#             "time": [self.from_entity(entity="time")],
#             "search_type": [
#                 self.from_trigger_intent(
#                     intent="book_appointment", value="spend"
#                 ),
#                 self.from_trigger_intent(
#                     intent="check_earnings", value="deposit"
#                 ),
#             ],
#         }
#
#     def validate_time(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         """Validate time value."""
#         timeentity = get_entity_details(tracker, "time")
#         parsedinterval = parse_duckling_time_as_interval(timeentity)
#         if not parsedinterval:
#             dispatcher.utter_message(template="utter_no_transactdate")
#             return {"time": None}
#         return parsedinterval
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         search_type = tracker.get_slot("search_type")
#         # DataUpdate(tracker.get_slot("PERSON"),tracker.get_slot("time"),tracker.get_slot("time2"))
#         dispatcher.utter_message(
#             template=f"utter_",
#         )
#         return [
#         ]
#
#
# class TransferForm(FormAction):
#     """Transaction search form"""
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "transfer_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["PERSON"]
#
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "PERSON": [self.from_entity(entity="PERSON")],
#         }
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         DataUpdate(tracker.get_slot("PERSON"))
#         dispatcher.utter_message(
#             template="utter_name",
#         )
#         return [
#         ]



   # @staticmethod
    # def transactions_db() -> Dict[Text, Any]:
    #     """Database of transactions"""
    #     return {
    #         "spend": {
    #             "starbucks": [{"amount": 5.50}, {"amount": 9.10}],
    #             "amazon": [
    #                 {"amount": 35.95},
    #                 {"amount": 9.35},
    #                 {"amount": 49.50},
    #             ],
    #             "target": [{"amount": 124.95}],
    #         },
    #         "deposit": {
    #             "employer": [{"amount": 1250.00}],
    #             "interest": [{"amount": 50.50}],
    #         },
    #     }

        # @staticmethod
    # def vendor_name_db() -> List[Text]:
    #     return [
    #         "emergency",
    #         "target",
    #         "routine",
    #     ]
    # def validate_vendor_name(
    #     self,
    #     value: Text,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     """Validate vendor_name value."""
    #     if value and value.lower() in self.vendor_name_db():
    #         return {"vendor_name": value}
    #     else:
    #         dispatcher.utter_message(template="utter_no_vendor_name")
    #         return {"vendor_name": None}

            # transactions_subset = self.transactions_db().get(search_type, {})
        # vendor = tracker.get_slot("vendor_name")
        # if vendor:
        #     transactions = transactions_subset.get(vendor.lower())
        #     vendor = f" with {vendor}"
        # else:
        #     transactions = [
        #         v for k in list(transactions_subset.values()) for v in k
        #     ]
        #     vendor = ""
        # numtransacts = len(transactions)
        # total = sum([t.get("amount") for t in transactions])
import unittest

from pydantic import ValidationError

from domain.events import StrategyCreated


class TestStrategyCreated(unittest.TestCase):
    def test_strategy_created_correct_format(self) -> None:
        event = StrategyCreated(
            **{
                "data": {
                    "id": "242754ab-607c-4b14-a219-51234edf57c7",
                    "name": "Test Strategy",
                }
            }
        )
        self.assertEqual(event.subject, "242754ab-607c-4b14-a219-51234edf57c7")
        self.assertEqual(event.data.id, "242754ab-607c-4b14-a219-51234edf57c7")
        self.assertEqual(event.data.name, "Test Strategy")

    def test_strategy_created_incorrect_format(self) -> None:
        with self.assertRaises(ValidationError):
            StrategyCreated(
                **{
                    "data": {
                        "id": "242754ab-607c-4b14-a219-51234edf57c7",
                        "title": "Test Strategy",
                    },
                }
            )

    def test_strategy_created_data_id_key_missing(self) -> None:
        with self.assertRaises(ValidationError):
            StrategyCreated(
                **{
                    "data": {
                        "key": "242754ab-607c-4b14-a219-51234edf57c7",
                        "name": "Test Strategy",
                    },
                }
            )

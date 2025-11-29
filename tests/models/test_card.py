from tests.test_template import Test
from app.models.model_card import Card
from datetime import date


class TestCard(Test):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_cardConstructionAndDeletion(self):

        title = "teste"
        description = "card para testes"
        position = 1
        deadline = date(2025, 1, 1)
        column_id = 1
        public_work_id = 1

        card = Card(title, description, position,
                    deadline, column_id, public_work_id)

        id = card.getId()
        card_from_database: Card = Card.getById(id)

        self.assertEqual(card_from_database.getTitle(), title)
        self.assertEqual(card_from_database.getDescription(), description)
        self.assertEqual(card_from_database.getPosition(), position)
        self.assertEqual(card_from_database.getDeadline(), deadline)
        self.assertEqual(card_from_database.getColumnId(), column_id)
        self.assertEqual(card_from_database.getPublicWorkId(), public_work_id)

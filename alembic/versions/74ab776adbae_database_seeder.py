"""database_seeder

Revision ID: 74ab776adbae
Revises: 597a1d2b2cd6
Create Date: 2023-08-04 22:25:58.943529

"""
from alembic import op
import sqlalchemy as sa
from db.models.user import User
from db.models.food_waste_category import FoodWasteCategory
from db.models.advertisement import Advertisement

# revision identifiers, used by Alembic.
revision = "74ab776adbae"
down_revision = "597a1d2b2cd6"
branch_labels = None
depends_on = None

user_id = []
category_id = []
advertisement_id = []
users = [
    {
        "type": 3,
        "name": "Kenny Jinhiro",
        "username": "kjinhiro",
        "email": "kjinhiro@gmail.com",
        "phone_number": "12390785129",
        "password": "12345678",
    },
    {
        "type": 3,
        "name": "Nur Azizah",
        "username": "nazzh",
        "email": "nazzh@gmail.com",
        "phone_number": "12390785129",
        "password": "12345678",
    },
    {
        "type": 2,
        "name": "Achmad Rijalu",
        "username": "achjaluwae",
        "email": "achjaluwae@gmail.com",
        "phone_number": "12390785129",
        "password": "12345678",
    },
    {
        "type": 2,
        "name": "Michael Eko",
        "username": "ssabrut",
        "email": "ssabrut@gmail.com",
        "phone_number": "12390785129",
        "password": "12345678",
    },
]

categories = [{"name": "Buah-buahan"}, {"name": "Sayur-sayuran"}]
advertisements = [
    {
        "food_waste_category_id": category_id[0],
        "name": "Butuh kulit apel merah, saya beli dengan harga bersaing!",
        "additional_information": "",
        "price": 1000,
        "requested_weight": 50,
        "minimum_weight": 1,
        "maximum_weight": 50,
        "ongoing_weight": 14,
    },
    {
        "food_waste_category_id": category_id[0],
        "name": "Butuh kulit pisang, saya beli dengan harga bersaing!",
        "additional_information": "",
        "price": 1500,
        "requested_weight": 100,
        "minimum_weight": 1,
        "maximum_weight": 100,
        "ongoing_weight": 20,
    },
    {
        "food_waste_category_id": category_id[0],
        "name": "Butuh pisang layu, saya beli dengan harga bersaing!",
        "additional_information": "",
        "price": 2000,
        "requested_weight": 30,
        "minimum_weight": 1,
        "maximum_weight": 30,
        "ongoing_weight": 24,
    },
    {
        "food_waste_category_id": category_id[1],
        "name": "Butuh kangkung layu",
        "additional_information": "",
        "price": 500,
        "requested_weight": 20,
        "minimum_weight": 1,
        "maximum_weight": 20,
        "ongoing_weight": 9,
    },
]


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    for user_data in users:
        user = User(**user_data)
        session.add(user)
        session.flush()
        user_id.append(user.id)

    for category_data in categories:
        category = FoodWasteCategory(**category_data)
        session.add(category)
        session.flush()
        category_id.append(category.id)

    for advertisement_data in advertisements:
        advertisement = Advertisement(**advertisement_data)
        session.add(advertisement)
        session.flush()
        advertisement_id.append(advertisement.id)


def downgrade() -> None:
    pass

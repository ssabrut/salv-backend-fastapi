"""database_seeder

Revision ID: 74ab776adbae
Revises: 597a1d2b2cd6
Create Date: 2023-08-04 22:25:58.943529

"""
from alembic import op
import sqlalchemy as sa
from db.models.user import User
from db.models.user import Address
from db.models.food_waste_category import FoodWasteCategory
from db.models.advertisement import Advertisement
from db.models.education import Education
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision = "74ab776adbae"
down_revision = "597a1d2b2cd6"
branch_labels = None
depends_on = None

user_id = []
category_id = []
advertisement_id = []
education_id = []

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return password_context.hash(password)


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    users = [
        {
            "id": "f49fffcb-e225-4ba9-b15b-a1849df28a38",
            "type": 3,
            "name": "Kenny Jinhiro",
            "username": "kjinhiro",
            "email": "kjinhiro@gmail.com",
            "phone_number": "12390785129",
            "image": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/profile_picture%2Fimages.jpeg?alt=media&token=19bf4f4c-7b85-4654-97aa-4bdc40595505",
            "password": get_password_hash("12345678"),
            "point": 100000,
        },
        {
            "id": "8a830bb8-c94b-41ec-b622-a199d89f1b4a",
            "type": 3,
            "name": "Nur Azizah",
            "username": "nazzh",
            "email": "nazzh@gmail.com",
            "phone_number": "12390785129",
            "image": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/profile_picture%2Fdownload.jpeg?alt=media&token=ec1c095a-dd1d-4704-926e-58ef96c672a1",
            "password": get_password_hash("12345678"),
            "point": 50000,
        },
        {
            "id": "ee5e4eff-8b15-4a4f-88c5-acdcece4bfd7",
            "type": 2,
            "name": "Achmad Rijalu",
            "username": "achjaluwae",
            "email": "achjaluwae@gmail.com",
            "phone_number": "12390785129",
            "image": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/profile_picture%2Fimages%20(1).jpeg?alt=media&token=108314c9-d623-4a3b-87ae-d26bd6229301",
            "password": get_password_hash("12345678"),
            "point": 25000,
        },
        {
            "id": "fba673f6-80c8-4137-b1a0-0dca6f01e9ed",
            "type": 2,
            "name": "Michael Eko",
            "username": "ssabrut",
            "email": "ssabrut@gmail.com",
            "phone_number": "12390785129",
            "image": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/profile_picture%2Fpexels-pixabay-220453.jpg?alt=media&token=753566f5-5a30-4c30-9772-dda6db6e28e9",
            "password": get_password_hash("12345678"),
            "point": 75000,
        },
    ]

    for user_data in users:
        user = User(**user_data)
        session.add(user)
        session.flush()
        user_id.append(user.id)

    user_address = [
        {
            "user_id": "f49fffcb-e225-4ba9-b15b-a1849df28a38",
            "province": "Jawa Timur",
            "city": "Surabaya",
            "subdistrict": "Sambikerep",
            "ward": "Sambikerep",
            "address": "JL. Boulevard Utara",
            "postal_code": "60219",
        }
    ]

    for address_data in user_address:
        address = Address(**address_data)
        session.add(address)
        session.flush()

    categories = [
        {
            "id": "5017578d-7911-4cae-8538-d5e085a9e202",
            "name": "Buah-buahan",
            "image": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/dashboard_image%2Fdownload%20(1).jpeg?alt=media&token=98677b8d-855c-4ade-8925-d472be0f403f",
        },
        {
            "id": "407ac75b-d365-40a3-9d39-38ccdfc49b8b",
            "name": "Sayur-sayuran",
            "image": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/dashboard_image%2Fdownload-removebg-preview%20(2)%201.png?alt=media&token=eb14f631-6721-460d-bc93-733d0d195c0f",
        },
    ]

    for category_data in categories:
        category = FoodWasteCategory(**category_data)
        session.add(category)
        session.flush()
        category_id.append(category.id)

    advertisements = [
        {
            "id": "8c9d6b2d-5d65-44cc-8316-101b11ea2f61",
            "food_waste_category_id": category_id[0],
            "user_id": user_id[2],
            "name": "Butuh kulit apel merah, saya beli dengan harga bersaing!",
            "additional_information": "",
            "price": 1000,
            "requested_weight": 50,
            "minimum_weight": 1,
            "maximum_weight": 50,
            "ongoing_weight": 0,
        },
        {
            "id": "cfb4a1fd-865e-4deb-970c-7ed0e46042b9",
            "food_waste_category_id": category_id[0],
            "user_id": user_id[2],
            "name": "Butuh kulit pisang, saya beli dengan harga bersaing!",
            "additional_information": "",
            "price": 1500,
            "requested_weight": 100,
            "minimum_weight": 1,
            "maximum_weight": 100,
            "ongoing_weight": 0,
        },
        {
            "id": "4e349a84-c268-4837-b50f-51740732b920",
            "food_waste_category_id": category_id[0],
            "user_id": user_id[3],
            "name": "Butuh pisang layu, saya beli dengan harga bersaing!",
            "additional_information": "",
            "price": 2000,
            "requested_weight": 30,
            "minimum_weight": 1,
            "maximum_weight": 30,
            "ongoing_weight": 0,
        },
        {
            "id": "ae52cfde-322d-43f3-bfe0-7c0507d29b37",
            "food_waste_category_id": category_id[1],
            "user_id": user_id[3],
            "name": "Butuh kangkung layu",
            "additional_information": "",
            "price": 500,
            "requested_weight": 20,
            "minimum_weight": 1,
            "maximum_weight": 20,
            "ongoing_weight": 0,
        },
    ]

    for advertisement_data in advertisements:
        advertisement = Advertisement(**advertisement_data)
        session.add(advertisement)
        session.flush()
        advertisement_id.append(advertisement.id)

    educations = [
        {
            "id": "5e4423c5-a27b-4776-9d25-a4e9b8803b70",
            "food_waste_category_id": category_id[0],
            "title": "Jangan Dibuang, Begini Cara Memanfaatkan Kulit Apel",
            "content": """
        Dalam menyantap apel, beberapa orang memiliki caranya tersendiri. Ada yang lebih suka menyantapnya langsung bersama dengan kulitnya, ada pula yang lebih suka mengkonsumsi apel tanpa kulit buahnya.
Bagi orang-orang yang lebih memilih untuk menyantap apel dengan mengupasnya terlebih dahulu, kulit apel kerap terbuang sia-sia. Padahal, ‘bungkus’ dari buah sehat ini dapat dimanfaatkan kembali, lho. Bahkan, kulit apel juga dapat ‘disulap’ menjadi berbagai hidangan lezat.
Kira-kira, apa saja cara yang dapat digunakan untuk memanfaatkan kembali kulit apel agar tak dibuang begitu saja?
        """,
            "thumbnail": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/education_thumbnail%2Fgbthbevbpzvufoswup8w.jpg?alt=media&token=535316af-a98b-4949-897b-e09ccd44312c",
            "preparation": "Olah menjadi keripik",
            "implementation": "Kulit apel ternyata bisa diolah menjadi sajian keripik yang lezat, lho. Caranya pun tak sulit, cukup panggang kulit apel yang telah diolesi mentega dan kayu manis hingga teksturnya berubah menjadi renyah. Selain rasanya yang enak, keripik kulit apel ini juga bisa kamu santap sebagai kudapan sehat.",
            "video": "https://www.youtube.com/watch?v=AMa0tx8O0iU",
        },
        {
            "id": "a9cb519d-07dd-4a4a-ab52-53ab4387954d",
            "parent_id": "5e4423c5-a27b-4776-9d25-a4e9b8803b70",
            "food_waste_category_id": category_id[0],
            "title": "Jangan Dibuang, Begini Cara Memanfaatkan Kulit Apel",
            "content": """
        Dalam menyantap apel, beberapa orang memiliki caranya tersendiri. Ada yang lebih suka menyantapnya langsung bersama dengan kulitnya, ada pula yang lebih suka mengkonsumsi apel tanpa kulit buahnya.
Bagi orang-orang yang lebih memilih untuk menyantap apel dengan mengupasnya terlebih dahulu, kulit apel kerap terbuang sia-sia. Padahal, ‘bungkus’ dari buah sehat ini dapat dimanfaatkan kembali, lho. Bahkan, kulit apel juga dapat ‘disulap’ menjadi berbagai hidangan lezat.
Kira-kira, apa saja cara yang dapat digunakan untuk memanfaatkan kembali kulit apel agar tak dibuang begitu saja?
        """,
            "thumbnail": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/education_thumbnail%2Fgbthbevbpzvufoswup8w.jpg?alt=media&token=535316af-a98b-4949-897b-e09ccd44312c",
            "preparation": "Sajikan sebagai teh",
            "implementation": "Tak banyak yang tahu bila kulit dari buah yang kaya serat ini dapat disajikan sebagai teh, yang mampu menenangkan tubuh. Rebus air dengan campuran kulit apel, kayu manis, dan madu. Untuk mendapatkan warna merah jambu yang cantik, gunakan kulit apel yang berwarna merah sebagai bahan utamanya.",
            "video": "https://www.youtube.com/watch?v=oEhy8vCNKT8",
        },
        {
            "id": "d7fac099-8c43-4864-b2de-dd06dc8eb012",
            "parent_id": "5e4423c5-a27b-4776-9d25-a4e9b8803b70",
            "food_waste_category_id": category_id[0],
            "title": "Jangan Dibuang, Begini Cara Memanfaatkan Kulit Apel",
            "content": """
        Dalam menyantap apel, beberapa orang memiliki caranya tersendiri. Ada yang lebih suka menyantapnya langsung bersama dengan kulitnya, ada pula yang lebih suka mengkonsumsi apel tanpa kulit buahnya.
Bagi orang-orang yang lebih memilih untuk menyantap apel dengan mengupasnya terlebih dahulu, kulit apel kerap terbuang sia-sia. Padahal, ‘bungkus’ dari buah sehat ini dapat dimanfaatkan kembali, lho. Bahkan, kulit apel juga dapat ‘disulap’ menjadi berbagai hidangan lezat.
Kira-kira, apa saja cara yang dapat digunakan untuk memanfaatkan kembali kulit apel agar tak dibuang begitu saja?
        """,
            "thumbnail": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/education_thumbnail%2Fgbthbevbpzvufoswup8w.jpg?alt=media&token=535316af-a98b-4949-897b-e09ccd44312c",
            "preparation": "Sebagai garnish salad",
            "implementation": "Tekstur kulit apel yang renyah dapat membuat sajian salad terasa lebih lezat. Selain itu, kulit apel juga kaya akan serat sehingga semakin menambah nutrisi pada sajian salad. Kamu bisa menaburkan irisan tipis kulit apel atau bahkan mencampurkannya bersama bahan-bahan lain saat membuat salad.",
            "video": "https://www.youtube.com/watch?v=c-6sLFpsWUk",
        },
        {
            "id": "399597a0-9bd1-4f56-b1ba-d60c87b176a0",
            "food_waste_category_id": category_id[0],
            "title": "Ternyata Bisa Dimakan! Ini 5 Cara Mengolah Kulit Jeruk, dari Dikeringkan hingga Jadi Selai",
            "content": """
        Bukan hanya lezat, kulit jeruk juga miliki banyak kandungan gizi yang baik untuk kesehatan tubuh.
Kulit jeruk mengandung vitamin C yang jumlahnya tidak kalah dari buahnya. Selain vitamin C, ada juga kandungan serat yang baik untuk pencernaan.
Bahkan, ada juga kandungan zat kimia lain seperti polifenol, folat, riboflavin, thiamine, vitamin B6, dan kalsium.
Dengan mengolah kulit jeruk secara tepat, teman-teman bisa mendapatkan banyak manfaat dari gizi yang ada di dalam kulit jeruk.
Untuk mengolah kulit jeruk, ada beberapa cara yang bisa teman-teman coba.
        """,
            "thumbnail": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/education_thumbnail%2Fkulit-jeruk-memiliki-banyak-manf-20210712074534.jpg?alt=media&token=0dec0cef-3b5c-48bb-b145-060dd48168c9",
            "preparation": "Campuran Smoothies",
            "implementation": "Selain dikeringkan, teman-teman bisa mengolah kulit jeruk menjadi campuran smoothies. Campuran kulit jeruk ini akan memberikan aroma wangi jeruk dan rasa segar dari buah jeruk. Untuk membuatnya, teman-teman bisa menggunakan buah atau sayur lain dan tambahkan parutan kulit jeruk. Pastikan hanya memarut kulit pada bagian luar dan jangan campurkan bagian putih kulit jeruk. Parutan kulit jeruk ini jugu bisa teman-teman campurkan pada salad buah dan sayur.",
            "video": "https://www.youtube.com/watch?v=Hf9dv67PBd8",
        },
        {
            "id": "221dc18f-c991-4d4d-b07d-df033239ac54",
            "parent_id": "399597a0-9bd1-4f56-b1ba-d60c87b176a0",
            "food_waste_category_id": category_id[0],
            "title": "Ternyata Bisa Dimakan! Ini 5 Cara Mengolah Kulit Jeruk, dari Dikeringkan hingga Jadi Selai",
            "content": """
        Bukan hanya lezat, kulit jeruk juga miliki banyak kandungan gizi yang baik untuk kesehatan tubuh.
Kulit jeruk mengandung vitamin C yang jumlahnya tidak kalah dari buahnya. Selain vitamin C, ada juga kandungan serat yang baik untuk pencernaan.
Bahkan, ada juga kandungan zat kimia lain seperti polifenol, folat, riboflavin, thiamine, vitamin B6, dan kalsium.
Dengan mengolah kulit jeruk secara tepat, teman-teman bisa mendapatkan banyak manfaat dari gizi yang ada di dalam kulit jeruk.
Untuk mengolah kulit jeruk, ada beberapa cara yang bisa teman-teman coba.
        """,
            "thumbnail": "https://firebasestorage.googleapis.com/v0/b/salv-amcc.appspot.com/o/education_thumbnail%2Fkulit-jeruk-memiliki-banyak-manf-20210712074534.jpg?alt=media&token=0dec0cef-3b5c-48bb-b145-060dd48168c9",
            "preparation": "Cara Membuat Lilin dari Kulit Jeruk - DIY - Kreatif",
            "implementation": "Bahkan kulit jeruk juga bisa teman-teman olah menjadi permen. Untuk mengolah kulit jeruk ini, teman-teman cukup merebusnya hingga mendidih. Setelah mendidih, saring air lalu campurkan gula pada air rebusan tersebut dan diamkan selama 10 menit hingga satu jam. Air akan memadat dan bisa dipotong-potong menjadi ukuran kecil. Permen ini bisa menjadi camilan yang alami dan tidak membuat berat badan meningkat. Nah, itu tadi lima cara mengolah kulit jeruk dan mendapatkan manfaat di dalamnya. Teman-teman bisa menjadikan kulit jeruk sebagai camilan hingga minuman hangat atau dingin.",
            "video": "https://www.youtube.com/watch?v=98_tWh4EYIM",
        },
    ]

    for education_data in educations:
        education = Education(**education_data)
        session.add(education)
        session.flush()
        education_id.append(education.id)


def downgrade() -> None:
    pass

from db.models.education import Education
from db.models.food_waste_category import FoodWasteCategory
from sqlalchemy.orm import Session
from sqlalchemy import desc
import utils


async def index(db: Session, token: str):
    educations = (
        db.query(Education)
        .join(
            FoodWasteCategory, Education.food_waste_category_id == FoodWasteCategory.id
        )
        .filter(Education.parent_id == None)
        .order_by(desc(Education.created_at))
        .all()
    )

    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        for i in range(len(educations)):
            educations[i] = {
                "id": educations[i].id,
                "thumbnail": educations[i].id,
                "title": educations[i].title,
                "category": educations[i].food_waste_category.name,
                "created_at": educations[i].created_at,
            }
        return educations
    return utils.credentials_exception


async def get(education_id: str, db: Session, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        education = (
            db.query(Education)
            .join(
                FoodWasteCategory,
                Education.food_waste_category_id == FoodWasteCategory.id,
            )
            .with_entities(
                Education.id,
                Education.title,
                Education.created_at,
                Education.content,
                Education.preparation,
                Education.implementation,
                Education.video,
            )
            .first()
        )

        children = [
            {
                "id": education.id,
                "title": education.title,
                "created_at": education.created_at,
                "content": education.content,
                "preparation": education.preparation,
                "implementation": education.implementation,
                "video": education.video,
            }
        ]

        childs = []

        for child in (
            db.query(Education)
            .join(
                FoodWasteCategory,
                Education.food_waste_category_id == FoodWasteCategory.id,
            )
            .filter(Education.parent_id == education_id)
            .filter(Education.id != education_id)
            .with_entities(
                Education.id,
                Education.title,
                Education.created_at,
                Education.content,
                Education.preparation,
                Education.implementation,
                Education.video,
            )
            .all()
        ):
            childs.append(
                {
                    "id": child.id,
                    "title": child.title,
                    "created_at": child.created_at,
                    "content": child.content,
                    "preparation": child.preparation,
                    "implementation": child.implementation,
                    "video": child.video,
                }
            )

        for child in childs[::-1]:
            children.append(child)

        data = {
            "id": education.id,
            "title": education.title,
            "created_at": education.created_at,
            "content": education.content,
            "preparation": education.preparation,
            "implementation": education.implementation,
            "video": education.video,
            "children": children,
        }

        return data
    return utils.credentials_exception

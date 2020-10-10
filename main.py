from sqlalchemy.orm import selectinload

from db_utils.models import User
from segmentation import Segmentation
from db_utils.session_factory import SessionFactory

session_fact = SessionFactory()

with session_fact.session_scope() as session:
    # get user for which we need segments
    user = session.query(User).options(
        selectinload(User.order)
    ).options(selectinload(User.preference)).filter_by(name='Piyush').first()


    user = User(name="Ritesh")
    session.add(user)


    # init segmentation object
    segmentation = Segmentation()

    # get user segments
    print(segmentation.get_user_segments(user))



import logging
from typing import TypeVar, Generic, Optional, Type, List
from uuid import UUID

from sqlalchemy.orm import Session

from hackathon_la.model import Base
from hackathon_la.model.models import Car

T = TypeVar("T", bound=Base)

PAGE_DEFAULT_LIMIT = 20
PAGE_DEFAULT_OFFSET = 0


class _Repository(Generic[T]):
    """
    Base generic Repository class.
    """
    _LOG = logging.getLogger(__name__)

    def __init__(self, session: Session, model: Type[T]) -> None:
        self._session = session
        self._model = model

    def get(self, id_: UUID) -> Optional[T]:
        """
        Gets a resource with the specified ID or None.

        :param id_: the ID of the resource
        :return: the resource with the given ID or None
        """
        return self._session.query(self._model).get(id_)

    def find_one_or_none(self, **kwargs) -> Optional[T]:
        """
        Finds a resource with the given attributes and returns it. Returns
        None if no resource was found with the given filters.

        :param kwargs: the attributes to filter on
        :return: the found resource or None
        :raises MultipleResultsFound: if multiple results were found
        """
        query = self._filter_on(kwargs)
        return query.one_or_none()

    def find_all(self, **kwargs) -> List[T]:
        """
        Finds multiple resources with the given attributes and returns them.

        :param kwargs: the attributes to filter on
        :return: an array of objects
        """
        query = self._filter_on(kwargs)
        return query.all()

    def save(self, model: T) -> T:
        """
        Persist the object state to the database.

        :param model: the model instance to be persisted.
        """
        self._session.add(model)
        self._session.merge(model)
        return model

    def delete(self, model: T) -> None:
        """
        Deletes the model instance.

        :param model: the model instance to be deleted.
        """
        self._session.delete(model)

    def _filter_on(self, kwargs):
        query = self._session.query(self._model)
        for criterion, value in kwargs.items():
            if hasattr(self._model, criterion):
                column = getattr(self._model, criterion)
                query = query.filter(column == value)
            else:
                self._LOG.debug("{} has no attribute {}".format(
                    type(self._model).__name__, criterion))
        return query


class CarRepository(_Repository[Car]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Car)

    def get_car(self):
        return self._session.query(Car).all()[0]

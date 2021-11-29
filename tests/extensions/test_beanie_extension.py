from typing import List

import pymongo
import pytest
from beanie import Document, init_beanie
from beanie.odm.fields import Indexed, PydanticObjectId

from pydantic_factories.extensions import BeanieDocumentFactory


class MyDocument(Document):
    name: str
    index: Indexed(str, pymongo.DESCENDING)  # type: ignore
    siblings: List[PydanticObjectId]


class MyFactory(BeanieDocumentFactory):
    __model__ = MyDocument


@pytest.fixture(scope="function")
async def beanie_init(mongo_connection):
    await init_beanie(database=mongo_connection.db_name, document_models=[MyDocument])


@pytest.mark.asyncio
async def test_handling_of_beanie_types(beanie_init):
    result = MyFactory.build()
    assert result.name
    assert result.index
    assert isinstance(result.index, str)


@pytest.mark.asyncio
async def test_beanie_persistence_of_single_instance(beanie_init):
    result = await MyFactory.create_async()
    assert result.id
    assert result.name
    assert result.index
    assert isinstance(result.index, str)


@pytest.mark.asyncio
async def test_beanie_persistence_of_multiple_instances(beanie_init):
    result = await MyFactory.create_batch_async(size=3)
    assert len(result) == 3
    for instance in result:
        assert instance.id
        assert instance.name
        assert instance.index
        assert isinstance(instance.index, str)

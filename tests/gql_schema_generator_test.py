from uuid import UUID
from uuid import uuid4

from ariadne import QueryType
from pydantic import BaseModel

from gql_schema_generator import generate_gql_schema
from gql_schema_generator import GQLOperation
from gql_schema_generator import GQLSchema


class HelloMessage(BaseModel):
    body: str
    from_user: UUID


query = QueryType()


@query.field('hello')
def resolve_playgrounds(_, info) -> HelloMessage:
    return HelloMessage(from_user=uuid4(), body='Hello world')


def test_generate_gql_schema():
    expected_schema = GQLSchema(
        query=[
            GQLOperation(
                filed_name='hello',
                return_type='HelloMessage',
            ),
        ],
        user_defined_types={HelloMessage},
    )

    assert expected_schema == generate_gql_schema([query])


def test_gql_schema_to_string():
    schema = GQLSchema(
        query=[
            GQLOperation(
                filed_name='hello',
                return_type='HelloMessage',
            ),
        ],
        user_defined_types={HelloMessage},
    )

    expected_str = """type Query {
 hello:HelloMessage
 }
 type HelloMessage{
body: String
fromUser: ID
 }
 """

    assert (
        expected_str.strip() == schema.to_gql_schema_str().strip()
    )

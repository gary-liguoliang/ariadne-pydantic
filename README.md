# ariadne-pydantic
**Generate GraphQL schema from Pydantic for Ariadne**

I like the Python GraphQL lib `Ariadne`, which takes the "Schema First" approach.
developers have to define the schema and also write the python code to create a query. 

However,  if `Pydantic` is being used in your project, all the info required by a GQL schema
could be extracted from `Pydantic` definitions.  so I created this lib to generate GQL
schemas from `Pydantic` definitions. 

## Usage

```
class HelloMessage(BaseModel):
    body: str
    from_user: UUID


query = QueryType()


@query.field('hello')
def resolve_hello(_, info) -> HelloMessage:
    request = info.context['request']
    user_agent = request.headers.get('user-agent', 'guest')
    return HelloMessage(
        body='Hello, %s!' % user_agent,
        from_user=uuid4(),
    )


# Generate type_defs from Pydantic types in query definition.
type_defs = generate_gql_schema_str([query])

schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers,
)
app = GraphQL(schema, debug=True)
```

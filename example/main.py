import uvicorn
from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL

type_defs = gql("""
    type Query {
        hello: HelloMessage!
    }
        
    type HelloMessage {
        body: String!
        fromUser: String!
    }
""")

query = QueryType()

@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return {
        "body": "Hello, %s!" % user_agent,
        "fromUser": "Ariadne Server"
    }


schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")

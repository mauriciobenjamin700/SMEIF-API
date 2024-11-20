from utils.messages.messages import generate_responses_documentation, generate_response



doc = generate_responses_documentation(
    [
        generate_response(200, "Success"),
        generate_response(409, "CPF already exists")
    ]
)

print(doc)
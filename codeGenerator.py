from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Directly setting the OpenAI API key
openai.api_key = ''

base_output_dir = "D:\\json\\codeGenerate"

@app.route('/generate-code', methods=['POST'])
def generate_code():
    data = request.json

    # Extracting data from the request
    project_name = data.get("projectName", "defaultproject").lower()
    model_name = data.get("modelName", "DefaultModel")
    fields = data.get("fields", [])
    repository_name = data.get("repositoryName", "DefaultRepository")
    service_name = data.get("serviceName", "DefaultService")
    controller_name = data.get("controllerName", "DefaultController")
    request_class_name = data.get("requestClassName", "DefaultRequest")
    main_class_name = data.get("mainClassName", "DefaultApplication")

    # Define prompts for generating code using OpenAI API
    prompts = {
        "model_class": f"Generate a Java model class for the following metadata:\nModel Name: {model_name}\nFields: {fields}\n",
        "repository_class": f"Generate a Java repository interface for the model class {model_name}.\n",
        "service_class": f"Generate a Java service class for the model class {model_name} and repository {repository_name}.\n",
        "controller_class": f"Generate a Java controller class for the service class {service_name}.\n",
        "request_class": f"Generate a Java request class for the model class {model_name}.\n",
        "main_class": f"Generate a Java main class named {main_class_name} with Spring Boot annotations.\n"
    }

    generated_code = {}
    for key, prompt in prompts.items():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        generated_code[key] = response.choices[0].message['content'].strip()

    # Create project directory if it doesn't exist
    project_dir = os.path.join(base_output_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)

    # File saving logic
    file_mapping = {
        "model_class": f"{model_name}.java",
        "repository_class": f"{repository_name}.java",
        "service_class": f"{service_name}.java",
        "controller_class": f"{controller_name}.java",
        "request_class": f"{request_class_name}.java",
        "main_class": f"{main_class_name}.java"
    }

    for key, filename in file_mapping.items():
        file_path = os.path.join(project_dir, filename)
        with open(file_path, 'w') as f:
            f.write(generated_code[key])

    return jsonify({"message": "Code generated and saved successfully", "generated_code": generated_code})

if __name__ == '__main__':
    app.run(debug=True)

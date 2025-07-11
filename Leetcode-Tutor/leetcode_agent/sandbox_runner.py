import docker

def run_code_in_docker(code: str, test_case: str) -> str:
    client = docker.from_env()
    try:
        full_code = f"{code}\nprint({test_case})"
        output = client.containers.run(
            "python:3.10-slim",
            f"python3 -c \"{full_code}\"",
            remove=True,
            network_disabled=True,
            mem_limit="50m",
            stdout=True,
            stderr=True
        )
        return output.decode()
    except Exception as e:
        return f"Execution error: {e}"

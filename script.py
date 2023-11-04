import yaml, requests, sys
from time import sleep


class RasaWebhookTestScript:
    def __init__(self, url, file, output_file):
        self.url = url
        self.file = file
        self.output_file = output_file

    def open_file(self):
        try:
            self.clear_file()
            with open(self.file, "r") as file:
                file_data = yaml.safe_load(file)
                self.loop_intents(file_data.get("nlu"))
        except Exception as e:
            print(f"Unexpected {e}, {type(e)}")

    def write_output(self, i, e):
        try:
            with open(self.output_file, "a") as file:
                file.write(f"\nIntent: {i}, Example: {e}")
        except Exception as e:
            print(f"Unexpected {e}, {type(e)}")

    def clear_file(self):
        try:
            with open(self.output_file, "w") as file:
                pass
        except Exception as e:
            print(f"Unexpected {e}, {type(e)}")

    def loop_intents(self, intents):
        print("Start requesting to the Rasa REST API...\n")
        for intent in intents:
            examples = yaml.safe_load(intent["examples"])
            for example in examples:
                params = {"message": example}
                response = requests.post(self.url, json=params)
                if response.status_code == 200:
                    if len(response.json()) == 0:
                        self.write_output(intent["intent"], example)
                        print("Failed")
                    else:
                        print("Success")
                else:
                    print(f"Error: {response.status_code}")
                sleep(1)
        print("\nTest Finished. Please check the output file!")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python script.py <rasa_rest_api_url> <nlu_file_path> <output_filename>"
        )
        sys.exit(1)
    test = RasaWebhookTestScript(sys.argv[1], sys.argv[2], sys.argv[3])
    test.open_file()

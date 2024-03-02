## Explaination
db_config.py: collection for variables that might need to be changed based on the user.
logg_creation.py: Meant to be run on its own. Does the Excel transfer, inserts the logg into the database and wipes the CSV.
main.py: Meant only to be run on demand. Includes everything related to user input and everything except handling of the logg files. 


## Configuration
- In db_config.py are the variables for the mySQL connector, database name and MongoDB configuration options.

### How to run
1. Create a MySQL container and a MongoDB container. I recommend using programs such as Docker to do this.
2. Create an Virtual environment by running this in the terminal:
    ```
    python -m venv venv
    ```
3. Activate the virtual environment by running the following commands in the terminal:
    - On Windows:
        ```
        .\venv\Scripts\Activate
        ```
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```
4. Install the requirements:
    ```
    pip install -r requirements.txt
    ```
5. Run logg_creation.py using VS-code or terminal
    ```
    py logg_creation.py
    ```
    ```
    python logg_creation.py
    ```
6. In another terminal run main.py
    ```
    py main.py
    ```
    ```
    python main.py
    ```
7. Use the program as you wish.


import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


class EnergyAgent:
    def __init__(self, csv_path, api_key):
        try:
            self.df = pd.read_csv(csv_path)
            print(f"Data loaded: {len(self.df)} rows.")
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.df = pd.DataFrame()

        # Connect to Gemini 2.5 Flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )

        # Create the agent
        self.agent = create_pandas_dataframe_agent(
            llm=self.llm,
            df=self.df,
            verbose=False,
            allow_dangerous_code=True,
            agent_executor_kwargs={"handle_parsing_errors": True}
        )

    def ask(self, user_query):
        try:
            full_query = f"{user_query}\n\nanalyze only the provided dataframe"
            response = self.agent.invoke(full_query)
            return response["output"]
        except Exception as e:
            return f"An error occurred while processing the request: {e}"

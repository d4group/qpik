# from crewai.tools import BaseTool
# from typing import Type
# from pydantic import BaseModel, ConfigDict, Field

# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

#     # Ustawienia konfiguracyjne dla Pydantic V2
#     model_config = ConfigDict(
#         extra='forbid'  # Nie pozwalaj na dodatkowe atrybuty
#     )

# class MyCustomTool(BaseTool):
#     name: str = "My Custom Tool"
#     description: str = (
#         "Clear description for what this tool is useful for; your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return f"This is an example of a tool output for argument: {argument}"

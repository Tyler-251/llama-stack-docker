import os
import json
from llama_stack_client.lib.agents.custom_tool import CustomTool
from llama_stack_client.types import ToolResponseMessage, UserMessage
from llama_stack_client.types.tool_param_definition_param import ToolParamDefinitionParam
from llama_stack_client.types import FunctionCallToolDefinition

class StoryTeller(CustomTool):
    def get_name(self) -> str:
        """Returns the name of the tool."""
        return "story_teller"

    def get_description(self) -> str:
        """Returns the description of the tool."""
        return "Generate a story."

    def get_type(self) -> str:
        """Returns the type of the tool."""
        return "function_call"
    
    def get_instruction_string(self) -> str:
        """Returns the instruction string for the tool."""
        return f"Use the function '{self.get_name()}' to: {self.get_description()}"

    def parameters_for_system_prompt(self) -> str:
        """Returns the parameters for the system prompt in JSON format."""
        return json.dumps(
            {
                "name": self.get_name(),
                "description": self.get_description(),
                "parameters": {name: definition.__dict__ for name, definition in self.get_params_definition().items()},
            }
        )
    
    def get_tool_definition(self) -> FunctionCallToolDefinition:
        """Returns the tool definition."""
        return FunctionCallToolDefinition(
            type="function_call",
            function_name=self.get_name(),
            description=self.get_description(),
            parameters=self.get_params_definition(),
        )

    def get_params_definition(self) -> dict[str, ToolParamDefinitionParam]:
        """Returns the parameters definition for the tool."""
        return {
            "story_name": ToolParamDefinitionParam(
                param_type="str",
                default="any story",
                description="The name of the story to generate.",
                required=True
            )
        }

    def run(self, messages: list[UserMessage]) -> list[ToolResponseMessage]:
        """Runs the tool with the given messages."""
        tool_call = self._find_tool_call(messages)
        if tool_call:
            story_name = tool_call.arguments.get('story_name', 'any story')
            response = ToolResponseMessage(
                role="ipython",
                tool_name=self.get_name(),
                content={
                    "type": "text",
                    "text": f"mock response from tool {self.get_name()} for {story_name}"
                },
                call_id=tool_call.call_id,
            )
            messages.append(response)
            return [response]
        return []

    def _find_tool_call(self, messages: list[UserMessage]):
        """Finds the tool call in the given messages."""
        for message in reversed(messages):
            if hasattr(message, 'tool_calls'):
                for tool_call in message.tool_calls:
                    if tool_call.tool_name == self.get_name():
                        return tool_call
        return None
# Demonstration 15: Creating Tools with @tool
## Scenario
Imagine you’re getting ready for your next trip. You want quick answers to simple questions. Where should I go? What should I pack? How long is the flight? But every time you look these up, you end up jumping between websites, comparing lists, or relying on memory.
To make this easier, you decide to build a **Simple Travel Helper Agent**, a beginner-friendly assistant that can answer these everyday travel questions instantly. It will have a list of tools that handle one specific task, making the system simple, predictable, and perfect for learning the fundamentals of tool calling before moving on to real-world integrations later in the course.
## Problem Statement
Create an autonomous travel helper that can use multiple internal tools to provide quick, structured answers to common travel queries. The agent should be able to:
- Suggest popular destinations for a given country
- Estimate approximate flight times between cities (using mock data)
- Recommend a packing list based on trip duration
- Offer rough budget ranges for different destinations
All tools must be defined in Python using the @tool decorator and integrated into an agent built with create_agent.
## What You Will Learn
1. Core Tool Fundamentals
- How to define custom tools using the @tool decorator
- How type hints automatically generate input schemas for tools
- How meaningful docstrings help the model understand when to use each tool
- How to assign custom tool names for clarity and better model reasoning

2. Integrating Tools Into the Agent
- How to register multiple tools inside the create_agent framework
- How the agent decides which tool to invoke based on the user’s request

3. Observing Tool Invocation
- How the model automatically selects tools during conversation
- How multiple simple tools can collaborate inside a single agent
- How improved tool descriptions enhance tool selection ac

# **Demonstration 16: Integrating External Tools into Your Agent**

## **Scenario**

In the previous lesson, you built a simple travel helper that relied entirely on internal Python tools with mock data. Real travelers want **real information**, not static values.

They want:

- fresh weather data  
- real flight prices  
- live search results  
- updated city guides  
- and more

To take your Simple Travel Helper Agent one step closer to a practical application, you now want it to integrate with **external tools**. These services will fetch real, up-to-date information from the outside world.

## **Problem Statement**

Upgrade your existing travel helper into a more powerful and realistic agent by connecting it to **external APIs or services**. Instead of relying only on Python functions with mock data, the agent should now be able to:

- Fetch **real-time weather** for any destination  
- Perform **web search** to gather live travel information  
- Query external APIs (e.g., **flight info, events, attractions**)  
- Combine internal and external tools to answer richer queries  

The external tools should be properly defined, registered, and integrated into the **create_agent** framework so the agent can decide **when to call them** and **how to combine their results** with internal tools.

## **What You Will Learn**

### **1. Understanding External Tools**
- What external tools are and how they differ from internal Python tools  
- How external tools enable real-time, dynamic, and up-to-date responses  
- When and why to use an external tool instead of a local function  

### **2. Integrating External APIs as Tools**
- How to wrap an external API call inside a Python function  
- How to convert that function into a tool using the `@tool` decorator  
- How to safely handle input schemas and API responses  

### **3. Registering External Tools With `create_agent`**
- How to include external tools **alongside internal tools**  
- How to provide tool descriptions that help the agent pick the right tool  
- How the agent chooses between internal vs external tools based on user intent  

### **4. Observing External Tool Usage**
- How the agent automatically invokes external tools during conversation  
- How external tools and internal tools work together  
- How to debug tool invocation when using external API calls  


#!/usr/bin/env python
# coding: utf-8

# In[20]:


import os
from crewai import Crew, Agent, LLM, Task, Process
from crewai_tools import BaseTool
from langchain_openai import AzureChatOpenAI
from langchain.agents import Tool

import warnings
warnings.filterwarnings('ignore')


# In[3]:


llm_4o = LLM(
    model="azure/gpt-4o",
    base_url="https://genai-openai-ai-mazinghacktivists.openai.azure.com/",
    api_key="446cd4ef4aad49e097e94e63a0593be2"
)


# In[76]:


from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict


# In[77]:


class CustomHandler(BaseCallbackHandler):
    """A custom handler for logging interactions within the process chain."""
    
    def __init__(self, agent_name: str) -> None:
        super().__init__()
        self.agent_name = agent_name

    def on_chain_start(self, serialized: Dict[str, Any], outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Log the start of a chain with user input."""
        st.session_state.messages.append({"role": "assistant", "content": outputs['input']})
        st.chat_message("assistant").write(outputs['input'])
        
    def on_agent_action(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """""Log the action taken by an agent during a chain run."""
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs['input'])
        
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Log the end of a chain with the output generated by an agent."""
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name).write(outputs['output'])


# In[78]:


business_agent = Agent(
    role="Senior Business Analyst",
    goal="Identify key risks and RWA optimization opportunities.",
    backstory="""You are a senior business analyst in barclays credit risk department. You are responsible for analyzing RWA related data for optimization of RWA.
    You are currently working on  a project to review the business data, check for any discrepancies, and suggest adjustments that could reduce RWA. You should
    focus on asset classifications, exposure amounts, and credit ratings.
    """,
    allow_delegation=False,
    llm=llm_4o,
    callbacks=[CustomHandler("Senior Business Analyst")],
    verbose=True,
)


# In[80]:


data_standardization_agent = Agent(
    role="Senior Data Standardization Advisor",
    goal="Ensure all reference data is standardized",
    backstory="""You are a senior  Data Standardization Advisor in barclays credit risk department. You are responsible for ensuring that all reference data
    is consistent across different formats. You are currently working on a project to convert all currency, date, asset type etc to a standard model
    to ensure correct risk-weighting classifications.
    """,
    allow_delegation=False,
    llm=llm_4o,
    callbacks=[CustomHandler("Senior Data Standardization Advisor")],
    verbose=True,
)


# In[81]:


anomaly_detection_agent = Agent(
    role="Senior Anomaly Detection Analyst",
    goal="Flag inconsistencies and outliers that could impact RWA.",
    backstory="""You are a senior Anomaly Detection Analyst in barclays credit risk department. You are responsible to identify any irregularies or anomalies
    in the data. You are currently working on a project to look for outlier values in exposure, credit ratings, and other key RWA metrics that could indicate data 
    issue and adversly impact RWA.
    """,
    allow_delegation=False,
    llm=llm_4o,
    callbacks=[CustomHandler("Senior Anomaly Detection Analyst")],
    verbose=True,
)


# In[82]:


customer_segmentation_agent = Agent(
    role="Senior Customer Segmentation Analyst",
    goal="Segment customer on the basis of risk profile, credit ratings etc",
    backstory="""You are a senior Customer Segmentation Analyst in barclays credit risk department. You are responsible to provide RWA optimization using 
    segmentation and capital optimization strategies based on customer profiles. You are currently working on a project to segment customers on the basis of
    credit ratings, loan types, industry and loan term and provide strategy to optimize RWA.
    """,
    allow_delegation=False,
    llm=llm_4o,
    callbacks=[CustomHandler("Senior Customer Segmentation Analyst")],
    verbose=True,
)


# In[64]:


rwa_optimization_agent = Agent(
    role="RWA Optimization Advisor",
    goal="Offers targeted recommendations to reduce RWA and suggest optimized capital allocation.",
    backstory="""You are a senior RWA Optimization Advisor at Barclays Bank PLC, skilled in providing RWA Optimization 
    strategies. Your job  is to provide strategies for minimizing RWA, recommend actions such as asset reclassification, securitization ,
    or reducing exposure high-risk assets. Besides, your job is to suggest optimized capital allocation to minimize RWA while managing risk exposure.
    """,
    allow_delegation=False,
    llm=llm_4o
)


# In[65]:


rwa_optimization_task = Task(
    description="Summarize all the RWA optimization suggestion",
    expected_output="A bullet list summary of top 10 most important RWA and capital allocation Optimization and all the points are explained properly.",
    agent = rwa_optimization_agent
)


# In[ ]:





# In[72]:



# In[7]:


import streamlit as st


# In[83]:


# Streamlit UI setup
st.title("💬 RWA Optima") 

# Initialize the message log in session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "In which scenario you want me to optimize RWA?"}]

# Display existing messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Define tasks for each agent
    

    business_analysis_task = Task(
        description=f"""Analyze the user input '{prompt}' and identify key risks and RWA optimization opportunities.""",
        expected_output="A bullet list summary of top 10 most important RWA Optimization opportunities.",
        agent = business_agent
    )

    data_standardization_task = Task(
        description=f"""Analyze the user input '{prompt}', and identify reference data standardization opportunity 
        so that correct risk weighting classification can be done.""",
        expected_output="A bullet list summary of top 10 most important reference data standardization opportunity.",
        agent = data_standardization_agent
    )
    
    anomaly_detection_task = Task(
        description=f"""Analyze the user input '{prompt}', and flag inconsistencies and outliers that could adversly impact RWA.""",
        expected_output="A bullet list summary of top 10 most important anomalies related with key RWA metrics.",
        agent = anomaly_detection_agent
    )
    
    customer_segmentation_task = Task(
        description=f"""Analyze the user input '{prompt}', and provide suggestions for RWA and capital optimization opportunities using customer segmentation.""",
        expected_output="A bullet list summary of top 10 most important RWA and capital optimization opportunities using customer segmentation. ",
        agent = customer_segmentation_agent
    )
    
    # Set up the crew and process tasks hierarchically
    project_crew = Crew(
        tasks=[business_analysis_task,data_standardization_task,anomaly_detection_task,customer_segmentation_task],
        agents=[business_agent,data_standardization_agent,anomaly_detection_agent,customer_segmentation_agent],
        process=Process.hierarchical,
        manager_llm=llm_4o,
        manager_callbacks=[CustomHandler("Crew Manager")],
        verbose=True
    )
    final = project_crew.kickoff()

    # Display the final result
    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)


# In[ ]:





from promptflow import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need


@tool
def llama_or_oai(llama_answer: str, oai_answer: str, llama_or_oai:bool) -> str:
  if llama_or_oai:
    return llama_answer
  else:
    return oai_answer
import subprocess
import yaml
import re
import os

def log(msg):
    print(msg)
    print('')

with open('interviews/harlan01.yml', 'r') as file:
    data = yaml.safe_load(file)

interviewer = data['interviewer']
interviewee = data['interviewee']
topics = data['topics']
log(f"Interviewer: {interviewer}")
log(f"Interviewee: {interviewee}")
log(f"Topics: {topics}")

system_prompt = f"""{interviewer['instructions']}

You are interviewing {interviewee['name']} about the following topics - listed in order of importance: {'; '.join(topics)}.

Here is the background information you have on {interviewee['name']}: {'; '.join(interviewee['background'])}.
"""

system_prompt = re.sub(r'\s+', ' ', system_prompt)

cmd_gen_question = f"llm --model gpt-4-1106-preview --system '{system_prompt}' 'Ask me a question.'"
log(f"cmd_gen_question: {cmd_gen_question}")

process = subprocess.run(cmd_gen_question, shell=True, check=True, text=True, capture_output=True)
question = process.stdout.strip()
log(f"Question: {question}")

cmd_speak_question = f"ospeak -v nova '{question}'"
log(f"cmd_speak_question: {cmd_speak_question}")
os.system(cmd_speak_question)

#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import re
import shlex
import subprocess
import sys
import yaml

MODEL ="llamafile"
# MODEL ="gpt-4-1106-preview"

def main():
    load_dotenv()
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

    cmd_gen_question = ["llm", "--model", MODEL, "--system", system_prompt, "Ask me a question."]
    log(f"cmd_gen_question: {shlex.join(cmd_gen_question)}")

    process = subprocess.run(cmd_gen_question, text=True, capture_output=True)
    if process.returncode != 0:
        print(process.stdout, file=sys.stdout)
        print(process.stderr, file=sys.stderr)
        sys.exit(1)

    question = process.stdout.strip()
    log(f"Question: {question}")

    cmd_speak_question = ["ospeak", "-v", "nova", question]
    log(f"cmd_speak_question: {shlex.join(cmd_speak_question)}")
    # hm, if we pipe the llm output to ospeak, would we get the first words much faster??
    process = subprocess.run(cmd_speak_question, text=True, capture_output=False, stderr=subprocess.STDOUT)
    if process.returncode != 0:
        print(process.stdout, file=sys.stdout)
        print(process.stderr, file=sys.stderr)
        sys.exit(1)


def log(msg):
    print(f"{msg}\n")

if __name__ == "__main__":
    main()

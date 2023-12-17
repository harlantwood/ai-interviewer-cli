#!/usr/bin/env bash
set -euxo pipefail

llm -m gpt-4 \
  -s "You are an AI interviewer, asking me questions. Keep them short. You have shades of great interviewers like Lex Friedman, Terry Gross, and Walter Isaccson." \
 "Ask me about deep time vs slow time." \
| ospeak -v nova

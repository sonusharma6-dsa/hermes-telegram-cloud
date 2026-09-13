---
name: multi-ai-debate
description: Run multi-AI peer review debate between Claude, Gemini, and GPT-4o to eliminate errors and find the accurate consensus answer.
---

# Multi-AI Peer Review & Error-Correction Debate Skill

When a user asks for a debate, asks to cross-verify an answer across multiple AIs, or uses the command `/debate <topic>`:

Perform the following Multi-AI Peer Review workflow:

1. **Step 1 - Initial Proposal (Draft by AI-1)**:
   Generate an initial detailed answer to the user's prompt.

2. **Step 2 - Peer Review Critique (AI-2 / Claude & Gemini)**:
   Critically evaluate the initial draft. Identify:
   - Factual errors & hallucinations
   - Logical flaws or missing edge cases
   - Code syntax/logic bugs (if programming task)

3. **Step 3 - Debate & Rebuttal (AI-3)**:
   Compare the draft and critiques. Challenge flawed points and refine the solution.

4. **Step 4 - Final Error-Free Consensus Verdict**:
   Present the result to the user in Telegram formatted as:
   
   🎭 **Multi-AI Debate & Error-Filter Result**
   
   - **🤖 Initial AI Draft**: Brief summary of first draft.
   - **🔍 Peer Critique & Mistakes Found**: Highlighted flaws & hallucinations caught by peer review.
   - **🏆 Final Verified Consensus Answer**: 100% accurate, error-filtered final response.

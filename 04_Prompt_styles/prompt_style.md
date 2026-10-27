# prompt_formats_reference

# LLM Prompt Formats & Templating Reference

A reference guide outlining the standard prompt formatting styles used across open-source and proprietary large language models.
 wsl --shutdown
wsl --shutdown
---

## 1. Alpaca Format

Developed by Stanford for instruction-tuning models like Stanford Alpaca (LLaMA-7B derivative). It divides task specifications into explicit instructions, contextual inputs, and the desired completion trigger.

### Standard Template

```
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
<SYSTEM_PROMPT_OR_TASK_DESCRIPTION>

### Input:
<USER_QUERY_OR_CONTEXT>

### Response:
```

### Template Without Input

When no additional context or data payload is required:

```
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
<USER_QUERY>

### Response:
```

---

## 2. ChatML (Chat Markup Language)

Introduced by OpenAI to standardize multi-turn dialogue, distinguish system/developer instructions from untrusted user input, and prevent prompt injection vulnerabilities.

### Special Tokens Template

```
<|im_start|>system
<SYSTEM_PROMPT><|im_end|>
<|im_start|>user
<USER_QUERY><|im_end|>
<|im_start|>assistant
<MODEL_RESPONSE><|im_end|>
```

### Structured JSON Representation

When interacting with API SDKs, ChatML is typically represented as a structured array of message objects:

```json
[
  {
    "role": "system",
    "content": "You are a concise technical documentation assistant."
  },
  {
    "role": "user",
    "content": "Explain the difference between mutable and immutable data structures."
  },
  {
    "role": "assistant",
    "content": "Mutable objects can be modified after creation, while immutable objects cannot."
  }
]
```

---

## 3. LLaMA & Mistral `[INST]` Format

Used by Meta’s LLaMA 2 / LLaMA 3 instruction models and Mistral AI’s base instruction models.

### Single-Turn Template

```
<s>[INST] <<SYS>>
<SYSTEM_PROMPT>
<</SYS>>

<USER_QUERY> [/INST]
```

### Multi-Turn Template

In multi-turn conversations, the system prompt is only included in the initial turn. Subsequent turns alternate between user inputs in `[INST] ... [/INST]` tags and plain assistant responses:

```
<s>[INST] <<SYS>>
You are an expert software engineer.
<</SYS>>

Write a JavaScript function to reverse an array in place. [/INST]
function reverseArray(arr) {
  let left = 0;
  let right = arr.length - 1;
  while (left < right) {
    [arr[left], arr[right]] = [arr[right], arr[left]];
    left++;
    right--;
  }
  return arr;
}
</s><s>[INST] What is its space complexity? [/INST]
The space complexity is O(1) auxiliary space because it reverses the array in place without allocating additional memory. </s>
```

---

## 4. Structured Chain of Thought (CoT) Prompt Pattern

When building autonomous agents or reasoning pipelines, prompts can be structured to enforce explicit step-by-step thinking prior to producing the final answer.

### Schema Definition

```json
{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": "string"
}
```

### Pipeline Flow

1. **`START`**: Acknowledges and parses the incoming problem parameters.
2. **`PLAN`**: Iterative, single-step reasoning, calculations, or logic verification.
3. **`OUTPUT`**: Final synthesized response provided to the user.
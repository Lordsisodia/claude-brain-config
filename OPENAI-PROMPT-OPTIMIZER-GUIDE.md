# 🧠 OpenAI Framework-Based Prompt Optimizer for Claude Code

## Overview

This system automatically rewrites your Claude Code prompts using OpenAI's proven prompting framework, transforming vague requests into structured, highly-effective prompts that get better results.

## 🚀 Quick Start

### Activate the Optimizer
```bash
~/.claude/scripts/activate-openai-optimizer.sh on
```

### Check Status
```bash
~/.claude/scripts/activate-openai-optimizer.sh status
```

### Test the System
```bash
~/.claude/scripts/activate-openai-optimizer.sh test
```

### Deactivate
```bash
~/.claude/scripts/activate-openai-optimizer.sh off
```

## 🎯 What It Does

### Before Optimization
```
"fix this bug"
```

### After Optimization
```markdown
# Role and Objective
You are an expert debugging assistant specializing in software engineering. Your primary goal is to identify, analyze, and provide precise solutions for code issues.

fix this bug

# Instructions  
- Analyze the problem systematically using a debugging methodology
- Identify root cause rather than treating symptoms
- Provide step-by-step troubleshooting approach
- Test hypotheses before implementing fixes

## Debugging Process
1. **Understand**: Read error messages and stack traces carefully
2. **Isolate**: Identify the specific component or function causing issues  
3. **Hypothesize**: Form theories about potential causes
4. **Test**: Verify theories with minimal code changes
5. **Fix**: Implement the most targeted solution
6. **Verify**: Confirm the fix resolves the issue completely

## Output Format
- Start with problem analysis
- Show exact code changes needed
- Explain why the fix addresses the root cause

---
**Important**: Please work through this systematically and don't stop until the task is completely resolved. Use available tools to gather information rather than making assumptions.

*🧠 Optimized using OpenAI Prompting Framework | Enhanced by Claude Code Intelligence*
```

## 🔧 How It Works

The optimizer applies OpenAI's 5 core rules:

### 1. **Clear Role Definition**
- Detects task type (debugging, UI, API, etc.)
- Assigns appropriate expert persona
- Sets clear objectives

### 2. **Specific Instructions**
- Adds concrete, actionable guidelines
- Includes quality requirements
- Provides workflow structure

### 3. **Chain of Thought**
- Adds systematic reasoning steps for complex tasks
- Encourages explicit planning
- Promotes step-by-step thinking

### 4. **Context & Examples**
- Discovers relevant project files
- Adds project-specific context
- Includes existing patterns to follow

### 5. **Output Format**
- Structures expected response format
- Provides clear delivery guidelines
- Ensures consistent results

## 📊 Analytics & Learning

### View Optimization Logs
```bash
tail -f ~/.claude/logs/openai-optimizer.log
```

### Check Analytics
```bash
ls ~/.claude/cache/openai-optimizer/
cat ~/.claude/analytics/enhancement-metrics.csv
```

### Analysis Data
The system tracks:
- Original vs optimized prompt length
- Task type detection accuracy
- Context discovery effectiveness
- User satisfaction patterns

## 🎛️ Configuration

### Current Hook Configuration
Located in: `~/.claude/settings.hooks.openai-enhanced.json`

The optimizer runs on every `UserPromptSubmit` with:
- 20-second timeout
- Prompt modification enabled
- Detailed logging

### Customize Optimization Rules

Edit the optimizer script:
```bash
nano ~/.claude/scripts/openai-prompt-optimizer.sh
```

Key sections to customize:
- **Role Detection** (line ~45): Add new task types
- **Context Discovery** (line ~120): Modify file search patterns  
- **Project Context** (line ~150): Add project-specific rules
- **Output Formats** (line ~200): Customize response structures

## 🧪 Testing & Validation

### Test Different Prompt Types
```bash
# Test vague prompts
~/.claude/scripts/openai-prompt-optimizer.sh "help me"

# Test specific tasks  
~/.claude/scripts/openai-prompt-optimizer.sh "create user authentication API"

# Test debugging requests
~/.claude/scripts/openai-prompt-optimizer.sh "fix the login error"
```

### Validate Improvements
1. **Before/After Comparison**: Check `~/.claude/cache/openai-optimizer/last-*.txt`
2. **Effectiveness Metrics**: Review log files for success rates
3. **User Experience**: Monitor Claude Code response quality

## 🔄 Integration with Existing System

The optimizer works alongside your existing enhancement system:

1. **OpenAI Optimizer** (Primary): Restructures prompt using proven framework
2. **Context Enhancer** (Secondary): Adds project-specific context
3. **Security Validator**: Validates safety
4. **Session Intelligence**: Tracks patterns

## 📈 Performance Impact

### Typical Improvements
- **Prompt Length**: 500-2000% expansion with structured content
- **Response Quality**: More precise, actionable answers
- **Task Completion**: Better Claude Code tool usage
- **Consistency**: Standardized prompt structure

### Metrics Tracking
```bash
# View enhancement metrics
column -t -s',' ~/.claude/analytics/enhancement-metrics.csv | head -10
```

## 🚨 Troubleshooting

### Optimizer Not Running
```bash
# Check if hooks are active
grep -q "openai-prompt-optimizer" ~/.claude/settings.hooks.json && echo "Active" || echo "Inactive"

# Verify script permissions
ls -la ~/.claude/scripts/openai-prompt-optimizer.sh
```

### Optimization Errors
```bash
# Check logs for errors
grep "ERROR" ~/.claude/logs/openai-optimizer.log

# Test manually
~/.claude/scripts/openai-prompt-optimizer.sh "test prompt"
```

### Performance Issues
```bash
# Check timeout settings in hooks
grep -A 5 "openai-prompt-optimizer" ~/.claude/settings.hooks.json

# Monitor execution time
time ~/.claude/scripts/openai-prompt-optimizer.sh "test prompt"
```

## 🎨 Customization Examples

### Add New Task Type
```bash
# Edit the role detection section
nano ~/.claude/scripts/openai-prompt-optimizer.sh

# Add after line ~70:
elif [[ "$prompt" =~ (documentation|docs|readme) ]]; then
    role_section="# Role and Objective
You are a technical documentation specialist. Your goal is to create clear, comprehensive documentation that helps developers understand and use the system effectively.

"
```

### Custom Project Context
```bash
# Add project-specific rules around line ~150:
if [[ -f "next.config.js" ]]; then
    context_additions="$context_additions
🚀 **NEXT.JS PROJECT DETECTED**
- Follow Next.js best practices for routing and data fetching
- Use proper Image optimization and SEO practices
- Consider server-side rendering implications"
fi
```

## 🔮 Future Enhancements

### Planned Features
- **Learning from Feedback**: Adaptive optimization based on success rates
- **Custom Templates**: User-defined prompt templates
- **A/B Testing**: Compare optimization strategies
- **Integration Analytics**: Track Claude Code tool usage improvements

### Experimental Features
```bash
# Enable experimental learning mode
echo "LEARNING_MODE=true" >> ~/.claude/scripts/openai-prompt-optimizer.sh
```

---

## 🎯 Best Practices

1. **Start Simple**: Test with basic prompts first
2. **Monitor Results**: Check logs regularly for optimization patterns
3. **Customize Gradually**: Add project-specific rules over time
4. **Measure Impact**: Track Claude Code response quality improvements
5. **Iterate**: Refine optimization rules based on usage patterns

## 📞 Support

- **Logs**: `~/.claude/logs/openai-optimizer.log`
- **Cache**: `~/.claude/cache/openai-optimizer/`
- **Configuration**: `~/.claude/settings.hooks.openai-enhanced.json`
- **Scripts**: `~/.claude/scripts/openai-prompt-optimizer.sh`

---

*🧠 Built using OpenAI's GPT-4.1 Prompting Framework | Integrated with SuperClaude Intelligence Systems*
import 'dotenv/config';
import { OpenAI } from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function generateFact() {
  const prompt = `
You are helping create YouTube Shorts for a channel called "1 Fact a Day".

Write a script for a 30-second short video. The script should:
- Start with a hook like "Did you know..." or "Here's a crazy fact..."
- Be factual, interesting, and engaging
- Use simple, friendly language
- End with a soft call-to-action like "Follow for more daily facts!"

Only output the 3–5 sentence script. Do NOT include hashtags, notes, or explanations.
`;

  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.8,
  });

  const factScript = response.choices[0].message.content;
  console.log(`\n🎬 Fact Script:\n\n${factScript}\n`);
  return factScript;
}

generateFact();

// “Did you know that honey never spoils? 
// Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old 
// — and still perfectly edible! It’s one of the few foods that can last forever. Follow for more daily facts!”


import { execSync } from "child_process";
execSync(`python3 tts.py "${fact.replace(/"/g, '\\"')}"`);
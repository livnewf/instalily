# PartSelect Chat Agent

A focused Next.js chat agent prototype for PartSelect that supports refrigerator and dishwasher replacement parts.

## Features

- Modern Next.js chat interface with quick action buttons
- Backend logic tailored to refrigerator and dishwasher parts only
- Product card responses for part recommendations
- Order and tracking support re-routing
- Extensible structure for adding a vector search or external catalog later

## Architecture

- Frontend: Next.js app router with client-side chat interaction.
- Backend: API route handles incoming queries and responds using a catalog retrieval engine in Python.
- Data: In-memory product catalog for refrigerator and dishwasher parts pulled from PartSelect's website regarding parts, repairs, and blog posts. All data pulled from https://github.com/zehuiwu/partselect-agent due to web-scraping blockages put in place by PartSelect.
- Agent: This program runs on HuggingFace's Qwen/Qwen-7b-Chat model for simple text generation of reliable query responses. Prompting of the model has been sufficiently tailored to the narrowly defined specialization in refrigerators and dishwashers.

## Notes

- This project now includes merged chat agent behaviors inspired by the Instalily template, including product cards, quick action prompts, and scoped refrigerator/dishwasher support.

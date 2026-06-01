# Shopify → Airtable Automation

## Overview
Webhook-based automation system that:
- Receives Shopify order webhooks
- Verifies authenticity
- Prevents duplicate processing
- Transforms order data
- Stores records in Airtable

## Tech Stack
- FastAPI
- Shopify Webhooks
- Airtable API
- SQLite (idempotency + retry tracking)

## Features
- Webhook signature verification
- Idempotency handling
- Retry mechanism for failed processing
- Clean layered architecture

## Flow
Shopify → FastAPI → Middleware → Controller → Service → Airtable

## Setup (Local)
1. Clone repo
2. Add `.env` file
3. Run:
   uvicorn server:app --reload

## Deployment
Deployed via Render (or compatible platform)

## Author
retiredmonk
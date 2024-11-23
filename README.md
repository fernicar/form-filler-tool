# Fill Me In

## Overview

Save time and eliminate the hassle of filling out web forms with the "Fill Me In" extension. Store your essential information locally and let the extension automatically complete forms for you with a single click. Say goodbye to repetitive typing and hello to a faster, more seamless browsing experience.

### Demo Video

[Watch the Demo Video](DemoVideo.webm)

> Note: Replace this with the appropriate video link or embed.

## Setup Instructions

To get started with "Fill Me In", follow the steps below:

1. **Start Docker Container**

   ```bash
   docker compose up -d --build
   ```

   _Wait briefly as Ollama downloads the model._

2. **Install Dependencies for the Extension**

   ```bash
   cd extensions
   npm install
   npm run dev:firefox
   ```

   For Chrome, simply run:

   ```bash
   cd extensions
   npm run dev
   ```

3. **Try it Out**
   You can test it by applying to a position in New York:
   [Ekimetrics - VIE in New York](https://jobs.lever.co/ekimetrics/c62e4fd4-acd5-4860-857a-15a6797696be/apply)

## Features & Benefits

- **Save Time**: Automate the process of filling out forms with a single click.
- **Protect Privacy**: Keep your data safe by storing it locally. No external servers involved.

## TODO List

- Implement retry mechanism on error when the JSON format is not respected by the Ollama model.
- Save the output of `GetUserData` in storage using `JSON.stringify` and reload using `JSON.parse`. This will allow the extension to retain field values without querying the Ollama model every time.
- Explore publishing the extension ([guide to publishing](https://wxt.dev/guide/essentials/publishing.html)).
- Test additional Ollama models.
- Experiment with Hugging Face models for zero-shot text classification (refer to transformers.js ReadMe).
- Develop a business plan.
- Identify target client profiles.

## Pitch Ideas

Today, people spend an excessive amount of time filling out forms. We have a solution for that—an extension that knows your profile: your motivations, skills, experiences, hobbies, contact information, and more.

Our extension is powered by an on-device "tailored" model capable of filling out forms for you—all while keeping your data private. Unlike some alternatives, your personal information stays with you, not with external entities like Google.

**Who is it for?**

- Students filling out internship or event applications
- Job seekers
- Individuals searching for a new home
- People who value their privacy
- Anyone who wants to save time

**Why choose us?**

- **Save Time**: Fill out forms quickly and easily.
- **Privacy Guaranteed**: Your data stays with you, securely. You can upload you files without compromising them.

## Business Model

The most appealing approach is a freemium model:

- **Free Tier**: Limited number of forms filled per month.
- **Premium Tier**: Unlimited form fills. We could offer either a one-time purchase for the premium version or a monthly subscription (e.g., 5 forms per month for free, unlimited access at X$/month).

### Client Profiles

- **Students**: Applying for internships, scholarships, or events.
- **Job Seekers**: Sending out job applications.
- **Apartment Hunters**: Filling out rental applications.

The common denominator is individuals who care about privacy and value their time.

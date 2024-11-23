# Fill Me In

Save time and eliminate the hassle of filling out web forms with our extension. Store all your essential information locally, and let the extension automatically complete forms for you with just one click. Say goodbye to repetitive typing and hello to a faster, smoother browsing experience!

## Setup

```
docker compose up -d --build
```

Wait a bit (Ollama is downloading a model).

```
cd extensions
npm run dev:firefox
```

or for chrome simply run 

```
cd extensions
npm run dev
```

## TODOS

- Add retrial on error if the JSON format is not respected by the Ollama model
- Presentation video using cap.so 
- Save the output of GetUserData in the storage as a string using `JSON.stringify` and load it back using `JSON.parse`. This will enable the extension to keep in memory the field values instead of asking to the Ollama model each time.
- Understand how easy publishing the extension will be `https://wxt.dev/guide/essentials/publishing.html`
- Enhance the prompt
- Try other Ollama models
- Try other HF models for zero shot text classification (cf transformers.js Readme.md)
- Find business plan
- Find typical client profiles

## Ideas for Pitch
People today fill a lot of forms, a lot. And it's a pain. We have a solution for that. An extention that knows how you are, your motivations, your skills, your experiences, your hobbies, your contact information, and more

This exention is powered by a on device "tailored" model that is able to fill forms for you without you having to type anything. Without sharing everything about you to the world (google, ...).

This is a game changer for people that fill a lot of forms, like students, job seekers, people that are looking for a new place to live, etc. People who care about their privacy. People who care about their time.

*TLDR*:
  - Save time (filling forms rapidly)
  - Save user's privacy (no data is shared with any external device)

*Client profiles* :
    - Students (Internships, Events, ...)
    - Job seekers
    - People looking for a new place to live 
  In general :
    - People who care about their privacy
    - People who care about their time

*Business model*:
    The most attractive model is a freemium model. The free version will be limited in the number of forms that can be filled per month. The premium version will have no limits. (We can also think about a one time payment for the premium version) or montly subscription (5 forms free per month, unlimited X$/month)
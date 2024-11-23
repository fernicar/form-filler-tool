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

or simply 

```
cd extensions
npm run dev:firefox
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
